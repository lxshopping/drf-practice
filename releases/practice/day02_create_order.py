"""Day02：创建发布单完整闭环（核心冲刺第 1 站）。

目标用时：45～60 分钟。

开始方式：
1. 只打开并修改本文件。
2. 运行 `python manage.py runserver`。
3. 在 Postman 中执行 “Day02 - 创建发布单” 场景。
4. 本地通过后一次 commit + push；无需上传 Postman 结果。

本文件已经通过 `releases/views.py` 接入：
    POST http://127.0.0.1:8000/api/release-orders/

输入边界：
- 前端提交 app_code、app_name、env_name、branch_name、jenkins_job_name。
- 后端生成 release_no；模型默认生成 CREATED 状态。
- release_no 与 status 即使由前端传入也必须被忽略。

本轮只练三件事：生成业务编号、理解 create()、区分 perform_create() 的职责。
占位实现可以启动，但重复创建场景故意不会通过。
"""

from rest_framework import viewsets

from releases.models import ReleaseOrder
from releases.practice.day01_serializer import Day01ReleaseOrderSerializer


def build_release_no():
    # [TASK 1] 生成可读且低碰撞的发布单号，格式建议为：
    # RO-年月日时分秒-8位大写随机串。
    # [CHECK] 连续执行 Postman 场景 01、02；两次都应返回 201，release_no 不同。
    # [HINT-1] 时间部分负责可读和排序，随机部分负责避免同一秒碰撞。
    # [HINT-2] 可组合 django.utils.timezone.now() 与标准库 uuid。
    # [HINT-3] 先分别得到时间字符串和 8 位随机串，再用 f-string 拼接。
    # [WHY] 发布单号属于后端可信字段，不能让客户端决定，也不能依赖数据库报唯一冲突。
    # [SOURCE] https://docs.djangoproject.com/en/5.2/topics/i18n/timezones/#django.utils.timezone.now
    # [BASELINE] 常量只允许第一条数据成功；请替换为真实生成逻辑。
    return "RO-D02-BASELINE"


class Day02ReleaseOrderSerializer(Day01ReleaseOrderSerializer):
    """复用 Day01 校验，把 release_no 收紧为后端生成字段。"""

    class Meta(Day01ReleaseOrderSerializer.Meta):
        read_only_fields = [
            *Day01ReleaseOrderSerializer.Meta.read_only_fields,
            "release_no",
        ]

    def create(self, validated_data):
        # [TASK 2] 不改变接口行为，独立写出 ModelSerializer 默认 create 的等价 ORM 创建逻辑。
        # [CHECK] 场景 01 仍返回 201；请求中的业务字段与响应一致。
        # [HINT-1] validated_data 已经过字段校验和对象级校验，是可保存的数据字典。
        # [HINT-2] 此处只创建一个 ReleaseOrder，不需要再次调用 is_valid() 或 save()。
        # [HINT-3] 使用模型 manager 的 create，并把 validated_data 解包为关键字参数。
        # [WHY] 先理解默认实现，后续遇到多对象写入或派生字段时才知道何时值得覆写 create()。
        # [SOURCE] https://www.django-rest-framework.org/api-guide/serializers/#customizing-multiple-create
        # [BASELINE] 框架默认实现当前可用；请从记忆写出等价的一行 ORM 代码。
        return super().create(validated_data)


class Day02ReleaseOrderViewSet(viewsets.ModelViewSet):
    queryset = ReleaseOrder.objects.all()
    serializer_class = Day02ReleaseOrderSerializer

    def perform_create(self, serializer):
        # [TASK 3] 调用 build_release_no()，通过 serializer.save(...) 注入后端字段。
        # [CHECK-A] 场景 01、02 连续创建成功，发布单号不同。
        # [CHECK-B] 场景 03 传入伪造 release_no/status，响应仍使用后端编号与 CREATED。
        # [HINT-1] perform_create() 接收的是已经 is_valid() 的 serializer。
        # [HINT-2] 传给 save() 的关键字参数会合并进 validated_data，再进入 create()。
        # [HINT-3] 不要直接 ReleaseOrder.objects.create；让 serializer 保持唯一保存入口。
        # [WHY] ViewSet 负责请求上下文和后端注入，Serializer 负责校验与持久化边界。
        # [SOURCE] https://www.django-rest-framework.org/api-guide/generic-views/#save-and-deletion-hooks
        # [BASELINE] 固定编号会让第二次创建触发唯一约束；请改成调用生成函数。
        serializer.save(release_no="RO-D02-BASELINE")


# 提交前自查：
# [ ] TASK 1：发布单号不再是常量，连续创建不冲突。
# [ ] TASK 2：create() 已从记忆写成等价 ORM 创建逻辑。
# [ ] TASK 3：perform_create() 通过 serializer.save(...) 注入后端编号。
# [ ] Postman 场景 01～03 已在本地执行；无需上传结果。
# [ ] 能口述：request.data -> is_valid() -> validated_data -> perform_create()
#     -> save(**kwargs) -> create(validated_data) -> instance -> response.data。
# [ ] python manage.py check 通过。
# [ ] python manage.py makemigrations --check --dry-run 无遗漏迁移。
