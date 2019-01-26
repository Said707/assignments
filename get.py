import telebot
from telebot import types
import json
import time
TOKEN = '699336375:AAE_mVS5z5fXQvNzVH3ISWxoXXWvTYpnJas'
#TOKEN = '790147863:AAEDQrQFd5s2Ds1PQPWdb5ZHiqOOGMBOT2A'
selectedGroup = [] # todo: save these in a file,
registerUserStep = {}  # so they won't reset every time the bot restarts
uploadFileStep = {} # being able to upload file
adminStep = {} # steps for teacher action
user_info = {} # for registration process

def sort_key(dic):
    return dic["full_name"]

with open("users.json", 'r') as f:
        dt = json.load(f)
        # is a LIST
dt.sort(key = sort_key)
with open("admins.json", 'r') as f:
        admins = json.load(f)
          # is a LIST


# KEYBOARD BUTTONS
startSelect = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2,one_time_keyboard=True)  # create selection keyboard
startSelect.add("Talaba", "O'qituvchi")

typeSelect = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=3,one_time_keyboard=True)  # create selection keyboard
typeSelect.add('Mustaqil ish', 'Laboratoriya ish', 'Amaliy ish')

group_message = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=4,one_time_keyboard=True)  # create selection keyboard
group_message.add("310-17", "311-17","312-17","313-17","314-17","315-17","316-17","317-17")
group_message.add("Barcha")

groupSelect = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=4,one_time_keyboard=True)  # create selection keyboard
groupSelect.add("310-17", "311-17","312-17","313-17","314-17","315-17","316-17","317-17")

hideBoard = types.ReplyKeyboardRemove()  # if sent as reply_markup, will hide the keyboard

with open("files.json", 'r') as f:
        documents = json.load(f) 
        # is DICTIONARY

commands = {  # command description used in the "help" command
    'start'       : 'Botni ishga tushirish',
    'upload'      : 'Fayl yuklash',
    'help'        : 'Mavjud komandalar bilan tanishish'
}
commands_admin = {  # command description for admin
    'send_message': 'Obunachilarga xabar yozish',
    'get_files'   : 'Fayllarni olish',
    'help'        : 'Mavjud komandalar bilan tanishish'
}
# STEP DEFINERS
def get_reg_step(uid):
    if uid in registerUserStep:
        return registerUserStep[uid]
    else:
        registerUserStep[uid] = 0
        return 0

def get_upload_step(uid):
    if uid in uploadFileStep:
        return uploadFileStep[uid]
    else:
        uploadFileStep[uid] = 0
        return 0
# ADMIN STAFF
def get_admin_step(uid):
    if uid in adminStep:
        return adminStep[uid]
    else:
        adminStep[uid] = 0
        return 0

def check_if_admin(uid):
    if uid in admins:
        return True
    else:
        return False



def check_if_not_exist(uid):
    with open("users.json", 'r') as f:
        data = json.load(f)
    for chid in data:
        if chid["id"] == uid or chid["group"] == uid:
            return False
    return True

def listener(messages):
# When new messages arrive TeleBot will call this function.
   for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            print(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)

# register listener          
bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener) 

# handle the "/start" command
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if check_if_admin(cid):
        command_help(m)
    elif check_if_not_exist(cid):
        bot.send_message(cid,"Salom hurmatli foydalanuvchi, o'zingizni tanishtiring!",reply_markup=startSelect)
        registerUserStep[cid] = 1
    else:
        bot.send_message(cid, "Hurmatli talaba! Siz haqingizdagi ma'lumot bazada oldindan mavjud!\nFayl yuklash uchun /upload komandasini bosing!")
        registerUserStep[cid] = 4 # user can upload files
        uploadFileStep[cid] = 0 # user can choose what type of file can upload
# STUDENT ? TEACHER ?
@bot.message_handler(func=lambda message: get_reg_step(message.chat.id) == 1)
def register_step_zero(m):
    cid = m.chat.id
    text = m.text
    bot.send_chat_action(cid, 'typing')
    if text == "Talaba":
        if check_if_not_exist(cid): 
            registerUserStep[cid] = 2 # user is a student
            bot.send_message(cid, "Salom!\nGuruh raqamingizni kiriting!\n(Masalan: 314-17)", reply_markup=hideBoard)
        else:
            bot.send_message(cid, "Siz haqingizdagi ma'lumot bazada oldindan mavjud!\nFayl yuklash uchun /upload komandasini bosing!")
            registerUserStep[cid] = 4 # user can upload files
            uploadFileStep[cid] = 0 # user can choose what type of file can upload
    elif text == "O'qituvchi":
        bot.send_message(cid,"Parolni kiriting!", reply_markup=hideBoard)
        registerUserStep[cid] = 100  # reset the users uploading step back to 0
        adminStep[cid] = 1
    
    else:
        bot.send_message(cid, "Sizga taqdim qilingan knopkalardan foydalaning, iltimos!")
        bot.send_message(cid, "Qayta urinib ko'ring!")

#registration process
@bot.message_handler(func=lambda message: get_reg_step(message.chat.id) == 2)
def register_step_one(m):
    cid = m.chat.id
    user_info["id"] =  cid
    user_info["group"] =  m.text
    bot.send_message(cid,"Yaxshi. Endi to'liq familiya ismingizni kiriting!\n(Masalan: Anvarov Doston)")
    registerUserStep[cid] = 3 # almost final step of reg

@bot.message_handler(func=lambda message: get_reg_step(message.chat.id) == 3)
def register_step_two(m):
    cid = m.chat.id
    global user_info
    user_info["full_name"] = m.text
    dt.append(user_info)
    print(user_info)
    user_info = {}
    print("\n")
    print(user_info)
    dt.sort(key = sort_key)
    with open("users.json", 'w') as wf:
        json.dump(dt, wf, indent=4)     # student has been registered and data saved
    bot.send_message(cid,"Ma'lumotlaringiz muvofaqqiyatli kiritildi!\nFayl yuklash uchun /upload komandasini bosing!")
    registerUserStep[cid] = 4 # user can upload files
    uploadFileStep[cid] = 0 # user can choose what type of file can upload

@bot.message_handler(commands=['upload'], func=lambda message: get_reg_step(message.chat.id) == 4 and get_upload_step(message.chat.id) == 0 or not check_if_not_exist(message.chat.id))
def command_upload(m):
    cid = m.chat.id
    bot.send_message(cid, "Qanday turdagi fayl yuklamoqchisiz?", reply_markup=typeSelect) # show the keyboard # mustaqil ish, laboratoriya, amaliy
    uploadFileStep[cid] = 1 # user can have chosen which type of doc to send 

@bot.message_handler(func=lambda message: get_upload_step(message.chat.id) == 1)
def msg_type_of_file_select(m):
    cid = m.chat.id
    text = m.text
    guide = f"Hurmatli foydalanuvchi!\n{text}ingiz nomi quyidagi ketma-ketlikda bo'lishi lozim!\
    \nMasalan: Anvarov Doston 314-17"
    warning = f"\nAks holda ma'lumot almashishda ayrim xatoliklar ro'y berishi mumkin."
    formats = " (.doc, .docs, .pdf)"
    # for some reason the 'upload_photo' status isn't quite working (doesn't show at all)
    bot.send_chat_action(cid, 'typing')
    if text == "Mustaqil ish":
        bot.send_message(cid,guide+" 1-M"+formats+warning,reply_markup=hideBoard)
        uploadFileStep[cid] = 2  # reset the users uploading step back to 0
    elif text == "Laboratoriya ish":
        bot.send_message(cid,guide+" 1-L"+formats+warning,reply_markup=hideBoard)
        uploadFileStep[cid] = 2  # reset the users uploading step back to 0
    elif text == "Amaliy ish":
        bot.send_message(cid,guide+" 1-A"+formats+warning,reply_markup=hideBoard)
        uploadFileStep[cid] = 2  # reset the users uploading step back to 0
    else:
        bot.send_message(cid, "Sizga taqdim qilingan knopkalardan foydalaning, iltimos!")
        bot.send_message(cid, "Qayta urinib ko'ring!")


# help page
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    if check_if_admin(cid):
        help_text = "Hurmatli o'qituvchi!\nSiz uchun quyidagi komandalar mavjud: \n"
        for key in commands_admin:  # generate help text out of the commands dictionary defined at the top
            help_text += "/" + key + ": "
            help_text += commands_admin[key] + "\n"
    else:
        help_text = "Hurmatli talaba!\nSiz uchun quyidagi komandalar mavjud: \n"
        for key in commands:  # generate help text out of the commands dictionary defined at the top
            help_text += "/" + key + ": "
            help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  # send the generated help page














works = types.InlineKeyboardMarkup(row_width=5)
mi1 = types.InlineKeyboardButton(text='1-MI📑',callback_data='1-M')
mi2 = types.InlineKeyboardButton(text='2-MI📑',callback_data='2-M')

lb1 = types.InlineKeyboardButton(text='1-LB📝',callback_data='1-L')
lb2 = types.InlineKeyboardButton(text='2-LB📝',callback_data='2-L')
lb3 = types.InlineKeyboardButton(text='3-LB📝',callback_data='3-L')
lb4 = types.InlineKeyboardButton(text='4-LB📝',callback_data='4-L')

ai1 = types.InlineKeyboardButton(text='1-AI👨‍💻',callback_data='1-A')
ai2 = types.InlineKeyboardButton(text='2-AI👨‍💻',callback_data='2-A')
ai3 = types.InlineKeyboardButton(text='3-AI👨‍💻',callback_data='3-A')
ai4 = types.InlineKeyboardButton(text='4-AI👨‍💻',callback_data='4-A')
works.add(mi1,mi2,lb1,lb2,lb3,lb4,ai1,ai2,ai3,ai4)

# ADMIN -- TEACHER STAFF
@bot.message_handler(func=lambda message: get_admin_step(message.chat.id) == 1)
def verification(m):
    cid = m.chat.id
    text = m.text
    strong_password = 'J25sp982tT9;6rM'
    if text == strong_password:
        if not check_if_admin(cid):
            admins.append(cid)
            with open("admins.json", 'w') as wf:
                json.dump(admins, wf, indent=4) 
        bot.send_message(cid, "Parol mos tushdi!")
        command_help(m)
        adminStep[cid] = 2
    else:
        adminStep[cid] = 0
        bot.send_message(cid, "Parol noto'g'ri!")
        command_start(m)


@bot.message_handler(func=lambda message: check_if_admin(message.chat.id) ,commands=['send_message'])
def command_send_message(m):
    cid = m.chat.id
    bot.send_message(cid, "Qaysi guruh talabalariga xabar yozmoqchisiz?", reply_markup=group_message)
    adminStep[cid] = 3 # send message command is selected


@bot.message_handler(func=lambda message: check_if_admin(message.chat.id) and adminStep[message.chat.id] == 3)
def send_gruop_message(m):
    cid = m.chat.id
    text = m.text
    bot.send_chat_action(cid, 'typing')
    if text == "Barcha" or not check_if_not_exist(text) :
        bot.send_message(cid,f"Demak, {text}ga yubormoqchi bo'lgan xabaringizni kiriting!",reply_markup=hideBoard)
        selectedGroup.append(text)
        adminStep[cid] = 4  
    elif check_if_not_exist(cid):
        bot.send_message(cid, "Ushbu guruh talabalaridan hech kim hali ro'yhatdan o'tmagan!")
    else:
        bot.send_message(cid, "Sizga taqdim qilingan knopkalardan foydalaning, iltimos!")
        bot.send_message(cid, "Qayta urinib ko'ring!")
 
@bot.message_handler(func=lambda message: check_if_admin(message.chat.id) and adminStep[message.chat.id] == 4)
def send_gruop_text(m):
    cid = m.chat.id
    text = m.text
    
    try:
        group_num = selectedGroup[-1]
    except:
        return command_help(m)

    if group_num != "Barcha":
        for each_user in dt:
            if each_user["group"] == group_num:
                bot.send_message(each_user["id"], "ADMIN:\n"+text)
    else:
        for each_user in dt:
            bot.send_message(each_user["id"], "ADMIN:\n"+text)

    bot.send_message(cid, "Xabar jo'natildi!")
    adminStep[cid] = 2


@bot.message_handler(func=lambda message: check_if_admin(message.chat.id), commands=['get_files'])
def command_get_files(m):
    cid = m.chat.id
    bot.send_message(cid, "Guruhni tanlang!", reply_markup=groupSelect)
    adminStep[cid] = 5 # get files command is selected

@bot.message_handler(func=lambda message: check_if_admin(message.chat.id) and adminStep[message.chat.id] == 5)
def get_files_gruop(m):
    cid = m.chat.id
    group_num = m.text
    bot.send_chat_action(cid, 'typing')
    if not check_if_not_exist(group_num) :
        list_of_students = f"{group_num}-guruhdan quyidagi talabalar ro'yhatdan o'tganlar:\n"
        i=1
        for each_user in dt:
            if each_user["group"] == group_num:
                list_of_students += str(i)+ "." + each_user["full_name"] + "\n"
                i+=1
        bot.send_message(cid, list_of_students,reply_markup=hideBoard)
        bot.send_message(cid, "Qaysi ishni olmoqchisiz?",reply_markup=works)
        selectedGroup.append(group_num)
        adminStep[cid] = 6  
    elif check_if_not_exist(cid):
        bot.send_message(cid, "Ushbu guruh talabalaridan hech kim hali ro'yhatdan o'tmagan!")
    else:
        bot.send_message(cid, "Sizga taqdim qilingan knopkalardan foydalaning, iltimos!")
        bot.send_message(cid, "Qayta urinib ko'ring!")



@bot.callback_query_handler(func=lambda call: True and check_if_admin(call.message.chat.id) and adminStep[call.message.chat.id] == 6)
def  inline_callback(call):
    cid = call.message.chat.id
    try:
        group_num = selectedGroup[-1]
    except:
        return command_help(m)
    check = True
    callback = call.data
    for file in documents:
        if file.__contains__(group_num):
            if file.__contains__(callback):
                bot.send_document(cid, documents[file])
                check = False
    if check:
        bot.send_message(cid, "Hozirchi fayllar yuklanmagan!")
    else:
        bot.send_message(cid,"------------------------------------------------------------------------------")
    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=callback)       
    








@bot.message_handler(func=lambda message: message.text == "0")
def bug(m):
    c = 780193419
    
    bot.send_message(c, "Hey")
    bot.send_message(c, "Said")

# filter on a specific message	
@bot.message_handler(func=lambda message: message.text == "hi")
def homeworks(m):
    for file in documents:
        if file.__contains__("1-M"):
            bot.send_document(m.chat.id, documents[file])

# default handler for every other text		
@bot.message_handler(content_types=['text'])
def print_message(m):
    cid = m.chat.id
    text = m.text
    if text in commands or text in commands_admin:
        command_help(m)
    bot.send_message(cid, "? \n/help")


@bot.message_handler(content_types=['document'])
def print_document(message):
    cid = message.chat.id
    if get_upload_step(cid) != 2:
        bot.send_message(cid, "Avval fayl turini tanlang!\n/upload")
        return 0
    file_id = message.document.file_id
    file_name = message.document.file_name
    print(file_name)
    documents[file_name] = file_id
    with open("files.json","w") as wf:
        json.dump(documents, wf, indent=4)
    bot.send_message(cid, "Yuklandi!")
    uploadFileStep[cid] = 0



#bot.polling(timeout=15)
def telegram_polling():
    try:
        bot.polling(none_stop=True, timeout=60) #constantly get messages from Telegram
    except:
        bot.stop_polling()
        time.sleep(10)
        telegram_polling()

if __name__ == '__main__':    
    telegram_polling()

