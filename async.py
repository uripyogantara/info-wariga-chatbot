import sys
from response import response
import asyncio
import telepot
from telepot.aio.loop import MessageLoop
from telepot.aio.delegate import pave_event_space, per_chat_id, create_open

class MessageCounter(telepot.aio.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(MessageCounter, self).__init__(*args, **kwargs)
        self._count = 0

    async def on_chat_message(self, msg):
        self._count += 1
        res = response()

        # print(msg["text"].lower())
        result = res.get_response(msg["text"].lower())
        print(result)

        for item in result:
            print(str(item))
            await self.sender.sendMessage(str(item))

TOKEN = "796693170:AAFb0M0YAuRMJgz83eus-Qfv_uPDgR5BKUY"

bot = telepot.aio.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, MessageCounter, timeout=10),
])

loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(bot).run_forever())
print('Listening ...')

loop.run_forever()