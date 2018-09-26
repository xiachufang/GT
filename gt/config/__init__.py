from .database import DatabaseConfig
from .yuque import YuqueConfig

DB_CONFIG = DatabaseConfig()
YUQUE_CONFIG = YuqueConfig()

__all__ = ['DB_CONFIG', 'YUQUE_CONFIG']
