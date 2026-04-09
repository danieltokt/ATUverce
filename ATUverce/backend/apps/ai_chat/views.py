from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import requests

from .models import ChatSession, ChatMessage


SYSTEM_PROMPT = """Ты — ATU Ассистент, дружелюбный ИИ помощник студентов колледжа Ала-Тоо в Бишкеке, Кыргызстан.
Помогаешь с учёбой, вопросами о колледже, карьерой, резюме. Отвечай коротко и по делу. Используй эмодзи."""


class ChatAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        message = request.data.get('message', '').strip()
        session_id = request.data.get('session_id')

        if not message:
            return Response({'error': 'Сообщение пустое'}, status=400)

        if session_id:
            try:
                session = ChatSession.objects.get(id=session_id, user=request.user)
            except ChatSession.DoesNotExist:
                session = ChatSession.objects.create(user=request.user)
        else:
            session = ChatSession.objects.create(user=request.user)
            session.title = message[:40] + ('...' if len(message) > 40 else '')
            session.save()

        ChatMessage.objects.create(session=session, role='user', content=message)

        history = ChatMessage.objects.filter(session=session).order_by('-created_at')[:10]

        try:
            response = requests.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": "phi3",
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        *[
                            {
                                "role": "user" if m.role == "user" else "assistant",
                                "content": m.content
                            }
                            for m in reversed(history)
                        ]
                    ],
                    "stream": False,
                    "options": {
                        "num_predict": 200
                    }
                },
                timeout=60
            )

            data = response.json()
            reply = data.get("message", {}).get("content", "").strip()

            if not reply:
                reply = "😅 Модель не ответила, попробуй переформулировать"

        except Exception as e:
            reply = f'Ошибка Ollama: {str(e)}'

        ChatMessage.objects.create(session=session, role='assistant', content=reply)

        return Response({
            'reply': reply,
            'session_id': session.id,
            'session_title': session.title,
        })


class SessionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sessions = ChatSession.objects.filter(user=request.user).order_by('-updated_at')[:30]
        return Response([
            {
                'id': s.id,
                'title': s.title or 'Чат',
                'updated_at': s.updated_at
            }
            for s in sessions
        ])


class SessionDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            session = ChatSession.objects.get(id=pk, user=request.user)
        except ChatSession.DoesNotExist:
            return Response({'error': 'Не найдено'}, status=404)

        messages = ChatMessage.objects.filter(session=session).order_by('created_at')
        return Response({
            'id': session.id,
            'title': session.title or 'Чат',
            'messages': [
                {
                    'role': m.role,
                    'content': m.content,
                    'created_at': m.created_at
                }
                for m in messages
            ]
        })

    def patch(self, request, pk):
        try:
            session = ChatSession.objects.get(id=pk, user=request.user)
        except ChatSession.DoesNotExist:
            return Response({'error': 'Не найдено'}, status=404)

        title = request.data.get('title', '').strip()
        if title:
            session.title = title[:100]
            session.save()
        return Response({'id': session.id, 'title': session.title})

    def delete(self, request, pk):
        try:
            session = ChatSession.objects.get(id=pk, user=request.user)
        except ChatSession.DoesNotExist:
            return Response({'error': 'Не найдено'}, status=404)

        session.delete()
        return Response({'deleted': True})