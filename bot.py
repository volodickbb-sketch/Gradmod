#!/usr/bin/env python3
"""
Telegram bot for monitoring master's student mood and burnout detection
using Copenhagen Burnout Inventory (CBI)
"""

import threading
from app.config.settings import settings
from app.config.database import init_db
from app.handlers.start_handler import StartHandler
from app.handlers.language_handler import LanguageHandler
from app.handlers.test_handler import TestHandler
from app.handlers.menu_handler import MenuHandler
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    ContextTypes,
)
from telegram import Update


# Conversation states
SELECTING_LANGUAGE, ANSWERING_QUESTION, VIEWING_RESULTS = range(3)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command handler"""
    handler = StartHandler()
    try:
        return await handler.handle(update, context)
    finally:
        handler.__del__()


async def language_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle language selection"""
    handler = LanguageHandler()
    try:
        return await handler.handle(update, context)
    finally:
        handler.__del__()


async def start_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the CBI test"""
    handler = TestHandler()
    try:
        return await handler.start_test(update, context)
    finally:
        handler.__del__()


async def ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ask the current question"""
    handler = TestHandler()
    try:
        await handler.ask_question(update, context)
    finally:
        handler.__del__()


async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle answer to question"""
    handler = TestHandler()
    try:
        return await handler.handle_answer(update, context)
    finally:
        handler.__del__()


async def show_results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show test results"""
    handler = TestHandler()
    try:
        return await handler.show_results(update, context)
    finally:
        handler.__del__()


async def view_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View test history"""
    handler = MenuHandler()
    try:
        await handler.view_history(update, context)
    finally:
        handler.__del__()


async def view_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View statistics"""
    handler = MenuHandler()
    try:
        await handler.view_stats(update, context)
    finally:
        handler.__del__()


async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show settings"""
    handler = MenuHandler()
    try:
        await handler.settings(update, context)
    finally:
        handler.__del__()


async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Return to main menu"""
    handler = MenuHandler()
    try:
        await handler.main_menu(update, context)
    finally:
        handler.__del__()


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel conversation"""
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END


def start_dashboard():
    """Start dashboard server in a separate thread"""
    from app.api.app import run_dashboard
    run_dashboard(host="0.0.0.0", port=5000, debug=False)


def main():
    """Main function to run the bot and dashboard"""
    if not settings.TELEGRAM_BOT_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN not found in environment variables")
        return
    
    # Initialize database
    init_db()
    print("✅ Database initialized")
    
    # Start dashboard in a separate thread
    dashboard_thread = threading.Thread(target=start_dashboard, daemon=True)
    dashboard_thread.start()
    print("📊 Dashboard started on http://localhost:5000")
    
    # Create bot application
    application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
    
    # Conversation handler for test
    test_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            CallbackQueryHandler(start_test, pattern="^start_test$"),
        ],
        states={
            SELECTING_LANGUAGE: [
                CallbackQueryHandler(language_selected, pattern="^lang_"),
            ],
            ANSWERING_QUESTION: [
                CallbackQueryHandler(handle_answer, pattern="^answer_"),
            ],
            VIEWING_RESULTS: [
                CallbackQueryHandler(start_test, pattern="^start_test$"),
                CallbackQueryHandler(view_history, pattern="^view_history$"),
                CallbackQueryHandler(view_stats, pattern="^view_stats$"),
                CallbackQueryHandler(main_menu, pattern="^main_menu$"),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    
    # Other handlers
    application.add_handler(test_handler)
    application.add_handler(
        CallbackQueryHandler(language_selected, pattern="^lang_")
    )  # For settings
    application.add_handler(CallbackQueryHandler(start_test, pattern="^start_test$"))
    application.add_handler(CallbackQueryHandler(view_history, pattern="^view_history$"))
    application.add_handler(CallbackQueryHandler(view_stats, pattern="^view_stats$"))
    application.add_handler(CallbackQueryHandler(settings, pattern="^settings$"))
    application.add_handler(CallbackQueryHandler(main_menu, pattern="^main_menu$"))
    
    # Start the bot
    print("🤖 Bot is running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
