__version__ = "0.1.0"
__author__ = "Sifat Hasan <sihabhossan633@gmail.com>"
__license__ = "MIT"

# Package-level imports
from .cli import cli
from .api import DeepSeekClient
from .config import ConfigManager
from .formatter import format_stream, format_error, format_code

__all__ = [
    'cli',
    'DeepSeekCLIClient',
    'ConfigManager',
    'format_stream',
    'format_error',
    'format_code'
]