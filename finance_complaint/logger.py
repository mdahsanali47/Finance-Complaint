import os
import logging
from datetime import datetime

from from_root import from_root

LOG_FILE = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}-log"

log_path = os.path.join(from_root("logs"), LOG_FILE)
os.makedirs(log_path, exist_ok=True)
 
LOG_FILE_PATH = os.path.join(log_path, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s",
    level=logging.INFO
)