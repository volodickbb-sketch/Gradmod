"""Menu handlers"""
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from app.utils.constants import MENU_TEXTS
from app.handlers.base import BaseHandler


class MenuHandler(BaseHandler):
    """Handler for menu operations"""
    
    async def view_history(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """View test history"""
        query = update.callback_query
        await query.answer()
        
        user_id = update.effective_user.id
        user = self.user_service.get_user(user_id)
        
        if not user:
            await query.edit_message_text("User not found")
            return
        
        language = user.language
        texts = MENU_TEXTS[language]
        
        # Get test history
        test_results = self.test_service.get_user_test_history(user.id, limit=5)
        
        if not test_results:
            keyboard = [[InlineKeyboardButton(texts["back"], callback_data="main_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(texts["no_history"], reply_markup=reply_markup)
            return
        
        # Format history
        history_text = f"{texts['history']}:\n\n"
        for i, test in enumerate(reversed(test_results), 1):
            date = test.created_at.strftime("%Y-%m-%d %H:%M")
            history_text += texts["history_item"].format(
                number=i,
                date=date,
                personal=test.personal_burnout,
                study=test.study_burnout,
                total=test.total_burnout,
            )
            history_text += "\n\n"
        
        keyboard = [[InlineKeyboardButton(texts["back"], callback_data="main_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(history_text, reply_markup=reply_markup)
    
    async def view_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """View statistics"""
        query = update.callback_query
        await query.answer()
        
        user_id = update.effective_user.id
        user = self.user_service.get_user(user_id)
        
        if not user:
            await query.edit_message_text("User not found")
            return
        
        language = user.language
        texts = MENU_TEXTS[language]
        
        # Get statistics
        stats = self.test_service.get_user_statistics(user.id)
        test_results = self.test_service.get_user_test_history(user.id, limit=1)
        
        if not test_results:
            keyboard = [[InlineKeyboardButton(texts["back"], callback_data="main_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(texts["no_history"], reply_markup=reply_markup)
            return
        
        last_test_date = test_results[0].created_at.strftime("%Y-%m-%d")
        
        stats_text = f"""{texts['avg_stats']}:

{texts['avg_personal']}: {stats['avg_personal_burnout']:.1f}%
{texts['avg_study']}: {stats['avg_study_burnout']:.1f}%
{texts['avg_total']}: {stats['avg_total_burnout']:.1f}%

{texts['tests_completed']}: {stats['total_tests']}
{texts['last_test']}: {last_test_date}"""
        
        keyboard = [[InlineKeyboardButton(texts["back"], callback_data="main_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(stats_text, reply_markup=reply_markup)
    
    async def settings(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show settings"""
        query = update.callback_query
        await query.answer()
        
        user_id = update.effective_user.id
        user = self.user_service.get_user(user_id)
        
        if not user:
            await query.edit_message_text("User not found")
            return
        
        language = user.language
        texts = MENU_TEXTS[language]
        
        current_lang = "English" if language == "en" else "Русский"
        settings_text = f"""{texts['settings']}:

{texts['select_language']}: {current_lang}"""
        
        keyboard = [
            [
                InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
                InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
            ],
            [InlineKeyboardButton(texts["back"], callback_data="main_menu")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(settings_text, reply_markup=reply_markup)
    
    async def main_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Return to main menu"""
        query = update.callback_query
        await query.answer()
        
        user_id = update.effective_user.id
        user = self.user_service.get_user(user_id)
        
        if not user:
            await query.edit_message_text("User not found")
            return
        
        language = user.language
        texts = MENU_TEXTS[language]
        
        keyboard = [
            [InlineKeyboardButton(texts["new_test"], callback_data="start_test")],
            [InlineKeyboardButton(texts["history"], callback_data="view_history")],
            [InlineKeyboardButton(texts["stats"], callback_data="view_stats")],
            [InlineKeyboardButton(texts["settings"], callback_data="settings")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(f"{texts['menu']}:", reply_markup=reply_markup)
