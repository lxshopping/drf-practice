from django.db import models


# Create your models here.
class ReleaseOrder(models.Model):

    class Status(models.TextChoices):
        CREATED = "CREATED", "待触发"
        TRIGGERING = "TRIGGERING", "触发中"
        RUNNING = "RUNNING", "运行中"
        SUCCESS = "SUCCESS", "成功"
        FAILED = "FAILED", "失败"

    release_no = models.CharField(max_length=64, unique=True, verbose_name="发布单号")
    app_code = models.CharField(max_length=64, verbose_name="应用编码")
    app_name = models.CharField(max_length=128, verbose_name="应用名称")
    env_name = models.CharField(max_length=64, verbose_name="环境名称")
    branch_name = models.CharField(max_length=64, verbose_name="代码分支")
    jenkins_job_name = models.CharField(max_length=255, verbose_name="Jenkins Job")
    status = models.CharField(
        max_length=64,
        choices=Status.choices,
        default=Status.CREATED,
        verbose_name="发布状态",
    )
    started_at = models.DateTimeField(null=True, blank=True, verbose_name="开始时间")
    finished_at = models.DateTimeField(null=True, blank=True, verbose_name="结束时间")
    error_message = models.TextField(blank=True, default="", verbose_name="错误信息")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        ordering = ["-id"]
        verbose_name = "发布单"
        verbose_name_plural = "发布单"

    def __str__(self):
        return f"{self.release_no} - {self.app_code}"


