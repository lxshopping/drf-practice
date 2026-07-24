"""Day01：Serializer 核心练习（当前接口实际使用的代码）。

开始方式：
1. 只打开并修改本文件，不需要来回查看 Chat。
2. 运行 `python manage.py runserver`。
3. 在 Postman 中执行 Day01 场景；每完成一个 TASK，只重跑对应 CHECK。
4. 填写 `docs/results/day01-postman.md`，然后 commit + push。

本文件已经通过 `releases/views.py` 接入：
    http://127.0.0.1:8000/api/release-orders/

说明：
- `releases/serializers.py` 保留的是此前练习成果，本轮不要先打开它照抄。
- 下面的占位实现只保证项目可以启动，业务结果故意不完整。
- 按 TASK 1 -> 5 顺序修改，不要一次性重写全部内容。
- 注释只给渐退式提示，不包含完整答案。
"""

from rest_framework import serializers

from releases.models import ReleaseOrder


class Day01ReleaseOrderSerializer(serializers.ModelSerializer):
    """围绕 ReleaseOrder 完成字段声明、只读边界与两层校验。"""

    # [TASK 1] 让 status_display 返回状态对应的中文展示值，而不是原始状态码。
    # [CHECK] 先执行 Postman 场景 07；CREATED 对应的展示值应为“待触发”。
    # [HINT-1] 这是输出字段，应声明在 Serializer 类中，而不是 Meta 中。
    # [HINT-2] Django choices 模型实例自带 get_<字段名>_display()。
    # [SOURCE] 完成后只追 Serializer.to_representation()。
    # [BASELINE] 这里故意返回原始 status，等待你修正。
    status_display = serializers.CharField(source="status", read_only=True)

    class Meta:
        model = ReleaseOrder

        # [TASK 2] 把临时的 "__all__" 改成明确字段清单，并补齐只读字段。
        # [CHECK] 执行 Postman 场景 02：输入 status=SUCCESS，保存后仍应为 CREATED。
        # [HINT-1] status、执行时间、错误信息和时间戳由后端维护。
        # [HINT-2] fields 决定输入/输出边界；read_only_fields 决定只输出、不接收。
        # [SOURCE] 完成后解释为什么只读字段不在 _writable_fields 中。
        # [BASELINE] 以下配置故意不完整，但能保证项目正常启动。
        fields = "__all__"
        read_only_fields = ["id"]

    def validate_app_code(self, value):
        # [TASK 3] 规范化 app_code，并拒绝内部仍含空格的值。
        # [CHECK-A] 场景 01：" DMS-MDM " 最终应保存并返回 "dms-mdm"。
        # [CHECK-B] 场景 03："dms mdm" 应返回 400，错误归属 app_code。
        # [HINT-1] 这是只依赖单字段的转换和校验，保留在 validate_app_code()。
        # [HINT-2] 注意处理顺序：先规范化，再判断规范化后的值。
        # [SOURCE] 卡住时定位 Field.run_validation()，不要通读整个 serializers.py。
        return value

    def validate_branch_name(self, value):
        # [TASK 4] 去除分支名首尾空格，并拒绝内部空格。
        # [CHECK] 可把场景 04 的 branch_name 临时改为 "release /v1" 验证错误字段。
        # [HINT-1] 此处只处理 branch_name 自身，不判断 prod/test。
        # [HINT-2] 需要 env_name 才能判断的规则应留给 validate(attrs)。
        return value

    def validate(self, attrs):
        # [TASK 5] 实现环境与分支的组合规则：
        # - prod 只允许 master 或 release/...；
        # - 非 prod 允许 feature/...。
        # [CHECK-A] 场景 04：prod + feature/test -> 400。
        # [CHECK-B] 场景 05：prod + master -> 201。
        # [CHECK-C] 场景 06：test + feature/test -> 201。
        # [HINT-1] attrs 中已经是各字段完成字段级校验后的值。
        # [HINT-2] 用一句中文先写清“什么时候才报错”，再翻译成布尔表达式。
        # [WHY] 完成后在总结中说明为什么此规则不能放进 validate_branch_name()。
        # [SOURCE] 只追 Serializer.run_validation() 与 to_internal_value() 的调用顺序。
        return attrs


# 提交前自查：
# [ ] TASK 1~5 均已完成。
# [ ] 7 个 Postman 固定场景均已执行。
# [ ] branch_name 内部空格的变化验证已执行。
# [ ] docs/results/day01-postman.md 已填写真实状态码和关键结果。
# [ ] docs/day01-serializer-core.md 已与当前代码同步。
# [ ] python manage.py check 通过。
# [ ] python manage.py makemigrations --check --dry-run 显示无遗漏迁移。
