# 视觉世界参考表

## 材质语言

材质一致性是独立于色彩与几何的第三类失败模式。agent 间压缩格式：`class + surface + 1 key attribute`；prompt 层展开为可生成的物理描述。

**材质类速查**：`fabric(cotton/linen/silk/wool/denim) | natural(wood/stone/leather) | metal(steel/aluminum/copper/brushed/polished) | glass(clear/frosted/mirror) | liquid(water/oil/blood) | bios(skin/hair/eye) | synthetic(plastic/rubber/carbon)`

### 材质展开速查

| 压缩 | prompt 展开 |
| --- | --- |
| fabric+velvet+soft | 短绒毛捕捉光线产生丝光，边缘磨损露底布 |
| fabric+denim+weathered | 靛蓝经纬纹理，膝部褪色泛白，边缘毛边，铜铆钉氧化 |
| natural+leather+aged | 棕色牛皮粒面纹理，弯折处皮纹裂纹，边缘磨损色深 |
| metal+steel+brushed | 拉丝不锈钢，平行刷纹均匀，光线沿线状高光，倒角反射 |
| metal+copper+patina | 青绿锈在凹陷堆积，露出暖色铜底，雨水冲刷痕 |
| glass+clear+frosted | 柔和漫射，边缘青绿色，手指印痕 + 细密划痕 |
| natural+stone+polished | 抛光大理石，灰色纹理放射状，反射柔和，边缘微小磕碰 |
| bios+skin+pore | 皮肤细纹肌理，颧骨泛红透毛细血管，毛孔均匀，干燥起皮 |
| bios+hair+fine | 每根发丝不同亮度反光，碎发飘散，自然弧度 |

**画质关键词**——有效：sharp focus, fine detail, texture visible, visible pores, material realism, natural variation。递减（慎用）：8K, hyperdetailed, intricate, masterpiece。无效：beautiful, stunning, gorgeous。皮肤：wet translucent dermis, visible capillaries, flyaway hairs。硬表面：crisp edges, consistent sharpness。

## 环境细节层次

环境不是背景。环境 dressing 缺失是"画面空洞"的首要原因。每场景激活 ≥1 项：

- **大气效果**（选 ≤2 项）：god rays through canopy / heat haze above asphalt / steam rising catching light / low-lying mist / condensation on window / breath fogging in cold air
- **天气与时间**：golden hour（暖+长影+rim）· blue hour（冷+剪影）· overcast（平）· rain（湿反射+水洼）· snow（积雪+足迹）· fog（低能见+光晕）· strong wind（摇摆+吹散）
- **飘落物**（≤1 种/场景）：cherry blossoms, embers, snowflakes, autumn leaves, dandelion seeds, ash, paper scraps, dust motes, fireflies
- **背景人群**：密度 sparse/moderate/dense；动态 blurred pedestrian movement / distant traffic / vendor steam

## 情绪动作化

### 身体锚点（禁用抽象情绪词）

| 情绪 | 可执行锚点 |
| --- | --- |
| 悲伤 | head lowered, shoulders trembling, eyes red-rimmed, breathing shallow |
| 紧张 | fingers tapping, breath quick, eyes darting, lips tight, weight shifting |
| 愤怒 | fists clenched, jaw tight, chest heaving, eyes fixed |
| 快乐 | smile reaches eyes, laugh lines, shoulders relaxed, bright eyes |
| 放松 | leaning back, eyes half-closed, slow deep breathing, shoulders dropped |
| 好奇 | leaning forward, head tilted, eyebrows furrowed, lips parted |
| 惊讶 | eyebrows raised, eyes wide, mouth open, breath caught, head pulls back |
| 恐惧 | body recoiling, eyes wide with sclera, hands raised, frozen |
| 坚定 | jaw set, shoulders squared, locked gaze, steady breathing |

### 微表情（≤1/3 秒，肌肉位移而非情绪名）

| 情绪 | 编码 |
| --- | --- |
| 悲伤 | 嘴角下拉 + 眉内角上抬 + 下眼睑微提升 + 鼻翼微扩 |
| 愤怒 | 眉间竖纹 + 眼皮微眯 + 嘴唇抿紧 + 鼻翼扩张 |
| 恐惧 | 眉平直上抬 + 露更多巩膜 + 嘴微张椭圆 + 下颌紧张 |
| 惊讶 | 眉高弧全抬 + 上眼睑最大提升 + 下颚下垂 + 前额水平褶皱 |
| 快乐 | 眼轮匝肌收缩（鱼尾纹）+ 下眼睑上推 + 嘴角外上斜拉 |
| 厌恶 | 鼻根横纹 + 上唇上提 + 下唇下压 + 嘴角后拉 |
| 轻蔑 | 单侧嘴角上拉 + 单侧眼微眯 + 头微偏 |

### 微动作

- **手部**：fingertips tapping / fingers wringing / thumb rubbing / nail pressing palm / knuckles white
- **呼吸**：slow deep belly / shallow rapid chest / held suspended / exhale shuddering
- **姿态**：weight shift / torso lean / shoulder roll / neck tilt / hip shift
- **目光**：steady contact / darting scanning / gaze drops / unfocused stare / eyelid flutter

### 环境交互（情绪在空间留下痕迹）

| 情绪 | 痕迹 |
| --- | --- |
| 悲伤 | 手划积灰台面留痕 / 窗上呵气画图案 / 站定雨中不避 / 盯冷咖啡 |
| 愤怒 | 拳锤桌面杯具震动 / 甩门 / 踢翻罐子 / 猛拉抽屉 |
| 快乐 | 踢落叶石子 / 手抚麦穗水面 / 转鞋跟 / 指尖弹伞上积水 |
| 紧张 | 反复开关打火机 / 翻卷纸页 / 把玩衣角 / 鞋底重复摩擦 |
| 放松 | 背靠墙下滑坐地 / 手指划墙面延线 / 重量完全卸在椅子 |
| 好奇 | 歪头身体前倾侵入空间 / 手指触碰摸索物体表面 |

## 角色语言

### 专属微动作（Signature Micro-gestures）

每个关键角色定义 2-3 个个人标记动作——不是通用情绪锚点，是这个角色独有的身体方言。例：把耳机线绕七圈又解开 / 说话前摸左耳垂 / 思考时指关节轻敲桌面匀速三下。每拍嵌入 ≤1 个（单拍单变量）；重复时变化幅度/速度/上下文。常见失败：签动零触发 → 关键行为拍强制安插；与情绪冲突 → 频次变化但不消失。

### 运动质量（Laban Effort）

| 维度 | 连续谱 | 心理关联 |
| --- | --- | --- |
| Weight | strong ↔ light | 全力施为 / 轻柔触碰 |
| Time | sudden ↔ sustained | 急促爆发 / 绵延不绝 |
| Space | direct ↔ indirect | 聚焦一点 / 环顾八方 |
| Flow | bound ↔ free | 拘束克制 / 奔放释放 |

八种动作驱力（Space + Weight + Time 组合）：

| 驱力 | Space | Weight | Time | prompt 短语 |
| --- | --- | --- | --- | --- |
| Float | indirect | light | sustained | floats, feet barely touch, loose gestures |
| Punch | direct | strong | sudden | explosive, deliberate weight, heavy steps |
| Glide | direct | light | sustained | continuous fluid, smooth transitions |
| Slash | indirect | strong | sudden | explodes and freezes, no transition |
| Dab | direct | light | sudden | bird-like, precise, no wasted motion |
| Wring | indirect | strong | sustained | holds tension, eyes roam, restrained |
| Flick | indirect | light | sudden | constant subtle motion, over-extends |
| Press | direct | strong | sustained | moves with weight, locked gaze |

Effort Profile 模板：`| 角色 | weight+time+space+flow → Drive |`，例 `| A(沉稳) | heavy+sustained+direct+bound → Press |`。Effort 与情绪冲突时，运动质量保持角色一致，情绪由速度/幅度调节。

### 角色-镜头关系

| 角色 | 距离 | 角度 | 运镜 |
| --- | --- | --- | --- |
| 主角/英雄 | MS-MCU | eye level+ / low | dolly + 跟拍 |
| 反派 | LS-MLS | low angle | 固定推近 |
| 导师/长者 | MS | 微 low angle | push-in |
| 脆弱者 | CU-ECU | 微 high angle | 手持微晃 |
| 神秘角色 | 变化 | oblique | 远摄不近身 |
| 喜剧角色 | 全身 | eye level wide | tracking + zoom |
| 恋人 | CU-ECU | eye level | smooth 环绕 |

### 角色间空间（Proxemics）

| 关系 | 距离 | 镜头 | 景深 | 叙事 |
| --- | --- | --- | --- | --- |
| 亲密 | <45cm | 双人 CU/ECU + OTS | 浅 | 爱情/对峙/暴力 |
| 个人 | 45-120cm | MS/MCU 正反打 | 正常 | 朋友/信任 |
| 社交 | 120-360cm | MLS/全景 | 深 | 正式/隔阂/阶级 |
| 公共 | >360cm | ELS 远景 | 深 | 孤独/对抗 |

距离变化 = 关系变化（社交→亲密 = 升温，亲密→社交 = 破裂）。单景中 3 拍内跨越 2 个距离带需过渡逻辑支撑，否则观众感知为空间跳跃。

### 情绪的个人化表达

通用层（上文身体锚点）保留，角色层覆盖：每角色定义 3 个情绪 × 个人化表达，每情绪 ≤3 条信号。例：`| A | 悲伤 → 1) 微笑但眼轮匝肌不动 2) 反复折叠手边物体 3) 语句完整度增加 |`。Duchenne Marker：`smile reaches mouth but not eyes, orbicularis oculi remains still`。角色层仅在情绪信号有区分度时定义，不替换通用层。

## 构图与安全边界

三分法 / 中心 / 负空间 / 引导线 / 框架——不叠加。**安全边界**：左右 ≥10%，上下 ≥8%，关键元素保持在边界内（防 9:16 边缘裁剪）。
