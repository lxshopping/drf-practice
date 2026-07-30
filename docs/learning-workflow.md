# DRF GitHub 驱动学习工作流

## 目标

把每日准备、编码、本地 Postman 验证、自动检查、逐行 Review 和最终验收串成一个快速闭环。用户拉取分支后，首先打开当天的可运行代码文件，直接根据代码注释完成练习；任务文档只做索引和验收补充，不再作为主要操作入口。Postman 结果默认只保留在本地，不要求填写结果表、截图或上传响应。

## 固定分工

| 位置 | 负责内容 |
|---|---|
| Work + GitHub | 检查进度、创建当天可运行代码骨架、维护 Draft PR、逐行 Review、最终验收 |
| 当天代码文件 | 写明 TASK、CHECK、渐退式提示和源码入口，是用户当天唯一主要入口 |
| 本地仓库 | 修改当天代码、启动 Django、用 Postman 边改边验、提交和 push |
| GitHub Actions | 每次 push 做语法、Django system check、迁移检查，并确认练习文件已接入运行路径 |
| Chat | 用于系统解释，以及本地 Postman 发现问题时直接反馈请求、响应和报错 |

## 分支与 PR 规则

- `main`：只保存已经验收的结果。
- 每次只保留一个活动分支：`practice/dayXX-topic`。
- 当天分支创建后立即建立 Draft PR，后续 Review 全部留在该 PR。
- 前一天未验收，不创建下一天的分支、代码文件或任务。
- 验收通过后才把 PR 标为 Ready；不自动合并。

## 代码优先原则

每天必须先创建一个真正可运行、已接入 URL/ViewSet 的代码练习文件，再补文档：

~~~text
releases/practice/dayXX_topic.py      当天唯一主要入口，包含可运行占位代码和行内任务
releases/views.py / releases/urls.py  只做必要接线，不包含核心答案
docs/tasks/dayXX-*.md                 时间安排、入口索引和完整验收清单
docs/results/dayXX-postman.md         可选本地检查模板，不要求填写或提交
postman/drf-practice...json           可直接执行的请求
Draft PR                              逐行 Review 与最终验收入口
~~~

代码文件必须满足：

1. 拉取后可导入，`python manage.py check` 能运行。
2. 已接入当天真实 HTTP 接口，不能再次出现“文件存在但未被 import”的情况。
3. 文件顶部直接写启动方式、接口地址和本地验证方式。
4. 按顺序标注 `[TASK]`、`[CHECK]`、`[HINT-1/2/3]`、`[WHY]`、`[SOURCE]`。
5. 占位实现必须明确标记 `[BASELINE]`，可以启动，但在完成任务前应有业务场景不通过。
6. 只准备非核心接线和最小占位，不提前提交当天核心题目的完整答案。
7. 旧日答案可以保留在 Git 历史或旧文件中，但当天入口不得直接继承完整答案；任务文件应要求先闭卷完成。

## 十日代码文件约定

只在上一日合入 main 后创建下一项：

| Day | 当天主要代码文件 |
|---|---|
| 01 | `releases/practice/day01_serializer.py` |
| 02 | `releases/practice/day02_create_order.py` |
| 03 | `releases/practice/day03_query.py` |
| 04 | `releases/practice/day04_trigger.py` |
| 05 | `releases/practice/day05_update.py` |
| 06 | `releases/practice/day06_jenkins.py` |
| 07 | `releases/practice/day07_callback.py` |
| 08 | `releases/practice/day08_approval.py` |
| 09 | `releases/practice/day09_actions.py` |
| 10 | `releases/practice/day10_rebuild.py` |

## 渐退式提示

1. L0：代码中只给业务目标、输入输出和验收场景。
2. L1：指出应该使用的 DRF 层或方法。
3. L2：给判断结构或伪代码。
4. L3：同一问题经过两次修改仍不通过时，才在 PR Review 中给最小参考片段。

Review 优先使用 PR 行内评论，不直接改学习者的核心答案：

- `[BLOCKER]`：不修复不能验收。
- `[FIX]`：明确错误与最小修改方向。
- `[HINT-1/2/3]`：按级别给提示。
- `[WHY]`：要求解释原因。
- `[SOURCE]`：值得追踪的 DRF/Django 源码入口。

## 边改边验闭环

~~~text
打开当天一个代码文件
  -> 完成一个 TASK
  -> 只跑对应 CHECK/Postman 请求
  -> 通过后 commit + push
  -> GitHub Check 自动反馈
  -> Work 在 Draft PR 行内 Review
  -> 根据评论继续修改
~~~

GitHub Check 负责确认文件已接入且代码能安全启动；业务结果由学习者在本地用 Postman 验证。无问题无需上传任何记录；有问题时直接反馈请求方法、URL、请求体、实际状态码和错误响应。

## 每日验收

每一天的推进门槛简化为：

- 当天核心代码已在指定练习文件完成。
- 练习文件确实被当前 View/URL import 使用。
- 学习者已在本地执行约定的 Postman 场景；未反馈问题即按本地验证通过处理，无需上传结果。
- GitHub Check 绿色。
- 至少一个变化题已完成。
- Draft PR 中没有未解决的 `[BLOCKER]`。

总结与知识点由 Work 根据代码、Review 和反馈补充，不再要求学习者先修改文档才能进入下一天。口述调用链和源码追踪用于强化掌握，不作为拖住进度的硬门槛。

## 用户每天只需执行

~~~bash
git fetch origin
git switch <当天分支>
git pull --ff-only
python manage.py migrate
python manage.py runserver
~~~

然后只打开任务文档最上方指定的 `releases/practice/dayXX_*.py`。完成一个小点后：

~~~bash
git add releases/practice/dayXX_*.py
git commit -m "practice(dayXX): <本次小目标>"
git push
~~~

不需要把 Git commit、Postman 结果或整份代码重新粘贴到 Chat；GitHub 会直接读取并 Review。本地验证失败时，只需直接反馈最小可复现请求和错误响应。
