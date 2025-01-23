import logging
import colorlog

log_colors_config = {
    'DEBUG': 'cyan',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
}

secondary_log_colors_config = {
    'name': {
        'DEBUG': 'blue',
        'INFO': 'blue',
        'WARNING': 'blue',
        'ERROR': 'blue',
        'CRITICAL': 'blue'
    },
    'levelname': log_colors_config
}


formatter = colorlog.ColoredFormatter(
    '%(log_color)s%(asctime)s - %(name_log_color)s%(name)s - %(levelname_log_color)s%(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    log_colors=log_colors_config,
    secondary_log_colors=secondary_log_colors_config
)


# Create a handler
handler = logging.StreamHandler()
handler.setFormatter(formatter)

# Get the root logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
