import logging

logger = logging.getLogger("BeatViewer")
logger.setLevel(logging.DEBUG)

fmt = "\033[33m[\033[0m\033[32mBeatViewer\033[33m]\033[0m"

formatter = logging.Formatter(f"{fmt} \033[90m%(asctime)s\033[0m: %(levelname)s %(message)s",
                              datefmt="%Y-%m-%d %H:%M:%S")

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

logging.addLevelName(logging.INFO, "\x1b[0;30;44mINFO\x1b[0m")
logging.addLevelName(logging.WARNING, "\x1b[0;30;43mWARNING\x1b[0m")
logging.addLevelName(logging.ERROR, "\x1b[0;30;41mERROR\x1b[0m")
logging.addLevelName(logging.CRITICAL, "\x1b[0;30;45mCRITICAL\x1b[0m")
logging.addLevelName(logging.DEBUG, "\x1b[0;30;46mDEBUG\x1b[0m")

logger.addHandler(console_handler)