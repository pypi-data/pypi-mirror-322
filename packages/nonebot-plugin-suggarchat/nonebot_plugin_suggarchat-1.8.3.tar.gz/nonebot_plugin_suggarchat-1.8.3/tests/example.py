from nonebot.plugin import require
require("nonebot_plugin_suggarchat")
#先require再作导入！！！！
from nonebot import logger
from nonebot_plugin_suggarchat.on_event import on_chat,on_poke
from nonebot_plugin_suggarchat.event import ChatEvent
from nonebot_plugin_suggarchat.matcher import SuggarMatcher
from nonebot.adapters.onebot.v11 import MessageSegment
chat = on_chat()
poke = on_poke()
@chat.handle()
async def chat_logic(event:ChatEvent):
    logger.info("收到消息事件")
    logger.info(f"{event.get_event_type()}")
    logger.info(f"{event.get_send_message}")
    

@poke.handle()
async def poke_logic(event:ChatEvent):
    logger.info("收到戳一戳事件")
    logger.info(f"{event.get_event_type()}")
    
