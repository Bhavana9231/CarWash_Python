from django.urls import path
from .consumer import MyConsumer
ws_urlpatterns = [
		path ('ws/some_url/', MyConsumer.as_asgi())
]
