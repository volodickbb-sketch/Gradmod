"""Language selection handler"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from app.utils.constants import MENU_TEXTS
from app.handlers.base import BaseHandler


class LanguageHandler(BaseHandler):
    """Handler for language selection"""
    
    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle language selection"""
        query = update.callback_query
        await query.answer()
        
        user_id = update.effective_user.id
        language = query.data.split("_")[1]
        
        # Update user language
        self.user_service.update_language(user_id, language)
        
        context.user_data["language"] = language
        context.user_data["answers"] = []
        context.user_data["current_question"] = 0
        
        texts = MENU_TEXTS[language]
        keyboard = [
            [InlineKeyboardButton(texts["new_test"], callback_data="start_test")],
            [InlineKeyboardButton(texts["history"], callback_data="view_history")],
            [InlineKeyboardButton(texts["stats"], callback_data="view_stats")],
            [InlineKeyboardButton(texts["settings"], callback_data="settings")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        lang_name = "English" if language == "en" else "Русский"
        await query.edit_message_text(
            f"✅ Language set to {lang_name}\n\n{texts['menu']}:",
            reply_markup=reply_markup,
        )
        
        return -1  # ConversationHandler.END
