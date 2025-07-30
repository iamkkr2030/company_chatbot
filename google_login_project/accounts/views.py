from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import time

from .models import ChatSession, ChatMessage
from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# @login_required
def home(request):
    if request.user.is_authenticated:
        return redirect('create_chat_session')
    return render(request, 'account/home.html')

@login_required
def create_chat_session_view(request):  # 새 채팅 세션을 만들고 해당 채팅방으로 이동
    try:
        ChatSession.objects.filter(
            user=request.user,
            title="새로운 채팅",
            messages__isnull=True
        ).delete()
    except ChatSession.DoesNotExist:
        pass
    
    chat_session = ChatSession.objects.create(user=request.user)
    return redirect('chat_session', session_id=chat_session.id)

@login_required
def chat_session_view(request, session_id): # 채팅방 변경
    chat_session = get_object_or_404(ChatSession, id=session_id, user=request.user)
    
    chat_sessions = ChatSession.objects.filter(user=request.user).annotate(
        message_count=Count('messages')
    ).filter(
        message_count__gt=0
    ).order_by('-created_at')

    context = {
        'chat_session': chat_session, # 보고 있는 채팅방
        'chat_sessions': chat_sessions, # 목록에 있는 채팅방 전부
    }
    return render(request, 'account/chat.html', context)

def stream_response_generator(user_prompt, chat_session): # 스트리밍 응답 생성
    # 1. 사용자 메시지 저장
    ChatMessage.objects.create(session=chat_session, role='user', content=user_prompt)

    # 2. 첫 메시지인 경우, 제목으로 설정
    if chat_session.messages.count() == 1:
        chat_session.title = user_prompt[:50] # 처음 50자로 제목 설정
        chat_session.save()

    # 3. 이전 대화 기록을 LangChain 형식으로 변환 (현재 세션의 메시지만)
    history_queryset = chat_session.messages.all().order_by('timestamp')
    langchain_messages = []
    for msg in history_queryset:
        if msg.role == 'user':
            langchain_messages.append(HumanMessage(content=msg.content))
        else:
            langchain_messages.append(AIMessage(content=msg.content))

    # 4. Gemini 모델 스트리밍 호출
    full_response = ""
    for chunk in llm.stream(langchain_messages):
        content = chunk.content
        full_response += content
        yield content
        time.sleep(0.02) # 자연스러운 출력을 위한 약간의 딜레이

    # 5. 전체 AI 응답 저장
    if full_response:
        ChatMessage.objects.create(session=chat_session, role='ai', content=full_response)

@login_required
@csrf_exempt
def get_gemini_response_stream(request, session_id):  # 스트리밍 프로세스를 시작
    if request.method == 'POST':
        chat_session = get_object_or_404(ChatSession, id=session_id, user=request.user)
        try:
            data = json.loads(request.body)
            user_prompt = data.get('message')

            if not user_prompt:
                return JsonResponse({'error': '메시지가 없습니다.'}, status=400)
            
            # 스트리밍 생성기 함수를 StreamingHttpResponse에 전달
            return StreamingHttpResponse(stream_response_generator(user_prompt, chat_session))

        except json.JSONDecodeError:
            return JsonResponse({'error': '잘못된 JSON 형식입니다.'}, status=400)
    
    return JsonResponse({'error': '잘못된 요청입니다.'}, status=400)

@login_required
def delete_chat_session_view(request, session_id):  # 채팅창 삭제
    # POST 요청일 때만 삭제 처리
    if request.method == 'POST':
        # 현재 로그인한 사용자가 소유한 채팅 세션인지 확인 후 가져옴 (없으면 404 오류)
        chat_session = get_object_or_404(ChatSession, id=session_id, user=request.user)
        # 해당 세션을 삭제
        chat_session.delete()
        # 삭제 후 새 채팅 화면으로 이동
        return redirect('create_chat_session')
    
    # POST 요청이 아니면 홈으로 보냄
    return redirect('home')
