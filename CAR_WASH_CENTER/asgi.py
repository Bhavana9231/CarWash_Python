# It exposes the ASGI callable as a module-level variable named `application`.
# For more information on this file, see
# https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/

import os
from django.core.asgi import get_asgi_application
from channels.routing import URLRouter
from channels.routing import ProtocolTypeRouter # Fixed typo
from channels.auth import AuthMiddlewareStack # Added AuthMiddlewareStack import
from APP_CAR_WASH_CENTER.routing import ws_urlpatterns # Added import for websocket routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CAR_WASH_CENTER.settings')

# Define the ASGI application
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            ws_urlpatterns
        )
    ),
})
