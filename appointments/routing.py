from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/queue/(?P<doctor_id>\w+)/$', consumers.QueueConsumer.as_asgi()),
    re_path(r'ws/display/$', consumers.DisplayMonitorConsumer.as_asgi()),
    re_path(r'ws/display-monitor/$', consumers.DisplayMonitorConsumer.as_asgi()),
]
