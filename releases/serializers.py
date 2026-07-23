from rest_framework import serializers
from releases.models import ReleaseOrder


class ReleaseOrderSerializer(serializers.ModelSerializer):

    # status_display是计算字段，数据库只有status字段，serializer有一对多，多对多，field，多种实现方式
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = ReleaseOrder
        # 为什么企业项目基本不会长期使用： 因为有些字段不需要返回，就不会使用__all__

        fields = [
            "id",
            "release_no",
            "app_code",
            "app_name",
            "env_name",
            "branch_name",
            "jenkins_job_name",
            "status",
            "status_display",
            "started_at",
            "finished_at",
            "error_message",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "status",
            "started_at",
            "finished_at",
            "error_message",
            "created_at",
            "updated_at",
        ]


    def validate_app_code(self, value):
        value = value.lower().strip()
        if " " in value:
            raise serializers.ValidationError("应用编码包含空格")
        return value

    def validate_branch_name(self, value):
        value = value.strip()
        if " " in value:
            raise serializers.ValidationError("分支名不能包含空格")
        return value

    # 这里不能写在validate_branch_name()中，原因是这个是全局的提交验证，不是单个字段的验证
    def validate(self, attrs):
        branch_name = attrs["branch_name"]
        env_name = attrs["env_name"]
        if (
            env_name == "prod"
            and branch_name != "master"
            and not branch_name.startswith("release/")
        ):
            raise serializers.ValidationError("分支名必须以release或master开头")
        return attrs

    # read_only_fields有用，简单来说就是只返回，不能提交
    # 怎么写测试验证？那需要写view和url才行吧？
    # 源码分析，导入什么模块？目前看起来报错，源码这块基本没找到




