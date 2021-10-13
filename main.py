import time
import random
import string
from pyrogram import Client
from pyrogram.errors import FloodWait
from captcha.image import ImageCaptcha
from pyrogram.handlers import MessageHandler
from pyrogram.handlers import UserStatusHandler


app = Client('my_account')

# Executes some problematic useless json
def safe_execute(statement1,statement2):
    try:
        temp = statement1[statement2]
        return temp
    except:
        return None


def get_updates(client,message):
    # Get message infos can directly be updated to the local variable store or database
    # all this available types can be gotten from https://docs.pyrogram.org/api/types/Message
    msgtext = message.text

    fromuser = message.from_user
    username1 = safe_execute(fromuser, 'first_name')
    username2 = safe_execute(fromuser, 'user_name')
    userisscammer = safe_execute(fromuser, 'is_scam')
    userisfake = safe_execute(fromuser, 'is_fake')
    userid = safe_execute(fromuser, 'user_id')
    isuser = safe_execute(fromuser, '_')
    print(isuser, userid, userisfake, userisscammer, username2, username1)
    messageid = message.message_id
    senderchat = message.sender_chat
    # Get category type
    isaudio = message.audio # may be used for easter egg
    isphoto = message.photo # may be used for easter egg
    isdocument = message.document # may be used for easter egg
    isstickers = message.sticker # may be used for easter egg
    isanimation = message.animation # may be used for easter egg
    isgame = message.game # may be used for easter egg
    isvideo = message.video 
    isvoice = message.voice # may be used for easter egg
    isvideo_note = message.video_note # may be used for easter egg
    iscaption = message.caption 
    iscontact = message.contact # may be used for easter egg
    islocation = message.location 
    iswebpage = message.web_page # may be used for easter egg
    isdice = message.dice # may be used for easter egg
    isgamehighscore = message.game_high_score # may be used for easter egg
    print(msgtext)


async def update_database():
    pass    # update the database or backups the database

# dont forget to add message
def send_ad(ad_type, contact): # message is gotten from the database ( an array with from 0 for text,1 -> 50 for photos, 51 -> 100 for videos, 101 -> 150 for docs, 151 -> voice)
    # 0 -> text only; 1 -> photo only; 2 -> video only; 3 -> doc only; 4 -> voice; 5 -> image+text; 6 -> video+text; 7 -> doc+text; 8 -> voice+text; 9 -> photo+video+text; 10 -> photo+video+docs+text; 11 -> photo+video+docs+voice+text
    if ad_type == '1':
        try:
            app.send_message(contact,"I like what you do, megakom is on his way men " + str(contact)+ " ca c'est zer")
        except FloodWait as e:
            time.sleep(e.x)
            app.send_message(contact,"I like what you do")
    elif ad_type == '2': # Create a separate function for this one
        try:
            app.send_photo(contact, r"C:\Users\THierry\Pictures\Screenshot_20200416-110216_WhatsApp.jpg", caption='shit' )
        except FloodWait as e:
            time.sleep(e.x)
            app.send_photo(contact, r"C:\Users\THierry\Pictures\Screenshot_20200416-110216_WhatsApp.jpg", caption='shit' )

    elif ad_type == '3':
        var = []
        var.append(contact)
        var.append(create_captcha())
        var.append(time.time())
        try:
            app.send_photo(contact, r"captcha.png", caption='check this captcha bro' )
            return var
        except FloodWait as e:
            time.sleep(e.x)
            app.send_photo(contact, r"captcha.png", caption='check this captcha bro' )
            return var


def create_captcha():
    # create an image instance
    image = ImageCaptcha(width = 280, height= 90)
    # printing uppercase letters
    letters = string.ascii_uppercase
    captcha_text = ''.join(random.choice(letters) for i in range(7))

    # generate image with given text
    data = image.generate(captcha_text)

    # save
    image.write(captcha_text, 'captcha.png')

    return captcha_text



def insert_in_db():
    pass

def read_from_db():
    pass

def re


class MegaKom:
    def __init__(self,app):
        self.app = app
        self.contacts = ['Ekotek_solutions','el_conio']
        self.ad_type = ['1','2','3']
        

    def run(self):
        # Set handler to get and handle updates when needed
        self.update_handler = MessageHandler(get_updates)
        self.app.add_handler(self.update_handler)

        
        # sends ads
        with app:
            for i in range(100): # stimulate an infinite loop
                send_ad(random.choice(self.ad_type), random.choice(self.contacts))






        





if __name__ == "__main__":
    Kombot = MegaKom(app)
    Kombot.run()

