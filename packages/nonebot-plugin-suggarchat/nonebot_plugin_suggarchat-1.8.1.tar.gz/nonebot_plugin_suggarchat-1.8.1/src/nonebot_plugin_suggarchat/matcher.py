from typing import Callable, List, Awaitable, Optional,override
import asyncio
import inspect
from nonebot import logger
from nonebot.exception import ProcessException,FinishedException,StopPropagation
from .event import SuggarEvent,FinalObject
import sys
from nonebot.adapters.onebot.v11 import MessageSegment
from .exception import BlockException,PassException,CancelException
"""
suggar matcher
用于触发Suggar中间件事件
"""
event_handlers = {}
running_tasks = []
handler_infos = {}
async def run_handle(handler, event, **args):
        await handler(event, **args)
        
class SuggarMatcher:
  event:SuggarEvent
  __processing_message:MessageSegment

  def __init__(self, event_type: str = ""):
        # 存储事件处理函数的字典
        global event_handlers,running_tasks
        self.event_handlers = event_handlers
        self.handler_infos = handler_infos
        self.running_tasks = running_tasks
        self.event_type = event_type
  
  def handle(self, event_type = None):
    if event_type==None and self.event_type != "":
        event_type = self.event_type
    def decorator(func: Callable[[Optional[SuggarEvent]], Awaitable[None]]):
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
            self.handler_infos[event_type] = {}
        self.event_handlers[event_type].append(func)
        self.handler_infos[event_type][func.__name__] = {"func":func,"signature":inspect.signature(func),"frame":inspect.currentframe().f_back}
        return func
    return decorator
  def stop(self):
    for task in self.running_tasks:
        try:
            task.cancel()
            
        except asyncio.CancelledError:
            logger.info(f"Task cancelled")
        except Exception as e:
            logger.error(f"cancelling task Error")
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logger.error(f"Exception type: {exc_type.__name__}")
            logger.error(f"Exception message: {str(exc_value)}")
            import traceback
            logger.error(traceback.format_tb(exc_traceback))
    self.running_tasks.clear()
  def stop_process(self):
      """
      阻止当前Suggar事件循环继续运行并立即停止当前的处理器。
      """
      raise BlockException()
  def cancel(self):
      """
      停止Nonebot层的处理器
      """
      raise FinishedException()
  def cancel_matcher(self):
      """
      停止当前Suggar事件处理并取消。
      """
      raise CancelException()
  def cancel_nonebot_process(self):
      """
      直接停止Nonebot的处理流程，不触发任何事件处理程序。
      """
      raise StopPropagation()
  def pass_event(self):
      """
      忽略当前处理器，继续处理下一个。
      """
      raise PassException()
  def append_message(self, message: MessageSegment) -> None:
        """
        在消息末尾追加内容

        :param message: 要追加的消息内容
        """
        self.__processing_message += message
  def set_message(self, value: MessageSegment) -> None:
        """
        设置消息内容

        :param value: 新的消息内容
        """
        self.__processing_message = value

  def apphead_message(self, value: MessageSegment) -> None:
        """
        在消息开头添加内容

        :param value: 要添加的消息内容
        """
        self.__processing_message = value + self.__processing_message
  async def trigger_event(self, event: SuggarEvent, **kwargs)->SuggarEvent:
    
    """
    触发特定类型的事件，并调用该类型的所有注册事件处理程序。
    
    参数:
    - event: SuggarEvent 对象，包含事件相关数据。
    - **kwargs: 关键字参数，包含事件相关数据。
    """
    event_type = event.get_event_type()  # 获取事件类型
    self.event = event
    self.__processing_message = event.message
    logger.info(f"Start running suggar event: {event_type}")
    # 检查是否有处理该事件类型的处理程序
    if event_type in self.event_handlers:
        
        # 遍历该事件类型的所有处理程序
        for handler in self.event_handlers[event_type]:
            # 获取处理程序的签名
            sig = inspect.signature(handler)
            info = self.handler_infos[event_type][handler.__name__]
            line_number = info['frame'].f_lineno
            file_name = info['frame'].f_code.co_filename
            # 获取参数类型注解
            params = sig.parameters
            # 构建传递给处理程序的参数字典
            args = {}
            for param_name, param in params.items():
                if param.annotation in kwargs:
                    args[param_name] = kwargs[param.annotation]
            # 调用处理程序
            try:
                logger.info(f"start running processing matcher '{handler.__name__}'(~{file_name}:{line_number})")
                
                await run_handle(handler, event, **args)
            except ProcessException as e:
                logger.info("Matcher stopped.")
                raise e
            except PassException:
                logger.info("Matcher pass.")
                continue
            except CancelException:
                logger.info("Matcher cancelled.")
                return
            except BlockException:
                break
            except Exception as e:
                logger.error(f"Error running suggar at file {inspect.getfile(handler)}")
                exc_type, exc_value, exc_traceback = sys.exc_info()
                logger.error(f"Exception type: {exc_type.__name__}")
                logger.error(f"Exception message: {str(exc_value)}")
                import traceback
                logger.error(traceback.format_tb(exc_traceback))
                continue
            finally:
                
                
                logger.info(f"matcher running done file {inspect.getfile(handler)} ")
        
    else:logger.info(f"No handler for event type: {event_type},skipped this event")
    return FinalObject(self.__processing_message)       