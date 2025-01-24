import pytest
from jiragen.core.config import ConfigManager
from loguru import logger
import sys

logger.remove()
logger.add(sys.stderr, level="DEBUG")

def test_configmanager():
    config_manager = ConfigManager()
    config_manager.load_config()
    print(config_manager.config)
    llm_config_dict = dict(config_manager.config["llm"])
    print(llm_config_dict)


if __name__ == "__main__":
    test_configmanager()
