# ATUverce 🎓

**Универсальная платформа студентов колледжа Ала-Тоо, Бишкек**

> Instagram + LinkedIn + WeChat + AI — всё в одном месте

## Возможности
- 📱 **Соцсеть** — посты, сторис, лайки, комментарии
- 👤 **Профили** — LinkedIn-стиль, навыки, портфолио
- 🪙 **Ala Coins** — монеты за активность + лидерборд
- 📰 **Новости** — события и объявления колледжа
- 🎓 **Клубы** — студенческие объединения
- 🤖 **ИИ Помощник** — чат с Claude AI
- 📱 **PWA** — работает как приложение на телефоне

## Стек
- **Backend**: Django + Django REST Framework + PostgreSQL
- **Frontend**: HTML + CSS + Vanilla JS
- **AI**: Anthropic Claude API
- **Деплой**: Vercel (фронт) + Railway (бэк) + Supabase (БД)

## Запуск локально

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # Заполни переменные
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Frontend
```bash
cd frontend
# Открой index.html через Live Server (VSCode) или:
python -m http.server 5500
```

## Деплой

### Backend (Railway)
1. Создай аккаунт на railway.app
2. New Project → Deploy from GitHub
3. Добавь переменные из `.env.example`
4. Добавь PostgreSQL сервис

### Frontend (Vercel)
1. Создай аккаунт на vercel.com
2. Import Git Repository → папка `frontend`
3. Готово! 🚀

## Система Ala Coins
| Действие | Монеты |
|---|---|
| Создать пост | +5 |
| Помочь студенту | +10 |
| Выложить сторис | +3 |
| Комментарий | +1 |
| Участие в клубе | +5 |

Made with ❤️ by студенты Ала-Тоо