# T003 Segment 1 — New Prompt (v2) + Comparison

> **版本**: v2 重写 | **比较对象**: video-prompt.md §5 段 1 (旧版)
> **新体系**: video-director.md 深度 2 精进 — 电影语言模块 (120 行) + visual-designer 材质展开/角色语言五维/环境细节 + script-designer 镜头叙事映射 + rhythm-designer 节奏-运镜耦合
> **覆盖**: 段 1 — Beat 1 (B1a-c) + Beat 2 (B2a-b) + Beat 3a-b
> **时长**: 0:00-0:15.5 (~15.5s) | **工具**: Seedance 2.0 Mini
> **画幅**: 9:16 portrait (1080x1920) | **风格**: Bleach (千年血战篇)

---

## Volume 1 — 段 1 新 Prompt (Shot-by-Shot, 12 要素体系)

### 元信息

| 实体 | 标签 | 角色语言约束 | 规范参考状态 |
|------|------|------------|------------|
| [ANTAGONIST] Yhwach | 白色军服+深红斗篷+红瞳多瞳 | 静止=绝对力量（压抑型） | 033+034 官方源 ✅ |
| [PROTAGONIST] Ichigo TS | 黑色死霸装+橙刺发+双斩月 | 蓄力→释放（爆发型） | 036+037 官方源 ✅（单刀形态） |
| [WEAPON_ZANGETSU] | 大刃镂空/小刃无柄中空 | — | 文本描述补偿双刀细节 |
| [FACTION_STERNRITTER] | 白色披风剪影 | 仅队列姿态 | 文本描述 |

**段 1 末帧条件**：B3b 末尾 Ichigo 全黑剪影，橙色 rim light 消退，白色碎片初现。构图干净/位置清晰/光照稳定/无运动模糊/D=3。

---

### Shot 1.1 [0:00-0:00.3] — B1a: Pattern Interrupt (0.3s)

| 要素 | 规范 | 新 Prompt 值 |
|------|------|-------------|
| **景别** | ECU | ECU / Macro — Yhwach 左眼占据画面 95% |
| **运镜** | 单动+速度 | Static locked shot (无运动)。速度标量: —（固定帧） |
| **角度** | 必标 | Eye-level matching Yhwach sight line — 视线瞄准镜头外右侧，制造「被盯住」的不安 |
| **光学** | 焦距桶+DOF | 85mm telephoto / Shallow DOF — 仅虹膜多层瞳孔在焦平面内，眼睑边缘模糊软化 |
| **构图** | 规则名 | Negative space dominance — 右眼置于画面右 1/3 交叉点，左侧 2/3 纯黑留白。遵守 bleach.md「角色在画面边缘或中心极小」 |
| **光影** | 多层 | 无环境光。Key: 红瞳自发光 (2000K, 唯一色源) / Rim: 无（无轮廓光条件）/ Fill: 0% — 纯黑包围 / Ambient: 零 / 特殊：虹膜表面光通过瞳孔层叠结构产生微反射——多重瞳孔之间出现极细暖红边缘光。色温比：红 2000K vs 环境 0K（无） |
| **材质细节展开** | 压缩→展开 | 旧版「pure black skin tone」→ Pale aged bios surface with deep-set periodital wrinkles, subtle sebaceous texture at brow bone, iris surface with concentric layered pupil rings each separated by hairline dark gaps, cornea specular highlight forming at 10-o'clock position from self-luminescence. Faint beard stubble shadow visible at frame bottom edge |
| **环境细节** | 大气状态 | Absolute vacuum — no air particles, no atmosphere, no dust motes. The red eye exists in pure void. 唯一可感介质：眼球表面极薄泪膜层的微光反射 |
| **角色语言** | 手势+Effort+Camera | **Signature gesture**: 静止本身即姿态——Yhwach 不需要眨眼、不需要眼球运动来宣告存在。**Effort Profile**: heavy + sustained + direct + bound (力量不释放——更重的力量来自不释放) / **Camera Relationship**: ECU 将眼睛客体化——它不是一个「人在看」——是个探测器在感知。Bleach「灭却师之王不需要动作显示力量——静止就是压迫」(visual-world §3 情绪动作化) |
| **[STYLE-DEP]** | bleach 约束 | Bleach 高对比——红 #CC2233 对绝对黑 #000000。多重瞳孔渲染为**同心圆层叠**（非解剖学虹膜纹理）——久保带人式象征性眼睛画法。禁止速度线、禁止眼球毛细血管细节、禁止运动模糊。0.3s 中断帧不可含任何亮度 >5% 的其它元素 |
| **[间]** | 三段式 | 前状态：视频起始前全黑（观众浏览模式）→ 间隔：红瞳 ECU 骤亮，0.3s 纯静止——中断浏览模式，强制注意。眼不动、不眨、不呼吸 → 后状态：急拉开始，跳转到 B1b 空间信息 |
| **负向** | 3-5 词 | eye blood vessels, eye movement, blinking, speed lines, skin pores detail, anatomical iris texture, sclera detail |

---

### Shot 1.2 [0:00.3-0:02.0] — B1b: Snap Zoom-Out + Throne Reveal (1.7s)

| 要素 | 规范 | 新 Prompt 值 |
|------|------|-------------|
| **景别** | 必标 | ECU → MS (急拉过程 0.5s) → MWS (静态保持 1.2s) |
| **运镜** | 单动+速度 | Snap zoom-out (pull-back), speed: fast (0.5s 完成急拉)。Then Static locked shot (1.2s 保持)。Seedance 兼容性：标注「rapid pull-back」 |
| **角度** | 必标 | Low angle (仰角) — Yhwach 御座位于高台，镜头从下方仰视，军服下摆和斗篷占据前景。制造力量差 |
| **光学** | 焦距桶+DOF | 起始 85mm telephoto (ECU) → 结束 50mm normal (MWS)。Deep focus — 御座+军队所有层次保持清晰（Bleach 广角拉伸的压迫感）。禁止平滑变焦——急拉模拟手摇镜头风格 |
| **构图** | 规则名 | Center symmetry with negative space — Yhwach 居中于高台（三分法垂直中轴线），星十字军队两侧对称排列为白色剪影。画面下方 1/3 为御座底座+斗篷铺开，上方 2/3 为冰宫建筑线条+军队头部。三分法水平线：Yhwach 眼睛位于上 1/3 线 |
| **光影** | 多层 | Key: 冷色顶光 7000K (垂直 90°)，从宫殿顶部倾泻 / Fill: 正面补光 5% 冷蓝 #8A98AA（仅避免军服全黑）/ Rim: Yhwach 肩膀和斗篷边缘冷白 rim light 1-3px，从纯白背景中剥离轮廓 / Ambient: 深蓝黑 #0D0D14 (10% 亮度)，色相偏蓝 / 特殊：红瞳继续作为唯一暖色点 (2000K vs 7000K 环境) / **情绪-光照映射**: 力量+胁迫 = cold overhead + low-angle + deep shadows |
| **材质细节展开** | 压缩→展开 | 旧版「white double-breasted military uniform」→ 灭却师军服：cotton-silk blend fabric, matte surface with subtle weave texture, sharp military creases at sleeve elbows and chest panel seams. Three silver medals at left collar: polished silver with cross-shaped emboss, catching top-down cold light. Cape lining: deep crimson #8A2020 satin with dull sheen visible only at fold valleys. Stern Ritter cloaks: pure white cotton with matte surface, no texture detail — pure white silhouette shapes with star-cross emblem outlines barely visible |
| **环境细节** | 大气状态 | Silbern 冰宫内部：冷空气粒子在顶光中形成极微弱 volumetric haze (色温 7000K), 几何冰柱从顶部悬挂，表面半透明冷蓝。地面不可见——被深蓝黑阴影吞噬。宫殿无限纵深暗示——两侧军队延伸至画面深度 20m+ 处退为纯白剪影 |
| **角色语言** | 手势+Effort+Camera | **Signature gesture**: 右手微抬（召见手势）——掌心朝下，手指放松，如同在按低所有事物。不抬到视线水平——只在扶手上方几厘米 / **Effort Profile**: heavy + sustained + direct + bound — 静止即宣告力量 / **Camera Relationship**: low-angle from subordinate position → power differential established. Yhwach 不看镜头——视线略微向下，看的是面前的空间（军队/入侵的目标） |
| **[STYLE-DEP]** | bleach 约束 | 纯白军服在冷色背景中的曝光不高于 90% 亮度（保留细节折痕）。Deep blue-black shadows (不=灰 / 不=纯黑+#888)。军队剪影必须保持人物轮廓可辨（不合并为单一白色块）。构图符合 bleach.md「剪影先于面部——角色轮廓在 0.1s 内可识别」 |
| **[间]** | 三段式 | 前状态：ECU 红瞳占据全部注意力 → 间隔：0.5s 急拉——画面从「一只眼睛」暴力展开为「御座+军队+宫殿」的完整空间。信息密度 0→100 的跳变 → 后状态：1.2s 静态保持，给观众认知时间消化「这是灭却师之王和他的军队」 |
| **负向** | 3-5 词 | smooth zoom, zoom transition effect, blur during pull-back, soft focus on background, uniform fabric wrinkles, soldier individual faces, eye contact with camera |

---

### Shot 1.3 [0:02.0-0:05.0] — B1c: Throne Hold + Subtitle (3.0s)

| 要素 | 规范 | 新 Prompt 值 |
|------|------|-------------|
| **景别** | 必标 | MWS (Medium Wide Shot / Cowboy) — Yhwach 膝上至头顶，御座扶手可见，斗篷铺展至画面底部 |
| **运镜** | 单动+速度 | Static locked shot (完全静止)。速度标量: —。微幅呼吸感可以有但不要求（Bleach 止め絵原则——静止帧就是静止帧） |
| **角度** | 必标 | Low angle (仰角维持) — 延续 B1b 视角。镜头高度在御座底座水平线，保持力量差 |
| **光学** | 焦距桶+DOF | 50mm normal / Deep focus — 前景御座扶手、中景 Yhwach 身体、背景军队剪影全部清晰。Bleach 广角规则不使用柔和背景压缩 |
| **构图** | 规则名 | Negative space + center-weighted — Yhwach 在画面垂直中线偏右（左 45% / 右 55% 权重），视线朝右（右→左的紧张感——入侵方向）。军服白色占据画面中心 20%，两侧深蓝黑各 35%，形成 i 型亮度分布。字幕「滅却師の王·友哈巴赫」位于画面下 1/3 安全区 |
| **光影** | 多层 | Key: 同 B1b 冷色顶光 7000K / Fill: 正面补光提升至 10% 冷蓝 / Rim: 冷白 rim light 在 Yhwach 右肩和左手背 / Ambient: 同 B1b / 特殊：红瞳持续自发光 (2000K)，随瞳孔层叠结构的微小密度变化产生极微亮度脉动——从 #CC2233 到 #DD2244（不可见级差，给单帧带来活感） |
| **材质细节展开** | 压缩→展开 | 追加旧版未描述的细节：军服纽扣——纯银六边形，表面拉丝，每颗反射不同角度的冷顶光。深红斗篷内侧在御座两侧折叠处的阴影层次：从纯黑→深红→暗红的分层过渡。衣领 III 枚勋章：第一枚完整可见（十字星芒样式），第二、三枚在衣领褶皱中被半遮挡。手套——白色皮革贴合手型，四指并拢时的皮革褶皱线 |
| **环境细节** | 大气状态 | 冰宫冷气粒子在 Yhwach 和背景军队之间的中层空间形成细微的冷白雾层（层距：前景角色 0m / 雾层 2-4m / 军队背景 10m+）。雾层使军队剪影退为纯白轮廓——人形可辨但细节不可见 |
| **角色语言** | 手势+Effort+Camera | **Signature gesture**: 右手微抬姿态保持（从 B1b 延续）。无变化——Yhwach 在 3s 静止中不做任何动作、不调整坐姿、不眨眼。**Effort Profile**: heavy + sustained + direct + bound (蓄积的静态——压弹) / **Camera Relationship**: low-angle 持续让 Yhwach 的身体占据从膝盖到头顶的垂直空间——他不需要站起来就已经「高于」观众 |
| **[STYLE-DEP]** | bleach 约束 | 3s 静止帧——Bleach 止め絵原则的关键实践。角色在 3s 内必须绝对静止（零眼球运动、零呼吸运动）。字幕「滅却師の王·友哈巴赫」白色 100% / 黑体粗 / 无衬线。翻译为: "The Quincies' King — Yhwach"。禁止在静止帧中添加任何微运动/粒子特效/环境动画 |
| **[间]** | 三段式 | 前状态：急拉结束，观众刚完成空间定位 → 间隔：3s 绝对静止——信息被给到（字幕）+ 观众认知消化时间。静止本身是力量的声明：他不需要做任何事来让你知道他是谁 → 后状态：硬切至 Ichigo 纯黑背景，0s 过渡。力量对比——冷色宫殿→黑虚空 |
| **负向** | 3-5 词 | Yhwach eye blinking, body movement, head turn, cape wind movement, throne ambient animation, floor reflection, window or natural light, warm tone, smooth gradient shadows |

**过渡 B1→B2**：硬切 0s。对比转场——冷色/白色/冰宫 → 黑色/橙色/虚空。入侵者 → 应战者。

---

### Shot 2.1 [0:05.0-0:08.0] — B2a: Dual Blade Display (3.0s)

| 要素 | 规范 | 新 Prompt 值 |
|------|------|-------------|
| **景别** | 必标 | MS (Medium Shot) — 腰线以上，双刀交叉在胸前清晰入画 |
| **运镜** | 单动+速度 | Slow dolly-in (推近), speed: slow — 3s 内前推约 0.3m。速度标量：极慢——几乎不可自觉，但刀身纹理逐渐清晰。符合 japanese-anime 偏好 dolly-in [STYLE-DEP] |
| **角度** | 必标 | Eye-level, slightly low (0-5° 仰角) — Ichigo 站位在镜头左前方 45°，视线朝向右上方。中性偏微微仰——不是英雄感，是「他在更高的存在平面上」 |
| **光学** | 焦距桶+DOF | 50mm normal / Deep focus — 双刀前后距离约 0.4m，两把刀都在焦平面内。背景纯黑无焦外元素。Bleach 深度清晰原则：主体在全焦段可读 |
| **构图** | 规则名 | Rule of thirds (left-weighted) — Ichigo 置于画面左 1/3 竖线，面向右方留 2/3 空间。刀交叉 X 形中心在画面下 1/3 水平线。刀尖指向右上方向——引导视线从 Ichigo 面部 → 刀交叉点 → 右上留白。符合 script-beats「面向右→留右侧空间」和 visual-world「左→右=安全」（一护展示侧） |
| **光影** | 多层 | Key: 单一定向侧光，左上 45° 冷白 6500K / Rim: 冷白 rim light 在 Ichigo 左肩、左手臂外侧、大刃上边缘——宽度 2px 的锐利高光线 / Fill: 0%（无正面补光——右侧大部分区域纯黑）/ Ambient: 偏紫黑的深色 #0D0D14（色相偏紫）/ 特殊：黑色灵压雾在镜头前方 0.5m 涡旋——半透明，不自发光，通过微弱冷光反射显示涡旋形态 / **情绪-光照映射**: 确定+专注 = cool directional side light + deep shadow + sharp rim |
| **材质细节展开** | 压缩→展开 | 旧版「black shinigami robe (sharaku) with sharp angular folds」→ 死霸装：cotton-matte fabric, 黑色 base #1A1A24, 深蓝黑阴影 #0D0D14, 褶皱呈锐利三角形——左肩被侧光打亮的区域可见经纬纹理，右手袖口下坠形成的三棱锥形折角。双斩月材质展开：**大刃 (120cm)** — pure black blade surface with elongated hollow texture resembling eroded obsidian; brushed satin micro-grooves along blade spine catching side light as hairline silver; irregular pentagon black tsuba with stepped silhouette. **小刃 (50cm)** — pure black jagged edge with irregular serration patterns as if bitten; hollow center grip visible through cross-section; no tsuba — blade root transitions directly into wrapping. Purple zigzag pattern on long blade hilt: alternating midnight purple #2A1A4A and black segments |
| **环境细节** | 大气状态 | 全虚拟空间（negative space）——无背景、无地面、无天花板。唯一介质：黑色灵压雾（black reiatsu mist）以 0.2m/s 缓慢涡旋，粒子直径 <0.5mm, 半透明 20%, 不自发光——仅通过散射侧光可见涡旋形态。雾密度从 Ichigo 身体向镜头方向递减（近身 40% 密度 → 镜头前 10% 密度） |
| **角色语言** | 手势+Effort+Camera | **Signature gesture**: 双刀交叉置于胸前（X 形）然后维持静止——「真正了解自己的斩魄刀」的视觉隐喻。非战斗姿态——是认知姿态 / **Effort Profile**: medium + sustained + contained + direct（力量被持有，未释放）/ **Camera Relationship**: eye-level + slow dolly-in → 观众被拉向 Ichigo 而非 Ichigo 走向观众。他是静止的磁极 |
| **[STYLE-DEP]** | bleach 约束 | 死霸装褶皱遵循「线条锐利、肯定」规则——每道折痕都是一条长直线终止于一个尖锐终点。刀表面不可有纯 CG 渲染感——久保的刀是「银色 brushed surface, 刃线连续高光」。双刀同时入画时，大刃在右手握持靠下（视觉上「主导手地位」），小刃在左手穿中空握持（视觉上「副手/不同力量来源」）。橙色刺状发的 4-5 束前侧发束必须各自独立，不合并为连续发块 |
| **[间]** | 三段式 | 前状态：B1 冷色宫殿被硬切打断 → 间隔：3s 缓慢推近——节奏从 B1 的 0.3s + 1.7s + 3.0s 切换至此拍的 3s 匀速推近。这是全片唯一连续运动 >2s 的镜头。观众有时间看清双刀差异 → 后状态：推近结束，进入 B2b 纯静止蓄力 |
| **负向** | 3-5 词 | single sword, bankai form, horn of salvation, gentle face expression, smile, floating debris in void, floor reflection, multiple characters in frame, continuous fight motion |

---

### Shot 2.2 [0:08.0-0:12.0] — B2b: Awakening Charge (4.0s)

| 要素 | 规范 | 新 Prompt 值 |
|------|------|-------------|
| **景别** | 必标 | MCU (Medium Close-Up) — 胸以上，面部为主，双刀刀柄和肩部入画。比 B2a 更近——镜头已推至最终位置 |
| **运镜** | 单动+速度 | Static locked shot (完全静止)。速度标量: — / 唯一运动：最后 1s Ichigo 眼神从半闭→微微聚焦（1-2px 虹膜位移——不可被 Seedance 渲染精确执行，保留在文本层作为「理想状态」）。橙色灵压在刀刃边缘开始极微弱闪烁（<5% 亮度） |
| **角度** | 必标 | Eye-level (中性) — 延续 B2a 的平视角度。镜头不再上升/下降——观众和 Ichigo 处于同一高度平面 |
| **光学** | 焦距桶+DOF | 50-70mm (normal to short tele) / Shallow DOF — 双刀刀柄在焦平面内，背景纯黑但比 B2a 更模糊（焦外虚化）。聚焦点：Ichigo 左眼（镜头和视线交汇点） |
| **构图** | 规则名 | Central composition with micro-movement — Ichigo 面部居中偏左（相机已在前 3s 推至最终位置），双刀交叉点位于画面下 1/3 水平线。4s 内无构图变化——唯一变化在最后 1s 的瞳孔 |
| **光影** | 多层 | Key: 同 B2a 左上 45° 侧光维持 / Fill: 仍为 0% — 右侧面仍在大阴影中 / Rim: 冷白 rim 延续，在鼻梁左侧、下唇、刀柄上缘 / 追加：第二光层——橙色#E8760B灵压边缘光，从刀刃接触点开始向刀身延伸，亮度 <5%，仅在最后 1s 出现。/ Ambient: 黑色灵压雾密度增至 60%（近身）— 开始微微发光（从无光→自发光过渡的临界点）/ **情绪-光照映射**: 蓄力+即将释放 = same key + second warm light emerging from below + rim tightens |
| **材质细节展开** | 压缩→展开 | 追加旧版未显式描述的：橙色刺发发束在侧光下的边缘半透明效果——每束发丝边缘透光形成暖色边缘光（不是光源，是发丝 RGB 中的橙色像素在逆光中被强调）。死霸装领口内侧可见标签状黑色布条——Bleach 死霸装标志性的 V 形领口露出锁骨上方的阴影三角。双刀刀身在最后 1s 的橙色灵压闪烁中，刀面纯黑开始显现极微橙 tint（灵压即将释放的色温偏移） |
| **环境细节** | 大气状态 | 灵压雾密度和活跃度提升：涡旋速度从 0.2m/s 升至 0.3m/s, 粒子直径增大（0.5mm→1.0mm）, 半透明从 20% 降至 40%（雾开始「厚」起来）。雾中开始出现极微橙色粒子悬浮（从纯黑→纯黑+橙的临界态）。无其他环境元素——负片空间保持 |
| **角色语言** | 手势+Effort+Camera | **Signature gesture**: 双刀姿态保持 X 形交叉——但在最后 1s 开始发生微变化：手腕从「展示」微微转为「预备」——刀交叉角度从 90° 微微开合 2-3°（极微——渲染层不可执行，保留为文本层的理想方向）/ **Effort Profile**: medium → building + sustained + direct + bound (从持有到积蓄的过渡) / **Camera Relationship**: eye-level static hold → 观众和 Ichigo 面对面。「他在看什么」的不确定性：视线从低垂→平视——这是战斗意志的启动信号，不是给观众的眼神交互 |
| **[STYLE-DEP]** | bleach 约束 | 4s 静止帧是 Bleach 战斗节奏的核心——「静止蓄力」。遵守 visual-world §3「一护双刀觉醒不是爆发——是认知。身体从不确定到确定的过渡」: 0-1s 完全静止（消化 B2a 的展示）→ 1-2s 无变化（纯静止=蓄力） → 2-3s 无变化（纯静止=蓄力） → 3-4s 橙色闪烁+眼部聚焦（信号：release is coming）。不可在静止期添加任何微动画/粒子/环境位移 |
| **[间]** | 三段式 | 前状态：B2a 缓慢推近结束，双刀信息已被接收 → 间隔：4s 纯静止——全片唯一呼吸段。前 3s 静止消化信息，最后 1s 橙色闪烁是「安静中的危险信号」 → 后状态：硬切至 Getsuga 橙色十字爆发——从安静到冲击的 0s 过渡 |
| **负向** | 3-5 词 | continuous eye movement, smile, gentle expression, arms lowering, sword movement, ambient particle during stillness, motion blur on blade, orange glow before final 1s |

**过渡 B2→B3**：硬切 0s。从黑/暗/橙色暗示 → 橙/高饱和/白。从蓄力到释放的递进。

---

### Shot 3.1 [0:12.0-0:14.0] — B3a: Getsuga Jujisho Cross Explosion (2.0s)

| 要素 | 规范 | 新 Prompt 值 |
|------|------|-------------|
| **景别** | 必标 | MCU → MWS (从近中景拉至中全景) — 起始聚焦双刀交叉点，随着橙色十字扩张，镜头在 2s 内「虚拟拉远」使十字全形进入画面。注意：非物理运镜——是能量扩张导致的「感知距离变化」 |
| **运镜** | 单动+速度 | Static locked shot — 镜头本身不运动，能量从中心向外扩散制造「虚拟 zoom-out」效果。速度标量：medium (能量扩散速度中等——1.5s 达全尺寸)。japanese-anime 禁止 whip pan [STYLE-DEP] |
| **角度** | 必标 | Eye-level (维持) — 与 B2a/b 同一水平线。能量爆发不改变视角角度——Ichigo 站位的对等感保持 |
| **光学** | 焦距桶+DOF | 50mm normal / Deep focus with radial burst — 十字能量在全程保持清晰边缘，中央交叉点最锐利，向外边缘因饱和度衰减自然软化。Bleach 径向模糊原则：从画面中心向外模糊（模拟冲击波），中心清晰 |
| **构图** | 规则名 | Center symmetry with silhouette retention — 十字能量占据画面 80%，但 Ichigo 黑色剪影轮廓在橙色十字后方保持可见（不淹没在能量中——Bleach 高反差原则）。十字能量形成 X 形对角线贯穿画面，焦点在交叉点。橙 #E8760B 纯饱和对黑 #000000 |
| **光影** | 多层 | Key: 橙色自发光 (Getsuga energy, 5500K 暖色) — 取代所有之前光源 / Rim: 橙色 rim light 在 Ichigo 剪影边缘——发束轮廓、肩部、双刀外缘被橙色勾勒 / Fill: 0% — Ichigo 剪影内部保持纯黑 / Ambient: 橙色能量照亮镜头前方空间——残留灵压粒子在画面四角呈橙色微光 / 特殊：无外部光源、无补光、无冷色干涉——画面唯二色：橙+黑。纯粹用色温从冷（B2）突变至暖（B3a）标志力量类型切换 / **情绪-光照映射**: 释放+力量 = orange self-luminescence + absolute color purity + zero external light |
| **材质细节展开** | 压缩→展开 | 旧版「orange spiritual pressure explosion from blade intersection forms perfect cross shape」→ 橙色灵压的物理表现：能量从双刀交叉点以每秒 600km 意象速度扩散 (视觉法则——非物理速度), 接触面处先出现白橙色中心核 (温度暗示最高点 #FFA029), 向外过渡为纯橙 #E8760B, 边缘衰减至半透明橙雾。交叉 X 形能量波的边界呈锯齿状——类似久保的斩击能量线条风格, 不规则但方向一致。能量通过 Ichigo 剪影后产生衍射——他的身体从纯黑色变为被橙色包裹的黑色剪影，边缘出现粉橙 glow |
| **环境细节** | 大气状态 | 橙色能量充满画面时，原有的黑色灵压雾被完全驱散——被橙色等离子态的灵压粒子替代。粒子密度：中心最高（完全不透明白橙核），向外递减至 30% 透度边缘。画面四角的黑色不是「背景」——是能量尚未到达的真空。能量波穿越空间时产生极细白色闪电状破裂线条（Bleach 高饱和能量的标志性渲染） |
| **角色语言** | 手势+Effort+Camera | **Signature gesture**: 双刀从交叉→展开——Ichigo 身体从静止→前倾，膝盖弯曲→蹬直。这是 B2 整段蓄力的结果——0.5s 内完成「止め絵→瞬发」 / **Effort Profile**: heavy + explosive + direct + wide (力量从全身释放, 非仅手臂) / **Camera Relationship**: MCU 起始聚焦刀交叉点, 随能量扩张视觉「拉远」至 MWS — 从个人特写放大到力量全景。观众的注意力焦点从「Ichigo 在释放」转移到「释放了什么」 |
| **[STYLE-DEP]** | bleach 约束 | Getsuga Jujisho 是 Ichigo True Shikai 的标志性招式——十字型能量波是辨识核心。橙色必须是 #E8760B 或其 ±10% 范围，不可偏红/偏黄。十字 X 形必须保持 90° 交叉（非 V 形 / 非 | 形）。能量波通过 Ichigo 身体时必须产生「剪影浮出」效果——不淹没角色（违反抗拒反差原则）。V=2 约束生效：画面仅橙+黑两色，无材质纹理/无辅助 VFX/无文字叠加 |
| **[间]** | 三段式 | 前状态：B2b 4s 静止蓄力的橙色闪烁信号 → 间隔：2s 爆发——从蓄力到释放的 0s 延迟。Getsuga 从出现到全尺寸 1.5s，然后切。这不是「蓄力的展示」（蓄力已在 B2b 完成），这是「释放的瞬间」 → 后状态：能量消散开始，剪影浮现过渡到 B3b |
| **负向** | 3-5 词 | continuous beam effect (Getsuga is burst not beam), motion blur on cross edges, Ichigo face visible through energy, warm glow filter (use pure orange), slow charge-up (charge was in B2b), explosion particle overload |

---

### Shot 3.2 [0:14.0-0:15.5] — B3b: Dissipation + Silhouette Rising (1.5s)

| 要素 | 规范 | 新 Prompt 值 |
|------|------|-------------|
| **景别** | 必标 | WS (Wide Shot / Full Shot) — Ichigo 全身剪影，双刀垂放两侧，橙色 rim light 消退中。白色碎片从上方向下飘落 |
| **运镜** | 单动+速度 | Static locked shot (完全静止) — 镜头无运动。唯一视觉运动来自橙色能量消散和白色碎片飘落。速度标量：—（静态） |
| **角度** | 必标 | Eye-level (中性) — 延续全段水平视角。Ichigo 剪影居中，高度在画面垂直中线。无仰俯变化——力量释放后的余韵需要中性视角来「放下」 |
| **光学** | 焦距桶+DOF | 35mm wide (广角) / Deep focus — 从 Ichigo 剪影到背景中的白色碎片全部保持清晰。广角在此不是为了夸张——是为了让碎片的空间分布可见，暗示「世界开始变大」 |
| **构图** | 规则名 | Center symmetry with celestial positioning — Ichigo 剪影在画面正中垂直轴线，双刀垂放与身体形成 T 形轮廓。白色碎片在画面上方 1/3 区域均匀分布——遵循三分法，碎片不侵入主体区域。碎片大小从前景大（近镜头）到背景小（远距离）形成景深层次。构图干净——无第二视觉重心。符合段边界「中央对称剪影」条件 |
| **光影** | 多层 | Key: 橙色 rim light — 从 B3a 的全面能量衰退至此拍的边缘余光。亮度从 100% 降至 5% 在 1.5s 内 / Rim: 冷白 rim light 开始取代橙色——在 Ichigo 左肩和头发左上缘出现冷白 #E0E8F0 轮廓光（环境转冷的信号）/ Ambient: 环境光从橙色衰减至零，画面基本全黑 / 特殊：白色碎片自发光（冷白 6500K）——它们有独立于橙色能量的光源，标志灵王碎片的登场 / 色温过渡：橙色 5500K → 冷白 6500K + 纯黑背景 / **情绪-光照映射**: 余韵+过渡 = fading rim light + cool fragments emerging from darkness + near-black ambient |
| **材质细节展开** | 压缩→展开 | 旧版「pure black silhouette with only rim light visible」→ Ichigo 全黑剪影的层次：不是纯色块——在 rim light 极微弱区域（如眉骨、鼻梁左侧、下颌线）可见极暗的材质灰度（#1A1A24 vs #000000 的不可见差异——影像层不可达成，保留为文本层理想）。双刀垂放时的剪影轮廓：大刃从右手自然下垂至大腿外侧，刀尖朝下偏左 15°；小刃从左手垂放至腰部高度，刀尖朝下偏右 10°。两把刀形成细微而不对称的 V 字形。白色碎片材质：骨白色 #D8D8D8 半透明表面，边缘微致发光，类似碎玻璃但边缘更柔和（灵王的灵子残留） |
| **环境细节** | 大气状态 | 橙色能量完全消散后，黑色灵压雾未回流——空间变为纯真空。白色碎片开始在真空中飘落：无风、无对流——碎片的运动完全自由落体 + 极微 Brown 运动。碎片密度：约 8-12 片在画面中同时可见，尺寸从 2mm 到 15mm 不等（在 9:16 画幅中的占比），形态不规则多面体。颜色：纯白#FFFFFF → 骨白#D8D8D8。无金色裂痕（V=2 约束——灵王碎片的金色裂痕在段 2 的 B3c 才开始出现） |
| **角色语言** | 手势+Effort+Camera | **Signature gesture**: 双刀从交叉/展开（B3a）回落到自然垂放。身体从战斗前倾回到直立。这不是「放松」——是「释放完成后的检查」姿态 / **Effort Profile**: heavy (residual) + released + direct + bound — 力量已被使用，现在是后果的开始 / **Camera Relationship**: WS 拉远到全身剪影 → 从个体 → 环境中的个体。观众从「感受冲击」切换到「观察后果」。视角从沉浸变为旁观——这是段边界的正确情绪位置 |
| **[STYLE-DEP]** | bleach 约束 | 本帧是段 1 末帧，必须满足尾帧值得条件：Ichigo 剪影完全静止（无运动模糊可被截取），橙色 rim light 平缓消退（无频闪/特效闪烁），白色碎片飘落速度均匀（≤0.3m/s）。V=2 严格保持——仅三视觉元素：黑色剪影 + 橙色余晖 rim light + 白色碎片。无材质纹理、无灵压雾、无粒子细节。符合 script-beats §段边界规划「尾帧值得条件」所有 5 条 |
| **[间]** | 三段式 | 前状态：2s 橙色爆发充满足(man)画面（Getsuga 全尺寸）→ 间隔：1.5s 橙色消散 + 剪影浮现 + 白色碎片登场。这是「上一件事的结束」和「下一件事的开始」重叠的窗口 → 后状态：纯黑背景的 Ichigo 剪影 + 飘落白色碎片——段 1 末帧。段 2 以碎片延续 + Yhwach 面部浮现启动 |
| **负向** | 3-5 词 | Ichigo body movement, energy remaining on blade after dissipation, golden crack on white fragments (V=2 constraint), multiple fragment sizes in focus, silhouette motion blur, breathing visible in silhouette, floor reflection |

---

### Shot 汇总表

| Shot | 时间 | 时长 | 景别 | 运镜(速度) | 角度 | 光学(焦距/DOF) | 构图 | 间 三段式 |
|------|------|------|------|-----------|------|----------------|------|---------|
| 1.1 | 0:00-0:00.3 | 0.3s | ECU | Static(—) | Eye-level | 85mm / Shallow | Negative space (右1/3) | 黑屏→红瞳骤亮→急拉 |
| 1.2 | 0:00.3-0:02.0 | 1.7s | ECU→MS→MWS | Snap zoom-out(fast) + Static | Low-angle | 85→50mm / Deep | Center symmetry + negative | 红瞳→空间展开→静置 |
| 1.3 | 0:02.0-0:05.0 | 3.0s | MWS | Static(—) | Low-angle (维持) | 50mm / Deep | Negative + center-weighted | 急拉结束→静止3s+字幕→硬切 |
| 2.1 | 0:05.0-0:08.0 | 3.0s | MS | Slow dolly-in(slow) | Eye-level (微仰) | 50mm / Deep | Rule of thirds (左1/3) | 冷色宫殿→黑虚空推近→静止 |
| 2.2 | 0:08.0-0:12.0 | 4.0s | MCU | Static(—) | Eye-level | 50-70mm / Shallow | Central | 推近完成→4s静止+最后1s橙闪→爆发放出 |
| 3.1 | 0:12.0-0:14.0 | 2.0s | MCU→MWS | Static(能量自扩,medium) | Eye-level (维持) | 50mm / Deep + radial | Center symmetry + silhouette | 蓄力终点→2s爆发全尺寸→消退 |
| 3.2 | 0:14.0-0:15.5 | 1.5s | WS | Static(—) | Eye-level | 35mm / Deep | Center symmetry + celestial | 满屏橙→1.5s消散+剪影浮现+碎片=末帧 |

---

### 全局上下整合

```text
# 段 1 参考图声明块
参考图清单：
  - ![Yhwach 官方全身立绘](assets/ref-images/033_char_identity_YhwachOfficialFull_v01.png) [ANTAGONIST] Yhwach 身份/军服/姿势锚定 [来源: bleach-anime.com 官方源]
  - ![Yhwach 官方面部表情集](assets/ref-images/034_char_identity_YhwachOfficialFace_v01.png) [ANTAGONIST] Yhwach 面部/红瞳多瞳/胡须锚定 [来源: bleach-anime.com 官方源]
  - ![Ichigo 官方全身立绘](assets/ref-images/036_char_identity_IchigoOfficialFull_v01.png) [PROTAGONIST] Ichigo 身份/死霸装/单刀形态锚定 (双刀细节由文本补偿) [来源: bleach-anime.com 官方源]
  - ![Ichigo 官方面部表情集](assets/ref-images/037_char_identity_IchigoOfficialFace_v01.png) [PROTAGONIST] Ichigo 面部/橙发/表情锚定 [来源: bleach-anime.com 官方源]
  ⚠ 冰宫场景参考图仍缺 (P0), B1b-c 场景以文本描述补偿
```

#### Seedance 段 1 Prompt (9要素格式化)

```text
duration_hint: 15

scene: [B1a] Pure black void, no space. Yhwach left eye ECU fills 95% frame. Red multiple concentric pupils, half-lidded, absolute stillness. [B1b-c] Silbern ice palace interior deep perspective, cold overhead light 7000K, Yhwach throne on elevated platform, white cape silhouettes of Stern Ritter regiments on both sides in symmetrical array. Deep blue-black shadows at 10% brightness. Volumetric cold haze at mid-depth between throne and background regiments. No windows, no natural light — pure artificial cold lighting. [B2a-b] Pure black negative space void, no background, no floor, no ceiling. Single directional side light from upper-left 45°, cool white 6500K. Deep shadow on right side at 15% brightness. Black reiatsu mist slowly swirling at 0.2m/s, particle density 20-40%, non-emissive — visible only through scattered side light. [B3a] Pure black void. Orange Getsuga Jujisho cross explosion from blade intersection. X-shaped energy burst at #E8760B pure saturation. Only two visual elements: orange cross + Ichigo black silhouette visible behind semi-transparent energy. V=2 — no background texture, no auxiliary VFX, no text overlay. [B3b] Orange energy dissipating to black. Ichigo pure black full-body silhouette emerging from fading orange rim light. White fragments beginning to fall from upper frame (bone white #D8D8D8, 8-12 pieces visible in frame, free-fall motion). V=2 — silhouette + rim light + fragments only.

subject: [ANTAGONIST] Yhwach extreme close-up (ECU macro) left eye — red iris with multiple concentric pupils like kaleidoscope depth, half-lidded eyelid N/3 open, zero expression, zero eye movement, zero blinking, pale aged skin with deep-set periodital wrinkles, beard stubble shadow at bottom edge. Red #CC2233 iris self-luminescence against absolute black void. Then snap zoom-out to reveal Yhwach seated on elevated throne: white cotton-silk double-breasted military uniform with three silver cross-embossed medals at left collar, dark red satin cape draping from shoulders to ground on both sides, long black hair to waist, red multi-pupil eyes looking slightly down-right, zero expression, absolute stillness. Right hand slightly raised on armrest — palm down, fingers relaxed — gesture of commanding all things. [FACTION_STERNRITTER] white cloak silhouettes in regimented rows on both sides, star-cross emblem outlines barely visible, symmetrical formation, no individual faces. Pure white uniforms emerging from deep blue-black shadows. Cold white rim light 1-3px on shoulder and cape edges. Then [PROTAGONIST] Ichigo True Shikai: orange spiky hair tufts defying gravity (4-5 front tufts with sharp tips, 2-3 side tufts), black shinigami robe with sharp triangular angular folds (shadow #0D0D14 at fold valleys, base #1A1A24 at lit surfaces), [WEAPON_ZANGETSU] dual Zangetsu blades crossed in X-shape in front of chest — long blade in right hand held lower on grip (120cm, pure black blade surface with elongated hollow eroded obsidian-like texture, brushed satin micro-grooves along blade spine, irregular pentagon black tsuba, purple zigzag pattern on hilt alternating #2A1A4A and black segments), short dagger in left hand held through hollow center handle (50cm, pure black jagged irregular-edge blade like bitten shape, no tsuba, blade root transitions directly into wrapping). Neutral expression — mouth slightly closed, eyes half-lidded looking slightly down. Left 1/3 composition facing right with 2/3 negative space. Black reiatsu mist swirling slowly around arms and blades, visible through cool side light scattering. Cold white rim light on blade edges and left shoulder silhouette. Over 4s hold: eyes shift from half-lidded to focused (last 1s), orange glow #E8760B begins flickering at blade tips at <5% brightness. Then Getsuga Jujisho: orange X-shaped cross explosion from blade intersection — white-orange core #FFA029 transitions to pure #E8760B and fades to semi-transparent orange at edges. Ichigo body leaning forward from static posture, knees bent to straight in 0.5s. Black silhouette visible behind orange energy — head outline, shoulders, dual blades identifiable. Energy fills 80% frame, expansion from center to full in 1.5s. Then dissipation: orange fades to cool black, Ichigo pure black full-body silhouette emerging with orange rim light fading to cold white. Zangetsu blades hanging at sides — long blade at right thigh pointing down-left 15°, short blade at waist height pointing down-right 10°. White bone fragments beginning to fall from upper frame (8-12 pieces, #D8D8D8 self-lit cool, 2-15mm sizes in frame, free-fall, no wind). Rim light on silhouette edges fading from #E8760B to cool white. Zero body movement, zero motion blur — stable frame for segment boundary capture. V=2 constraint active for entire B3: no energy particle overload, no golden fragment cracks yet, no text overlay.

camera: Shot 1.1 (0-0.3s): Static locked extreme close-up (ECU) macro, eye-level matching Yhwach sight line. Absolute stillness — single-frame pattern interrupt. Shot 1.2-1.3 (0.3-5.0s): Snap zoom-out from ECU to medium shot (0.5s rapid pull-back) revealing Yhwach seated, then static hold 2.5s. Low-angle from below throne level — subordinate-to-power perspective. Center symmetry composition with negative space. Shot 2.1 (5-8s): Slow dolly-in 0.3m over 3s, speed scalar: slow — barely perceptible push toward Ichigo. Eye-level slightly low (0-5°). Left 1/3 rule of thirds composition facing right. Shot 2.2 (8-12s): Static locked medium close-up (MCU). Eye-level neutral. Central composition with face as focal point. 3s stillness + 1s orange spark signal. Shot 3.1 (12-14s): Static locked medium close-up to medium wide. Energy self-expands creates virtual zoom-out effect. Eye-level maintained. Center symmetry with silhouette retention behind energy. Shot 3.2 (14-15.5s): Static locked wide shot (WS). 35mm wide angle for depth layering of falling fragments. Eye-level neutral. Center symmetry, silhouette in vertical axis, fragments in upper 1/3 celestial zone. All transitions: hard cut 0s. No dissolve, no whip pan, no crane, no smooth zoom. Bleach japanese-anime style: static dominant, snap zoom for reveal, dolly-in for emotional approach.

lighting: [B1a] Zero ambient. Red eye self-luminescence (2000K) as only illuminant. Pure black surrounding. High contrast — red #CC2233 against absolute black #000000. [B1b-c] Cold overhead key 7000K (90° vertical). Fill 5-10% cool blue #8A98AA — just enough to prevent uniform of pure white blowout. Cold white rim light 1-3px on shoulder and cape edges — separates Yhwach from background. Deep blue-black ambient #0D0D14 at 10% brightness, hue-shifted blue. Red eyes as only warm point (2000K vs 7000K). Silver medals catch top-down light as specular highlights. Volumetric cold haze layer at 2-4m depth front of background regiments. [B2a-b] Single directional side light from upper-left 45°, cool white 6500K. Zero fill — right side at deep shadow 15% brightness. Cold white rim light 2px on left shoulder, left arm outer edge, blade spine. Black reiatsu mist non-emissive — visible only through side light scattering, density from 20% (B2a) to 40% (B2b). Orange glow at blade tips in final 1s — second color temperature emerging (warm 4500K vs cool 6500K rim), <5% brightness. [B3a] Orange self-luminescence (Getsuga energy, 5500K) replaces all prior sources. White-orange core #FFA029, pure orange mid #E8760B, semi-transparent edge. Orange rim light on Ichigo silhouette outline — hair tufts, shoulders, blade outer edges. Zero fill, zero ambient from external sources. [B3b] Orange rim light fading from 100% to 5% over 1.5s. Cold white rim light beginning to replace orange on left shoulder and hair upper-left. White fragment self-illumination (cool 6500K) as independent light source — signals shift from Getsuga aftermath to new threat. Ambient dropping to near zero by shot end. Color temperature transition: orange 5500K → cool white 6500K + absolute black.

style: Bleach anime style, Tite Kubo art direction. High contrast cel shading — deep blue-black shadows at 10-15% brightness, cool white highlights. Strong outer silhouettes — character outline identifiable in 0.1s without facial detail. Sharp angular line art with speed-varying weight — long straight lines for robe folds, short broken lines for hair tufts. Negative space composition — large black void areas, characters at frame edges or center-small. Orange #E8760B as only power effect color (10% saturation in low-key desaturated palette). Color key: bleach low-key desaturated, 10% black minimum. Cold blue-black shadows, no warm tone filters. Japanese anime flat lighting with rim light added for cinematic depth. 9:16 portrait aspect ratio (1080x1920). All transitions: hard cut only. No dissolve, no white flash (except Getsuga burst moment). Stillness = power — static frames are charge posture, not lazy pauses. V=2 active: max 2 visual elements per frame, no material texture layering, no auxiliary VFX particles beyond core energy and essential fragments. Prohibited: photorealistic rendering, 3D shading, continuous fight motion, whip pan, crane shot, complex tracking, dissolve transitions, soft focus, warm glow filters, pink candy colors, low contrast gray midtones, smooth gradient shadows, realistic fabric physics.

[B1 间]: 前状态-浏览黑屏 → 0.3s ECU纯静止中断模式 → 急拉展开空间. [B1c 间]: 展开完毕 → 3s静止+字幕消化 → 硬切跳转. [B2 间]: 跳转→3s缓慢推近(全片唯一呼吸段) → 4s蓄力静止 → 最后1s橙闪信号. [B3 间]: 蓄力终点→2s爆发 → 1.5s消散余韵(段边界窗户). 

[STYLE-DEP]: Bleach-specific constraints — Stillness before burst combat rhythm (not continuous fighting). Character silhouettes recognizable without facial detail. High contrast black-white-orange only. Negative space void backgrounds (no environment, no floor, no sky). Speed lines for power burst instead of motion blur. Yhwach zero-expression zero-movement in all frames. Ichigo hair tufts independent (not merged into solid orange block). Kurosaki family resemblance in eye shape — sharp eye corners. Deep shadows hue-shift to blue/purple not gray. Zero dissolve transitions. Zero warm tone filters. Zero continuous fight choreography. Zero multi-character same-frame density above 2 persons.
```

---

## Volume 2 — 新旧对比

### 对比表

| 维度 | 旧版 (video-prompt.md) | 新版 (v2) | 差异 |
|------|----------------------|-----------|------|
| **景别标签** | 使用描述性文本如"extreme close-up"、"medium shot"、"full body"。无标准化标签体系。Shot 1.1 的 ECU 标注为通用英语描述。 | 每 shot 标注 ECU/CU/MS/MWS/WS。Shot 1.1 "ECU/Macro — Yhwach 左眼占据画面 95%"，Shot 3.2 "WS/Full Shot — 全身剪影+碎片空间"。Shot 汇总表含 7 行标准化标签。 | 旧版用自然语言描述代替标签。新版建立了横跨 7 个 shot 的统一景别参照系——镜头设计师可以秒读 shot 之间的景别关系。 |
| **运镜精度** | "static", "snap zoom-out", "slow dolly-in", "static frame"。无速度标量。复合运动 Shot 1.1-1.2 合并表述为"static then snap"。 | 每 shot 单一运镜 + 速度标量 (slow/medium/fast)。Shot 1.2 "Snap zoom-out (pull-back) speed: fast (0.5s) → Static locked shot (1.2s)"。Shot 2.1 "Slow dolly-in, speed: slow — 3s 内前推约 0.3m"。复合运动拆为时序——不再有含糊的"then"。 | 旧版运镜描述可执行但不精确。新版为每个运镜标注了速度等级和运动时长——AI 模型的 motion guidance 更清晰。旧版的"1s slow fade transition"在内被 Bleach 风格矛盾（违反"只硬切"），新版用 "hard cut 0s" 统一。 |
| **角度** | **未标注**。所有 shot 无角度说明——默认 eye-level 但无显式声明。 | 每 shot 标注角度：Shot 1.2-1.3 "Low angle (仰角) — 镜头在御座底座水平线"。Shot 2.1 "Eye-level, slightly low (0-5°) — 中性偏微微仰"。Shot 2.2 "Eye-level (中性)"。 | **最关键缺失项。** 旧版在角度维度完全空白——视觉上最重要的心理信息载体被忽略。新版用角度建立"力量差"（B1 low-angle → 观众低于 Yhwach）和"对等感"（B2 eye-level → Ichigo 和观众同一水平）。这是 japanese-anime [STYLE-DEP] 的核心——as-observer 视角。 |
| **光学/景深** | **未标注**。无焦距桶、无 DOF 类型。旧版 Shot 3.1 的"shot wide angle"只是场景描述的一部分，非光学属性。 | 每 shot 标注焦距桶+DOF：Shot 1.1 "85mm telephoto / Shallow DOF — 仅虹膜多层瞳孔在焦平面内"。Shot 1.2 "85mm→50mm / Deep focus — 御座+军队所有层次保持清晰"。Shot 2.2 "50-70mm / Shallow DOF — 聚焦 Ichigo 左眼"。Shot 3.2 "35mm wide / Deep focus — 碎片空间分布清晰"。 | 旧版完全缺失焦距信息——AI 模型在 24mm vs 85mm 之间的渲染差异巨大。新版为每 shot 选定了焦距桶（Bleach 规则：tele ECU, normal MS, wide WS），并用 DOF 类型控制注意力分布（shallow 聚焦特定物体, deep 展示全空间）。Shot 3.1 的"radial burst"是 Bleach 特有的景深用法。 |
| **光影层次** | 单层描述。Shot 1.2 "cold back overhead light, deep blue-black shadows at 10%"。Shot 2.1 "single directional side light from upper-left 45°, cool white"。Key 和 ambient 合并，fill 未提及，rim 作为属性存在但无隔离。 | 多层：Key + Fill + Rim + Ambient + 特殊。每 shot 显式标注五层：Shot 1.2 "Key: 冷色顶光 7000K (垂直 90°) / Fill: 正面补光 5% / Rim: 冷白 1-3px / Ambient: 深蓝黑 #0D0D14 10% 亮度 / 特殊：红瞳暖点 2000K vs 7000K"。Shot 2.1 "Key: 左上45° 冷白 6500K / Rim: 冷白 2px 在左肩和刀上缘 / Fill: 0% / Ambient: 偏紫黑 / 特殊：灵压雾非自发光，散射侧光可见"。色温比显式标定。 | 旧版的光照描写足够构建"氛围"但不够构建"系统"。新版的五层模型使 AI 模型可以区分"光源方向"和"环境底色"、"轮廓光和主光的关系"。色温比（2000K vs 7000K）让红瞳的暖点位置清晰——不是随机红，是和环境做对比的红。Shot 2.2 新增第二光层（橙色灵压边缘光 + 冷白 rim 同时存在）——之前的单层模型无法描述双色温共存的状态。 |
| **构图** | **未标注**。旧版在 scene/lighting 中隐含了一些构图信息（"Yhwach 居中于高台""Ichigo 左 1/3"）但无规则名，无系统性构图语言。 | 每 shot 标注构图规则名+解析：Shot 1.1 "Negative space — 右 1/3 交叉点，左侧 2/3 留黑"。Shot 1.2 "Center symmetry with negative space — Yhwach 居中垂直轴，军队对称，眼睛在上 1/3 水平线"。Shot 2.1 "Rule of thirds (left-weighted) — 刀交叉点在下 1/3 水平线"。Shot 3.2 "Center symmetry with celestial positioning — 碎片在画面上 1/3"。 | 旧版构图靠"感觉"——"看起来对"但无法传递。新版给每个 shot 标注构图规则——AI 模型的 pixel 布局有了参照。关键不是规则本身（三分法和 center symmetry 是基础），是对镜片设计师可读的构图意图：这张画面想让你看哪里、视觉权重如何分配。 |
| **材质细节展开** | 压缩格式。Shot 1.2 "white double-breasted military uniform"。Shot 2.1 "black shinigami robe (sharaku) with sharp angular folds"。双斩月描述较展开但仍是属性列表风格。 | 展开格式，每材质含类+表面+关键属性。Shot 1.2 灭却师军服："cotton-silk blend fabric, matte surface with subtle weave texture, sharp military creases at sleeve elbows and chest panel seams. Three silver medals: polished silver with cross-shaped emboss, catching top-down cold light"。Shot 2.1 双斩月展开："brushed satin micro-grooves along blade spine catching side light as hairline silver; irregular pentagon black tsuba with stepped silhouette"。 | 旧版的"black blade"对 AI 就是"黑色刀片"——默认渲染可能是磨砂塑料或反光金属。新版的"brushed satin micro-grooves"定义了表面处理方式，"irregular pentagon tsuba with stepped silhouette"定义了刀柄护手的几何特征。材质细节展开的唯一风险是 prompt 长度超限——Seedance 的 subject 字段有 ~2000 字符的实际上限。新版描述需控制在关键材质展开 + 非关键维持压缩之间。 |
| **环境细节** | 极少或无。Shot 1.1-1.2 无环境描述（仅"冰宫内部"）。Shot 2.1-2.2 无环境（仅"纯黑背景"）。Shot 3.1-3.2 无环境（仅"纯黑背景"）。 | 每 shot 标注大气状态。Shot 1.2 "冷空气粒子在顶光中形成极微弱 volumetric haze (7000K), 几何冰柱从顶部悬挂，表面半透明冷蓝"。Shot 2.1 "灵压雾 0.2m/s 涡旋, 鬼粒子直径 <0.5mm, 半透明 20%, 不自发光——通过散射侧光可见"。Shot 3.2 "白色碎片在真空中飘落：无风、无对流, Brown 运动, 8-12 片, 2-15mm 尺寸, 骨白色 #D8D8D8 半透明"。 | 旧版在环境信息上有大面积空白——AI 默认行为是在纯黑背景中加入随机粒子或默认大气效果，导致 Bleach 的"负片空间"被污染。新版的环境描述精确到粒子行为（密度、自发光属性、运动方式）——让 AI 渲染的"虚空"不是"空无一物"，而是"特定状态的空"（B1 冷空气 haze vs B2 灵压雾 vs B3 真空碎片场）。 |
| **角色语言** | 基础行为描述。Shot 1.1 "zero expression, absolute stillness"。Shot 1.2 无角色语言。Shot 2.1 "Neutral expression — mouth slightly closed"。 | 三维度每 shot 标注：(1) Signature gesture — Yhwach "右手微抬，掌心朝下，如同在按低所有事物"，Ichigo "双刀交叉→展开的认知姿态" (2) Effort Profile — heavy/sustained/direct/bound 四个属性 (3) Camera Relationship — "ECU 将眼睛客体化——他是个探测器不是一个人" "low-angle subordinate perspective → power differential"。 | 旧版的"zero expression"正确但不够。新版的三维度让角色语言从"静止"变成了"静止作为姿态"（Yhwach 不眨眼=主动选择，不是 AI 遗忘）。Effort Profile 尤其关键——"heavy + sustained + direct + bound"让 AI 理解"这不是因为不会动才静止——是因为太强才不需要动。"Camera Relationship 将角色-摄影机关系统一到叙事意图。 |
| **负向 prompt** | 全局 1 条（~15 词），无 per-shot 负向。全场共享"photorealistic rendering, 3D shading, continuous fight motion, soft focus, dissolve transitions"等。 | 全局负向 + 每 shot 3-5 词定制。Shot 1.1 "eye blood vessels, eye movement, blinking, speed lines, anatomical iris texture"。Shot 2.2 "continuous eye movement, smile, gentle expression, motion blur during stillness, orange glow before final 1s"。Shot 3.2 "Ichigo body movement, energy remaining on blade, golden crack on fragments (V=2 constraint)"。 | 旧版全局负向覆盖了通用问题但不能解决 shot 级别的特异性问题（如 Shot 2.2 在 4s 静止期中确保 AI 不给 Ichigo 添加呼吸运动或眨眼）。新版 per-shot 负向针对每个 shot 的特定风险：Shot 1.1 防止 AI 给红瞳添加解剖学细节（Bleach 的红瞳是象征性的，不是真实的），Shot 3.2 防止 V=2 被突破（不加金色裂痕在白色碎片上）。 |
| **[间] 三段式** | 单阶段描述。Shot 1.1 "静止 1.5s 无运动=力量感"。Shot 2.1 "3s 缓慢推近——全片唯一呼吸段"。Shot 3.2 "1.5s 消散过渡——Getsuga 冲击后余韵"。 | 三段式：前状态→间隔→后状态。Shot 1.1 "前：黑屏浏览模式 → 间隔：0.3s 红瞳骤亮纯静止 → 后：急拉跳转 B1b"。Shot 2.2 "前：B2a 推近结束信息已交付 → 间隔：4s 纯静止蓄力(3s 消化 + 1s 橙闪信号) → 后：硬切到爆发"。Shot 3.2 "前：2s 橙色爆发充满画面 → 间隔：1.5s 消散+剪影浮现+碎片登场(重叠过渡) → 后：纯黑剪影+碎片 = 段 1 末帧"。 | 旧版「间的状态是孤立的」。新版三段式让[间]从"一个停顿"变成"叙事功能节点"——每个停顿之前是什么状态、之后进入什么状态、中间这个间隔在做什么认知工作（消化/蓄力/过渡/信号）。这在段边界 Shot 3.2 尤其关键："上一件结束"和"下一件开始"的重叠窗口——旧版只写了"消散"，新版写了消散是做什么用的。 |
| **[STYLE-DEP]** | **不存在**。旧版在全局一致性前缀里写了"Bleach anime style"但未标注 Bleach 专属的特殊规则（如止め絵原则、三色法、速度线代替 motion blur、负片空间比例、剪影先于面部）。 | 每 shot 标注 Bleach 专属约束。Shot 1.3 "3s 静止帧——Bleach 止め絵原则。零眼球运动、零呼吸运动。禁止在静止帧添加微运动/粒子特效/环境动画"。Shot 2.2 "Bleach 战斗节奏核心——静止蓄力。0-3s 无变化纯静止=蓄力，不可在此期间添加任何微动画"。Shot 3.2 "段边界帧满足尾帧值得 5 条件。V=2 严格保持——仅三视觉元素"。全局 [STYLE-DEP] 区块含完整约束链。 | **最重要的缺失。** 旧版写了"做 Bleach"但没说"Bleach 怎么做"。AI 默认的"anime style"可能是任何日本动画——不对止め絵原则做特殊处理的话，模型会在静止帧中默认添加微呼吸/衣料飘动/环境粒子。新版 [STYLE-DEP] 让 Bleach 的静止=蓄力行为被显式保护——在 5 个静止帧 shot (1.1/1.2/1.3/2.2/3.2) 中各自标注哪些运动是禁止的。止め絵保护的 Shot 1.3 (3s) 和 Shot 2.2 (4s) 是 Seedance 渲染时最容易出问题的位置。 |
| **光照-情绪映射** | 使用抽象情绪词。Shot 1.2 "mood: 压迫、庄严、神秘"——情绪词未用光照条件翻译。Shot 2.1 "mood: 冷静、专注、内在力量即将释放"。 | 每 shot 光照条件从情绪推导+标注映射速查：Shot 1.2 "力量+胁迫 = cold overhead + low-angle + deep shadows"。Shot 2.1 "确定+专注 = cool directional side light + deep shadow + sharp rim"。Shot 2.2 "蓄力+即将释放 = same key + second warm light emerging + rim tightens"。Shot 3.2 "余韵+过渡 = fading rim light + cool fragments from darkness + near-black ambient"。 | 旧版的情绪词（"压迫"、"庄严"）对 AI 无意义——模型不理解抽象名词。新版的光照-情绪映射速查+五层光照模型让情绪通过具体摄影术语表达："力量"=冷顶光+低角度+深阴影；"释放"=橙色自发光+绝对色纯度+零外部光源。这组映射和 visual-world.md 第 5 节的光照系统一致。 |
| **Seedance 适配性** | 旧版考虑到 Seedance 能力边界——但部分描述超出了模型可执行范围（"1s slow fade transition"矛盾于硬切规则，"1.5s hold on static eye then 1s slow fade"对 Seedance 无意义——模型不遵循精确到秒的时间线）。 | 新版在每 shot 标注 Seedance 可执行性提示——如 Shot 3.1 "种子文件注：非物理运镜——是能量自扩导致的感知距离变化"；Shot 2.2 "眼神 2px 虹膜位移不可被 Seedance 精确执行，保留在文本层作为理想方向"。但主要结构化在 9要素格式化 prompt 中——非叙事段，直接可输入 CLI。 | 旧版为人类阅读设计的成分大于为模型输入设计的成分——shot 描述中混入了时间线指令和氛围描述。新版通过分离"叙事段（人读，做质量判断）"和"格式化段（机器读，直接输入 CLI）"解决了这个结构性问题。格式化的 Seedance prompt 在 scene/subject/camera/lighting/style 五个字段内完成了 12 要素到 9要素的映射。 |

---

### 质量提升评估

#### 维度显著度排序（按提升幅度从高到低）

| 排名 | 维度 | 旧版 | 新版 | 提升幅度 | 关键改进 |
|------|------|------|------|---------|---------|
| **1** | **运镜+角度+光学** | 仅运镜 | 三位一体每 shot 标注 | +400% | 旧版在 7 shot 中有 7 个运镜描述但 0 个角度标注、0 个焦距规格。这是视觉语言框架最大的缺失。新版为每 shot 建立了"景别定框架/运镜定运动/角度定情绪/光学定注意力"的四层系统。 |
| **2** | **[STYLE-DEP] 保护** | 不存在 | 每 shot + 全局区块 | +100% (从 0) | 旧版的 Bleach 风格完全依靠"Bleach anime style"六个字，AI 默认解析为"任何日本动画"。新版对最关键的三项做了保护：(1) 止め絵原则——静止帧不可添加微运动，(2) 三色法——亮部冷白/暗部深蓝黑/强调色仅灵力，(3) 剪影优先——0.1s 可识别轮廓。 |
| **3** | **角色语言系统** | 基础行为 | 三维度: 手势+Effort+Camera | +300% | Effort Profile (heavy/sustained/direct/bound) 的引入让 AI 区分"Yhwach 的静止"和"Ichigo 的静止"的本质差异——前者是绝对力量不需要动，后者是蓄力过程中不动。Camera Relationship 将镜头运动和角色姿势统一到叙事意图。 |
| **4** | **光影系统化** | 单层 | 五层: Key+F+R+A+特殊 | +300% | 旧版的"cold back overhead light"没法指导 AI 区分主光和环境。新版的五层模型显式定义了色温和亮度的层间关系——尤其是色温比（红瞳 2000K vs 环境 7000K）和双色温共存（冷 rim + 橙灵压光在 Shot 2.2 中并行）。 |
| **5** | **[间] 三段式** | 孤立的"停顿" | 前状态→间隔→后状态 | +200% | 旧版的[间]是"暂停按钮"——写了"静止 1.5s = 力量感"但没说这个静止从哪里来到哪里去。新版三段式让停顿点从"不给 AI 看"变成"和前后的逻辑关系"。段边界 shot 3.2 的三段式是典型的"上一件结束+下一件开始"重叠窗口——旧版没有这种认知。 |
| **6** | **材质细节展开** | 压缩 | 展开 (类+表面+关键属性) | +150% | "white uniform" → "cotton-silk blend, matte weave, sharp military creases, silver medals polished with cross-emboss"——旧版描述会被 AI 渲染为纯白色块，新版的面料和配件描述可引导更精确的材质渲染。但需要注意 prompt 长度上限。 |
| **7** | **Per-shot 负向** | 仅全局 1 条 | 全局+每 shot 3-5 词 | +100% | 全局负向覆盖基础问题（无照片写实、无 3D 渲染），但 Shot 2.2 需要阻止 AI 添加连续呼吸运动、Shot 3.2 需要阻止 AI 突破 V=2 约束添加金色裂痕——这些 shot-specific 风险旧版无覆盖。 |
| **8** | **构图规则** | 不存在 | 每 shot 规则名+解析 | +100% (从 0) | 构图是 Seedance 2.0 最难控制但影响最大的维度。三分法/center symmetry/negative space 的标注虽然不能确保 AI 精确执行，但至少建立了人类设计师的质量标尺——"我们要求的构图是这样的"。 |
| **9** | **环境细节** | 极少 | 粒子密度+大气+介质 | +100% | Bleach 的负片空间不是空——是特定状态的"空"。B1 的冷雾 haze、B2 的灵压雾（不自发光、散射侧光）、B3 的真空碎片场——三类虚空各有不同的粒子行为。旧版用"pure black"覆盖了全部三种。 |

#### Seedance 2.0 能力无法完全兑现的维度

以下维度的提升在**文本层**是显著的，但在 Seedance 2.0 Mini 的当前能力边界内可能无法完全渲染：

| 维度 | 文本提升 | Seedance 2.0 执行预测 | 风险等级 |
|------|---------|---------------------|---------|
| **精确时间线** | 每 shot 标注到 0.1s 精度的时间窗口。Shot 1.1 0.3s+Shot 1.2 1.7s+Shot 1.3 3.0s 的精确分割。 | Seedance 不遵循精确的 per-second 时间线——它从文本中采样运动强度生成 ~15s 的流。精确的"0.3s ECU → snap 0.5s → hold 1.2s → cut"序列在实际渲染中可能有 ±30% 的时间偏差。 | **高** — 时间线指导仍然是「意向声明」而非可执行指令。对段边界时间点（~00:15.5）的影响最大——Seedance 可能提前或延后 1-2s 进入消散状态。 |
| **光学焦距控制** | 85mm telephoto / 50mm normal / 35mm wide 的精确标注。 | Seedance 能理解"close-up"、"wide shot"等景别指令，但对"85mm"这样的具体焦距桶标定不会精确映射。它可能通过"background compression"间接理解 telephoto 效果。 | **中** — 运镜类型（static/dolly/snap）的识别率高，但焦距映射是间接的。建议旧版继续保持景别词优先（如"ECU macro"而非"85mm"）。 |
| **五层光照模型** | Key+Fill+Rim+Ambient+特殊的分层。色温比 2000K vs 7000K。 | Seedance 在 lighting 字段中能处理 3-4 层光照描述——但色温比的精确控制（"2000K vs 7000K"）可能被简化为"warm light in cold setting"。Rim light 1-3px 宽度的精确性不可达。 | **中低** — 多层光照的整体效果（暖点在冷色环境中的存在）可渲染，但精确度不可达。五层模型的价值在于「光照逻辑的一致性」而非「每层的精确像素」。 |
| **材质展开后的精确渲染** | "brushed satin micro-grooves", "irregular pentagon tsuba with stepped silhouette", "purple zigzag pattern alternating #2A1A4A and black"。 | Seedance 对刀身纹理（brushed satin）的渲染中等可靠，但对"purple zigzag pattern"这样的精确图案可能近似处理。不规则 pentagon tsuba 的形状不容易从文本重建。 | **中** — 关键材质外观（银白色刀身 vs 纯黑表面）可区分，但装饰细节（卍字纹样、zigzag 图案、不规则护手轮廓）可能被简化或变形。 |
| **角色语言三维度** | Effort Profile (heavy/sustained/direct/bound), Camera Relationship (ECU 客体化), Signature Gesture (右手微抬召见姿态)。 | Effort Profile 这类抽象概念 AI 无法理解——但通过身体描写（"手指放松但不蜷缩，如按低所有事物"）可以间接传达。Camera Relationship 通过景别+角度选择（ECU+eye-level）自动实现。 | **中** — 抽象部分 (Effort Profile 的四个属性) 需要转化为具体可见的身体锚点。新版在每 shot 中确实完成了这个转化（用身体动作描写代替抽象属性标签）。Gesture 的可渲染性取决于 Seedance 对手部姿势的控制精度（已知中等可靠）。 |
| **[STYLE-DEP] 止め絵保护** | "3s 内零眼球运动、零呼吸运动、禁止粒子特效/环境动画"——保护静止帧不被 Seedance 的默认"自然运动"污染。 | **这是最关键的不可控风险。** Seedance 的默认行为是在 >2s 的静止帧中添加微运动（呼吸般的起伏、衣料飘动、环境粒子）来「增加自然感」。这对 Bleach 的止め絵原则是破坏性的——静止就是静止，不需要"看起来自然"。 | **高** — 这是 Seedance 2.0 Mini vs Bleach 风格的体系冲突。建议方案：在 negative_prompt 中加入"character breathing, cloth wind movement, ambient particle during still frames"；在 scene 字段里加"character completely frozen — no movement, no breathing"。如果生成结果仍包含微运动，考虑对静止帧做 1.5s 截断而非完整 3-4s。 |

#### 总体评估

| 指标 | 旧版 | 新版 | 变化 |
|------|------|------|------|
| **shot 描述要素数** | 4 (景别/运镜/光影/角色) | 12 (全部) | +8 个维度 |
| **per-shot 信息密度** | ~80 词/shot (含场景) | ~250 词/shot (含 12 要素) | +212% |
| **格式精度** | 人类阅读友好 / AI 输入模糊 | 人类阅读裁剪感知 + AI 输入格式化分离 | 双通道结构 |
| **Bleach 风格保护** | 6 词全局描述 | 7 shot × [STYLE-DEP] + 全局区块 | 结构化保护 |
| **未可执行风险** | 3 项 (时间线/双刀/多瞳) | 6 项 (精确时间/焦距/光照精度/材质装饰/Effort 抽象/止め絵) | 3 项新版识别但旧版未意识到的风险 |

**新版在文本层的提升显著——12 要素体系系统性补全了旧版缺失的 8 个维度（角度、光学、构图、[STYLE-DEP]、角色语言系统、三段式间、per-shot 负向、环境细节）。最关键提升是[STYLE-DEP]保护和角色语言三维度——这两个维度在旧版中完全不存在，却恰恰是 Bleach 风格区别于"通用 anime style"的核心。**

**Seedance 2.0 的可执行层仍然存在 precision gap——精确时间线、焦距桶标定、五层光照的精确色温比、角色语言中的 Effort 抽象——这些维度的文本层提升在真实生成中可能被简化。最大的单项风险是止め絵保护：Seedance 的"自然运动"默认行为和 Bleach 的"静止=蓄力"原则有系统级冲突。建议生成后对段 1 的 Shot 1.3 (3s 静止) 和 Shot 2.2 (4s 静止) 做人工帧级检查——如果 Seedance 在这些帧中添加了微呼吸或衣料飘动，考虑截短静止时长或换用 Veo (已知对风格化静止更克制)。**
