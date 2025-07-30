from django.urls import path
from . import views

urlpatterns = [
    # '/' 경로는 이제 로그인/새 채팅 선택 화면
    path('', views.home, name='home'),

    # '새 채팅' 버튼을 누르면 이 URL이 호출됨
    path('chat/new/', views.create_chat_session_view, name='create_chat_session'),

    # 각 채팅방은 고유 ID를 가진 URL을 가짐
    path('chat/<uuid:session_id>/', views.chat_session_view, name='chat_session'),

    # 스트리밍 응답을 위한 URL (세션 ID 포함)
    path('get-gemini-response/<uuid:session_id>/', views.get_gemini_response_stream, name='get_gemini_response_stream'),
    
    # 삭제 기능을 위한 URL 추가
    path('chat/delete/<uuid:session_id>/', views.delete_chat_session_view, name='delete_chat_session'),
]