from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from automation.consumers import OperationStatusConsumer

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('operation-status/', OperationStatusConsumer.as_asgi()),
        ])
    )
})
