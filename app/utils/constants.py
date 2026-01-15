"""Constants and configuration"""
from typing import Dict, List

# Response options mapping
RESPONSE_OPTIONS = {
    "always": 100,
    "often": 75,
    "sometimes": 50,
    "seldom": 25,
    "never": 0,
}

# CBI Questions structure
CBI_QUESTIONS = {
    "en": {
        "personal": [
            "How often do you feel tired?",
            "How often are you physically exhausted?",
            "How often are you emotionally exhausted?",
            'How often do you think: "I can\'t take it anymore"?',
            "How often do you feel worn out?",
            "How often do you feel weak and susceptible to illness?",
        ],
        "study": [
            "Do you feel worn out at the end of the studying day?",
            "Are you exhausted in the morning at the thought of another day of studying?",
            "Do you feel that every hour of studying is tiring for you?",
            "Do you have enough energy for family and friends during leisure time?",
            "Is your studying emotionally exhausting?",
            "Does your studying frustrate you?",
            "Do you feel burnt out because of your studying?",
        ],
    },
    "ru": {
        "personal": [
            "Как часто вы чувствуете усталость?",
            "Как часто вы физически истощены?",
            "Как часто вы эмоционально истощены?",
            'Как часто вы думаете: "Я больше не могу этого вынести"?',
            "Как часто вы чувствуете себя измотанным?",
            "Как часто вы чувствуете слабость и подверженность болезням?",
        ],
        "study": [
            "Чувствуете ли вы себя измотанным в конце учебного дня?",
            "Чувствуете ли вы себя истощенным утром при мысли о новом учебном дне?",
            "Чувствуете ли вы, что каждый час учебы утомляет вас?",
            "Хватает ли вам энергии для семьи и друзей в свободное время?",
            "Является ли ваша учеба эмоционально истощающей?",
            "Фрустрирует ли вас ваша учеба?",
            "Чувствуете ли вы выгорание из-за учебы?",
        ],
    },
}

# Response options text
RESPONSE_TEXTS = {
    "en": {
        "always": "Always",
        "often": "Often",
        "sometimes": "Sometimes",
        "seldom": "Seldom",
        "never": "Never/almost never",
    },
    "ru": {
        "always": "Всегда",
        "often": "Часто",
        "sometimes": "Иногда",
        "seldom": "Редко",
        "never": "Никогда/почти никогда",
    },
}

# Menu texts
MENU_TEXTS = {
    "en": {
        "welcome": "Welcome to GradMood Bot! 👋\n\nThis bot helps monitor your mood and detect early signs of burnout.\n\nSelect your language:",
        "start_test": "Let's start the Copenhagen Burnout Inventory (CBI) test.\n\nThis test consists of 13 questions and will help assess your level of burnout.\n\nPress /start_test when you're ready!",
        "question": "Question {current}/{total}",
        "results": "📊 Your Results",
        "personal_burnout": "Personal Burnout",
        "study_burnout": "Study-related Burnout",
        "total_burnout": "Total Burnout Score",
        "interpretation": "Interpretation",
        "low": "Low (0-33)",
        "moderate": "Moderate (34-66)",
        "high": "High (67-100)",
        "low_desc": "You're doing well! Keep maintaining a healthy balance.",
        "moderate_desc": "You may be experiencing some stress. Consider taking breaks and managing your workload.",
        "high_desc": "⚠️ You may be experiencing significant burnout. Consider seeking support and taking time to rest.",
        "menu": "Main Menu",
        "new_test": "🆕 Start New Test",
        "history": "📈 View History",
        "stats": "📊 Statistics",
        "settings": "⚙️ Settings",
        "select_language": "Select Language",
        "no_history": "You haven't completed any tests yet.",
        "history_item": "Test #{number}\nDate: {date}\nPersonal: {personal}%\nStudy: {study}%\nTotal: {total}%",
        "avg_stats": "Average Statistics",
        "avg_personal": "Average Personal Burnout",
        "avg_study": "Average Study Burnout",
        "avg_total": "Average Total Burnout",
        "tests_completed": "Tests Completed",
        "last_test": "Last Test Date",
        "back": "⬅️ Back",
    },
    "ru": {
        "welcome": "Добро пожаловать в GradMood Bot! 👋\n\nЭтот бот помогает отслеживать ваше настроение и выявлять ранние признаки выгорания.\n\nВыберите язык:",
        "start_test": "Давайте начнем тест Copenhagen Burnout Inventory (CBI).\n\nЭтот тест состоит из 13 вопросов и поможет оценить ваш уровень выгорания.\n\nНажмите /start_test когда будете готовы!",
        "question": "Вопрос {current}/{total}",
        "results": "📊 Ваши Результаты",
        "personal_burnout": "Личное Выгорание",
        "study_burnout": "Учебное Выгорание",
        "total_burnout": "Общий Балл Выгорания",
        "interpretation": "Интерпретация",
        "low": "Низкий (0-33)",
        "moderate": "Умеренный (34-66)",
        "high": "Высокий (67-100)",
        "low_desc": "У вас все хорошо! Продолжайте поддерживать здоровый баланс.",
        "moderate_desc": "Вы можете испытывать некоторый стресс. Рассмотрите возможность делать перерывы и управлять нагрузкой.",
        "high_desc": "⚠️ Вы можете испытывать значительное выгорание. Рассмотрите возможность обратиться за поддержкой и отдохнуть.",
        "menu": "Главное Меню",
        "new_test": "🆕 Начать Новый Тест",
        "history": "📈 История",
        "stats": "📊 Статистика",
        "settings": "⚙️ Настройки",
        "select_language": "Выбрать Язык",
        "no_history": "Вы еще не прошли ни одного теста.",
        "history_item": "Тест #{number}\nДата: {date}\nЛичное: {personal}%\nУчебное: {study}%\nВсего: {total}%",
        "avg_stats": "Средняя Статистика",
        "avg_personal": "Среднее Личное Выгорание",
        "avg_study": "Среднее Учебное Выгорание",
        "avg_total": "Среднее Общее Выгорание",
        "tests_completed": "Пройдено Тестов",
        "last_test": "Дата Последнего Теста",
        "back": "⬅️ Назад",
    },
}


def get_questions(language: str) -> List[str]:
    """Get all questions in order"""
    questions = CBI_QUESTIONS[language]["personal"] + CBI_QUESTIONS[language]["study"]
    return questions


def get_interpretation(score: float, language: str) -> tuple:
    """Get interpretation text for a score"""
    texts = MENU_TEXTS[language]
    if score <= 33:
        return texts["low"], texts["low_desc"]
    elif score <= 66:
        return texts["moderate"], texts["moderate_desc"]
    else:
        return texts["high"], texts["high_desc"]
