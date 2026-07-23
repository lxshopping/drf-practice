from django.test import TestCase

from releases.models import ReleaseOrder
from releases.serializers import ReleaseOrderSerializer

# Create your tests here.


# serializer = ReleaseOrderSerializer(data=data)
# is_valid = serializer.is_valid()
# print(serializer.validated_data)
# print(serializer.errors)


class ReleaseOrderSerializerTest(TestCase):

    def build_valid_data(self):
        return {
            "release_no": "release_no",
            "app_code": "app_code",
            "app_name": "app_name",
            "env_name": "env_name",
            "branch_name": "branch_name",
            "jenkins_job_name": "jenkins_job_name",
        }
    def test_status_is_read_only(self):
        data = self.build_valid_data()
        data["status"] = ReleaseOrder.Status.SUCCESS

        serializer = ReleaseOrderSerializer(data=data)

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )

        order = serializer.save()

        self.assertEqual(
            order.status,
            ReleaseOrder.Status.CREATED,
        )