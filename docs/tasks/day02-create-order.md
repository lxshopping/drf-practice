# Day02｜创建发布单闭环

主要入口：[`releases/practice/day02_create_order.py`](../../releases/practice/day02_create_order.py)

今天不再做“两小时 + 文档收尾”，只完成一个 45～60 分钟闭环：

1. 5 分钟：不看旧代码，口述 `request.data -> is_valid -> save -> create`。
2. 25 分钟：从上到下完成代码中的 TASK 1～3。
3. 10 分钟：本地运行 Postman 的 Day02 三个请求；结果不上传。
4. 10 分钟：只追 `BaseSerializer.save()`、`ModelSerializer.create()`、`CreateModelMixin.perform_create()` 三个入口。
5. 5 分钟：一次 commit + push，然后直接在 Chat 说“Day02 已提交”。

## 验收行为

- 最小业务输入可创建发布单并返回 201。
- 连续创建两次得到不同的后端发布单号。
- 客户端不能覆盖 `release_no` 与 `status`。
- Day01 的字段与组合校验仍有效。
- 当前 View/URL 确实使用 Day02 文件。
- GitHub Check 绿色且没有未解决的 `[BLOCKER]`。

Postman 本地失败时，只需反馈：请求名、方法、URL、请求体、实际状态码和错误响应；无需截图或结果文档。

## 冲刺规则

Day02 通过后，不等待本 PR 合并。Work 会在同一个 `practice/day02-core-sprint` 分支继续接入 Day03；Day02～Day05 全部完成后才把滚动 PR 标记为 Ready。
