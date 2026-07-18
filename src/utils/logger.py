# src/utils/logger.py

import logging

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO
)

def log_message(message):
    logging.info(message)