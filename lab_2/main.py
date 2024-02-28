import telebot
import openpyxl

bot = telebot.TeleBot('6044597431:AAHKzsRoMb54EGZu9n-M7x13RlLA3OR6RrE')


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     "Привет! Я бот для учета посещаемости и баллов студентов. Чтобы начать, введите /help.")


# Обработчик команды /help
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "Список доступных команд: /start - старт бота /help - помощь "
                                      "/attendance - учет посещаемости и баллов")


# Обработчик команды /attendance
@bot.message_handler(commands=['attendance'])
def attendance(message):
    # Запрашиваем у пользователя ФИО и предмет
    bot.send_message(message.chat.id,
                     "Введите ФИО и предмет через запятую (например, Иванов Иван Иванович, Математика):")
    bot.register_next_step_handler(message, attendance_handler)


# Обработчик для получения ФИО и предмета от пользователя
def attendance_handler(message):
    # Разбиваем сообщение пользователя на ФИО и предмет
    try:
        fio, subject = message.text.split(',')
    except ValueError:
        bot.send_message(message.chat.id,
                         "Неверный формат ввода. Введите ФИО и предмет через запятую (например, Иванов Иван Иванович, "
                         "Математика):")
        return

    # Открываем файл Excel с данными по посещаемости
    try:
        workbook = openpyxl.load_workbook('Students.xlsx')
    except FileNotFoundError:
        bot.send_message(message.chat.id, "Файл с данными по посещаемости не найден.")
        return

    # Получаем лист с данными по посещаемости
    sheet = workbook.active
    # Ищем строку с данными по ФИО и предмету
    is_found = False
    for row in sheet.iter_rows():
        if row[0].value.strip() == fio.strip() and row[1].value.strip() == subject.strip():
            is_found = True
            bot.send_message(message.chat.id, fio + " " + subject + " посещаемость " + str(row[2].value) + " баллы " +
                             str(row[3].value))
            break
    if not is_found:
        bot.send_message(message.chat.id, "Студент не найден.")
    # Закрываем файл Excel
    workbook.close()


# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.send_message(message.chat.id, "Я не понимаю, что вы хотите сказать. Введите /help для списка команд.")


# Запускаем бота
bot.polling()