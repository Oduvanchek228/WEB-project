import logging
from telegram.ext import Application, MessageHandler, CommandHandler, filters
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from data import db_session
from data.users import User
from data.news import News

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

reply_keyboard = [['/help', '/users'],
                  ['/news', '/last_news'],
                  ['/exit']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

db_session.global_init('db/users.db')
db_session.global_init('db/blogs.db')
db_sess = db_session.create_session()


async def start(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет, {user.mention_html()}! Чтобы увидеть все доступные команды, введите /keyboard.",
    )


async def help_command(update, context):
    await update.message.reply_text(
        """Справка:
            /keyboard - открыть виджет со всеми доступными 
                                   командами
            /exit - убрать виджет
            /users - просмотреть всех пользователей
            /news - просмотреть все объявления
            /last_news - просмотреть 5 последних объявлений""")


async def reaction_to_messages(update, context):
    await update.message.reply_text('Пожалуйста, введите команду вместо обычного сообщения')


async def users(update, context):
    users_list = [user.name + '\n' + user.about + '\n' for user in db_sess.query(User).all()]
    await update.message.reply_text('\n'.join(users_list))


async def news(update, context):
    news_list = [news.title + '\n' + news.content + '\n' + f'Автор - {news.user.name}' + '\n' for news in
                 db_sess.query(News).all()]
    await update.message.reply_text('\n'.join(news_list))


async def last_five_news(update, context):
    news_list = [news.title + '\n' + news.content + '\n' + f'Автор - {news.user.name}' + '\n' for news in
                 db_sess.query(News).all()][-5:]
    await update.message.reply_text('Последние объявления на сайте:' + '\n\n' + '\n'.join(news_list))


async def keyboard(update, context):
    await update.message.reply_text(
        "Перед вами все доступные на данный момент команды",
        reply_markup=markup
    )


async def close_keyboard(update, context):
    await update.message.reply_text(
        "Команды скрыты",
        reply_markup=ReplyKeyboardRemove()
    )


def main():
    application = Application.builder().token('Paste your token here').build()

    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, reaction_to_messages)

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("users", users))
    application.add_handler(CommandHandler("news", news))
    application.add_handler(CommandHandler("last_news", last_five_news))
    application.add_handler(CommandHandler("keyboard", keyboard))
    application.add_handler(CommandHandler("exit", close_keyboard))
    application.add_handler(text_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
