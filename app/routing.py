from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
<<<<<<< HEAD
    re_path(r'ws/chat/(?P<solicitud_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
=======
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
>>>>>>> e7b3cd303bb562f80b2754fe157fe3701b4aa029
]