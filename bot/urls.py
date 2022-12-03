
from rest_framework.routers import DefaultRouter
from bot.views import DeleteChatHistoryView, SendMessageView
from django.urls import path, include

router = DefaultRouter()
router.register(r"clear-chat", DeleteChatHistoryView, basename="clear")
router.register(r"send-message",SendMessageView , basename="message")

urlpatterns = [
    path("", include(router.urls)),
    
]
