from rest_framework import viewsets

from releases.models import ReleaseOrder
from releases.practice.day01_serializer import Day01ReleaseOrderSerializer


class ReleaseOrderViewSet(viewsets.ModelViewSet):
    """当前活动练习的 HTTP 入口；每天只切换 serializer_class 的来源。"""

    queryset = ReleaseOrder.objects.all()
    serializer_class = Day01ReleaseOrderSerializer
