from uuid import uuid4

from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


def user_deserializer(user):
    """
    User instance deserialize to json
    :param user:
    :return:
    """
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'f_name': user.first_name,
        'l_name': user.last_name
    }
def _generate_unique_uri():
    """
    generating unique URL for chat session
    :return:
    """
    return str(uuid4()).replace('-', '')[:15]


class TrackDateAbstractModel(models.Model):
    """
    Tracking date creation or date update
    """
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ChatSession(TrackDateAbstractModel):
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    uri = models.URLField(default=_generate_unique_uri)


class ChatSessionMessage(TrackDateAbstractModel):
    """
    Model to storing messages for a session
    """
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    chat_session = models.ForeignKey(ChatSession, related_name='messages',
                                     on_delete=models.PROTECT)
    message = models.TextField(max_length=2000)

    def to_json(self):
        """
        deserialization message to json
        :return:
        """
        return {'user': user_deserializer(self.user), 'message': self.message}


class ChatSessionMember(TrackDateAbstractModel):
    """
    storing all users in a chat session
    """
    chat_session = models.ForeignKey(ChatSession, related_name='members',
                                     on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
