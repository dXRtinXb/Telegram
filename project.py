#!/usr/bin/python
from Api_id_key import *
import telebot
import logging
import time
import os
from DMLP import *
from DQL import *
from telebot.types import(
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButton,
)

products = get_product_data()

os.makedirs("photos", exist_ok=True)
os.makedirs("documents", exist_ok=True)

server = "my PC"
logging.basicConfig(
    filename="my_log.log",
    level=logging.INFO,
    format=f"%(asctime)s - %(name)s - {server} - %(levelname)s - %(message)s",
)

channel_id = -1002117867754
admins = [6771281659]
leader = 6771281659
API_TOKEN =API_key


def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        # print(m.forward_from_chat.id)
        if m.content_type == "text":
            # print the sent message to the console
            print(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)
            logging.info(
                str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text
            )
        elif m.content_type == "photo":
            print(
                str(m.chat.first_name) + " [" + str(m.chat.id) + "]: New photo recieved"
            )
            logging.info(
                str(m.chat.first_name)
                + " ["
                + str(m.chat.id)
                + "]: New photo recieved, file id: "
                + m.photo[-1].file_id
            )
        elif m.content_type == "document":
            print(
                str(m.chat.first_name)
                + " ["
                + str(m.chat.id)
                + "]: New document recieved"
            )
            logging.info(
                str(m.chat.first_name)
                + " ["
                + str(m.chat.id)
                + "]: New document recieved, file id: "
                + m.document.file_id
            )


bot = telebot.TeleBot(API_TOKEN, num_threads=20, skip_pending=True)
bot.set_update_listener(listener)


def send_message(*args, **kwargs):
    try:
        return telebot.util.antiflood(bot.send_message, *args, **kwargs)
    except Exception as e:
        pass


user_step = dict()  # {cid: step, ...}   ->  {1439019496: 1, ...}
user_info = dict()  # {cid: {'first_name': first name', 'last_name': last name}, ...}
KnownUsers = []  # [cid, ...]


def get_user_step(cid):
    if cid not in KnownUsers:
        KnownUsers.append(cid)
    return user_step.setdefault(cid, 0)
    # if cid in user_step:
    #     return user_step[cid]
    # else:
    #     user_step[cid] = 0
    #     return user_step[cid]


commands = {  # command description used in the "help" command
    "start": "Get used to the bot , you must do it first ",
    "help": "Gives you information about the available commands",
    "add_product": " tells you how to add a product for us" ,
    "show_me_ids": "shows you the firs ten ids as a key board markup for easyer work" , 
    "feedback" : "for more help and bugs"

}

                                                  # in out of order
admin_command = {                                                       
    'ALT_f4' : "all data base and informations will be restored" , 
    'names_&_ids' : 'the admin will see the names and ids of the customers'
}
def final_warning(cid):
    bot.send_message(cid , 'are you sure?')
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("YES")
    markup.add("NO")



def gen_markup(code, qty ):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("➖", callback_data=f"edit_{code}_{qty-1}"),
        InlineKeyboardButton(str(qty), callback_data=str(qty - 1)),
        InlineKeyboardButton("➕", callback_data=f"edit_{code}_{qty+1}"),
    )
    markup.add(InlineKeyboardButton("Addtocart", callback_data=f"Add to cart_{code}_{qty}"))
    markup.add(InlineKeyboardButton("Cancel", callback_data=f"cancel"))
    return markup


def is_spam(cid):
    return False


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    cid = call.message.chat.id
    if is_spam(cid):
        return
    mid = call.message.id
    data = call.data
    call_id = call.id
    command, code, qty = data.split("_")
    f2 = open(f"{code}_price.txt" , 'r')
    price = f2.read()
    print(f"cid: {cid} mid: {mid} data: {data}")
    # bot.answer_callback_query(call_id, f'data: {data}')
    # markup = InlineKeyboardMarkup()
    # markup.add(InlineKeyboardButton('button 1', callback_data=str(int(data)+1)))
    # markup.add(InlineKeyboardButton('channel link', url='https://t.me/DailyProjects'))
    # markup.add(InlineKeyboardButton('google link', url='https://google.com'))
    # bot.edit_message_reply_markup(cid, mid, reply_markup=markup)
    if data.startswith("edit"):
        command, code, qty = data.split("_")
        if qty == "0":
            bot.answer_callback_query(call_id, f"quantity can not be zero")
        else:
            config = {'user': 'root', 'password': '1387@1387', 'host': 'localhost', 'database': 'project'}
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute(f"SELECT PRODUCT_CAPTION FROM PRODUCT WHERE ID ={code}  ;")
            result = cursor.fetchall()
            products = [i['PRODUCT_CAPTION'] for i in result]
            product_caption = (products[-1])
            cursor.close()
            conn.close()
            bot.answer_callback_query(call_id, f"quantity increased to {qty}")
            bot.edit_message_caption(
                f"{product_caption} \ntotal cost(Toman): {int(qty) *float(price)}",
                cid,
                mid,
                reply_markup=gen_markup(code, int(qty)),
            )
    elif data == "cancel":
        bot.answer_callback_query(call_id, "process canceled")
        bot.edit_message_reply_markup(cid, mid, reply_markup=None)
    elif data.startswith("Add to cart"):
        print(data)
        insert_sale(cid)
        command, code, qty = data.split("_")
        config = {'user': 'root', 'password': '1387@1387', 'host': 'localhost', 'database': 'project'}
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT ID FROM SALE WHERE CUST_ID ={cid}  ;")
        result = cursor.fetchall()
        sale_ids = [i['ID'] for i in result]
        sale_id = (sale_ids[-1])
        cursor.close()
        conn.close()
        insert_SALE_ROW_data(code , int(qty) , sale_id  )
        print(f'GG , qty saved with {qty}')
        bot.send_message(cid,'added to cart')
        


@bot.message_handler(commands=["start"])
def start_command(message):
    cid = message.chat.id
    cids =custom_get_customer_data('CID' , cid )
    print(cids)
    if  int(cid) not in cids  :
        insert_customer_data(cid , message.chat.first_name , message.chat.last_name)
    elif int(cid) in cids :
        mid = message.message_id
        # bot.reply_to(message, 'welcome to bot')
        send_message(cid, "welcome to bot", reply_to_message_id=mid)
        # send_message(cid, 'welcome to bot')
        command_help(message)
        cid = message.chat.id
        insert_customer_data(cid , message.chat.first_name , message.chat.last_name)
    else:
        bot.send_message(cid  , "hi sir")

@bot.message_handler(commands = ['feedback'])
def feed_back_sender(message):
    cid = message.chat.id
    bot.send_message(cid , 'thanks you for helping us ')
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('CALL_US')
    markup.add('SUPPORT')
    send_message(cid, "WE CAN HELP YOU BY THESE", reply_markup=markup)


@bot.message_handler(commands=["help"])
def command_help(message):
    cid = message.chat.id
    get_user_step(cid)
    help_text = "The following commands are available: \n"
    for (
        key
    ) in (
        commands
    ):  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    if cid in admins:
        help_text += "**admin commands**\n"
        for key in admin_command:
            help_text += "/" + key + ": "
            help_text += admin_command[key] + "\n"
    send_message(cid, help_text)


#@bot.message_handler(commands=["home"])
#def home_command(message):
#    cid = message.chat.id
#    markup = ReplyKeyboardMarkup(resize_keyboard=True)
#    markup.add(buttons["products"])
#    markup.add(buttons["support"])
#    send_message(cid, "welcome to my store bot", reply_markup=markup)



#@bot.message_handler(func=lambda message: message.text == buttons["products"])
#def button_one_handler(message):
#    cid = message.chat.id
#   hideboard = ReplyKeyboardRemove()
#    send_message(cid, "button محصولات pressed", reply_markup=hideboard)

#bot.message_handler(content_types=["photo"])
#def photo_handler(message):
#    cid = message.chat.id
#    mid = (message.photo[-1].file_id)
#    bot.send_message(cid , mid)
#    print(message.photo[-1].file_id)
#    os.makedirs(os.path.join("photos", str(cid)), exist_ok=True)
#    file_info = bot.get_file(message.photo[-1].file_id)
#    content = bot.download_file(file_info.file_path)
#    filename = os.path.join("photos", str(cid), file_info.file_path.split("/")[-1])
#    with open(filename, "wb") as f:
#        f.write(content)





                                                            #saving  product event=>


@bot.message_handler(func=lambda message: message.text == 'yes')
def insert_s(message):
    cid = message.chat.id
    insert_sale(cid)    

@bot.message_handler(commands= ['add_product'])
def helper(message):
    cid = message.chat.id
    bot.send_message(cid , 'please send the photo of your product with this caption : ')
    bot.send_message(cid , 'product id:    |   product_name :     , product_description :     ,  product_price :       ,    product_inventory:           ' )
    ids = get_product_data()

    if ids == []:
        max_id= 100
    else :
        max_id= max(ids)
        max_id += 1 
    bot.send_message(cid , f'your product id is going to be :  {max_id}')


@bot.message_handler(content_types=["photo"])
def photo_handler(message):
    CAPTION = message.caption
    pid = (message.photo[-1].file_id)
    cid = message.chat.id
    captions = []
    captions.append(message.caption)
    cap = []
    for i in range(4):
        b = (captions[0])
        b = b.split(',')
    cap.append(b[0])
    cap.append(b[1])
    cap.append(b[2])
    cap.append(b[3])
    final = []
    print(final)
    for i in cap:
        lst = (i.split(':'))[-1] 
        final.append(lst) 
    insert_product_data(final[0] , final[1] , final[2] , final[3] , pid , CAPTION )
    bot.send_photo(channel_id , pid , caption =  message.caption )
    bot.send_message(cid , 'your product data have been inserted sucssesfully')
    bot.send_message(cid , 'are you sure?')


                                                            #showing products event=>
@bot.message_handler(commands =["show_me_ids"])
def id_shower (message):
    cid = message.chat.id
    data = get_product_data()
    print(data)
    print(len(data))
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for i in data:
        markup.add (InlineKeyboardButton ( i ))
    bot.send_message(cid, "the ids are these:", reply_markup=markup)
    bot.send_message(cid , 'wich one?')


@bot.message_handler(func=lambda message: message.text == 'CALL_US')
def call_US_handler(message):
    cid = message.chat.id
    bot.send_message(cid , 'need more help or you have any problem ? \n call this number: 09**********0 \n we wish that this could help you')


@bot.message_handler(func=lambda message: message.text == 'SUPPORT')
def support_handler(message):
    cid = message.chat.id
    bot.send_message(cid , "send me a text of your problem\nNOTE: don't use any insult or any (+18) words or you will be banned for all of your life ")
    user_step[cid] = 1





@bot.message_handler(content_types=['text'])
def product_sender(message):
    cid = message.chat.id
#    if os.path.exists(f"{cid}.txt"):
#        os.remove(f"{cid}.txt")
#    else:
#       print("the file doesn't exists")
#    f = open(f"{cid}.txt ", 'a' )
    text = message.text
#    f.write(text)
    config = {'user': 'root', 'password': '1387@1387', 'host': 'localhost', 'database': 'project'}
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT MID FROM PRODUCT WHERE ID ={text}  ;")
    result = cursor.fetchall()
    sale_ids = [i['MID'] for i in result]
    mid = (sale_ids[-1])
    cursor.close()
    conn.close()
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT PRODUCT_CAPTION FROM PRODUCT WHERE ID ={text}  ;")
    result = cursor.fetchall()
    captions= [i['PRODUCT_CAPTION'] for i in result]
    CAPTION = (captions[-1])
    cursor.close()
    conn.close()
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT INVENTORY FROM PRODUCT WHERE ID ={text}  ;")
    result = cursor.fetchall()
    sale_ids = [i['INVENTORY'] for i in result]
    inv = (sale_ids[-1])
    cursor.close()
    conn.close()
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT PRICE FROM PRODUCT WHERE ID ={text}  ;")
    result = cursor.fetchall()
    prices = [i['PRICE'] for i in result]
    price = (prices[-1])
    cursor.close()
    conn.close()
    bot.send_photo( cid,mid,caption=f'{CAPTION}\n WARNING:the quantity is the max amount you can by , if you make it more than that , you are ordering us to buy more and give you more , take care of this think' ,reply_markup = gen_markup(text, inv))
    if os.path.exists(f"{text}_price.txt"):
        os.remove(f"{text}_price.txt")
    else:
        print("the file doesn't exists")
    f2 = open(f'{text}_price.txt', 'a')
    f2.write(str(price)) 




@bot.message_handler(content_types=['text'])
def text_sender(message):
    cid = message.chat.id 
    if user_step[cid] == 1 :
        text = message.text
        name  = custom_get_customer_data('CUSTOMER' , 'FIRST_NAME' , cid  )
        for i in admins:
            bot.send_message(i , f" you have an message from :\n user_id={cid}\n user_name={name} \n the message is this: \n {text}")
        user_step[cid]=0
    elif user_step[cid]!=1:
        pass

    



# default handler for every other text
@bot.message_handler(func=lambda message: True, content_types=["text"])
def command_default(message):
    # cid = message.chat.id
    # text = message.text
    # hideboard = ReplyKeyboardRemove()
    # if text == buttons['products']:
    #     send_message(cid, 'button محصولات pressed', reply_markup=hideboard)
    # elif text == buttons['support']:
    #     send_message(cid, 'button پشتیبانی pressed', reply_markup=hideboard)
    # else:
    send_message(
        message.chat.id,
        "I don't understand \"" + message.text + '"\nMaybe try the help page at /help',
    )




def sample():
    try:
        return send_message(e, "hello")
    except Exception as e:
        return f"error happend, {e}"


# print(sample())

bot.infinity_polling()