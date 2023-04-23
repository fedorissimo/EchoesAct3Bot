# Импортируем необходимые классы.
import logging
import datetime
from telegram.ext import Application, MessageHandler, filters, CommandHandler, CallbackContext, ChatMemberHandler, \
    Updater
from telegram import Chat, Bot
import sqlite3
from random import randint
from youdotcom import Chat

# Импорт библиотек

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
            '/youchat;/yc - Запрос для нейросети, аналога ChatGPT\n'
            '/stats - Выводит статистику сообщений\n'
            '/help - Выводит информацию о боте'
            '/stand_desc - Ввести описание стенда')

with open('token.txt', 'r') as tokenstr:
    tokenread = tokenstr.readline()
    if tokenread != 'TOKEN' and tokenread != '':
        BOT_TOKEN = tokenread
    else:
        logging.fatal('Введите свой токен в файл token.txt')
BADWORDS = ["дебил", "лох", "дура", "лохушка"]
# Константы
bot = Bot(BOT_TOKEN)


# Функция для проверки наличия стенда
def check_stand(user, wherefrom):
    conn = sqlite3.connect('tgusers.db')
    cursor = conn.cursor()
    cursor.execute('SELECT stand FROM everything WHERE user_id = ?', (str(user),))
    isstand = cursor.fetchone()
    if isstand is not None and isstand[0] != '' and isstand[0] is not None:
        return 1
    else:
        if wherefrom == 'start':
            cursor.execute('UPDATE everything SET stand = (?) WHERE user_id=?', ('NO_STAND', str(user),))
            conn.commit()
        elif wherefrom == 'mystand':
            return 2


async def echo(update, context):
    # Приветствие новых пользователей
    if update.message.new_chat_members:
        for new_member in update.message.new_chat_members:
            await update.message.reply_text('Приветствую!')
    # Часть Егора (обнаружение ругательств)
    try:
        for i in BADWORDS:
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
    cursor.execute('SELECT messages FROM everything WHERE user_id = ?', (str(user),))
    messagenum = cursor.fetchone()
    # Добавление нового пользователя в БД, проверка кол-ва сообщений
    if not messagenum:
        messagenum = '0'
        cursor.execute('INSERT INTO everything (user_id, user_name, messages) VALUES (?, ?, ?)',
                       (str(user), update.message.from_user.first_name, messagenum))
        await update.message.reply_text('Привет!')
    else:
        cursor.execute('UPDATE everything SET messages = (?) WHERE user_id=?',
                       (str(int(messagenum[0]) + 1), str(user),))
    conn.commit()
    # Просто функция эхо-бота
    if 'эхо' in update.message.text:
        await update.message.reply_text('Я получил сообщение ' + update.message.text[4:])
    # Обнаружение рикролла
    if update.message.text in RICKROLLS:
        await update.message.reply_text('Обнаружен рикролл')


# Напишем соответствующие функции.
# Их сигнатура и поведение аналогичны обработчикам текстовых сообщений.
async def start(update, context):
    """Отправляет сообщение когда получена команда /start"""
    conn = sqlite3.connect('tgusers.db')
    cursor = conn.cursor()
    user = update.message.from_user.id
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    cursor.execute('SELECT stand FROM everything WHERE user_id = ?', (str(user),))
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
    cursor.execute('SELECT * FROM everything WHERE user_id = ?', (str(user),))
    checker = check_stand(user, 'mystand')
    # Проверка, есть ли у пользователя стенд
    if checker == 1:
        await update.message.reply_text('Нельзя иметь более одного стенда')
    else:
        # Тут получение id, имени и стенда
        cursor.execute('UPDATE everything SET stand = (?) WHERE user_id=?', (' '.join(newstand), str(user),))
        conn.commit()
        cursor.execute('SELECT * FROM everything')
        await update.message.reply_text(f'Твой стенд - {" ".join(context.args)}\n')
        await update.message.reply_text('Вы описать свой стенд командой /stand_desc')


async def stats(update, context):
    """Выводит статистику"""
    # Вывод кол-ва отправленных пользователем сообщений
    conn = sqlite3.connect('tgusers.db')
    cursor = conn.cursor()
    user = update.message.from_user.id
    cursor.execute('SELECT * FROM everything WHERE user_id = ?', (str(user),))
    messagenum = cursor.fetchall()[0][-1]
    await update.message.reply_text(f'Кол-во отправленных сообщений: {messagenum}')


async def randomnum(update, context):
    """Выводит рандомное число"""
    randnum = randint(int(context.args[0]), int(context.args[1]))
    await update.message.reply_text(randnum)


async def youchat(update, context):
    """Чат-бот"""
    # Запрос нейросети и вывод ответа в чат
    msg = context.args
    chat = Chat.send_message(message=msg, api_key="HYKVVNYMTOU6N0C7BABLBHD3GSYRBA7J5MZ")
    await update.message.reply_text(chat['message'])


async def help_command(update, context):
    """Выводит список команд"""
    await update.message.reply_text(HELPLINE)


async def st_desc(update, context):
    """Позволяет описать свой стенд"""
    desc = context.args
    conn = sqlite3.connect('tgusers.db')
    cursor = conn.cursor()
    # Добавление описания в БД
    user = update.message.from_user.id
    cursor.execute('UPDATE everything SET stand_desc = (?) WHERE user_id=?', (' '.join(desc), str(user),))
    conn.commit()
    await update.message.reply_text('Описание применено')


def main():
    # Создаём объект Application.
    application = Application.builder().token(BOT_TOKEN).build()

    text_handler = MessageHandler(filters.TEXT, echo)

    # Команды
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
    # Регистрируем обработчик в приложении.
    application.add_handler(text_handler)

    # Запуск приложения
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
