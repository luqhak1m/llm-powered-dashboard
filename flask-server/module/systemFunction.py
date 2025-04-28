import logging

# Configure logging
logging.basicConfig(
    filename='app.log',  # Logs will be stored in 'app.log'
    level=logging.INFO,   # Set logging level
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log format
)

def log_message(message):
    """Logs the given message."""
    logging.info(message)