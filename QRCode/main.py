import qrcode
import message,app
import telegram
from telegram import InlineKeyboardMarkup,InlineKeyboardButton
from telegram.ext import CommandHandler,MessageHandler,filters,ApplicationBuilder,CallbackQueryHandler
import os
import cv2
with open("token.bot","r",encoding="utf-8") as file:
    bot=ApplicationBuilder().token(file.read()).build()
async def textHandeler(update,context):
    info=update.effective_user
    text=update.message.text
    qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
    )
    qr.add_data(text)
    path=os.path.join("cach",str(info.id))
    if not os.path.exists(path):
        os.makedirs(path)
    qr.make(fit=True)
    qr.make_image(fill_color="black", back_color="white").save(path + "/photo.bng")
    await context.bot.send_photo(chat_id=info.id,photo=open(os.path.join(path,"photo.bng"),"rb"),caption="uploaded by {} ".format(str(info.id)))

    os.remove(path+"/photo.bng")

async def img(update,contextt):
    info=update.effective_user
    id=await message.Sendmessage(info.id,"downloading your photo")
    path=os.path.join("cach",str(info.id))
    if not os.path.exists(path):
        os.makedirs(path)
    try:
        try:
            get=await update.message.photo[-1].get_file()
        except:
            get=await update.message.effective_attachment.get_file()
        await get.download_to_drive(path+"/photo.png")
        await message.Editmessage(info.id,"extracting qr code",id)
        img = cv2.imread(path+"/photo.png")
        qr_code_detector = cv2.QRCodeDetector()
        try:
            decoded_objects = qr_code_detector.detectAndDecodeMulti(img)
            await message.Editmessage(info.id,decoded_objects[1][0],id)
        except:
            await message.Editmessage(info.i,"no QR code fownd",id)

        os.remove(path+"/photo.png")
    except Exception as e:
        print(e)
        await message.Editmessage(info.id,"error while downloading",id)

async def start(update,contextt):
    info=update.effective_user
    keyboard=InlineKeyboardMarkup([[InlineKeyboardButton("donate",url="https://www.paypal.me/AMohammed231")],[InlineKeyboardButton("help",callback_data="help")]])
    await message.Sendmessage(chat_id=info.id,text="welcome " + str(info.first_name) + " to this bot. please send image to extract QR code from it or send text to create qr code",reply_markup=keyboard)
async def helb(update,contextt):
    links="""<a href="https://t.me/mesteranasm">telegram</a>

<a href="https://t.me/tprogrammers">telegram channel</a>

<a href="https://x.com/mesteranasm">x</a>

<a href="https://Github.com/mesteranas">Github</a>

email:
anasformohammed@gmail.com

<a href="https://Github.com/mesteranas/QRCode_telegram_bot">visite project on Github</a>
"""
    info=update.effective_user
    await message.Sendmessage(info.id,"""name: {}\nversion: {}\ndescription: {}\n developer: {}\n contect us {}""".format(app.name,str(app.version),app.description,app.developer,links))
async def callBake(update,contextt):
    q=update.callback_query
    q.answer()
    if q.data=="help":
        await helb(update,contextt)

print("running")
bot.add_handler(CommandHandler("start",start))
bot.add_handler(CommandHandler("help",helb))
bot.add_handler(CallbackQueryHandler(callBake))
bot.add_handler(MessageHandler(filters.Document.ALL,img))
bot.add_handler(MessageHandler(filters.TEXT,textHandeler))
bot.add_handler(MessageHandler(filters.PHOTO,img))
bot.run_polling()