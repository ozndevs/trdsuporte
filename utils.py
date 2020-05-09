import amanobot.aio

from db import conn, cur
from config import sudos


class DbUtils:
    def __init__(self, bot: amanobot.aio.Bot):
        self.bot = bot

    async def forward_messages(self, from_chat_id: int, message_id: int):
        for sudo in sudos:
            m = await self.bot.forwardMessage(sudo, from_chat_id, message_id)
            await self.set_message(from_chat_id=from_chat_id,
                                   to_chat_id=sudo,
                                   from_message_id=message_id,
                                   to_message_id=m["message_id"])

    async def send_message_to_origin(self, to_chat_id: int, to_message_id: int, text: str):
        """
        :param to_chat_id:
            chat_id of the message received by the recipient.
        :param to_message_id:
            message_id of the message received by the recipient.
        :return: The sent message.
        """
        from_chat_id, from_message_id = await self.get_message_details(to_chat_id=to_chat_id,
                                                                       to_message_id=to_message_id)
        return await self.bot.sendMessage(from_chat_id, text, reply_to_message_id=from_message_id)

    async def set_message(self, from_chat_id: int, to_chat_id: int, from_message_id: int, to_message_id: int):
        """
        :param from_chat_id:
            chat_id of the origin message.
        :param to_chat_id:
            chat_id of the message the bot just forwarded.
        :param from_message_id:
            message_id of the origin message.
        :param to_message_id:
            message_id of the message the bot just forwarded.
        :return: True
        """
        cur.execute(f"INSERT INTO msgs_to_{to_chat_id} VALUES (?,?,?)",
                    (from_chat_id, from_message_id, to_message_id))
        conn.commit()

    async def get_message_details(self, to_chat_id: int, to_message_id: int):
        """
        :param to_chat_id:
            chat_id of the message the bot forwarded.
        :param to_message_id:
            message_id of the message the bot forwarded.
        :return: a tuple containing the chat_id and message_id of the origin chat.
        """
        cur.execute(f"SELECT from_chat_id, from_message_id from msgs_to_{to_chat_id} WHERE to_message_id = ?", (to_message_id,))
        data = cur.fetchone()
        if not data:
            raise ValueError("Message not registered.")
        else:
            return data
