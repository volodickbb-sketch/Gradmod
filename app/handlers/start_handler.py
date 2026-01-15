"""Start command handler"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from app.utils.constants import MENU_TEXTS
from app.handlers.base import BaseHandler


class StartHandler(BaseHandler):
    """Handler for /start command"""
    
    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle start command"""
        user_id = update.effective_user.id
        
        # Get or create user
        self.user_service.get_or_create_user(user_id, "en")
        
        keyboard = [
            [
                InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
                InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            MENU_TEXTS["en"]["welcome"], reply_markup=reply_markup
        )
        
        return 0  # SELECTING_LANGUAGE
