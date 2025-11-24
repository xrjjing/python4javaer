"""logging 基本用法示例。"""

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)

logger.info("程序启动")
logger.warning("这是一个警告")

try:
    1 / 0
except ZeroDivisionError:
    logger.error("发生除零错误", exc_info=True)


