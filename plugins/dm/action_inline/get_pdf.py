# fileName : plugins/dm/action_inline/get_pdf.py
# copyright ©️ 2021 nabilanavab

fileName = "plugins/dm/action_inline/get_pdf.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

from configs.log          import log
from plugins.utils.work   import work
from logger               import logger
from libgenesis           import Libgen
from plugins.utils.util   import getLang, translate
from pyrogram             import Client as ILovePDF, filters
from pyrogram.types       import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaDocument

async def download(current, total, bot, callbackQuery):
    try:
        await bot.edit_inline_reply_markup(
            inline_message_id = callbackQuery.inline_message_id,
            reply_markup = InlineKeyboardMarkup(
                [[ InlineKeyboardButton("📥 DOWNLOADED {:.2f}% 📥".format(current/total*100), callback_data=f"{callbackQuery.data}")],[
                   InlineKeyboardButton("🗑️ CANCEL 🗑️", callback_data=f"c{callbackQuery.data[1:]}")]]
            ))
    except MessageNotModified as e:
        logger.debug("🐞 %s: %s" %(fileName, e))
    except FloodWait as e:
        logger.debug("🐞 %s: %s" %(fileName, e))
        await asyncio.sleep(e.x)
    except Exception as e:
        logger.debug("🐞 %s: %s" %(fileName, e))


@ILovePDF.on_callback_query(filters.regex("lib"))
async def pdfDriver(bot, callbackQuery):
    try:
        lang_code = await getLang(callbackQuery.from_user.id)
        trCHUNK, _ = await translate(text="INLINE", lang_code=lang_code)
        
        if not ( callbackQuery.from_user.id == int(callbackQuery.data.split("|")[2]) ):
            return await callbackQuery.answer(trCHUNK['cbNotU'])
        
        getMSG = await bot.get_messages(
            chat_id = int(log.LOG_CHANNEL),
            message_ids = int(callbackQuery.data.split("|")[1])
        )
        
        if getMSG.empty:
            return await callbackQuery.answer(trCHUNK['old'])
        
        if await work(callbackQuery, "check", False):
            return await callbackQuery.answer(trCHUNK['inWork'])
        cDIR = await work(callbackQuery, "create", False)
        
        await bot.edit_inline_reply_markup(
            inline_message_id = callbackQuery.inline_message_id,
            reply_markup = InlineKeyboardMarkup(
                [[ InlineKeyboardButton("🍪 COOKING DATA 🍪", callback_data = f"{callbackQuery.data}")],[
                    InlineKeyboardButton("🗑️ CANCEL 🗑️", callback_data = f"c{callbackQuery.data[1:]}") ]]
            )
        )
        
        caption = getMSG.caption
        md5 = caption.splitlines()[0].split(':')[1].strip()
        link = f'http://library.lol/main/{md5}'
        
        file = await Libgen().download(
            link, dest_folder=cDIR, progress=download,
            progress_args=[bot, callbackQuery]
        )
        
        await bot.edit_inline_reply_markup(
            inline_message_id = callbackQuery.inline_message_id,
            reply_markup = InlineKeyboardMarkup(
                [[ InlineKeyboardButton("🐍 STARTED UPLOADING 🐍", callback_data=f"{callbackQuery.data}")],[
                    InlineKeyboardButton("🗑️ CANCEL 🗑️", callback_data=f"c{callbackQuery.data[1:]}")]]
            )
        )
        
        await bot.edit_inline_media(
            inline_message_id=callbackQuery.inline_message_id,
            media=InputMediaDocument(media=file, caption=getMSG.caption),
            reply_markup = InlineKeyboardMarkup(
                [[ InlineKeyboardButton(text="♻️ SEARCH AGAIN ♻️", switch_inline_query_current_chat="")]]
            )
        )
        return await work(callbackQuery, "delete", False)
    
    except Exception as e:
        logger.exception("🐞 %s: %s" %(fileName, e), exc_info=True)
        await work(callbackQuery, "delete", False)


@ILovePDF.on_callback_query(filters.regex('^cD\|'))
async def close(bot, callbackQuery):
    try:
        if not (callbackQuery.from_user.id == int(callbackQuery.data.split("|")[2])):
            return await callbackQuery.answer("message not for you..")
        
        await callbackQuery.answer("🗑️")
        await work(callbackQuery, "delete", False)
    except Exception as e:
        logger.exception("🐞 %s: %s" %(fileName, e), exc_info=False)

# Author: @nabilanavab

