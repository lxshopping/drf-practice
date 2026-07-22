# Day01：Serializer 核心总结

- 日期：2026-07-22
- 练习分支：`day01-serializer-core`
- 练习对象：`ReleaseOrderSerializer`
- 本日目标：掌握显式字段、计算字段、字段级校验、对象级校验、只读字段及 Serializer 单元测试。

## 一、当前完成情况

本次是在不照着参考源码的情况下完成第一遍，已经能够独立回忆 `ModelSerializer`、`Meta`、`fields`、`read_only_fields`、`validate_<field>()` 和 `validate()` 的基本结构。

当前已经完成：

- 练习代码从错误的 `releases/serializers-core.py` 移回 `releases/serializers.py`。
- 使用显式 `fields`，不再长期依赖 `fields = "__all__"`。
- `status_display` 已声明在 Serializer 类中。
- `status`、开始时间、结束时间、错误信息和时间戳已配置为只读字段。
- 已开始编写“前端提交 status 也不能覆盖模型默认状态”的测试。

当前仍未完成：

- `validate()` 最后缺少 `return attrs`。
- `validate_branch_name()` 只允许 `release`，但对象级校验又试图允许 `master`，两层规则冲突。
- `validate_status()` 对只读字段不会生效，应删除。
- `tests.py` 中测试函数不在 `TestCase` 子类中，`self` 和 `build_valid_data()` 也没有来源，当前测试不会被 Django 正确执行。
- `app_code` 的 `strip + lower` 变化题尚未完成。
- 模型中的 `TRIGGRTING` 仍应修正为 `TRIGGERING`，并生成新迁移。

因此 Day01 当前属于“已理解主要结构，但还未通过可运行测试”，暂不进入 Day02。

## 二、Serializer 的核心执行链

### 1. 输入与校验

```text
普通 dict / request.data
        ↓
Serializer(data=data)
        ↓ 保存为 initial_data
is_valid()
        ↓
run_validation()
        ↓
to_internal_value()
        ↓ 只遍历可写字段
字段自身校验
        ↓
validate_<字段名>(value)
        ↓
validate(attrs)
        ↓
validated_data
        ↓
save()
        ↓
create(validated_data) 或 update(instance, validated_data)
```

### 2. 输出序列化

```text
模型实例
   ↓
Serializer(instance)
   ↓
serializer.data
   ↓
to_representation(instance)
   ↓ 遍历可读字段
返回普通 dict
```

必须区分三个数据：

| 数据 | 含义 | 出现时间 |
|---|---|---|
| `initial_data` | 前端最初传入的原始数据 | `Serializer(data=...)` 后 |
| `validated_data` | 过滤只读字段并通过全部校验后的可信数据 | `is_valid()` 成功后 |
| `serializer.data` | 用于响应输出的序列化结果 | 序列化实例或保存成功后 |

## 三、为什么 `serializers-core.py` 没有生效

Django 不会自动扫描应用目录下所有名字带 `serializer` 的文件。Python 只会加载代码中明确导入的模块。

项目正常导入的是：

```python
from releases.serializers import ReleaseOrderSerializer
```

这个导入路径只能定位到：

```text
releases/serializers.py
```

原来的 `releases/serializers-core.py` 有两个问题：

1. 没有任何运行代码导入它，所以文件存在也不会执行。
2. 文件名包含 `-`，不能通过普通的 Python 点号模块路径导入。

因此当时实际运行的仍是旧 `releases/serializers.py`，练习文件只是一个没有接入调用链的孤立文件。

结论：判断代码是否生效，不能只看文件是否存在，要顺着实际的 `import` 路径定位。

## 四、为什么字段不能声明在 `Meta` 中

Serializer 类创建时，DRF 的元类会扫描 Serializer 类本身的属性，把其中的 `Field` 对象收集到 `_declared_fields`。

正确声明：

```python
class ReleaseOrderSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

    class Meta:
        model = ReleaseOrder
        fields = ["status", "status_display"]
```

如果把 `status_display` 写进 `Meta`：

```python
class Meta:
    status_display = serializers.CharField(...)
```

它只会成为 `Meta.status_display`，不会成为 `ReleaseOrderSerializer` 的字段，也不会进入 `_declared_fields`。

`Meta` 的职责是提供配置，例如：

- 绑定哪个 `model`；
- 使用哪些 `fields`；
- 哪些字段是 `read_only_fields`；
- `extra_kwargs` 等字段配置。

`Meta.fields` 只是“最终允许 Serializer 使用哪些字段名称”的清单，不等于声明一个新的字段。模型中没有 `status_display`，Serializer 类中又没有正确声明时，DRF 无法构造该字段。

## 五、为什么原来的 `or` 条件永远报错

原来的判断类似：

```python
if not branch.startswith("release") or not branch.startswith("master"):
    raise serializers.ValidationError(...)
```

设：

- A：分支以 `release` 开头；
- B：分支以 `master` 开头。

原条件是 `not A or not B`。根据德摩根定律：

```text
not A or not B == not (A and B)
```

也就是说，只有一个分支同时以 `release` 和 `master` 开头时才能通过，但这是不可能的。

| 分支 | A | B | `not A or not B` | 结果 |
|---|---:|---:|---:|---|
| `release/v1` | 真 | 假 | 真 | 报错 |
| `master` | 假 | 真 | 真 | 报错 |
| `feature/x` | 假 | 假 | 真 | 报错 |

真正想表达的是“既不是 release，也不是 master 才报错”，逻辑应是：

```text
not A and not B == not (A or B)
```

更重要的是职责划分：

- `validate_branch_name()`：只检查单个分支值是否合法，例如允许 `master` 或 `release/...`。
- `validate()`：检查多个字段之间的关系，例如 `prod` 环境必须使用指定发布分支。

当前代码的字段级校验拒绝 `master`，对象级校验却允许 `master`，仍需要统一规则。

## 六、为什么只读 `status` 不在 `validated_data` 中

`read_only=True` 的含义不是“前端传了就报错”，而是：

- 反序列化输入时不接收这个字段；
- 序列化输出时仍然可以返回这个字段。

DRF 在 `to_internal_value()` 中只遍历 `_writable_fields`。`status` 被设置为只读后，不属于可写字段，因此：

1. 前端提交的 `status="SUCCESS"` 仍存在于 `initial_data`；
2. DRF 不会把它放入 `validated_data`；
3. `validate_status()` 也不会被调用；
4. `save()` 得不到前端提交的 status；
5. 创建 `ReleaseOrder` 时使用模型默认值 `CREATED`。

因此下面的业务判断不应读取 `attrs["status"]`：

```python
def validate(self, attrs):
    status = attrs["status"]
```

它可能产生 `KeyError`。如果以后在更新接口中需要判断数据库对象当前状态，应考虑从 `self.instance.status` 获取，而不是从只读输入字段获取。

## 七、为什么 Serializer 测试不需要 View 和 URL

Serializer 自己就是一个可以独立调用的 Python 组件，它负责：

- 输入数据转换；
- 字段校验；
- 对象级校验；
- 创建或更新模型；
- 将模型转换成响应数据。

因此可以直接测试：

```text
准备 data
   ↓
ReleaseOrderSerializer(data=data)
   ↓
is_valid()
   ↓
检查 errors / validated_data
   ↓
save()
   ↓
检查数据库对象
```

只有在测试以下内容时才需要 View 和 URL：

- HTTP 路由是否正确；
- GET、POST、PATCH 等请求方法；
- HTTP 状态码；
- 登录认证与权限；
- 最终 Response 结构。

今天的目标是 Serializer 核心，因此直接写 Serializer 单元测试更快，也更容易判断错误究竟来自 Serializer 还是 View。

当前 `tests.py` 还需要调整为：

- 创建一个继承 `django.test.TestCase` 的测试类；
- 把 `build_valid_data()` 定义为测试类方法；
- 把 `test_status_is_read_only()` 放进测试类；
- 使用 `python manage.py test releases -v 2` 验证测试确实被发现和执行。

## 八、源码最终怎样定位

### 1. 定位项目实际使用的业务代码

不要根据文件名猜，直接查询 Python 最终加载的模块：

```bash
python manage.py shell -c "import inspect; from releases.serializers import ReleaseOrderSerializer; print(ReleaseOrderSerializer.__module__); print(inspect.getsourcefile(ReleaseOrderSerializer))"
```

也可以查看整个模块文件：

```bash
python manage.py shell -c "import releases.serializers as m; print(m.__file__)"
```

这能直接证明当前运行时加载的是哪个 `serializers.py`。

### 2. 定位 DRF 框架源码

先查看 DRF 安装位置：

```bash
python -m pip show djangorestframework
```

再用 `inspect` 定位类或方法：

```bash
python manage.py shell -c "import inspect; from rest_framework.serializers import Serializer; print(inspect.getsourcefile(Serializer)); print(inspect.getsource(Serializer.run_validation))"
```

查看 `is_valid()`：

```bash
python manage.py shell -c "import inspect; from rest_framework.serializers import BaseSerializer; print(inspect.getsource(BaseSerializer.is_valid))"
```

查看字段收集机制时，可以继续定位：

- `SerializerMetaclass`；
- `Serializer.get_fields()`；
- `ModelSerializer.build_field()`；
- `Serializer.to_internal_value()`；
- `Serializer.run_validation()`；
- `BaseSerializer.save()`。

在 VS Code 中也可以对 `ModelSerializer`、`is_valid`、`run_validation` 按住 Ctrl 点击跳转。遇到异常时优先顺着 traceback 从自己的代码向 DRF 源码追踪，比在整个依赖目录中盲目搜索更快。

### 3. 本日最重要的源码调用链

```text
BaseSerializer.is_valid()
        ↓
Serializer.run_validation(initial_data)
        ↓
Serializer.to_internal_value(data)
        ↓
Field.run_validation()
        ↓
validate_<field>(value)
        ↓
Serializer.validate(attrs)
        ↓
validated_data
```

理解这条链，就能解释字段为什么被忽略、校验器为什么没有执行、错误在哪一层产生。

## 九、测试验收清单

| 测试场景 | 预期结果 |
|---|---|
| 模型状态为 `RUNNING` 后序列化输出 | `status_display` 为“运行中” |
| 输入包含 `status="SUCCESS"` | `validated_data` 中没有 status，保存后仍为 `CREATED` |
| 合法普通分支 | 字段级校验通过 |
| 非法分支 `feature/test` | 字段级校验失败 |
| `prod` 与不允许的分支组合 | 对象级校验失败 |
| `app_code=" DMS-MDM "` | 变化题完成后得到 `dms-mdm` |
| 所有合法数据 | `validate()` 返回 attrs，保存成功 |

执行命令：

```bash
python manage.py check
python manage.py test releases -v 2
```

不能只看到命令退出码为 0，还要确认输出中确实发现并执行了预期的测试数量。

## 十、本次错误与原因

| 错误 | 根本原因 |
|---|---|
| 练习文件没有生效 | 文件不在实际 import 路径，且文件名含 `-` |
| `status_display` 放在 Meta | 混淆了“字段声明”和“Serializer 配置” |
| `or` 判断全部失败 | 把“两个都不满足”写成“任意一个不满足” |
| 从 attrs 读取只读 status | 没区分 `initial_data` 与 `validated_data` |
| 认为测试必须经过 URL | 混淆 Serializer 单元测试与 API 集成测试 |
| `validate()` 没有返回 attrs | 忘记对象级校验既要检查，也必须返回校验后的数据 |
| 测试函数写在类外 | 混淆普通函数与 Django `unittest` 测试发现规则 |

## 十一、变化题结论

变化题要求把前端传入的 `app_code` 先去除首尾空格，再统一转换成小写，例如：

```text
" DMS-MDM " → "dms-mdm"
```

它属于单字段转换，应使用字段级校验入口完成。当前尚未实现，也没有测试，不能标记为完成。

## 十二、掌握情况与下一次复写

- 独立完成程度：能够不看源码写出主要框架。
- 当前掌握程度：基本结构已建立，但字段收集、反序列化数据流、布尔条件和测试发现机制仍不稳定。
- 本日状态：待修正、待测试、待最终提交。

下一次闭卷复写只保留三个目标：

1. 正确声明 `status_display`，并解释为什么必须位于 `Meta` 外。
2. 写出字段级校验与对象级校验，确保规则不冲突且 `validate()` 返回 attrs。
3. 不经过 View 和 URL，独立完成只读 status 的 Serializer 测试。

完成 Day01 的标准：代码可导入、全部测试真实执行并通过、变化题完成、总结文档随代码一起推送到 GitHub。
