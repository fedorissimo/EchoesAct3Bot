# Импортируем необходимые классы.
import logging
import datetime
from telegram.ext import Application, MessageHandler, filters, CommandHandler, CallbackContext
import telegram
import csv
import sqlite3


# Запускаем логгирование
# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
# )
#
# logger = logging.getLogger(__name__)
dt_now = datetime.datetime.now()

name = 1
stand = 2


# Определяем функцию-обработчик сообщений.
# У неё два параметра, updater, принявший сообщение и контекст - дополнительная информация о сообщении.
async def echo(update, context):
    # У объекта класса Updater есть поле message,
    # являющееся объектом сообщения.
    # У message есть поле text, содержащее текст полученного сообщения,
    # а также метод reply_text(str),
    # отсылающий ответ пользователю, от которого получено сообщение.
    if 'эхо' in update.message.text:
        await update.message.reply_text('Я получил сообщение ' + update.message.text[4:])


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


async def stands(update, context):
    """Выводит список пользователей и их стендов"""
    # standlist = ''
    # with open('stands.csv', 'r') as f:
    #     csv_read = csv.reader(f, delimiter=',', lineterminator="\n")
    #     for i in csv_read:
    #         standlist += ' - '.join(i[1:3])
    #         standlist += '\n'
    conn = sqlite3.connect('tgusers.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM test')
    users = cursor.fetchall()
    print(users)
    usersprint = ''
    for i in users:
        usersprint += f'{i}\n'
    await update.message.reply_text(usersprint)


async def mystand(update, context):
    """Позволяет выбрать стенд"""
    msg = update.message.text
    newstand = msg[9:]
    # with open('stands.csv', 'r') as f:
    #     csv_read = csv.reader(f, delimiter=',', lineterminator="\n")
    #     if newstand not in csv_read and update.message.from_user.id not in csv_read:
    #         with open('stands.csv', 'a') as fw:
    #             csv_write = csv.writer(fw, delimiter=',', lineterminator="\n")
    #
    #             csv_write.writerow([update.message.from_user.id, update.message.from_user.first_name, newstand])
    conn = sqlite3.connect('tgusers.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO test (user_id, user_name, stand) VALUES (?, ?, ?)',
                   (update.message.from_user.id, update.message.from_user.first_name, newstand))
    conn.commit()
    cursor.execute('SELECT * FROM test')
    users = cursor.fetchall()
    print(users)
    print(msg)
    await update.message.reply_text(f'Твой стенд - {msg[9:]}')


async def stats(update, context):
    """Отправляет сообщение когда получена команда /time"""
    dt_now = datetime.datetime.now().time()
    await update.message.reply_text(str(dt_now))


def main():
    # Создаём объект Application.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    application = Application.builder().token('5896234992:AAHwqWZCwgXLfb-pSilve6BEZoy5C0-9Ta0').build()

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
    application.add_handler(CommandHandler("mystand", mystand))
    application.add_handler(CommandHandler("stands", stands))
    # application.add_handler(CommandHandler("new_member", set_welcome))
    # Регистрируем обработчик в приложении.
    application.add_handler(text_handler)

    # Запускаем приложение.
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
