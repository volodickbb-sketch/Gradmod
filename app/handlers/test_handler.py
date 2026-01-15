"""Test handlers"""
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from app.utils.constants import (
    MENU_TEXTS,
    RESPONSE_TEXTS,
    RESPONSE_OPTIONS,
    get_questions,
    get_interpretation,
)
from app.handlers.base import BaseHandler


class TestHandler(BaseHandler):
    """Handler for test operations"""
    
    async def start_test(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start the CBI test"""
        user_id = update.effective_user.id
        user = self.user_service.get_user(user_id)
        language = user.language if user else "en"
        
        context.user_data["language"] = language
        context.user_data["answers"] = []
        context.user_data["current_question"] = 0
        
        questions = get_questions(language)
        context.user_data["questions"] = questions
        
        await self.ask_question(update, context)
        return 1  # ANSWERING_QUESTION
    
    async def ask_question(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Ask the current question"""
        language = context.user_data.get("language", "en")
        current = context.user_data["current_question"]
        questions = context.user_data["questions"]
        texts = MENU_TEXTS[language]
        
        if current >= len(questions):
            await self.show_results(update, context)
            return 2  # VIEWING_RESULTS
        
        question_text = questions[current]
        response_texts = RESPONSE_TEXTS[language]
        
        keyboard = [
            [
                InlineKeyboardButton(
                    response_texts["always"], callback_data="answer_always"
                ),
                InlineKeyboardButton(response_texts["often"], callback_data="answer_often"),
            ],
            [
                InlineKeyboardButton(
                    response_texts["sometimes"], callback_data="answer_sometimes"
                ),
                InlineKeyboardButton(response_texts["seldom"], callback_data="answer_seldom"),
            ],
            [InlineKeyboardButton(response_texts["never"], callback_data="answer_never")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        question_num = current + 1
        total = len(questions)
        header = texts["question"].format(current=question_num, total=total)
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                f"{header}\n\n{question_text}", reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                f"{header}\n\n{question_text}", reply_markup=reply_markup
            )
    
    async def handle_answer(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle answer to question"""
        query = update.callback_query
        await query.answer()
        
        answer_key = query.data.split("_")[1]
        score = RESPONSE_OPTIONS[answer_key]
        context.user_data["answers"].append(score)
        context.user_data["current_question"] += 1
        
        await self.ask_question(update, context)
        return 1  # ANSWERING_QUESTION
    
    async def show_results(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show test results"""
        user_id = update.effective_user.id
        language = context.user_data.get("language", "en")
        answers = context.user_data["answers"]
        
        # Calculate scores
        scores = self.test_service.calculate_scores(answers)
        
        # Get or create user
        user = self.user_service.get_or_create_user(user_id, language)
        
        # Save test result
        self.test_service.save_test_result(
            user.id,
            scores["personal"],
            scores["study"],
            scores["total"],
        )
        
        texts = MENU_TEXTS[language]
        
        # Format results
        personal_level, personal_desc = get_interpretation(scores["personal"], language)
        study_level, study_desc = get_interpretation(scores["study"], language)
        total_level, total_desc = get_interpretation(scores["total"], language)
        
        results_text = f"""{texts['results']}

{texts['personal_burnout']}: {scores['personal']}% ({personal_level})
{personal_desc}

{texts['study_burnout']}: {scores['study']}% ({study_level})
{study_desc}

{texts['total_burnout']}: {scores['total']}% ({total_level})
{total_desc}"""
        
        keyboard = [
            [InlineKeyboardButton(texts["new_test"], callback_data="start_test")],
            [InlineKeyboardButton(texts["history"], callback_data="view_history")],
            [InlineKeyboardButton(texts["stats"], callback_data="view_stats")],
            [InlineKeyboardButton(texts["back"], callback_data="main_menu")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                results_text, reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(results_text, reply_markup=reply_markup)
        
        return 2  # VIEWING_RESULTS
