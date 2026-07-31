# DRF 核心冲刺计划（十日计划压缩版）

- 项目：`lxshopping/drf-practice`
- 业务主线：发布中心 `ReleaseOrder`
- 目标：先形成可迁移到真实项目的 DRF 请求闭环，再用项目需求反复强化。
- 节奏：每个 session 45～60 分钟；时间允许时每天最多完成 2 个 session。
- 证据：代码、真实接线、GitHub Check 与本地 API 行为；不要求上传 Postman 结果或手工总结。

## 为什么调整

旧方案把“每天建分支、等 Review、等合并、维护文档”放大成了主要成本，导致一个已经掌握的知识点也要占用一整天。新的方法把重复时间用于短回忆，把新时间用于完整业务闭环：每次只增加一个决策点，并马上接到真实 HTTP 接口。

## 五站核心路线

| Session | 状态 | 主要代码文件 | 业务闭环 | 必须掌握 | 预计用时 |
|---|---|---|---|---|---|
| Day01 | 已完成并合入 main | `releases/practice/day01_serializer.py` | 输入边界与校验 | fields、read_only、字段/对象校验、输入输出数据流 | 已完成 |
| Day02 | 当前 | `releases/practice/day02_create_order.py` | 创建发布单 | `is_valid/save`、`create`、`perform_create`、后端生成字段 | 45～60 分钟 |
| Day03 | Day02 验收后在同一 PR 接入 | `releases/practice/day03_query_update.py` | 查询、筛选与修改边界 | `get_queryset`、查询参数、`select_related`、PUT/PATCH、`partial` | 60 分钟 |
| Day04 | Day03 验收后在同一 PR 接入 | `releases/practice/day04_actions.py` | 触发发布与审批动作 | `@action`、权限、状态判断、幂等、service 边界、异常转换 | 60～75 分钟 |
| Day05 | Day04 验收后在同一 PR 接入 | `releases/practice/day05_callback.py` | Jenkins 回调与并发闭环 | `transaction.atomic`、`select_for_update`、重复回调、成功/失败状态 | 60～75 分钟 |

Day02～Day05 共用 `practice/day02-core-sprint` 和一个 Draft PR。每一站通过后直接在同一分支切换当前代码入口，不等待日级 PR 合并。Day05 全部通过后才把该 PR 标记为 Ready。

## 每次练习的最优结构

1. 5～8 分钟主动回忆：不看旧文件，口述上一站的请求调用链或写出核心类/方法签名。
2. 25～30 分钟实现：只改当天一个 `releases/practice/dayXX_*.py`。
3. 10 分钟本地 Postman：一个正常场景、一个边界场景、一个失败场景；无问题不上传。
4. 5～10 分钟源码定位：只追本次直接相关的 1～3 个方法，不通读源码。
5. 5 分钟一次 commit + push，然后在 Chat 说“DayXX 已提交”。

如果核心行为第一次就正确，不再追加格式性作业。若使用了大量提示，只把该小段加入下一站开头的 5 分钟闭卷复写，不让整条路线停一天。

## 验收与前进规则

满足以下四项即可进入下一站：

- 当天核心代码满足任务行为。
- 当前 View/URL 实际使用当天文件。
- GitHub Check 绿色。
- 没有未解决的 `[BLOCKER]`，且学习者没有反馈本地请求失败。

以下都不是推进门槛：Postman 截图、结果文件、手工总结、固定提交数量、等待下一个整点 Review。

## Day05 后立即进入真实项目

不再继续为“学完十天”而模拟。直接把真实发布项目拆成四个纵向切片：

1. 创建发布单：模型、Serializer、ViewSet、数据库落单。
2. 触发 Jenkins：service 封装、超时/异常、状态更新。
3. 回调闭环：鉴权、幂等、事务、日志与失败信息。
4. Vue 联调：创建、列表、详情、触发、状态刷新和错误展示。

每个切片沿用同一套小闭环：需求契约 → 最小实现 → 本地请求 → Review → 下一切片。遇到真实错误时再补相关 DRF 知识，比预先横向学完所有 API 更快、更牢。

## 结束标准

- 能从需求判断逻辑应放在 Serializer、ViewSet、`@action` 还是 service。
- 能独立完成 ReleaseOrder 的创建、查询/修改、业务动作和回调状态流转。
- 能用事务与行锁处理重复回调和并发更新。
- 能根据请求生命周期和 traceback 定位问题，而不是靠照抄完整答案。
