# Day01 收尾：Serializer 核心 + Postman 验证

- 日期：2026-07-24
- 分支：`practice/day01-finish`
- 时间：09:00–11:00
- 练习对象：`ReleaseOrderSerializer`
- 今天只做 Day01，不进入 Day02
- 不写、不补 Django 单元测试；验证方式统一为本地运行 + Postman + GitHub Check

## 一、开始方式

第一次拉取：

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

接口入口：

~~~text
http://127.0.0.1:8000/api/release-orders/
~~~

`views.py`、`urls.py` 和 Router 已经接好，它们只是 Day01 的 HTTP 测试骨架。今天不需要把时间花在路由上。

## 二、两小时安排

| 时间 | 任务 | 完成标志 |
|---|---|---|
| 09:00–09:10 | 拉分支、迁移、启动服务 | GET 接口不是 404，终端无异常 |
| 09:10–09:25 | 用 Postman 跑一遍当前基线 | 知道当前哪些规则已经生效 |
| 09:25–09:55 | 闭卷复写 Serializer 核心部分 | 能独立写出字段、只读配置和两层校验 |
| 09:55–10:30 | 逐个跑 6 个 Postman 场景 | 每改一处，立即只重跑对应场景 |
| 10:30–10:45 | 按需追踪两处 DRF 源码 | 能说清输入校验链和输出链 |
| 10:45–11:00 | 更新结果、总结、提交并 push | GitHub Check 通过，等待 PR Review |

## 三、主动复写范围

直接在 `releases/serializers.py` 中复写下面几部分，Git 历史就是备份，不额外复制答案文件：

1. `status_display` 的声明。
2. `Meta.fields` 与 `read_only_fields`。
3. `validate_app_code()`。
4. `validate_branch_name()`。
5. `validate()`。

复写时先关闭旧总结，不照抄。完成一个方法就启动/重载服务，并只跑与它对应的 Postman 请求，不要等所有代码改完再验证。

## 四、业务规则

今天以这些规则为准，避免旧总结里的规则冲突：

- `app_code`：先去掉首尾空格，再转小写；中间仍有空格则拒绝。
- `branch_name`：去掉首尾空格；中间有空格则拒绝。
- 只有 `env_name=prod` 时限制分支：允许 `master` 或 `release/...`。
- 非生产环境允许 `feature/...`。
- `status`、时间字段和错误信息均为只读；前端即使传入也不能进入 `validated_data`。
- 创建后的默认状态仍由模型决定，为 `CREATED`。

## 五、Postman 验证场景

导入仓库中的 `postman/drf-practice.postman_collection.json` 后，从 Day01 文件夹逐个执行。

| 场景 | 关键输入 | 预期 |
|---|---|---|
| 1. 合法生产发布单 | `app_code=" DMS-MDM "`、`prod`、`release/v1` | 201；返回 `app_code=dms-mdm` |
| 2. 只读状态不可覆盖 | 输入 `status=SUCCESS` | 201；返回状态仍为 `CREATED` |
| 3. 应用编码含内部空格 | `app_code="dms mdm"` | 400；错误位于 `app_code` |
| 4. 生产环境非法分支 | `prod + feature/test` | 400；对象级校验错误 |
| 5. 生产环境 master | `prod + master` | 201 |
| 6. 测试环境 feature | `test + feature/test` | 201 |
| 7. 输出展示字段 | GET 列表 | 每项包含 `status_display` |

每次 POST 都使用不同的 `release_no`，否则会被唯一约束拦截，掩盖真正的 Serializer 结果。

## 六、渐退式提示

只有卡住时才向下看；每一级最多使用一次。

### 提示 1：定位职责

- 只依赖一个输入值的规则，放在 `validate_<field>()`。
- 同时依赖环境和分支的规则，放在 `validate()`。
- 只读字段不会进入 `attrs`。

### 提示 2：判断结构

生产分支规则应表达为：

~~~text
如果是 prod，并且既不是 master，也不是 release/ 开头，则报错
~~~

### 提示 3：排错路径

先看 Postman 响应体中的错误字段，再看 Django 终端 traceback；只在仍无法解释时追踪：

~~~text
is_valid()
  -> Serializer.run_validation()
  -> Serializer.to_internal_value()
  -> Field.run_validation()
  -> validate_<field>()
  -> validate()
~~~

## 七、源码追踪（只追两处）

~~~bash
python manage.py shell -c "import inspect; from rest_framework.serializers import Serializer; print(inspect.getsource(Serializer.run_validation)); print(inspect.getsource(Serializer.to_internal_value))"
python manage.py shell -c "import inspect; from rest_framework.serializers import Serializer; print(inspect.getsource(Serializer.to_representation))"
~~~

不要通读整个 DRF 源码。只回答两个问题：

1. 为什么只读 `status` 不会进入 `validated_data`？
2. 为什么 `status_display` 会出现在响应数据里？

## 八、边改边验的提交节奏

建议只做两个学习提交，避免提交动作反过来拖慢练习：

~~~bash
git add releases/serializers.py docs/results/day01-postman.md
git commit -m "practice(day01): rewrite serializer validation"
git push

git add docs/day01-serializer-core.md docs/results/day01-postman.md
git commit -m "docs(day01): finish serializer review"
git push
~~~

每次 push 后 GitHub 会自动运行 Django Check。代码问题会在 Draft PR 中按行评论，不需要再把整段代码复制到 Chat。

## 九、Day01 验收标准

必须全部满足才进入 Day02：

- [ ] 7 个 Postman 场景均与预期一致。
- [ ] `python manage.py check` 通过。
- [ ] `python manage.py makemigrations --check --dry-run` 显示无遗漏迁移。
- [ ] GitHub Check 为绿色。
- [ ] `docs/results/day01-postman.md` 已填写真实结果。
- [ ] `docs/day01-serializer-core.md` 已删除“尚未完成”的过期结论，并与代码一致。
- [ ] 能口述 `to_internal_value() -> Field.run_validation() -> validate_<field>() -> validate()`。
- [ ] 代码、验证记录和总结都已 push 到当前分支。

未全部通过时，下一个工作日继续这个分支，不创建 Day02。
