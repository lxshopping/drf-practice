# DRF GitHub 核心冲刺工作流

## 目标

把学习主线压缩为“一个代码入口 → 本地 API 验证 → push → 即时 Review → 下一核心点”。代码是练习主体；文档、Postman 记录和固定日历都不能拖住推进。

## 当前分支策略

- `main`：保存已完成的大阶段结果。
- Day01 已验收并合入 `main`。
- `practice/day02-core-sprint`：Day02～Day05 共用的唯一活动分支与 Draft PR。
- 同一时刻只接入一个 `releases/practice/dayXX_*.py`，上一站验收后在同一分支切换下一站。
- 不再要求每个 Day 单独建 PR、等待合并后才能继续。
- Day05 完成后，才把滚动 PR 标为 Ready；仍由用户决定何时合并。

## 固定分工

| 位置 | 负责内容 |
|---|---|
| Work + GitHub | 准备可运行骨架、切换当前接线、维护一个滚动 Draft PR、Review 与阶段验收 |
| 当天代码文件 | 唯一主要入口，包含 TASK、CHECK、渐退式提示、WHY、SOURCE 与 BASELINE |
| 本地仓库 | 写核心代码、启动 Django、运行 Postman、一次提交并 push |
| GitHub Actions | 每次 push 检查语法、Django 配置、迁移和当前入口接线 |
| Chat | push 后立即请求 Review；本地请求失败时反馈最小请求与错误响应 |

## 代码入口要求

当前文件必须：

1. 可导入，`python manage.py check` 能运行。
2. 被真实 View/URL 使用，不能只是孤立练习文件。
3. 从上到下包含 `[TASK]`、`[CHECK]`、`[HINT-1/2/3]`、`[WHY]`、`[SOURCE]`、`[BASELINE]`。
4. 基线能启动，但至少一个关键业务场景故意不通过。
5. 只准备非核心接线，不替学习者提交核心答案。

## 45～60 分钟闭环

~~~text
5～8 分钟：闭卷回忆上一站的调用链或核心签名
25～30 分钟：只修改当前一个代码文件
10 分钟：本地 Postman 跑正常、边界、失败场景
5～10 分钟：只追当前直接相关的源码入口
5 分钟：一次 commit + push，立即在 Chat 请求 Review
~~~

时间允许可在同一天完成两个 session，但每天最多两站，避免只追速度而没有回忆间隔。

不再要求每个 TASK 单独 commit。一次 session 一个清晰提交即可。

## Postman 与总结

- Postman 只在本地运行；无问题时不填写、不截图、不上传结果。
- 发生问题时，直接反馈请求名、方法、URL、请求体、实际状态码与错误响应。
- 总结由 Work 根据代码和 Review 精简维护，不要求学习者先改文档。
- 口述调用链用于强化记忆，但不是拖住下一站的形式门槛。

## Review 与验收

用户 push 后直接在 Chat 说“DayXX 已提交”，立即触发 Review；定时检查只作为漏检兜底，不必等待下一个整点。

Review 仍使用：

- `[BLOCKER]`：真实行为错误，不修复不能前进。
- `[FIX]`：明确错误与最小修改方向。
- `[HINT-1/2/3]`：按需逐级揭示。
- `[WHY]`：解释责任边界或运行原因。
- `[SOURCE]`：只指向直接相关源码。

一站满足以下条件就立即接下一站：

- 核心代码符合接口行为；
- 当前 View/URL 已使用该文件；
- GitHub Check 绿色；
- 无未解决 `[BLOCKER]`；
- 学习者未反馈本地 Postman 错误。

Postman 上传记录、手工总结、固定提交数、等待当前 PR 合并都不是推进门槛。

## 用户操作

首次切到核心冲刺分支：

~~~bash
git fetch origin
git switch --track origin/practice/day02-core-sprint
python manage.py migrate
python manage.py runserver
~~~

已经有本地分支时：

~~~bash
git switch practice/day02-core-sprint
git pull --ff-only
python manage.py runserver
~~~

完成当前 session 后：

~~~bash
git add releases/practice/dayXX_*.py
git commit -m "practice(dayXX): complete core task"
git push
~~~

然后直接在 Chat 说“DayXX 已提交”。不要粘贴整份代码；若 Postman 失败，只贴最小错误信息。

## 核心冲刺之后

Day05 通过并合入后，不再为补齐模拟天数停留。直接转入真实发布项目的创建发布单、Jenkins 触发、回调事务和 Vue 联调四个纵向切片；遇到知识缺口再做 15～30 分钟针对性练习。
