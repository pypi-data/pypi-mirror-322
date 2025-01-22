from nonebot.adapters import Event, Message, Bot
from nonebot import on_message,on_command
import random
from nonebot.plugin import PluginMetadata
from nonebot_plugin_session import extract_session, SessionIdType
from nonebot.rule import to_me
from nonebot.params import CommandArg

from .config import Config
from .config import config

__plugin_meta__ = PluginMetadata(
    name="随机复读插件",
    description="简单的随机复读插件",
    usage="可以随机复读上一条信息(包括图片,表情包)",
    type="application",
    homepage="https://github.com/hriyel/nonebot_reply.git",
    config=Config,
    supported_adapters={"~onebot.v11"},
    extra={},
)

group_whitelist = config.group_whitelist  
repeat_frequency = config.repeat_frequency
reply = on_message(priority=3, block=False)
repl = on_command("flag change",rule=to_me(),aliases={"状态调整"},priority=2,block=False)

text = {}  # 存储当前消息
flag = True
words = ""

def should_repeat(group_id): #判断是否复读  
    if random.randint(1, repeat_frequency) == 1:
        return True

@repl.handle()
async   def rel_handle(args:Message = CommandArg()):
    global  flag    
    if flag == True:
        flag = False
    else:
        flag = True
    status = flag
    words = f"已将复读插件状态调整为{status}"
    await repl.send(words)
    
@reply.handle()
async def plush_handler(bot: Bot, event: Event):
    global text
    session = extract_session(bot, event)
    group_id = session.get_id(SessionIdType.GROUP).split("_")[-1]
    
    if group_id not in group_whitelist and flag == True:
        return
    
    msg = event.get_message()
    
    if should_repeat(group_id) == True:
        await reply.send(msg)