# fileName: plugins/dm/action_inline/default_ans.py
# copyright ©️ 2021 nabilanavab
fileName = "plugins/dm/action_inline/default_ans.py"

from plugins.utils   import *
from configs.db      import myID
from configs.config  import images
from lang            import langList
from pyrogram.types  import (InputTextMessageContent, InlineKeyboardMarkup,
                             InlineKeyboardButton, InlineQueryResultPhoto)

async def default_ans(inline_query) -> list:
    try:
        lang_code = await util.getLang(inline_query.from_user.id)
        CHUNK, _ = await util.translate(text="inline_query", lang_code=lang_code)
        
        # Getting Lang Data..
        BUTTON = CHUNK['TOP']
        _lang = { langList[lang][1]:f"https://t.me/{myID[0].username}?start=-l{lang}" for lang in langList }
        BUTTON.update(_lang)
        BUTTON.update({"♻" : "-|refresh"})
        BUTTON = await util.createBUTTON(
            btn = BUTTON,
            order = int(f"1{((len(BUTTON)-2)//3)*'3'}{(len(BUTTON)-2)%3}1")
        )
        
        answer = [
            InlineQueryResultPhoto(
                photo_url = "https://github.com/telegram-account/scratchPDF/assets/53673312/3a89d06b-65f9-4efc-8c32-3dcd67771d97", reply_markup = BUTTON,
                title = CHUNK['capt'],
                caption = CHUNK['capt'], description = CHUNK['des']
            ),
            InlineQueryResultPhoto(
                photo_url = "https://graph.org/file/91ef937e900888c572086.jpg",
                title="search pdf file",
                reply_markup = InlineKeyboardMarkup(
                    [[
                        InlineKeyboardButton(
                            text = "♻️ SEARCH ♻️",
                            switch_inline_query_current_chat = ""
                        ),
                        InlineKeyboardButton(
                            text = "💖 SHARE SEARCH 💖",
                            switch_inline_query = ""
                        )
                    ]]
                ),
                input_message_content = InputTextMessageContent("__The ‘**♻️ SEARCH ♻️**’ option allows you to search for PDF files within the same chat__,\n\n"
                          "__while the ‘**💖 SHARE SEARCH 💖**’ feature enables you to search for PDFs in a different chat__"),
            )
        ]
        
        return answer
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(fileName, Error), exc_info = True)
