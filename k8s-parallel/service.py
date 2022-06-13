import logging
import os
import time

log_file = "service.log"

logging.basicConfig(
        filename=log_file,
        filemode='a',
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s : %(message)s',
        level=logging.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S')

logging.debug("This is the line before getting the env variable")
logging.debug(os.getenv('JOB_COMPLETION_INDEX'))
time.sleep(300)
logging.debug("This is the line after getting the env variable")
