import logging
import os
from datetime import datetime

# Create logs directory if it doesn't exist
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Generate log file name based on date & time
LOG_FILE = f"{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.log"
LOG_PATH = os.path.join(LOG_DIR, LOG_FILE)

# Configure logging
logging.basicConfig(
    filename=LOG_PATH,
    format="[ %(asctime)s ] %(levelname)s - %(name)s - %(message)s",
    level=logging.INFO,
)

# ------------ TEST LINE TO CHECK IF IT WORKS -------------
logging.info("Logging system is working properly!")
# ----------------------------------------------------------
