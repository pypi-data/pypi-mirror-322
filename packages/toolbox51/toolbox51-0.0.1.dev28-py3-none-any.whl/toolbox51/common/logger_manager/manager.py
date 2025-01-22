# ruff: noqa: E402 - Module level import not at top of file


import asyncio
import logging
import time

from ..singleton import SingletonMeta
from ..logging import touch_logger, new_logger


class LoggerManager(metaclass=SingletonMeta):
    
    default_level: int
    use_relative_path: bool
    record: dict[str, float] = {}
    logger: logging.Logger
    secondary_logger: logging.Logger
    
    def __init__(self, default_level:int = logging.DEBUG, use_relative_path:bool = False) -> None:
        self.default_level = default_level
        self.use_relative_path = use_relative_path
        self.logger = new_logger("MANAGER_GLOBAL", level=self.default_level, use_relative_path=use_relative_path)
        self.secondary_logger = new_logger("MANAGER_SECONDARY", level=self.default_level, use_relative_path=use_relative_path)
        
    def set_default_level(self, level: int) -> None:
        self.default_level = level
        self.logger.setLevel(level)
        self.secondary_logger.setLevel(level)
        
    def use_relative_path_on(self) -> None:
        self.use_relative_path = True
        self.logger = new_logger("MANAGER_GLOBAL", level=self.default_level, use_relative_path=True)
        self.secondary_logger = new_logger("MANAGER_SECONDARY", level=self.default_level, use_relative_path=True)
        
    def use_relative_path_off(self) -> None:
        self.use_relative_path = False
        self.logger = new_logger("MANAGER_GLOBAL", level=self.default_level, use_relative_path=False)
        self.secondary_logger = new_logger("MANAGER_SECONDARY", level=self.default_level, use_relative_path=False)

    def register(self, name:str) -> logging.Logger:
        self.record[name] = now_time = time.time()
        
        # 清除长期不用的logger
        to_delete = [k for k, v in self.record.items() if now_time - v > 600]
        for item in to_delete:
            self.unregister(item)
        
        return touch_logger(name, level=self.default_level, use_relative_path=self.use_relative_path)
        
    def unregister(self, name:str) -> None:
        self.record.pop(name)
        try:
            logger = touch_logger(name)
            handlers = logger.handlers[:]
            for handler in handlers:
                logger.removeHandler(handler)
                handler.close()
            logger.name in logging.Logger.manager.loggerDict and\
                logging.Logger.manager.loggerDict.pop(logger.name) # type: ignore
        except Exception:
            pass
    
    @property
    def current_logger(self) -> logging.Logger:
        try:
            current_task = asyncio.current_task()
            current_name = current_task.get_name() if current_task else "MANAGER_GLOBAL"
            if(current_name not in self.record):
                logger = self.register(current_name)
                return logger
            self.record[current_name] = time.time()
            return touch_logger(name=current_name)
        except RuntimeError:
            return self.logger
        except Exception:
            return self.secondary_logger
    
    def debug(self, msg: object, stacklevel: int = 1) -> None:
        msg_s = self._obj2str(msg)
        self.current_logger.debug(msg_s, stacklevel=stacklevel+1)
    
    def info(self, msg: object, stacklevel: int = 1) -> None:
        msg_s = self._obj2str(msg)
        self.current_logger.info(msg_s, stacklevel=stacklevel+1)
    
    def warning(self, msg: object, stacklevel: int = 1) -> None:
        msg_s = self._obj2str(msg)
        self.current_logger.warning(msg_s, stacklevel=stacklevel+1)
    
    def error(self, msg: object, stacklevel: int = 1) -> None:
        msg_s = self._obj2str(msg)
        self.current_logger.error(msg_s, stacklevel=stacklevel+1)
    
    def critical(self, msg: object, stacklevel: int = 1) -> None:
        msg_s = self._obj2str(msg)
        self.current_logger.critical(msg_s, stacklevel=stacklevel+1)
    
    def _obj2str(self, obj:object) -> str:
        match obj:
            case list():
                return " ".join([self._obj2str(x) for x in obj])
            case str():
                return obj
            case int() | float() | bool():
                return str(obj)
            case _:
                return str(obj)
            
from ..utils import inspect_stack_check

if(inspect_stack_check(["unittest", "pytest"])):
    logger = LoggerManager(use_relative_path=False)
    logger.debug("在测试模式中启用")
else:
    logger = LoggerManager(use_relative_path=True)