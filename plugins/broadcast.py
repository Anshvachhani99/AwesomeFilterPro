
from pyrogram import Client, filters
import datetime
import time
from database.users_chats_db import db
from info import ADMINS
from utils import broadcast_messages
import asyncio
        
@Client.on_message(filters.command("broadcast") & filters.user(ADMINS) & filters.reply)
# https://t.me/GetTGLink/4178
async def verupikkals(bot, message):
    users = await db.get_all_users()
    b_msg = message.reply_to_message
    sts = await message.reply_text(
        text='Broadcasting your messages...'
    )
    start_time = time.time()
    total_users = await db.total_users_count()
    done = 0
    blocked = 0
    deleted = 0
    failed =0

    success = 0
    async for user in users:
        pti, sh = await broadcast_messages(int(user['id']), b_msg)
        if pti:
            success += 1
        elif pti == False:
            if sh == "Blocked":
                blocked+=1
            elif sh == "Deleted":
                deleted += 1
            elif sh == "Error":
                failed += 1
        done += 1
        await asyncio.sleep(2)
        if not done % 20:
            await sts.edit(f"**Broadcast in progress:**\n\n**Total Users** {total_users}\n**Completed:** {done} / {total_users}\n**Success:** {success}\n**Blocked:** {blocked}\n**Deleted:** {deleted}")    
    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
    await sts.edit(f"<b>Broadcast Completed:\nCompleted in {time_taken} seconds.\n\nTotal Users {total_users}\nCompleted: {done} / {total_users}\nSuccess: {success}\nBlocked: {blocked}\nDeleted: {deleted}</b>")

   
@Client.on_message(filters.command("gpbroadcast") & filters.user(ADMINS) & filters.reply)
async def gpbroadcast(bot, message):
    chats = await db.get_all_chats()
    b_msg = message.reply_to_message
    sts = await message.reply_text(
        text='**Broadcasting your messages...**'
    )
    start_time = time.time()
    total_chats = await db.total_chat_count()
    done = 0
    failed =0

    success = 0
    async for chat in chats:
        pti, sh = await broadcast_messages(int(chat['id']), b_msg)
        if pti:
            success += 1
        elif pti == False:
            if sh == "Error":
                failed += 1
        done += 1
        await asyncio.sleep(2)
        if not done % 20:
            await sts.edit(f"Groups Broadcast in progress...\n\nTotal Groups: <code>{total_chats}</code>\nCompleted: <code>{done}</code> / <code>{total_chats}</code>\nSuccess: <code>{success}</code>\nFailed: <code>{failed}</code>")
    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
    await sts.edit(f"Groups Broadcast Completed.\nCompleted in {time_taken} seconds.\n\nTotal Groups: <code>{total_chats}</code>\nCompleted: <code>{done}</code> / <code>{total_chats}</code>\nSuccess: <code>{success}</code>\nFailed: <code>{failed}</code>")    
