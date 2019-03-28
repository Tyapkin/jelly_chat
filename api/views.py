from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from .models import ChatSession, ChatSessionMember, ChatSessionMessage, user_deserializer


# we won`t make use DRF serializers for our simple models

class ChatSessionView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        chat_session = ChatSession.objects.create(owner=user)

        return Response({
            'status': 'success',
            'uri': chat_session.uri,
            'message': 'New chat session create'
        })

    def patch(self, request, *args, **kwargs):
        User = get_user_model()
        uri = kwargs['uri']
        username = request.data['username']
        user = User.objects.get(username=username)
        chat_session = ChatSession.objects.get(uri=uri)
        owner = chat_session.owner

        if owner != user:
            chat_session.members.get_or_create(user=user, chat_session=chat_session)

        owner = user_deserializer(owner)
        members = [
            user_deserializer(chat_session.user)
            for chat_session in chat_session.members.all()
        ]
        members.insert(0, owner)  # meke the owner the first member

        return Response({
            'statuc': 'success',
            'members': members,
            'message': '{} joined to chat'.format(user.username),
            'user': user_deserializer(user)
        })


class ChatSessionMessageView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """
        return all messages in a chat session
        """
        uri = kwargs['uri']
        chat_session = ChatSession.objects.get(uri=uri)
        messages = [
            chat_session_message.to_json()
            for chat_session_message in chat_session.messages.all()
        ]

        return Response({
            'id': chat_session.id,
            'uri': chat_session.uri,
            'messages': messages
        })

    def post(self, request, *args, **kwargs):
        """
        create new message in a chat session
        """
        uri = kwargs['uri']
        message = request.data['message']
        user = request.user
        chat_session = ChatSession.objects.get(uri=uri)

        ChatSessionMessage.objects.create(user=user, chat_session=chat_session,
                                          message=message)

        return Response({
            'status': 'success',
            'uri': chat_session.uri,
            'message': message,
            'user': user_deserializer(user)
        })
