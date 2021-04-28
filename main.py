from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
from filmobot_token import TOKEN
from random import randint
from telegram import ReplyKeyboardMarkup
import datetime
import sqlite3

global LOG_IN
LOG_IN = False
global NAME
global AGE



global GANRE
global REITING


def init(update, context):
    update.message.reply_text(F"""Здравствуйте, я Filmobot. Я помогу Вам подобрать 
фильм, сериал или мультфильм на Ваш вкус. 
Как я могу к Вам обращаться?""")
    return 1


def get_name(update, context):
    global NAME
    NAME = update.message.text
    update.message.reply_text(f'''Приятно познакомиться, {NAME}, 
Укажите пожалуйста Ваш возраст, чтобы я мог подобрать контент соответствующий 
Вашему возрасту и который будет Вам интересен.''')
    return 2


def stop(update, context):
    update.message.reply_text('/choose_film')
    return ConversationHandler.END


def log_out(update, context):
    global LOG_IN
    LOG_IN = False
    update.message.reply_text('Спасибо. Приходите еще.')


def get_age(update, context):
    global AGE
    AGE = update.message.text
    if AGE.isdigit():
        if int(AGE) < 0:
            update.message.reply_text('Вы еще не родились, попробуйте еще раз')
            return 2
        if int(AGE) > 150:
            update.message.reply_text('В таком возрасте смотреть фильмы вредно, введите свой возраст.')
            return 2
        update.message.reply_text('''Введите пароль для своего аккаунта.
Пароль должен содержать цифры, буквы латинского авфавита, как заглавные, так и прописные''')
        return 3
    update.message.reply_text('Введите свой возраст арабскими цифрами')
    return 2


def get_password(update, context):
    global password
    global LOG_IN
    global AGE
    global NAME
    password = update.message.text
    alpha = 'qwertyuiopasdfghjklzxcvbnmйцукенгшщзхъфывапролджэячсмитьбю'
    ALPHA = 'QWERTYUIOPASDFGHJKLZXCVBNNMЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ'
    digit = '1234567890'
    alpha_OK = False
    ALPHA_OK = False
    digit_OK = False
    for i in password:
        if i in alpha:
            alpha_OK = True
        if i in ALPHA:
            ALPHA_OK = True
        if i in digit:
            digit_OK = True
    if alpha_OK and ALPHA_OK and digit:
        try:
            con = sqlite3.connect(".\\Filmobot_users.sqlite")
            cur = con.cursor()
            sql = '''insert into Filmobot_users (User_name, User_age, User_password) values (?, ?, ?)'''

            cur.execute(sql, (NAME, AGE, password))
            con.commit()
            cur.close()
            con.close()
            update.message.reply_text(
                'Добро пожаловать. Теперь пройдите опрос, чтобы понять какие фильмы Вам интересны. /choose_film')
            print(NAME)
            print(AGE)
            LOG_IN = True
            return ConversationHandler.END
        except:
            update.message.reply_text(
                'Пользователь с таким именем или паролем уже существует. Попробуйте еще раз, /start')
            return ConversationHandler.END
    if not alpha_OK:
        update.message.reply_text('Нет букв в нижнем регистре')
    elif not ALPHA_OK:
        update.message.reply_text('Нет букв в вверхнем регистре')
    elif not digit_OK:
        update.message.reply_text('Нет цифр')
    return 3


def log_in(update, context):
    update.message.reply_text('Введите имя под которым Вы регитстрировались')
    return 1


def check_base(update, context):
    global NAME
    con = sqlite3.connect(".\\Filmobot_users.sqlite")
    cur = con.cursor()
    cur.execute("SELECT Id FROM Filmobot_users WHERE User_name=?", (update.message.text,))
    NAME = update.message.text
    rows = cur.fetchall()
    if len(rows) == 1:
        update.message.reply_text("Введите пароль")
        return 2
    elif len(rows) == 0:
        update.message.reply_text(
            "Вы ввели неправильный логин или такого пользователя не существует, попробуйте еще раз, /start")
        return ConversationHandler.END


def is_in_base(update, context):
    global LOG_IN
    LOG_IN = False
    reply_keyboard = [['/yes'],
                      ['/no'],
                      ['/stop']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        "Вы уже зарегестрированы здесь?",
        reply_markup=markup)


def check_password(update, context):
    global LOG_IN
    global AGE
    global NAME
    con = sqlite3.connect(".\\Filmobot_users.sqlite")
    cur = con.cursor()
    cur.execute("SELECT User_password FROM Filmobot_users WHERE User_name=?", (NAME,))

    rows = cur.fetchall()
    print(rows)
    if len(rows) == 1:
        if update.message.text == rows[0][0]:
            update.message.reply_text(
                "Вход выполнен! Теперь пройдите опрос, чтобы понять какие фильмы Вам интересны. /choose_film")
            cur = cur.execute("SELECT User_age FROM Filmobot_users WHERE User_name=?", (NAME,))
            AGE = int(str(cur.fetchall()[0])[1:3])
            print(AGE)
            LOG_IN = True
            return ConversationHandler.END
        else:
            update.message.reply_text('Вы ввели неправильный пароль, /start')
            return  ConversationHandler.END
    elif len(rows) == 0:
        update.message.reply_text("Такого пароля не существует, попробуйте еще раз. /start")
        return ConversationHandler.END


def ask_ganre(update, context):
    print(1)
    if not LOG_IN:
        update.message.reply_text('Вы не вошли в систему /start')
        return
    reply_keyboard = [['/Horror'],
                      ['/Dram'],
                      ['/Melodram'],
                      ['/Comedy'],
                      ['/Thriller'],
                      ['/Stop'],
                      ['/Logout']]

    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    update.message.reply_text(
        "Какой жанр вам интересен?",
        reply_markup=markup)


def comedy(update, context):
    global GANRE
    GANRE = 'Комедия'
    if not LOG_IN:
        update.message.reply_text('Вы не вошли в систему /start')
        return ConversationHandler.END
    con = sqlite3.connect(".\\Filmobot_users.sqlite")
    cur = con.cursor()
    G = 'Комедия'
    cur.execute("SELECT Film_name FROM Films WHERE Film_ganre=?", (G,))

    rows = cur.fetchall()
    for i in range(len(rows)):
        rows[i] = rows[i][0]
    print(rows)
    update.message.reply_text(
        'Вот список фильмов. ' + ', '.join(rows) + '. Напишите название понравившегося фильма, чтобы узнать больше.')
    return 1


def horror(update, context):
    global GANRE
    GANRE = 'Ужасы'
    if not LOG_IN:
        update.message.reply_text('Вы не вошли в систему /start')
        return ConversationHandler.END
    con = sqlite3.connect(".\\Filmobot_users.sqlite")
    cur = con.cursor()
    G = 'Ужасы'
    cur.execute("SELECT Film_name FROM Films WHERE Film_ganre=?", (G,))

    rows = cur.fetchall()
    for i in range(len(rows)):
        rows[i] = rows[i][0]
    print(rows)
    update.message.reply_text(
        'Вот список фильмов. ' + ', '.join(rows) + '. Напишите название понравившегося фильма, чтобы узнать больше.')
    return 1


def dram(update, context):
    global GANRE
    GANRE = 'Драма'
    if not LOG_IN:
        update.message.reply_text('Вы не вошли в систему /start')
        return ConversationHandler.END
    con = sqlite3.connect(".\\Filmobot_users.sqlite")
    cur = con.cursor()
    G = 'Драма'
    cur.execute("SELECT Film_name FROM Films WHERE Film_ganre=?", (G,))

    rows = cur.fetchall()
    for i in range(len(rows)):
        rows[i] = str(rows[i][0])
    print(rows)
    update.message.reply_text(
        'Вот список фильмов. ' + ', '.join(rows) + '. Напишите название понравившегося фильма, чтобы узнать больше.')
    return 1


def print_login(update, context):
    global LOG_IN
    print(LOG_IN)


def melodram(update, context):
    global GANRE
    GANRE = 'Мелодрама'
    if not LOG_IN:
        update.message.reply_text('Вы не вошли в систему /start')
        return ConversationHandler.END
    con = sqlite3.connect(".\\Filmobot_users.sqlite")
    cur = con.cursor()
    cur.execute("SELECT Film_name FROM Films WHERE Film_ganre=?", (GANRE,))

    rows = cur.fetchall()
    for i in range(len(rows)):
        rows[i] = str(rows[i][0])
    print(rows)
    update.message.reply_text(
        'Вот список фильмов. ' + ', '.join(rows) + '. Напишите название понравившегося фильма, чтобы узнать больше.')
    return 1


def print_login(update, context):
    global LOG_IN
    print(LOG_IN)


def thriller(update, context):
    global GANRE
    GANRE = 'Боевик'
    if not LOG_IN:
        update.message.reply_text('Вы не вошли в систему /start')
        return ConversationHandler.END
    con = sqlite3.connect(".\\Filmobot_users.sqlite")
    cur = con.cursor()
    cur.execute("SELECT Film_name FROM Films WHERE Film_ganre=?", (GANRE,))

    rows = cur.fetchall()
    for i in range(len(rows)):
        rows[i] = str(rows[i][0])
    print(rows)
    update.message.reply_text(
        'Вот список фильмов. ' + ', '.join(rows) + '. Напишите название понравившегося фильма, чтобы узнать больше.')
    return 1


def print_login(update, context):
    global LOG_IN
    print(LOG_IN)


def send_treller(update, context):
    global AGE
    global GANRE
    if not LOG_IN:
        update.message.reply_text('Вы не вошли в систему /start')
        return ConversationHandler.END

    con = sqlite3.connect(".\\Filmobot_users.sqlite")
    cur = con.cursor()
    G = update.message.text
    if G in ['/Horror', '/Dram', '/Melodram', '/Comedy', '/Thriller', '/Logout']:
        update.message.reply_text('Если Вы хотите выбрать другой жанр нажмите /stop')
        return 1
    cur.execute("SELECT Tiser FROM Films WHERE Film_name=?", (G,))

    rows = cur.fetchall()
    for i in range(len(rows)):
        rows[i] = str(rows[i][0])
    # print(rows)
    if len(rows) == 0:
        update.message.reply_text(
            'Вы выбрали фильм которого нет в базе. Напишите название так же как в списке выше или выберете фильм от туда')
        return 1

    cur.execute("SELECT Tiser FROM Films WHERE Film_name=? AND Age_restriction<=?", (G, AGE,))

    rows = cur.fetchall()
    for i in range(len(rows)):
        rows[i] = str(rows[i][0])
    print(rows)
    if len(rows) == 0:
        update.message.reply_text('Вы слишком малы для таких фильмов. /choose_film')
        return ConversationHandler.END
    cur.execute("SELECT Tiser FROM Films WHERE Film_name=?", (G,))

    rows = cur.fetchall()
    cur.execute("SELECT Reiting FROM Films WHERE Film_name=?", (G,))
    rows1 = cur.fetchall()
    for i in range(len(rows)):
        rows[i] = str(rows[i][0])
    for i in range(len(rows1)):
        rows1[i] = str(rows1[i][0])
    update.message.reply_text(rows[0] + ' Рейтинг этого фильма  ' + rows1[0] + ' /choose_film')
    return ConversationHandler.END


def main():
    updater = Updater(TOKEN, use_context=True)
    global GANRE
    global REITING
    global NAME
    global LOG_IN
    global AGE
    global password
    NAME = ''
    AGE = 0
    password = ''

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("login", print_login))
    dp.add_handler(CommandHandler("start", is_in_base))
    dp.add_handler(CommandHandler("Logout", log_out))
    dp.add_handler(CommandHandler("Stop", stop))

    yes = ConversationHandler(
        entry_points=[CommandHandler('yes', log_in)],
        states={
            1: [MessageHandler(Filters.text, check_base)],
            2: [MessageHandler(Filters.text, check_password)],
            3: [MessageHandler(Filters.text, stop)]
        },

        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(yes)

    no = ConversationHandler(
        entry_points=[CommandHandler('no', init)],
        states={
            1: [MessageHandler(Filters.text, get_name)],
            2: [MessageHandler(Filters.text, get_age)],
            3: [MessageHandler(Filters.text, get_password)],
            4: [MessageHandler(Filters.text, is_in_base)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(no)
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    dp.add_handler(CommandHandler('choose_film', ask_ganre))

    H = ConversationHandler(
        entry_points=[CommandHandler('Horror', horror)],
        states={
            1: [MessageHandler(Filters.text, send_treller)],
            2: [MessageHandler(Filters.text, stop)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(H)

    D = ConversationHandler(
        entry_points=[CommandHandler('Dram', dram)],
        states={
            1: [MessageHandler(Filters.text, send_treller)],
            2: [MessageHandler(Filters.text, stop)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(D)

    M = ConversationHandler(
        entry_points=[CommandHandler('Melodram', melodram)],
        states={
            1: [MessageHandler(Filters.text, send_treller)],
            2: [MessageHandler(Filters.text, stop)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(M)

    C = ConversationHandler(
        entry_points=[CommandHandler('Comedy', comedy)],
        states={
            1: [MessageHandler(Filters.text, send_treller)],
            2: [MessageHandler(Filters.text, stop)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(C)

    T = ConversationHandler(
        entry_points=[CommandHandler('Thriller', thriller)],
        states={
            1: [MessageHandler(Filters.text, send_treller)],
            2: [MessageHandler(Filters.text, stop)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(T)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()



