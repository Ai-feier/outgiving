# 三方交叉审查报告 — 2026-07-20

> 审查人：visual-designer
> 审查对象：video-director, script-designer, rhythm-designer
> 阅读基线：四 agent 深度精进 R22 + 2026-07-20 交叉审计后版本

---

## visual-designer 审查

### video-director: 🟡5项 / 🔴1项

#### D1 — 9要素公式消费: 🟡 材质无专属字段，需嵌入 scene/style

我的六维产出（镜头/运镜/布光/色彩材质/构图/景深）中，director 的 9 要素公式 `[景别]+[主体]+[动作]+[场景]+[光影]+[运镜/动]+[风格]+[画质]+[间]` 可以承载：

- 布光 → `lighting` 字段 ✓
- 运镜 → `camera` 字段 ✓
- 镜头（焦段）→ 嵌入 `scene` 或 `camera`（以景别词优先） ✓
- 构图 → 嵌入 `scene`（空间描述） ✓
- 景深 → 嵌入 `style` 或 `scene` ✓
- 色彩材质 → **无专属字段**。需散入 `subject`（角色服装）、`scene`（环境表面）、`style`（画质关键词）。意味着我的材质系统（class+surface+1key → 物理展开描述）在 dispatch 传递时没有结构化的接收端。

director 的 SDK 映射表行 182-188 确认：9 要素映射到 5 个字段（scene/subject/camera/lighting/style），[间]和材质均无独立字段。与此前交叉审计发现一致（审计4问题4.2）。

影响程度：材质展开文本可嵌入 subject/scene 的自由文本段，功能上不丢失。但嵌入位置决策权在 director 而非 visual-designer，可能导致材质精度在跨拍间不一致。

#### D2 — [STYLE-DEP] 一致性: 🟡 布光默认值存在张力

我的日系布光（行27）：「情绪优先。色相偏移阴影、透过光、无物理光源逻辑。」
director 的 japanese-anime 光影（行379）：「默认 flat lighting（赛璐璐着色=无阴影）。」

两者不直接冲突但存在张力：我倾向情绪化色相偏移光，他倾向默认 flat。他同时提到「指定 volumetric + rim 可增加电影感」——说明 flat 是工具层面的安全默认值而非风格硬约束。当六维显式指定布光时，director 应以六维为准。

其他维度：
- 运镜：我禁快速旋转/whip pan/complex tracking/crane；他禁 whip pan/handheld 过度抖动，偏好 dolly-in + static + slow pan。我比他更严格（crane/complex tracking 也在禁列），无冲突。✓
- 景深：我的「径向模糊/空气透视，非物理镜头 DOF」与他的「deep focus default」互补——deep focus 是默认景深量级，径向模糊是日系模糊的质。✓
- 转场：我未在六维定义转场，他行 397 禁止 whip pan/fast spin，与我的运镜禁止一致。✓

#### D3 — 素材装配协议: 🟡 仅读 asset-lab.md，不读 {type}-index.md 子索引

director 的 Step 1 库存清单（行 214-217）：以需求清单索引 asset-lab.md，未命中则查 ref-images/ 物理文件。

但我的资产系统（行 335-336）有三文件：taxonomy-registry.md（受控词汇）+ asset-lab.md（根清单）+ {type}-index.md（子索引，含风格列、appears_in_style、replaced_by 链等详细元数据）。

director 不读子索引，意味着：
1. 风格兼容性元数据（appears_in_style）对 director 不可见——他只能依赖 asset-lab.md 表中的版本/状态/质量三字段
2. replaced_by 版本链无法追溯——如果 asset-lab.md 中只有旧版本路径而链接到了新版，director 不知道
3. 三文件之间的同步偏差无法被 director 检测

相比之下，script-designer 的 Step 8a（行 349-363）会直接查询子索引并读 replaced_by 链——更完整。

影响评估：asset-lab.md 作为同步根清单如果保持最新，功能上够用。但子索引的元数据优势未被利用。建议 director 素材装配 Step 1 补充「对需引用的资产，回读对应子索引验证元数据」。

#### D4 — 分镜确认门: 🔴 阻塞规则未被 director 消费

我的分镜确认门阻塞规则（行 456）：「P0 关键拍（钩子拍/规范参考拍/情绪转折拍）分镜图未确认 → 阻塞 video-director Phase 0 预检。」

但 director 的 Phase 0 预检（行 68-72）：
- 读 TOGETHER.md §3-4
- 读 material-backlog-TXXX.md
- 读 gates/image-gen-*（生图确认门）
- 检查 asset-lab → ref-images/

**完全不检查 gates/storyboard-* 或 assets/storyboards/ 的状态。**

两个文件对同一件事（P0 关键拍分镜就绪判断）做了不同约定：
- 我说「未确认 → 阻塞」的行 456 对 director 无约束力
- director 的 Phase 0 没有 storyboard gate 检查步骤

这是配置冲突而非单方面缺失。需双方对齐：要么我在行 456 的阻塞规则改为建议而非硬阻塞，并在 Phase 0 预检中增加分镜门状态检查；要么 director 在 Phase 0 追加 storyboard gate 检查步骤。**二选一，不能各自定义阻塞规则。**

需决策：行 456 改为「P0 关键拍分镜图未确认 → 阻塞。Phase 0 预检追加 storyboard gate 检查」，同时在 director 对应节补充检查步骤。

#### D5 — 负面参考: 🟡 止め絵负向覆盖完整，但通用防护层在 director 缺失

我的负向 prompt 体系（行 113-124）有四层防护：
1. **扁平防护**：no flat lighting/blurry textures
2. **结构防护**：no deformed hands/fingers/faces
3. **运动防护**：no flicker/jitter/warping
4. **风格防护**：no cartoon saturation unless specified
5. **身份防护**：no extra characters/face swapping

director 的负向策略：
- 止め絵 negative（行 405）：`"character breathing movement, cloth wind movement, ambient particle animation during still frames, micro-movement in locked shots"` — 仅覆盖运动层面的微运动
- 止め絵优先级高于所有负向（行 409）— 这是子集的优先级声明
- 自检「负向已填」（行 465）— 确认存在但不指定内容

director 没有通用负向模板。他的负向只针对止め絵场景，不覆盖结构变形（deformed hands）、风格溢出（cartoon saturation）、身份混入（extra characters/face swapping）这四个我定义的防护域。

当 director 合成 prompt 时，他的 negative_prompt 字段可能只填充止め絵特定的几条。我的通用防护层需要在 TOGETHER.md 或 material-backlog 中传递，否则可能丢失。

影响：非止め絵拍的 prompt 负向可能过于单薄。止め絵拍的负向因为优先级声明只聚焦微运动，结构/身份防护同样可能缺失。

#### D6 — 角色语言消费: 🟡 情绪外化系统显式引用✓，Proxemics 完全不消费

我的五维角色语言：
1. **专属微动作** — director 的 entity 标签注册（行 419）可绑定 `<tag>`，签动通过 subject「动作」段嵌入。无专属机制，但可承接。🟡
2. **Effort Profile** — director 行 201-202 明确标注 Effort Profile 执行精度「中」，策略「搭配身体锚点一起使用」。有意识，有策略。✓
3. **角色-镜头关系** — director 有完整镜头系统（景别/运镜/角度/光学）。桥接靠视觉DNA表中 camera relationship 字段 → 翻译为每拍 shot size + angle + movement。有路径但无自动化。🟡
4. **Proxemics** — **director 不消费。** 他的 shot relationship 定型（行 154-156）覆盖因果/回声/对比/同时/跳跃五类拍间关系，不包含角色间空间距离。矛盾矩阵格式也无 proxemics 项。Proxemics 在我和 script-designer 之间交易，director 无接收端。🔴（低于阻塞阈值，因为 script 已做 proxemics 设计且 beat 级标注存在，但 director 合成时无法针对 proxemics 做镜头决策）
5. **情绪个人化表达** — 行 456-456 显式引用 visual-designer 情绪动作化系统 + 角色语言§5。这是最完整的消费。✓

情绪外化映射速查表（行 384-390）是 director 自己的独立系统，不依赖我的角色语言。两套并存是冗余设计——如果两者不一致，需要矛盾矩阵裁决。建议明确「通用情绪 → director 外化映射表」，「角色专属情绪 → visual 角色语言§5」。

### script-designer: OK / 🟡2项 / 🔴0项

#### S1 — 视觉资产需求路径格式: OK

script-designer 的视觉资产需求（行 367-371, 173）使用我的命名规范路径：
`assets/characters/CHR_T002_LinBei_canonical_v01.png` — 与 `{Type}_{TopicID}[_{StyleTag}]_{EntityName}_{Variant}_v{NN}.{ext}` 一致。✓

他的 Step 8a （行 349-363）查子索引时按类型分流（characters-index.md/scenes-index.md/storyboards-index.md），匹配字段含名称/风格/appears_in_style/appears_in_topic，继承我的 taxonomy-registry 体系。完整对接。✓

#### S2 — 情绪锚→身体锚点: 🟡 10% 情绪锚无直接映射

我的情绪→身体锚点表（行 130-140）覆盖 9 种情绪：悲伤/紧张/愤怒/快乐/放松/好奇/惊讶/恐惧/坚定。

script-designer 的情绪锚表（行 58-71）覆盖额外几种在他的映射表中不存在而我未覆盖的：
- 力量/英雄（power/hero）— 可分解为「坚定+低角度+全身景别」，但无独立身体锚点
- 孤独/渺小（loneliness/smallness）— 可分解为「悲伤+空间隔离感」，无独立锚点
- 释放/解脱（release/relief）— 可分解为「放松+深呼吸+肩部下垂」
- 怀旧/回忆（nostalgia/memory）— 无对应

实际上 script 行 72 明确说：「情绪锚关键词本身不建议写入 prompt——director 有独立的情结外化系统。」所以 script 的情绪锚不需要被我完全覆盖——它们只做景别方向的叙事意图，不替代情绪外化。这是我的担忧多虑了。

真正的风险是：当 script 在 beat 模板「AI prompt 指令」的情绪外化字段（行 181）需填入「具体可拍摄的身体/环境细节」时，我的 9 种锚点可能不够覆盖上述 4 种 scene-level 情绪。但 script 的行 180 写的是「情绪外化:[具体可拍摄的身体/环境细节]」——script 设计师自己负责在此处完成外化。我的系统是参考不是依赖。

结论：功能上不依赖全覆盖，但建议补充「力量/孤独/释放/怀旧」4 种 scene-level 情绪的身体锚点提示，作为脚本设计师的参考。

#### S3 — 角色行为弧线对接: 🟡 情绪个人化表达（维度5）无显式接收字段

script-designer 的角色行为弧线节（行 222-290）显式对接我的角色语言四维，但在行 230-236 的对接表中只列了 4 维（专属微动作/运动质量/角色-镜头关系/角色间空间），缺少我的**第5维：情绪个人化表达**。

他新增的「角色 PAD」字段（行 188）覆盖了「角色感受到什么情绪」但不覆盖「角色如何表现这种情绪」。我的维度 5 输出的是表达方式信号（如「微笑但眼轮匝肌不动」），script 没有对应的接收字段。

与交叉审计（审计 3 问题 3.2）一致。script 的设计备注中可承载，但非结构化的。

#### S4 — 规范参考节拍: OK

完美对齐 GroundShot 星形一致模型。

我的定义（行 283-284）：「观众判定一致性的基准不是前一帧——是每个实体首次清晰出现的规范参考。所有后续出现与此原点比较，非链式传递。」

script-designer（行 42-43）：「每个实体首次清晰出现的节拍定义其规范参考……所有后续出现与此原点比较，非链式传递。」

具体执行：
- 规范参考节拍表（行 404）：`[实体名→首次清晰出现拍号]`
- 每实体≤1组合图（行 194）
- 规范参考拍 prompt 精度加倍（行 379）
- GroundShot 质量感知调度（行 42-43）

所有细节一致。✓

### rhythm-designer: OK / 🟡0项 / 🔴0项

#### R1 — V 值独立性: OK

rhythm-designer 行 32-33：「核心：CF<2（单边约束），V 由 visual 独立管理。」

他的 rhythm_intensity 公式（行 167）：`(ID + ED + CL + CF) / 4` — 不包含 V。✓

V>=4 调整（行 172）：「V>=4延至~1.2s」— 这是对 V 的反应性适应，不是定义或约束。

Phase 0（行 193）：「读 visual V」— 读取但不修改。✓

量化指标表（交叉审计审计5）：完全对齐。✓

#### R2 — 通道堆叠: OK

通道堆叠≤2 带显式标注（行 33）。

V≥4 时场景视觉已经复杂——通道堆叠≤2 是天然合理的。V=5（人群+高度细节+7+材质类）不可能再开启多通道同时轰炸观众。

无冲突。✓

#### R3 — 情绪密度 vs 视觉密度: OK

ED 是节奏的维度（情绪密度），V 是视觉的维度（帧内复杂度）。两套正交系统。

ED=5 + V=1 是经典的"情绪高潮特写"模式——一张脸承载全部情绪。符合电影语言。✓

ED=1 + V=5 是"环境建立镜头"——信息传达为主，无情绪负荷。✓

ED=5 + V=5 是最极端场景（情绪峰值 + 视觉峰值）。rhythm 的 CL 约束（1.5-2.0）+ ASL≥1.8s 在此场景下提供硬性保护——不会同时让观众承受最高频的视觉切和最密集的情绪冲击。✓

无冲突条件。✓

---

## 最终判定: 有未解决问题（🔴1项需对齐）

| agent | 判定 | 关键项 |
|-------|------|--------|
| video-director | 🟡5 + 🔴1 | **🔴 D4** 分镜确认门阻塞规则配置冲突 — 我定义的阻塞规则 director 未实现 |
| script-designer | 🟡2 | 🟡 S2 4种scene-level情绪锚无身体锚点 / 🟡 S3 维度5无结构接收字段 |
| rhythm-designer | OK | 全部OK |

### 需处理的 🔴 项

**D4: 分镜确认门阻塞规则配置冲突**

状态：我的行 456 设置「P0 关键拍分镜图未确认 → 阻塞 director Phase 0 预检」，但 director 的 Phase 0 没有检查 storyboard gate 的步骤。双方定义了不同的就绪条件。

建议解决方案（二选一）：

方案 A（当前更保守，推荐）：我在行 456 将「阻塞」改为「建议阻塞」并标注「需 director Phase 0 追加 storyboard gate 检查步骤」，同时在 director Phase 0 预检（行 68-72）末尾追加：
```
- [ ] 检查 storyboard gate 状态：gates/storyboard-*.md 已通过。P0 关键拍（钩子拍/规范参考拍/情绪转折拍）分镜图未确认 → 阻塞
```
硬阻塞保留，但双向确认。

方案 B：我取消行 456 的阻塞声明，改为「分镜图可作为 RefImg 参考图输入，非阻塞条件。确认状态写入 TOGETHER.md §6 资源追踪。」P0 关键拍改用目标工具的参考图锚定（参考 director 的 RefImg 门禁）。这样分镜门从阻塞门降级为建议门，不阻塞 Phase 0。

选择方案 A 以保持当前设计意图完整。

### 需共识的 🟡 项

**D5: 通用负向防护层协同**

我在行 113-124 定义四层防护（扁平/结构/运动/风格/身份）但 director 的负向只针对止め絵场景。建议 TOGETHER.md 中明确：非止め絵拍使用 visual-designer 的通用负向防御模板（`no flat lighting/blurry textures, no deformed hands/fingers/faces, no flicker/jitter/warping, no extra characters/face swapping`），止め絵拍在此基础上追加止め絵专用的微运动负向。由 director 在 prompt 合成时执行，不做新约束——仅确认执行路径。

**D2 布光默认值张力**

在具体项目中，当 visual-designer 通过六维指定布光时，director 应以上游六维为准而非默认 flat lighting。六维布光默认走情绪优先逻辑，flat lighting 是工具层的 fallback 而非设计层的约定。

**S3: 情绪个人化表达无结构接收字段**

script-designer 的 beat 模板已满（行 164-190 共 19 个字段），不建议新增字段。建议脚本设计师在「角色标记动作」字段中用 `[PERSON_1: overcontrolled smile/Duchenne absent]` 格式嵌入表达信号，不新增独立字段。
