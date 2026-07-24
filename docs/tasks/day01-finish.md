# Day01 收尾：Serializer 核心 + Postman 验证

- 日期：2026-07-24
- 分支：`practice/day01-finish`
- 时间：09:00–11:00
- 今天只做 Day01，不进入 Day02
- 不要求补 Django 单元测试；验证方式为本地运行 + Postman + GitHub Check

## 今天唯一主要入口

拉取后只打开：

~~~text
releases/practice/day01_serializer.py
~~~

任务、TODO、对应 Postman 场景、渐退式提示和源码入口都已经写在这个代码文件中。它已经通过 `releases/views.py` 接入：

~~~text
http://127.0.0.1:8000/api/release-orders/
~~~

`releases/serializers.py` 保留此前练习成果，但当前接口不再使用它；闭卷完成前不要打开照抄。

## 开始方式

首次拉取：

~~~bash
git fetch origin
git switch -c practice/day01-finish --track origin/practice/day01-finish
python manage.py migrate
python manage.py runserver
~~~

以后继续：

~~~bash
git switch practice/day01-finish
git pull --ff-only
python manage.py runserver
~~~

## 两小时安排

| 时间 | 任务 | 完成标志 |
|---|---|---|
| 09:00–09:10 | 拉分支、启动服务、打开当天代码文件 | GET 接口不是 404 |
| 09:10–09:20 | 阅读代码顶部和 TASK 1~5，不看旧答案 | 知道每个任务对应哪个 Postman 场景 |
| 09:20–10:10 | 按 TASK 顺序完成；每完成一个只跑对应 CHECK | 业务规则逐项变绿 |
| 10:10–10:30 | 跑完 7 个固定场景和 branch_name 变化验证 | 状态码与关键字段符合预期 |
| 10:30–10:45 | 只追代码中标记的 SOURCE | 能说明输入校验链与输出链 |
| 10:45–11:00 | 填结果、更新总结、commit、push | GitHub Check 通过并等待 Review |

## 固定 Postman 场景

导入 `postman/drf-practice.postman_collection.json`，执行 Day01 文件夹：

| 场景 | 预期 |
|---|---|
| 01 合法生产发布单 | 201；`app_code=dms-mdm`、`status=CREATED` |
| 02 输入 status=SUCCESS | 201；保存后仍为 `CREATED` |
| 03 app_code 含内部空格 | 400；错误归属 `app_code` |
| 04 prod + feature/test | 400；对象级校验拒绝 |
| 05 prod + master | 201 |
| 06 test + feature/test | 201 |
| 07 GET 列表 | 200；`status_display` 为状态中文展示值 |

变化验证：临时把场景 04 的分支改成 `release /v1`，应由 `branch_name` 字段级校验拒绝。

每次 POST 使用不同 `release_no`，避免唯一约束掩盖真正结果。

## 提交节奏

完成一个小点即可 push，不必等全部结束：

~~~bash
git add releases/practice/day01_serializer.py docs/results/day01-postman.md
git commit -m "practice(day01): finish <本次小目标>"
git push
~~~

最后再提交总结：

~~~bash
git add docs/day01-serializer-core.md docs/results/day01-postman.md
git commit -m "docs(day01): finish serializer review"
git push
~~~

## Day01 验收标准

- [ ] 代码文件中的 TASK 1~5 全部完成。
- [ ] 7 个固定 Postman 场景均与预期一致。
- [ ] branch_name 内部空格变化验证通过。
- [ ] `python manage.py check` 通过。
- [ ] `python manage.py makemigrations --check --dry-run` 无遗漏迁移。
- [ ] GitHub Check 为绿色，并确认当前 Serializer 来自 `releases.practice.day01_serializer`。
- [ ] `docs/results/day01-postman.md` 填写真实结果。
- [ ] `docs/day01-serializer-core.md` 与当前代码一致。
- [ ] 能口述 `to_internal_value() -> Field.run_validation() -> validate_<field>() -> validate()`。
- [ ] Draft PR 中没有未解决的 `[BLOCKER]`。

未全部通过时继续当前分支，不创建 Day02。
