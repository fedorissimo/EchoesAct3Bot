# Импортируем необходимые классы.
import logging
import datetime
from telegram.ext import Application, MessageHandler, filters, CommandHandler, CallbackContext, ChatMemberHandler, \
    Updater
from telegram import Chat, Bot
import csv
import sqlite3
from random import randint
from youdotcom import Chat

# Импорт библиотек
BOT_TOKEN = ""
badwords = ["дебил", "лох", "дура", "лохушка"]
bot = Bot(BOT_TOKEN)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
# Логирование


RICKROLLS = ['https://www.youtube.com/watch?v=dQw4w9WgXcQ&pp=ygUO0YDQuNC60YDQvtC70Ls%3D',
             'https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley']
HELPLINE = ('Основные команды:\n'
            '/date - Вывести дату\n'
            '/time - Вывести время\n'
            '/mystand - Выбрать стенд (нужно ввести название стенда)\n'
            '/stands - Список стендов\n'
            '/random - Выводит случайное число (нужно ввести два числа через пробел)\n'
            '/youchat;/yc - Запрос для нейровсети, аналога ChatGPT\n'
            '/stats - Выводит статистику сообщений\n'
            '/help - Выводит информацию о боте')


# Константы
# Определяем функцию-обработчик сообщений.
# У неё два параметра, updater, принявший сообщение и контекст - дополнительная информация о сообщении.
def make_table(chat_id):
    conn = sqlite3.connect('tgusers.db')
    cursor = conn.cursor()
    print('test')
    print(chat_id)
    curstr = f'''CREATE TABLE {str(chat_id)[1:]}(product VARCHAR(20) PRIMARY KEY, count INTEGER, price INTEGER)'''
    cursor.execute(curstr)
    conn.commit()


def check_stand(user, wherefrom):
    conn = sqlite3.connect('tgusers.db')
    cursor = conn.cursor()
    cursor.execute('SELECT stand FROM everything WHERE user_id = ?', (user,))
    isstand = cursor.fetchone()
    if isstand is not None and isstand[0] != '':
        return 1
    else:
        if wherefrom == 'start':
            cursor.execute('UPDATE everything SET stand = (?) WHERE user_id=?', ('NO_STAND', user,))
            conn.commit()
        elif wherefrom == 'mystand':
            return 2


async def echo(update, context):
    # У объекта класса Updater есть поле message,
    # являющееся объектом сообщения.
    # У message есть поле text, содержащее текст полученного сообщения,
    # а также метод reply_text(str),
    # отсылающий ответ пользователю, от которого получено сообщение.
    # print(help_command(update.message.new_chat_members))
    # Тут должно быть определение новых пользователей, но оно не работает
    if update.message.new_chat_members:
        for new_member in update.message.new_chat_members:
            # Bot was added to a group chat
            # Another user joined the chat
            await update.message.reply_text('Приветствую!')
    try:
        for i in badwords:
            if i in update.message.text and update.message.chat_id != update.message.from_user.id:
                await bot.ban_chat_member(update.message.chat_id, update.message.from_user.id)
                break
            elif i in update.message.text and update.message.chat_id == update.message.from_user.id:
                    await update.message.reply_text('Не говорите мне плохие слова!')
                    break
    except Exception as e:
        await update.message.reply_text(
            'Дорогой владелец/админ, подумайте какой пример вы показываете, говоря плохие слова!')
    # Работа с базой данных
    conn = sqlite3.connect('tgusers.db')
    cursor = conn.cursor()
    user = update.message.from_user.id
    cursor.execute('SELECT * FROM everything WHERE user_id = ?', (user,))
    messagenum = cursor.fetchall()[0][-1]
    if messagenum is None:
        messagenum = '0'
    cursor.execute('UPDATE everything SET messages = (?) WHERE user_id=?', (str(int(messagenum) + 1), user,))
    conn.commit()
    # Просто функция эхо-бота
    if 'эхо' in update.message.text:
        await update.message.reply_text('Я получил сообщение ' + update.message.text[4:])
    # Never Gonna Give You Up
    if update.message.text in RICKROLLS:
        await update.message.reply_text('Обнаружен рикролл')


# Напишем соответствующие функции.
# Их сигнатура и поведение аналогичны обработчикам текстовых сообщений.
async def start(update, context):
    """Отправляет сообщение когда получена команда /start"""
    conn = sqlite3.connect('tgusers.db')
    cursor = conn.cursor()
    user = update.message.from_user.id
    chat_id = update.message.chat_id
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    # if chat_id != user and chat_id not in tables:
    #     make_table(chat_id)
    cursor.execute('SELECT stand FROM everything WHERE user_id = ?', (user,))
    isstand = cursor.fetchone()
    check_stand(user, 'start')
    await update.message.reply_text('Если вы это читаете, то бот даже работает)\n' + HELPLINE)


async def printdate(update, context):
    """Отправляет дату, когда получена команда /date"""
    dt_today = datetime.date.today()
    await update.message.reply_text(str(dt_today))


async def printtime(update, context):
    """Отправляет время, когда получена команда /time"""
    dt_now = datetime.datetime.now().time()
    await update.message.reply_text(str(dt_now))


async def stands(update, context):
    """Выводит список пользователей и их стендов"""
    # Стенды - способности пользователя (из JoJo)
    # Тут работа с БД
    conn = sqlite3.connect('tgusers.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM everything')
    users = cursor.fetchall()
    print(users)
    usersprint = ''
    # Показ всех стендов из БД
    for i in users:
        usersprint += f'{i}\n'
    await update.message.reply_text(usersprint)


async def mystand(update, context):
    """Позволяет выбрать стенд"""
    # Снова БД
    newstand = context.args
    user = update.message.from_user.id
    conn = sqlite3.connect('tgusers.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM everything WHERE user_id = ?', (user,))
    checker = check_stand(user, 'mystand')
    if checker == 1:
        await update.message.reply_text('Нельзя иметь более одного стенда')
    else:
        # Тут получение id, имени и стенда
        cursor.execute('INSERT INTO everything (user_id, user_name, stand) VALUES (?, ?, ?)',
                       (user, update.message.from_user.first_name, newstand[0]))
        conn.commit()
        cursor.execute('SELECT * FROM everything')
        await update.message.reply_text(f'Твой стенд - {" ".join(context.args)}\n')
        await update.message.reply_text('Вы описать свой стенд командой /st_desc')


async def stats(update, context):
    """Выводит статистику"""
    # вывод кол-ва отправленных пользователем сообщений
    conn = sqlite3.connect('tgusers.db')
    cursor = conn.cursor()
    user = update.message.from_user.id
    cursor.execute('SELECT * FROM everything WHERE user_id = ?', (user,))
    messagenum = cursor.fetchall()[0][-1]
    await update.message.reply_text(f'Кол-во отправленных сообщений: {messagenum}')


async def randomnum(update, context):
    """Выводит рандомное число"""
    # Тут и так понятно
    randnum = randint(int(context.args[0]), int(context.args[1]))
    await update.message.reply_text(randnum)


async def youchat(update, context):
    """Чат-бот"""
    # Запрос нейросети и вывод ответа в чат
    msg = context.args
    chat = Chat.send_message(message=msg, api_key="HYKVVNYMTOU6N0C7BABLBHD3GSYRBA7J5MZ")
    await update.message.reply_text(chat['message'])


async def newmember(update, context):
    """Чат-бот"""
    # Не работает
    await update.message.reply_text('Прив')


async def greet_chat_members(update, context):
    """Уведомляет об изменении числа участников группы"""
    await update.effective_chat.send_message(f'Изменилось число участников группы')


async def help_command(update, context):
    """Выводит список команд"""
    await update.message.reply_text(HELPLINE)


async def st_desc(update, context):
    """Позволяет описать свой стенд"""
    desc = context.args
    conn = sqlite3.connect('tgusers.db')
    cursor = conn.cursor()
    user = update.message.from_user.id
    cursor.execute('UPDATE everything SET stand_desc = (?) WHERE user_id=?', (' '.join(desc), user,))
    conn.commit()
    await update.message.reply_text('Описание применено')


def main():
    # Создаём объект Application.
    # Проверка токена из файла
    with open('token.txt', 'r') as tokenstr:
        tokenread = tokenstr.readline()
        if tokenread != 'TOKEN' and tokenread != '':
            application = Application.builder().token(tokenread).build()
        else:
            logging.fatal('Введите свой токен в файл token.txt')

    # Нет, я не забыл про ключ
    # Создаём обработчик сообщений типа filters.TEXT
    # из описанной выше асинхронной функции echo()
    # После регистрации обработчика в приложении
    # эта асинхронная функция будет вызываться при получении сообщения
    # с типом "текст", т. е. текстовых сообщений.
    text_handler = MessageHandler(filters.TEXT, echo)

    # Зарегистрируем их в приложении перед
    # регистрацией обработчика текстовых сообщений.
    # Первым параметром конструктора CommandHandler я вляется название команды.
    application.add_handler(ChatMemberHandler(greet_chat_members, ChatMemberHandler.CHAT_MEMBER))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("date", printdate))
    application.add_handler(CommandHandler("time", printtime))
    application.add_handler(CommandHandler("mystand", mystand))
    application.add_handler(CommandHandler("stands", stands))
    application.add_handler(CommandHandler("random", randomnum))
    application.add_handler(CommandHandler("youchat", youchat))
    application.add_handler(CommandHandler("yc", youchat))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("stand_desc", st_desc))
    # application.add_handler(CommandHandler("new_member", set_welcome))
    # Регистрируем обработчик в приложении.
    application.add_handler(text_handler)

    # Запускаем приложение.
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
