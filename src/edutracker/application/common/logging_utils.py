import logging

def log_requested(logger, action: str, **kwargs):
    logger.info(f"{action} requested", extra=kwargs)

def log_computed(logger, action: str, **kwargs):
    logger.info(f"{action} computed", extra=kwargs)