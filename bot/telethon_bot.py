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
BOT_TOKEN = config("BOT_TOKEN") # bot token

from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.web import WebSiteManagementClient
from azure.identity import ClientSecretCredential


subscription_id ="9a4cf7ee-66b8-4224-96c2-beed2f52435c" #you can get it from azure portal
client_id ="df173e71-2a1c-487e-895a-e846c098a8b1"
secret="zLK8Q~Fz1-35cx.UjLBd2MmJAxRSiWq3pSj01bsW"
tenant="e12f7f7b-e026-4457-ab17-34655c69a628"

credentials = ClientSecretCredential(
    client_id= client_id,
    client_secret=secret,
    tenant_id = tenant
)

resource_client = ResourceManagementClient(credentials,subscription_id)
web_client = WebSiteManagementClient(credentials,subscription_id)
media_file_path = None


# client = TelegramClient("session/session-master1", api_id, api_hash)
client_1 = TelegramClient("session/session-main", api_id, api_hash).start(bot_token=BOT_TOKEN)


@client_1.on(events.NewMessage())
async def handler(event):
    auto_send = await sync_to_async(TelegramSettings.objects.get, thread_sensitive=True)(id=1)
    """
    If the message is sent in the channel "Test Channel", then the message will be sent to the group
    "Test Group Channel Trial"
    
    :param event: The event object that was just received
    """

    if (event.chat.title == "PREMIUM SIGNALS®" and auto_send.auto_send and "#BULLISHHH" in event.raw_text):
        text = auto_send.auto_send_text
        if media_file_path is None:
            await client_1.send_message(1796998430, f"{text}")
        await client_1.send_file(1796998430, file = media_file_path)
        
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
        media_file_path = response.media
        if response.media is None:
            await client_1.send_message(1796998430, f"{response.text}", buttons=[[Button.url("Cornix Premium Bot", "https://t.me/cornix_premuim_Bot")]])
        await client_1.send_file(1796998430, file = response.media, caption=f"{response.text}",buttons=[[Button.url("Cornix Premium Bot", "https://t.me/cornix_premuim_Bot")]])
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
    # #restart your azure web app
    web_client.web_apps.restart("AlexResources","cornix-bot")
    await start(event)


@client_1.on(events.CallbackQuery(data="pause_bot"))
async def pause_bot(event):
    status = await sync_to_async(TelegramSettings.objects.get, thread_sensitive=True)(id=1)
    await event.respond("Premium Bot is now paused")
    status.bot_status = True
    await sync_to_async(status.save, thread_sensitive=True)()
    # #restart your azure web app
    web_client.web_apps.restart("AlexResources","cornix-bot")
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


with client_1:
    client_1.run_until_disconnected()
