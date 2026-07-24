# DRF 十个工作日业务主线

- 项目：`lxshopping/drf-practice`
- 业务对象：发布中心 `ReleaseOrder`
- 方法：业务驱动 + 渐退式提示 + 主动复写 + Postman 反馈 + 按需追踪源码
- 每天：09:00–11:00
- 规则：日期是最早开始日；任何一天未验收，后续整体顺延
- 入口规则：每天先创建并接入一个带注释、可运行的代码练习文件；用户以该文件为主，不需要对着 Chat 或长任务文档操作

| Day | 最早日期 | 业务主题 | 当天主要代码文件 | 核心能力 | 变化题 | 源码入口 |
|---|---|---|---|---|---|---|
| 01 | 07-24 周五 | Serializer 收尾与 HTTP 验证 | `releases/practice/day01_serializer.py` | fields、read_only、source、字段/对象校验、输入输出数据流 | prod 与非 prod 使用不同分支规则 | `run_validation`、`to_internal_value`、`to_representation` |
| 02 | 07-27 周一 | 创建发布单完整闭环 | `releases/practice/day02_create_order.py` | `serializer.is_valid/save`、`create`、`perform_create`、后端生成字段 | 前端只传最小字段，后端补发布单号和默认状态 | `BaseSerializer.save`、`ModelSerializer.create` |
| 03 | 07-28 周二 | 列表、详情与筛选 | `releases/practice/day03_query.py` | `ModelViewSet`、`get_queryset`、查询参数、分页、`select_related` | app/env/status/keyword 组合筛选 | `ListModelMixin.list`、`GenericAPIView.get_queryset` |
| 04 | 07-29 周三 | 触发发布业务动作 | `releases/practice/day04_trigger.py` | `@action(detail=True)`、状态判断、幂等保护、HTTP 状态码 | CREATED 可触发，RUNNING 重复触发要拒绝 | `ViewSetMixin`、Router 动态路由 |
| 05 | 07-30 周四 | PUT/PATCH 与修改边界 | `releases/practice/day05_update.py` | `update`、`partial_update`、`partial=True`、只读与可修改字段 | 运行中的发布单禁止修改分支 | `UpdateModelMixin.update/partial_update` |
| 06 | 07-31 周五 | 服务层与 Jenkins 触发 | `releases/practice/day06_jenkins.py` | `services.py` 拆分、外部调用、异常转换、视图保持薄 | Jenkins 失败时状态与错误信息可解释 | DRF `APIException` 与自定义异常处理 |
| 07 | 08-03 周一 | 回调、事务与并发 | `releases/practice/day07_callback.py` | 手动模拟 callback、`transaction.atomic`、`select_for_update`、幂等 | 同一回调重复到达不重复改变结果 | Django 事务与 QuerySet 锁定路径 |
| 08 | 08-04 周二 | 提交与审批状态机 | `releases/practice/day08_approval.py` | submit/approve/reject、权限检查、合法状态流转 | 非待审批状态不能 approve | `APIView.initial`、`check_permissions`、`@action` |
| 09 | 08-05 周三 | cancel/retry/logs/batch-trigger | `releases/practice/day09_actions.py` | detail/collection action、不同 Serializer、日志只读接口 | 只允许 FAILED 重试；批量操作逐项返回结果 | `get_serializer_class`、`ReadOnlyModelViewSet` |
| 10 | 08-06 周四 | 闭卷复写最小发布中心 | `releases/practice/day10_rebuild.py` | 从 model 到 router 重建 create/list/filter/trigger/callback，完整 Postman 回归 | 更换一个业务字段或状态规则后重新跑通 | 从 `APIView.dispatch` 串起完整请求链 |

## 每日代码文件统一格式

每个 `dayXX_*.py` 文件必须包含：

1. 顶部写启动命令、接口地址和结果记录文件。
2. 按顺序写 `[TASK]`，用户从上往下完成。
3. 每个 TASK 紧邻对应 `[CHECK]` 或 Postman 场景。
4. 提示按 `[HINT-1/2/3]` 渐退，不提前给完整实现。
5. 只列当天直接相关的 `[SOURCE]`。
6. 占位实现标为 `[BASELINE]`，保证能启动但不会让全部业务场景直接通过。
7. 文件必须被当天 View/URL 实际 import，GitHub Check 验证接线。

## 每日固定结构

1. 10 分钟：拉分支、启动服务、打开当天代码文件。
2. 40 分钟：按文件内 TASK 逐项独立实现。
3. 30 分钟：按 CHECK 逐场景 Postman 验证，边改边验。
4. 20 分钟：完成变化题并追踪一个直接相关源码点。
5. 20 分钟：填写结果、总结、commit、push，等待 PR Review。

## 十天结束标准

- 能从需求自然判断应写在 Serializer、ViewSet、`@action` 还是 service。
- 能独立完成 ReleaseOrder 创建、查询、筛选、修改、业务动作、回调和状态流转。
- 能正确使用事务与 `select_for_update()` 处理重复回调/并发状态更新。
- 能通过 traceback 和调用链定位问题，而不是盲目搜索依赖源码。
- 仓库中保留十天代码、Postman 记录、总结和可回看的 PR Review。
