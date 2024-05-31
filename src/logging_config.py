# Process Name: 
# Please write the name of this process
# Description:  
# Please write description of process
# Inputs:       
# Please explain the inputs this process expects
# Outputs:      
# Please explain the outputs this process returns

import logging.config

# log module configuration
LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "format": "%(asctime)s %(levelname)s %(message)s",
        }
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "json",
        }
    },
    "loggers": {"": {"handlers": ["stdout"], "level": "DEBUG"}},
}

logging.config.dictConfig(LOG_CONFIG)