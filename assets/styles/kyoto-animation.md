# Kyoto Animation Style

> 京阿尼。不是"画风"，是对"真实的人如何感受世界"的视觉翻译。

## 核心美学

**角色的身体不撒谎。** 京阿尼的角色不是靠台词表达情绪——是靠身体。手指的犹豫、肩膀的微微下沉、眼神不聚焦的瞬间。这些微动作不是装饰，是叙事本身。

**光是记忆的质地。** 不是物理光照。是回忆里的光——窗边逆光的粉尘感、黄昏走廊的暖橙色漫反射、教室里的荧光灯冷白 + 窗外暖绿的补色。光在这里是时间流逝的标记。

**空间里有人活过。** 不是"场景"。是"某个人的房间"——书桌上摊开的笔记本、墙角的褪色贴纸、窗台上的灰尘。背景不是角色的容器，是角色内心世界的外延。

**运动服从情绪的节奏。** 平静时连头发飘动的速度都慢下来。激动时连背景都在呼吸。不是"动作快慢"——是整个世界和角色一起感受同一个情绪频率。

## 视觉语言

### 角色

- 面部：大眼睛是京阿尼标签，但**眼睛的焦点状态比大小重要**——失焦望向远方 vs 直视对方 vs 低头看自己手指
- 体型：女性角色纤细但不失力量感，男性角色修长。不追求夸张比例
- 头发：分层飘动，发梢半透明透光。风中头发的运动层次比角色动作更多
- 制服/日常服：精确到褶皱位置和布料垂坠方向。服装是性格的一部分

### 色指定

- 基调：高明度、中低饱和。整体偏向暖灰底
- 记忆色优先：天空比真实更蓝一点，樱花比真实更粉一点——不是写实，是"记忆中该有的颜色"
- 光色分离：同一场景中亮部偏暖（阳光）、暗部偏冷（天光反射），形成自然的色温对比
- 禁止：高饱和纯色大面积使用、滤镜式全局调色

### 摄影处理

- 柔焦/浅景深：不是模糊——是不在焦点上的部分稍微柔化，模拟人眼关注点
- 逆光溢光：角色轮廓周围 1-3px 的暖白溢光层，窗户/门口场景必用
- 空气透视：远处景物饱和度降低 + 轻微蓝移，近景暖、远景冷
- 镜头眩光：不是特效——是几个六角形光斑散落在画面边缘，像眼镜片上的反光

### 背景

- 参考级精度：建筑透视准确、植物有物种特征、室内物品有使用痕迹
- 水彩底 + 线稿：远景色块用湿水彩晕染感，中近景保留线稿结构
- 季节感：不靠"字幕写春天"——靠光线角度、植被密度、空气中的花粉感
- 校服/通勤/日常场景：不是"地点"，是"每天经过的地方"

## 时间与运动

**静止中的微动。** 京阿尼的"静止"帧从不真正静止——发丝飘动、窗帘呼吸、远处树叶沙沙、杯中水面的微小涟漪。这些不是"为了让画面不无聊"——是"这个瞬间在时间中继续流逝"的证据。

**情绪的物理重量。** 一个角色从椅子上站起来——不是运动学。是"先叹气，肩膀下沉，然后手撑扶手，停顿，站起来"——每一个子动作都是情绪的外化。

**对话中的身体。** 说话时手的位置（抱臂/放桌上/摸头发/握拳藏在口袋里）、目光的位置（看对方眼睛/看窗外/看自己手指）、身体的角度（正对/侧身/背对一半）——对话的信息有一半在台词之外。

## AI Prompt 约束

```yaml
style: kyoto-animation
line_art: subtle_thin_lines, less_emphasis_on_outline
shading: cel_with_soft_edge, warm_light_cool_shadow
color: high_key, low_mid_saturation, memory_color_priority
background: watercolor_wash_base, photorealistic_perspective_with_painterly_texture
camera: soft_focus_on_subject, backlight_bloom_1-3px, atmospheric_perspective
motion: micro_movements_in_stillness, emotion_driven_timing, cloth_hair_secondary_motion
character: realistic_proportions, large_expressive_eyes_with_focus_state, subtle_body_language
prohibited: high_saturation_pure_colors, exaggerated_proportions, static_true_stills, global_filter_grading
```

## 参考作品

- 紫罗兰永恒花园 (Violet Evergarden) — 光与水的极致
- 声之形 (A Silent Voice) — 身体语言的教科书
- 吹响吧！上低音号 (Hibike! Euphonium) — 日常中的戏剧光
- 冰菓 (Hyouka) — 灰色调的青春
- CLANNAD — 光与季节的叙事
