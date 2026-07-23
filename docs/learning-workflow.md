# DRF GitHub 驱动学习工作流

## 目标

把每日准备、代码提交、自动检查、逐行 Review 和最终验收都放进 GitHub。日常编码仍在本地 VS Code/Codex 中完成，不再来回复制代码到 Chat。

## 固定分工

| 位置 | 负责内容 |
|---|---|
| Work + GitHub | 检查进度、准备当天分支与任务文件、维护 Draft PR、逐行 Review、最终验收 |
| 本地仓库 | 阅读任务、闭卷复写、启动 Django、用 Postman 验证、提交和 push |
| GitHub Actions | 每次 push 自动做语法、Django system check、迁移检查和迁移执行 |
| Chat | 仅在需要系统解释概念时使用，不作为每天练习的操作入口 |

## 分支与 PR 规则

- `main`：只保存已经验收的结果。
- 每次只保留一个正在练习的分支：`practice/dayXX-topic`。
- 当天分支创建后立即建立 Draft PR，后续 Review 全部留在该 PR。
- 前一天未验收，不创建下一天；延续原分支和原任务。
- 验收通过后才把 PR 标为 Ready，并合入 `main`。

## 每日任务包

Work 在当天开始前准备：

~~~text
docs/tasks/dayXX-*.md                当天两小时任务、业务规则和分级提示
docs/results/dayXX-postman.md        Postman 实测记录模板
postman/drf-practice...json          可直接执行的请求
releases/...                         只准备非学习重点的基础骨架
Draft PR                             逐行评论与验收入口
~~~

不会提前提交当天核心题目的完整答案。

## 渐退式提示

1. L0：只给业务目标、输入输出和验收场景。
2. L1：指出应该使用的 DRF 层或方法。
3. L2：给判断结构或伪代码。
4. L3：同一问题经过两次修改仍不通过时，才给最小参考片段。

Review 优先使用 PR 行内评论，不把答案直接改进你的代码。评论统一使用：

- `[BLOCKER]`：不修复不能验收。
- `[FIX]`：明确错误与修改方向。
- `[HINT-1/2/3]`：按级别给提示。
- `[WHY]`：要求解释为什么。
- `[SOURCE]`：值得追踪的 DRF/Django 源码入口。

## 边改边验闭环

~~~text
实现一个小点
  -> 只跑对应 Postman 请求
  -> 通过后 commit + push
  -> GitHub Check 自动反馈
  -> Work 在 Draft PR 行内 Review
  -> 根据评论修改并再次 push
~~~

GitHub Check 只负责“代码能否安全启动”；业务结果仍以 Postman 记录为准。

## 每日验收

每一天必须同时具备：

- 当天核心代码。
- Postman 真实结果，不要求 Django 单元测试。
- GitHub Check 绿色。
- 总结文档与实际代码一致。
- 至少一个变化题。
- 只追踪与当日问题直接相关的源码。
- 能口述当天关键调用链。
- Draft PR 中没有未解决的 `[BLOCKER]`。

## 用户每天只需执行

~~~bash
git fetch origin
git switch <当天分支>
git pull --ff-only
python manage.py migrate
python manage.py runserver
~~~

完成一个小点后：

~~~bash
git add <本次文件>
git commit -m "practice(dayXX): <本次小目标>"
git push
~~~

不需要把 Git commit、测试输出和整份代码重新粘贴到 Chat；GitHub 中已经能直接读取和 Review。
