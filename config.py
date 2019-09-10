import logging

DB_NAME = "CurrencyEye.db"

HTTP_TIMEOUT = 15

IP_LIST = ["127.0.0.1", "127.0.0.10"]

LOGGING = {
    'version': 1,
    'formatters': {
        'default': {
            'format': "[%(asctime)s] [%(levelname)s] - %(name)s: %(message)s",
        },
    },

    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'filename': 'new.log',
        },
    },
    'loggers': {
        'CurrencyEye': {
            'handlers': ['file', ],
            'level': logging.DEBUG
        },
        'Api': {
            'handlers': ['file',],
            'level': logging.DEBUG
        },
        'Tasks': {
            'handlers': ['file',],
            'level': logging.DEBUG
        },
    },
}
