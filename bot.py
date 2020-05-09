import amanobot.aio
import asyncio
from config import sudos, token
from utils import DbUtils
from amanobot.aio.loop import MessageLoop

bot = amanobot.aio.Bot(token)

mhelper = DbUtils(bot)

loop = asyncio.get_event_loop()

async def handle(msg):
    tp = amanobot.glance(msg)
    if tp[0] == "text":
        if msg["text"] == "/start" or msg["text"] == "/help" or msg["text"] == "/ajuda":
            await bot.sendMessage(msg["chat"]["id"], f"""Olá *{msg["from"]["first_name"]}* 😃👋 esse é o suporte do Trending Groups 

👉 Envie uma reclamação, elogio ou peça ajuda abaixo.

👉 Caso esse bot estiver em manutenção fale diretamente com os donos: @pauloalmeida20 (idealizador) ou @alissonlauffer (desenvolvedor).""",
                                  parse_mode="markdown")
        elif msg["from"]["id"] in sudos:
            if not msg.get("reply_to_message"):
                await bot.sendMessage(msg["chat"]["id"], "Você precisa responder a mensagem de algum usuário.")
            else:
                try:
                    await mhelper.send_message_to_origin(msg["from"]["id"],
                                                         msg["reply_to_message"]["message_id"], msg["text"])
                except Exception as e:
                    await bot.sendMessage(msg["chat"]["id"], str(e))
        else:
            await mhelper.forward_messages(msg["chat"]["id"], msg["message_id"])


answerer = amanobot.aio.helper.Answerer(bot)

loop.create_task(MessageLoop(bot, handle).run_forever())
loop.run_forever()
