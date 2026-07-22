from rest_framework import serializers
from releases.models import ReleaseOrder


class ReleaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReleaseOrder
        fields = "__all__"
        read_only_fields = [
            "status",
            "started_at",
            "finished_at",
            "error_message",
            "created_at",
            "updated_at",
        ]
