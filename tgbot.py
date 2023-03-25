# Импортируем необходимые классы.
import logging
import datetime
from telegram.ext import Application, MessageHandler, filters, CommandHandler


# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)
dt_now = datetime.datetime.now()


# Определяем функцию-обработчик сообщений.
# У неё два параметра, updater, принявший сообщение и контекст - дополнительная информация о сообщении.
async def echo(update, context):
    # У объекта класса Updater есть поле message,
    # являющееся объектом сообщения.
    # У message есть поле text, содержащее текст полученного сообщения,
    # а также метод reply_text(str),
    # отсылающий ответ пользователю, от которого получено сообщение.
    await update.message.reply_text('Я получил сообщение ' + update.message.text)


# Напишем соответствующие функции.
# Их сигнатура и поведение аналогичны обработчикам текстовых сообщений.
async def start(update, context):
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user
    await update.message.reply_html(
        rf"Оно работает!",
    )


async def help_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text("Стенд не может помогать будучи телеграм-ботом...")


async def printdate(update, context):
    """Отправляет сообщение когда получена команда /date"""
    dt_today = datetime.date.today()
    await update.message.reply_text(str(dt_today))


async def printtime(update, context):
    """Отправляет сообщение когда получена команда /time"""
    dt_now = datetime.datetime.now().time()
    await update.message.reply_text(str(dt_now))


def main():
    # Создаём объект Application.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    application = Application.builder().token('5896234992:AAE_TiFFUIV0HUouxrLxaPLfJo8EWxDYZEQ').build()

    # Создаём обработчик сообщений типа filters.TEXT
    # из описанной выше асинхронной функции echo()
    # После регистрации обработчика в приложении
    # эта асинхронная функция будет вызываться при получении сообщения
    # с типом "текст", т. е. текстовых сообщений.
    text_handler = MessageHandler(filters.TEXT, echo)
    # Зарегистрируем их в приложении перед
    # регистрацией обработчика текстовых сообщений.
    # Первым параметром конструктора CommandHandler я
    # вляется название команды.
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("date", printdate))
    application.add_handler(CommandHandler("time", printtime))
    # Регистрируем обработчик в приложении.
    application.add_handler(text_handler)

    # Запускаем приложение.
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
