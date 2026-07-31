"""当前活动练习的 HTTP 接线。

滚动核心冲刺期间这里只切换当前 session 的 ViewSet；核心答案始终留在
`releases/practice/dayXX_*.py`。
"""

from .practice.day02_create_order import (
    Day02ReleaseOrderViewSet as ReleaseOrderViewSet,
)
