from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from channels.auth import AuthMiddlewareStack
from worker import DataPublisher
from worker import DataConsumer


application = ProtocolTypeRouter({
    "websocket":
        AuthMiddlewareStack(
            URLRouter([
                path("channel/", DataPublisher),
                path("datalink/", DataConsumer)
            ])
        )
})
