from asyncio import events
from html import entities
import time
from telethon import TelegramClient, events, Button
from decouple import config

from account.models import TelegramSettings
# from account.models import TelegramSettings
from .serializers import BotSerializer, ClearChatSerializer
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from account.models import TelegramSettings
from investment.models import InvestmentPlan
from asgiref.sync import sync_to_async, async_to_sync

api_id= config("API_ID", cast = int) # You can get api_hash and api_id by creating an app on
api_hash = config("API_HASH") # my.telegram.org/apps (needed if you use MTProto instead of BotAPI)
BOT_TOKEN = config("BOT_TOKEN") #bot token

# from azure.common.credentials import ServicePrincipalCredentials
# from azure.mgmt.resource import ResourceManagementClient
# from azure.mgmt.web import WebSiteManagementClient

# subscription_id ="9a4cf7ee-66b8-4224-96c2-beed2f52435c" #you can get it from azure portal
# client_id ="xxx"
# secret="xxx"
# tenant="e12f7f7b-e026-4457-ab17-34655c69a628"

# credentials = ServicePrincipalCredentials(
#     client_id= client_id,
#     secret=secret,
#     tenant = tenant
# )

# #resource_client = ResourceManagementClient(credentials,subscription_id)
# web_client = WebSiteManagementClient(credentials,subscription_id)

# #restart your azure web app
# web_client.web_apps.restart("your_resourceGroup_name","your_web_app_name")



# async def start():
#     user_chat = await sync_to_async(TelegramSettings.objects.get, thread_sensitive=True)(chat_id="698485392")
#     user_chat_id = user_chat.chat_id
#     user_message_id = user_chat.message_id
#     await client.delete_messages(int(user_chat_id),user_message_id,revoke=True)


# client = TelegramClient("session/session-master1", api_id, api_hash)
client_1 = TelegramClient("session/session-master", api_id, api_hash).start(bot_token=BOT_TOKEN)



# @client.on(events.NewMessage(pattern=r"/help"))
# async def start(event):
    
#     user_chat = await sync_to_async(TelegramSettings.objects.get, thread_sensitive=True)(chat_id=event.message.chat_id)
#     us    er_chat_id = user_chat.chat_id
#     user_message_id = user_chat.message_id
#     await client.delete_messages(int(user_chat_id),user_message_id,revoke=True)


# @client.on(events.NewMessage(chats=("Test Channel")))
# async def start(event):
#     print(event.raw_text)


@client_1.on(events.NewMessage())
async def handler(event):
    auto_send = await sync_to_async(TelegramSettings.objects.get, thread_sensitive=True)(id=1)
    """
    If the message is sent in the channel "Test Channel", then the message will be sent to the group
    "Test Group Channel Trial"
    
    :param event: The event object that was just received
    """
    if (event.chat.title == "Test Channel" and auto_send.auto_send and "#BULLISHHH" in event.raw_text):
        text = auto_send.auto_send_text
        await client_1.send_message("https://t.me/testgroupchanneltrial", f"{text}", buttons=[[Button.url("Cornix Premium Bot", "https://t.me/cornix_premuim_Bot")]])

        
@client_1.on(events.NewMessage(pattern=r"/start"))
async def start(event):
    buttons = [
        [Button.inline("Restart bot", data="start")],
        [Button.inline("Send message", data="message")],
        [Button.inline("Settings", data="settings")],
        [Button.inline("save auto text", data="auto_send")],
        [Button.inline("Setup payment message", data="payment")],
        [Button.inline("Pause Bot", data="pause")],
    ]
    await event.respond("Choose an option: ", buttons=buttons)

@client_1.on(events.CallbackQuery(data="start"))
async def start_bot(event):
    await start(event)

@client_1.on(events.CallbackQuery(data="message"))
async def message(event):
    async with client_1.conversation(event.chat_id) as conv:
        await conv.send_message("Please Type the message you want to send")
        response = await conv.get_response()
        await client_1.send_message("https://t.me/testgroupchanneltrial", f"{response.text}", buttons=[[Button.url("Cornix Premium Bot", "https://t.me/cornix_premuim_Bot")]])
        # await client_1.send_file("https://t.me/testgroupchanneltrial", file = response.media, caption=f"{response.text}", buttons=[[Button.url("Cornix Premium Bot", "https://t.me/cornix_premuim_Bot")]])
        await conv.send_message("Message sent successfully")
        await start(event)

@client_1.on(events.CallbackQuery(data="auto_send"))
async def setup_auto_message(event):
    async with client_1.conversation(event.chat_id) as conv:
        await conv.send_message("Please Type the message you want to save")
        response = await conv.get_response()
        auto_send = await sync_to_async(TelegramSettings.objects.get, thread_sensitive=True)(id=1)
        auto_send.auto_send_text = response.text
        await sync_to_async(auto_send.save, thread_sensitive=True)()
        await conv.send_message("Text set successfully")
        await start(event)





@client_1.on(events.CallbackQuery(data="settings"))
async def settings(event):
    auto_send = await sync_to_async(TelegramSettings.objects.get, thread_sensitive=True)(id=1)
    async with client_1.conversation(event.chat_id) as conv:
        buttons = [[Button.inline("Off", data="off_auto_send")] if auto_send.auto_send else [Button.inline("On", data="on_auto_send")]]
        await conv.send_message("Turn on or Turn off the auto message sending settings", buttons=buttons)


@client_1.on(events.CallbackQuery(data="pause"))
async def pause(event):
    status = await sync_to_async(TelegramSettings.objects.get, thread_sensitive=True)(id=1)
    async with client_1.conversation(event.chat_id) as conv:
        buttons = [[Button.inline("Resume", data="resume_bot")] if status.bot_status else [Button.inline("Pause", data="pause_bot")]]
        await conv.send_message("Pause or Resume the Premium Bot", buttons=buttons)


@client_1.on(events.CallbackQuery(data="resume_bot"))
async def resume_bot(event):
    status = await sync_to_async(TelegramSettings.objects.get, thread_sensitive=True)(id=1)
    await event.respond("Premium Bot is now resumed")
    status.bot_status = False
    await sync_to_async(status.save, thread_sensitive=True)()
    await start(event)


@client_1.on(events.CallbackQuery(data="pause_bot"))
async def pause_bot(event):
    status = await sync_to_async(TelegramSettings.objects.get, thread_sensitive=True)(id=1)
    await event.respond("Premium Bot is now paused")
    status.bot_status = True
    await sync_to_async(status.save, thread_sensitive=True)()
    await start(event)

        
@client_1.on(events.CallbackQuery(data="off_auto_send"))
async def off_auto_send(event):
    
    auto_send = await sync_to_async(TelegramSettings.objects.get, thread_sensitive=True)(id=1)
    await event.respond("Auto send is off")
    auto_send.auto_send = False
    await sync_to_async(auto_send.save, thread_sensitive=True)()
    await start(event)

    

@client_1.on(events.CallbackQuery(data="on_auto_send"))
async def on_auto_send(event):
    auto_send = await sync_to_async(TelegramSettings.objects.get, thread_sensitive=True)(id=1)
    if auto_send.auto_send_text == "" or auto_send.auto_send_text is None:
        await event.respond("Please set the auto send text first")
        return await start(event)
    auto_send.auto_send = True
    await sync_to_async(auto_send.save, thread_sensitive=True)()
    await event.respond("Auto send is now on")
    await start(event)


@client_1.on(events.CallbackQuery(data="payment"))
async def payment(event):
    payment_plan = await sync_to_async(InvestmentPlan.objects.get, thread_sensitive=True)(id=1)
    async with client_1.conversation(event.chat_id) as conv:
        await conv.send_message("Please Type the message payment plan message")
        response = await conv.get_response()
        payment_plan.description = response.text
        await sync_to_async(payment_plan.save, thread_sensitive=True)()
        await event.respond("payment plan Message set successfully")
        await start(event)




# @client_1.on(events.NewMessage())
# async def handler(event):
#   if (event.chat.title == "BitCoin Price (Live)"):
#     text = event.raw_text 
#     print(text)
    ##parse your text
    # await client_1.send_message("https://t.me/testgroupchanneltrial", text)

with client_1:
    client_1.run_until_disconnected()

# with client:
#     client.run_until_disconnected()


    







# async def main():
#     await client.run_until_disconnected()
#     dialogs = await client.get_dialogs(5)
#     for dialog in dialogs:
#         if dialog.name == 'Alexanda_bot':
#             await client.delete_dialog(dialog.name, revoke=True)
#             print(f"Deleteda {dialog.name}")
#             time.sleep(1)






# if __name__ == '__main__':
#     print("Bot started")
#     client.run_until_disconnected()


# with TelegramClient('anon', api_id, api_hash) as Uclient:
#     # client.loop.run_until_complete(client.send_message('Alexanda_bot', 'Hello, user account sending message trial!'))
#     user = Uclient.loop.run_until_complete(Uclient.get_entity('+2347037241240'))
#     # client.loop.run_until_complete(client.delete_dialog('Alexanda_bot',revoke=True))
#     print(user)

# async def main():
#     await client.run_until_disconnected()
#     dialogs = await client.get_dialogs()
#     for dialog in dialogs:
#         if dialog.name == 'Alexanda_bot':
#             await client.delete_dialog(dialog.name, revoke=True)
#             print(f"Deleted {dialog.name}")
#             time.sleep(1)