# Rewrote with experimental bleck magik
# code-rgb


import io
import os
import random
import time


from pyrogram.errors import YouBlockedUser

from userge import Message, userge
from userge.utils.exceptions import StopConversation


@userge.on_cmd(
    "q",
    about={
        "header": "Quote a message",
        "flags": {"-l": "limit, for multiple messages"},
        "usage": "Reply {tr}q -l[message limit]",
        "examples": ["{tr}q", "{tr}q -l3"],
    },
    allow_via_bot=False,
    del_pre=True,
)
async def quotecmd(message: Message):
    """quotecmd"""
    reply = message.reply_to_message
    quote_list = []
    self_mid = False
    args = ""
    if reply:
        if "l" in message.flags:
            limit = message.flags.get("l", 1)
            if not limit.isdigit():
                await message.err("give valid no. of message to quote", del_in=5)
                return
            num_ = min(int(limit), 24)
            async for msg in userge.iter_history(
                message.chat.id, limit=num_, offset_id=reply.message_id, reverse=True
            ):
                if msg.message_id != message.message_id:
                    quote_list.append(msg.message_id)
            if message.filtered_input_str:
                self_mid = True
                await message.edit(message.filtered_input_str)
        else:
            quote_list.append(reply.message_id)
            if message.input_str:
                self_mid = True
                await message.edit(message.input_str)
    else:
        args = message.input_str
    if self_mid:
        quote_list.append(message.message_id)
    else:
        await message.delete()
    if not args and len(quote_list) == 0:
        await message.err("Reply to a message or provide an input to quote !", del_in=5)
        return
    try:
        async with userge.conversation("QuotLyBot", timeout=100) as conv:
            try:
                if quote_list:
                    await userge.forward_messages(
                        "QuotLyBot", message.chat.id, quote_list
                    )
                    if self_mid:
                        await message.delete()
                elif args:
                    await conv.send_message(args)
            except YouBlockedUser:
                await message.edit("first **unblock** @QuotLyBot")
                return
            quote = await conv.get_response(mark_read=True)
            if not (quote.sticker or quote.document):
                await message.err("something went wrong!")
                return
            message_id = reply.message_id if reply else None
            if quote.sticker:
                await userge.send_sticker(
                    chat_id=message.chat.id,
                    sticker=quote.sticker.file_id,
                    reply_to_message_id=message_id,
                )
            else:
                await userge.send_document(
                    chat_id=message.chat.id,
                    document=quote.document.file_id,
                    reply_to_message_id=message_id,
                )
    except StopConversation:
        await message.err(
            "@QuotLyBot Didn't respond in time\n:(  please try again later...", del_in=5
        )









@userge.on_cmd(
    "t",
    about={
        "header": "quotes text and kangs it",
        "flags": {"already flagged"},
        "usage": "Reply {tr}kang [emoji('s)] [pack number] to a sticker or "
        "an image to kang it to your userbot pack.",
        "examples": [
            "{tr}t",
        ],
    },
    allow_channels=False,
    allow_via_bot=False,
)
async def quotecmd(message: Message):
    """quotecmd"""
    reply = message.reply_to_message
    quote_list = []
    self_mid = False
    args = ""
    if reply:
        if "l" in message.flags:
            limit = message.flags.get("l", 1)
            if not limit.isdigit():
                await message.err("give valid no. of message to quote", del_in=5)
                return
            num_ = min(int(limit), 24)
            async for msg in userge.iter_history(
                message.chat.id, limit=num_, offset_id=reply.message_id, reverse=True
            ):
                if msg.message_id != message.message_id:
                    quote_list.append(msg.message_id)
            if message.filtered_input_str:
                self_mid = True
                await message.edit(message.filtered_input_str)
        else:
            quote_list.append(reply.message_id)
            if message.input_str:
                self_mid = True
                await message.edit(message.input_str)
    else:
        args = message.input_str
    if self_mid:
        quote_list.append(message.message_id)
    else:
        await message.delete()
    if not args and len(quote_list) == 0:
        await message.err("Reply to a message or provide an input to quote !", del_in=5)
        return
    try:
        async with userge.conversation("QuotLyBot", timeout=100) as conv:
            try:
                if quote_list:
                    await userge.forward_messages(
                        "QuotLyBot", message.chat.id, quote_list
                    )
                    if self_mid:
                        await message.delete()
                elif args:
                    await conv.send_message(args)
            except YouBlockedUser:
                await message.edit("first **unblock** @QuotLyBot")
                return
            quote = await conv.get_response(mark_read=True)
            if not (quote.sticker or quote.document):
                await message.err("something went wrong!")
                return
            message_id = reply.message_id if reply else None
            if quote.sticker:
                await userge.send_sticker(
                    chat_id=message.chat.id,
                    sticker=quote.sticker.file_id,
                    reply_to_message_id=message_id,
                )
            else:
                await userge.send_document(
                    chat_id=message.chat.id,
                    document=quote.document.file_id,
                    reply_to_message_id=message_id,
                )
    except StopConversation:
        await message.err(
            "@QuotLyBot Didn't respond in time\n:(  please try again later...", del_in=5
        )
async def kang_(message: Message):
    """kang a sticker"""
    user = await userge.get_me()
    replied = quote.sticker
    photo = None
    emoji_ = None
    is_anim = False
    resize = False
    if replied and replied.media:
        if replied.photo:
            resize = True
        elif replied.document and "image" in replied.document.mime_type:
            resize = True
        elif replied.document and "tgsticker" in replied.document.mime_type:
            is_anim = True
        elif replied.sticker:
            if not replied.sticker.file_name:
                await message.edit("`Sticker has no Name!`")
                return
            emoji_ = replied.sticker.emoji
            is_anim = replied.sticker.is_animated
            if not replied.sticker.file_name.endswith(".tgs"):
                resize = True
        else:
            await message.edit("`Unsupported File!`")
            return
        await message.delete()
        photo = await userge.download_media(message=replied, file_name=Config.DOWN_PATH)
    else:
        await message.edit("`I can't kang that...`")
        return
    if photo:
        args = message.filtered_input_str.split()
        pack = 1
        if len(args) == 2:
            emoji_, pack = args
        elif len(args) == 1:
            if args[0].isnumeric():
                pack = int(args[0])
            else:
                emoji_ = args[0]

        if emoji_ and emoji_ not in (
            getattr(emoji, _) for _ in dir(emoji) if not _.startswith("_")
        ):
            emoji_ = None
        if not emoji_:
            emoji_ = "🤔"

        u_name = user.username
        u_name = "@" + u_name if u_name else user.first_name or user.id
        packname = f"a{user.id}_by_x_{pack}"
        custom_packnick = Config.CUSTOM_PACK_NAME or f"{u_name}'s kang pack"
        packnick = f"{custom_packnick} Vol.{pack}"
        cmd = "/newpack"
        if resize:
            photo = resize_photo(photo)
        if is_anim:
            packname += "_anim"
            packnick += " (Animated)"
            cmd = "/newanimated"
        exist = False
        try:
            exist = await message.client.send(
                GetStickerSet(stickerset=InputStickerSetShortName(short_name=packname))
            )
        except StickersetInvalid:
            pass
        if exist is not False:
            async with userge.conversation("Stickers", limit=30) as conv:
                try:
                    await conv.send_message("/addsticker")
                except YouBlockedUser:
                    await message.edit("first **unblock** @Stickers")
                    return
                await conv.get_response(mark_read=True)
                await conv.send_message(packname)
                msg = await conv.get_response(mark_read=True)
                limit = "50" if is_anim else "120"
                while limit in msg.text:
                    pack += 1
                    packname = f"a{user.id}_by_userge_{pack}"
                    packnick = f"{custom_packnick} Vol.{pack}"
                    if is_anim:
                        packname += "_anim"
                        packnick += " (Animated)"
                    await message.edit(
                        "`Switching to Pack "
                        + str(pack)
                        + " due to insufficient space`"
                    )
                    await conv.send_message(packname)
                    msg = await conv.get_response(mark_read=True)
                    if msg.text == "Invalid pack selected.":
                        await conv.send_message(cmd)
                        await conv.get_response(mark_read=True)
                        await conv.send_message(packnick)
                        await conv.get_response(mark_read=True)
                        await conv.send_document(photo)
                        await conv.get_response(mark_read=True)
                        await conv.send_message(emoji_)
                        await conv.get_response(mark_read=True)
                        await conv.send_message("/publish")
                        if is_anim:
                            await conv.get_response(mark_read=True)
                            await conv.send_message(f"<{packnick}>", parse_mode=None)
                        await conv.get_response(mark_read=True)
                        await conv.send_message("/skip")
                        await conv.get_response(mark_read=True)
                        await conv.send_message(packname)
                        await conv.get_response(mark_read=True)
                        if "-d" in message.flags:
                            await message.delete()
                        else:
                            out = (
                                "__kanged__"
                                if "-s" in message.flags
                                else f"[kanged](t.me/addstickers/{packname})"
                            )
                            await message.edit(
                                f"**Sticker** {out} __in a Different Pack__**!**"
                            )
                            time.sleep(1)
                            await message.delete()
                        return
                await conv.send_document(photo)
                rsp = await conv.get_response(mark_read=True)
                if "Sorry, the file type is invalid." in rsp.text:
                    await message.edit(
                        "`Failed to add sticker, use` @Stickers "
                        "`bot to add the sticker manually.`"
                    )
                    return
                await conv.send_message(emoji_)
                await conv.get_response(mark_read=True)
                await conv.send_message("/done")
                await conv.get_response(mark_read=True)
        else:
            await message.edit("`Brewing a new Pack...`")
            async with userge.conversation("Stickers") as conv:
                try:
                    await conv.send_message(cmd)
                except YouBlockedUser:
                    await message.edit("first **unblock** @Stickers")
                    return
                await conv.get_response(mark_read=True)
                await conv.send_message(packnick)
                await conv.get_response(mark_read=True)
                await conv.send_document(photo)
                rsp = await conv.get_response(mark_read=True)
                if "Sorry, the file type is invalid." in rsp.text:
                    await message.edit(
                        "`Failed to add sticker, use` @Stickers "
                        "`bot to add the sticker manually.`"
                    )
                    return
                await conv.send_message(emoji_)
                await conv.get_response(mark_read=True)
                await conv.send_message("/publish")
                if is_anim:
                    await conv.get_response(mark_read=True)
                    await conv.send_message(f"<{packnick}>", parse_mode=None)
                await conv.get_response(mark_read=True)
                await conv.send_message("/skip")
                await conv.get_response(mark_read=True)
                await conv.send_message(packname)
                await conv.get_response(mark_read=True)
        if "-d" in message.flags:
            await message.delete()
        else:
            out = (
                "__kanged__"
                if "-s" in message.flags
                else f"[kanged](t.me/addstickers/{packname})"
            )
        await message.edit(f"**Sticker** {out}**!**")
        time.sleep(1)
        await message.delete()
        if os.path.exists(str(photo)):
            os.remove(photo)

            