import uuid
from django.db import models
from django.contrib.auth.models import User

class ChatSession(models.Model):
    """채팅 세션을 저장하는 모델 (하나의 채팅방)"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default="새로운 채팅")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"

class ChatMessage(models.Model):
    """채팅 메시지를 저장하는 모델"""
    # 이제 user가 아닌 session에 연결됩니다.
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10) # 'user' 또는 'ai'
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.session.title} - {self.role}: {self.content[:50]}"