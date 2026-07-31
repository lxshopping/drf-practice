# Day01：Serializer 核心总结

- 当前分支：`practice/day01-finish`
- 实际入口：`releases/practice/day01_serializer.py`
- 接口：`/api/release-orders/`
- 状态：已完成核心代码，按“本地 Postman、不上传结果”的新规则通过 Day01

## 一、本次完成

- `status_display` 通过 `source="get_status_display"` 输出 choices 中文值，并保持只读。
- Serializer 使用显式 `fields`，后端维护的状态、执行时间、错误信息和时间戳设为只读。
- `validate_app_code()` 完成首尾去空格、转小写，并拒绝内部空格。
- `validate_branch_name()` 只处理分支字段自身的规范化和内部空格。
- `validate()` 负责跨字段规则：prod 只允许 `master` 或 `release/...`，非 prod 可以使用 `feature/...`。
- `validate()` 正确返回 `attrs`。
- 当前 ViewSet 已实际导入 Day01 Serializer；GitHub Actions `DRF Practice Check` run #19 通过。

Postman 由学习者在本地执行，结果无需写入仓库。未反馈问题即按本地验证通过处理；若后续发现问题，直接反馈最小可复现请求和错误响应即可。

## 二、关键调用链

输入校验：

```text
request.data
  -> Serializer(data=...)
  -> is_valid()
  -> Serializer.run_validation()
  -> to_internal_value()
  -> Field.run_validation()
  -> validate_<field>()
  -> validate(attrs)
  -> validated_data
  -> save()
```

输出序列化：

```text
model instance
  -> Serializer(instance)
  -> serializer.data
  -> to_representation(instance)
  -> response data
```

## 三、为什么这样分层

### 字段级校验

`validate_app_code()` 和 `validate_branch_name()` 只依赖单个字段，适合做规范化与该字段自身规则。这样错误能归属到具体字段，也便于复用。

### 对象级校验

prod 与 branch 的关系同时依赖 `env_name` 和 `branch_name`，必须放在 `validate(attrs)`。如果把它写入 `validate_branch_name()`，该方法拿不到已完成校验的完整字段集合。

### 只读 status

`status` 不属于 `_writable_fields`。即使前端提交 `status="SUCCESS"`，它也不会进入 `validated_data`，保存时仍使用模型默认值 `CREATED`；但序列化输出仍会包含 status。

## 四、非阻塞改进

- `fields` 可改成每行一个字段，便于 Review；不影响当前功能。
- prod 分支错误提示应精确写成“必须为 master 或以 release/ 开头”；不影响判断逻辑。
- 当前 `attrs["env_name"]` 与 `attrs["branch_name"]` 适用于 Day01 完整 POST。Day05 学 PATCH 时，需结合 `attrs.get()` 与 `self.instance` 处理缺失字段。

## 五、掌握与后续

Day01 结论：Serializer 字段边界、单字段校验、跨字段校验和输入输出链已经形成可运行闭环，可以进入 Day02。

Day02 聚焦：创建发布单完整闭环，包括 `serializer.is_valid()`、`save()`、`create()`、`perform_create()`，以及由后端生成发布单号和默认状态。
