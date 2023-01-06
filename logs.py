import logging
import pathlib
import logging.handlers
import datetime

def file_renamer(filename):
    split = filename.split('.')
    return ".".join(split[:-3] + [split[-1], split[-2]])


def setUpLogger(loggers):
    logger = logging.getLogger(loggers)
    logger.setLevel(logging.DEBUG)
    
    logs_dir = pathlib.Path('logs')
    logs_dir.mkdir(exist_ok=True)
    # Create a handler that records all activity
    everything = logging.handlers.TimedRotatingFileHandler(logs_dir / f'ALL-LOGS.tennisbot.{format(datetime.datetime.today(), "%Y-%m-%d")}.log',
                                                           when='midnight', encoding='UTF-8')
    # Do not use loggging.NOTSET, does not work for some reason
    # use logging.DEBUG if you want the lowest level
    everything.setLevel(logging.DEBUG)

    # Create a handler that records only ERRORs and CRITICALs
    errors_only = logging.handlers.TimedRotatingFileHandler(logs_dir / f'ONLY-ERRORS-CRITICALS.tennisbot.{format(datetime.datetime.today(), "%Y-%m-%d")}.log',
                                                            when='midnight', encoding='UTF-8')
    errors_only.setLevel(logging.ERROR)

    # Rename files so .log is the file extension
    everything.namer, errors_only.namer = (file_renamer,) * 2
    
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    everything.setFormatter(formatter)
    errors_only.setFormatter(formatter)
    

    # Add handlers to the logger
    logger.addHandler(everything)
    logger.addHandler(errors_only)

    # Create a handler so we can see the output on the console
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)

    # Add handler to the logger
    logger.addHandler(console)