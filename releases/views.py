from rest_framework import viewsets

from releases.models import ReleaseOrder
from releases.serializers import ReleaseOrderSerializer


class ReleaseOrderViewSet(viewsets.ModelViewSet):
    """Day01 的 HTTP 测试入口；练习重点仍是 Serializer。"""

    queryset = ReleaseOrder.objects.all()
    serializer_class = ReleaseOrderSerializer
