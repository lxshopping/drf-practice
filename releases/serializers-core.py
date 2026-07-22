from pyexpat import model

from django.db import models
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from releases.models import ReleaseOrder   



class ReleaseOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReleaseOrder
        # 为什么企业项目基本不会长期使用： 因为有些字段不需要返回，就不会使用__all__
        status_display = serializers.SerializerMethodField(source="get_status_display")
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
            "status_display",
            "started_at",
            "finished_at",
            "error_message",
            "created_at",
            "updated_at",
        ]
    
    # status_display是计算字段，数据库只有status字段，serializer有一对多，多对多，field，多种实现方式

    def validate_status(self, attrs):
        return attrs 
    
    def validate_branch_name(self,attrs):
        if not attrs.strip():
            raise serializers.ValidationError("分支名不能为空")
        
        if not attrs.startswith("release"):
            raise serializers.ValidationError("分支名必须以release开头")
        return attrs

# 这里不能写在validate_branch_name()中，原因是这个是全局的提交验证，不是单个字段的验证
    def validate(self, attrs):
        branch_name = attrs["branch_name"]
        if not branch_name.startswith("release") or not branch_name.startswith("master"):
            raise serializers.ValidationError("分支名必须以release或master开头")

        if attrs["status"] == "RUNNING":
            raise serializers.ValidationError("状态为RUNNING的不能修改")
        return attrs

# read_only_fields有用，简单来说就是只返回，不能提交
# 怎么写测试验证？那需要写view和url才行吧？
# 源码分析，导入什么模块？目前看起来报错，源码这块基本没找到
    serializer.is_valid()
    serializer.save()