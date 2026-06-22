# x-writer 精进调研备忘（2026-07-17）

## 调研来源

### 直接访问并全文提取的内容（可用）
1. **SocialPilot** — "X (Twitter) Algorithm: Ranking Factors & Growth Tips (June 2026)"
   URL: https://www.socialpilot.co/blog/twitter-algorithm
   内容：算法 2026 全景，3 阶段排序，回复权重最高，TweepCred，作者多样性上限

2. **Sprout Social** — "How the Twitter Algorithm Works in 2026 [+6 Strategies]"
   URL: https://sproutsocial.com/insights/twitter-algorithm/
   内容：信号层级、bookmark + repost > likes-only、Premium 2x-4x boost、链接惩罚 50-90%、回复 prioritize

3. **Buffer** — "Best Time to Post on Twitter/X in 2026: 8.7 Million Posts Analyzed"
   URL: https://buffer.com/library/best-time-to-post-on-twitter/
   内容：最佳时间周二 9am，周三 10am，最佳日期周三>周二>周四

4. **X 官方推荐算法开源代码 README**（2026-05-15 更新版）
   URL: https://github.com/xai-org/x-algorithm
   内容：Grok transformer 架构、Phoenix retrieval + ranking、128 条互动窗口、14 种行为预测、无手工特征

### 尝试访问但被阻止的来源
- Social Media Today — 403 Forbidden
- Hootsuite — Network unreachable
- Later — 404

## 关键发现 vs 旧版假设

### 确认保留的
- Bookmark 仍是强信号（Sprout Social: "bookmarks + reposts drastically outperform likes-only"）
- Thread > 单条推文（多源确认，长注意力保持）
- 第一推完整判断原则不变
- 回复链（Reply Chain）策略有效
- 外部链接惩罚极严（可加严至 50-90%）
- 第一小时窗口关键

### 需要调整的
1. **回复信号已超过书签成为最高权重信号**。旧版强调 bookmark 为最强信号，实际回复权重远高于书签
2. **回复质量已是直接排名信号**（2026 年 3 月 downvote 功能）。旧版未提及
3. **作者多样性上限**（Author Diversity Cap）。多发不增收，这是新约束
4. **视频 <2:20 获得显著 boost**。X 的 AI 分析视频内容
5. **时间衰减更明确**：每 6 小时失去一半可见度分值
6. **Posted time data updated**：Buffer 2026 年 870 万帖子分析确认周二 9am

### 已过时/删除的假设
- 旧版引用 Buffer 2019 年的时间数据 → 更新为 2026 年 Buffer 数据
- 旧版引用 "bookmark 10x like" 作为最高信号 → 修正为 reply 最高，bookmark 第二梯队
- 旧版说 "图比文本好" → 2026 年纯文本互动率 3.6% vs 图片 3.4%，差距缩小

## 下次精进方向
- 监控 2026 Q3-Q4 算法变化（当前从 3 月起无变化）
- 收集 xAI 后续算法更新公告
- 搜索 "X Articles" 长文功能对 Thread 策略的替代影响
