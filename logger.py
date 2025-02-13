import logging
import os


def setup_logger(repo_name, branch):

    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, f"{repo_name}_{branch}.log")

    # Configure logging
    logging.basicConfig(
        filename=log_file,
        filemode="a",
        format="%(asctime)s - %(levelname)s -  %(message)s",
        level=logging.INFO
    )

    # create a logger instance
    logger = logging.getLogger(__name__)

    # Add a separator line at the start of each script execution
    logger.info("\n" + "-" * 50 + "\nStarting run....\n" + "-" * 50)

    return logger
