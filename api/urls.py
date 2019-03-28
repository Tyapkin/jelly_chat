from django.urls import path

from .views import ChatSessionView, ChatSessionMessageView


urlpatterns = [
    path('chats/', ChatSessionView.as_view(), name='chats_list'),
    path('chats/<uri>/', ChatSessionView.as_view(), name='chat_detail'),
    path('chats/<uri>/messages/', ChatSessionMessageView.as_view(), name='chat_messages')
]
