import logging

# Configure logging
logging.basicConfig(
    filename="app.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s -  %(message)s",
    level=logging.INFO
)

# create a logger instance
logger = logging.getLogger(__name__)

# Add a separator line at the start of each script execution
logger.info("\n" + "-" * 50 + "\nStarting run....\n" + "-" * 50)
