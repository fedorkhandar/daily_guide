# daily_guide
Notes and guidelines for bad memory guy

## 1. Syntax notes

### 1.1. Markdown

The reference [markdownguide.org](https://www.markdownguide.org/basic-syntax/).

## 2. Git and Github notes

### 2.1. Git

### 2.2. Github

## 3. Linux notes

### 3.1. Screen

### 3.2. Users

### 3.3. Python installation

### 3.4. Ports

`sudo fuser -vn tcp`**`<PORT>`** &mdash; Find who occupies the port

`kill -9`**`<PID>`** &mdash; Kill it

### 3.4. Executable python script

0. Write `#!/usr/bin/python3` in the first line of the `<my_script.py>`
1. `dos2unix my_script.py` &mdash; format the file
2. `chmod ugo+x my_script.py` &mdash; set the rights
3. `./my_script.py` &mdash; run it 

`sudo apt-get install dos2unix` &mdash; install **dos2unix**

### 3.5. pm2

`pm2 start myscript.py --name my_job --interpreter python3 --restart-delay 10000` &mdash; create job

`sudo pm2 restart my_job` &mdash; restart job

`sudo pm2 logs my_job` &mdash; show logs

`sudo pm2 start my_job` &mdash; start job
 
`sudo pm2 stop my_job` &mdash; stop job

## 4. Python

### 4.1. Linters

`vulture my_script.py >> _1.txt` &mdash; detects unused code (with probability)

`black my_script.py` &mdash; autoformat (changes file)

`pylint my_script.py >> _1.txt` &mdash; large linter

`flake8 my_script.py >> _1.txt` &mdash; large linter

### 4.2. Files and config

Filetree

    logs/log.log
    config/config.ini
    lib/mylibrary.py
    main.py

main.py

    import configparser
    import logging
    import sys
    sys.path.insert(1, 'lib')
    import mylibrary

    config = configparser.ConfigParser()
    config.read("config/config.ini")
    
config/config.ini

    [logger]
    rootname=parser
    base_level=DEBUG
    show_level=DEBUG
    file_level=ERROR
    path_to_logs=logs/log.log
    log_size=26214400
    
### 4.3. Logging

Filetree as in [Section 4.2](#4.2.-files-and-config)

config.ini

    [logger]
    rootname=parser
    base_level=DEBUG
    show_level=DEBUG
    file_level=ERROR
    path_to_logs=logs/log.log
    log_size=26214400
    
When **backupcount** is non-zero, the system will save old log files by appending the extensions. When current logfile is filled, it is closed and renamed to log.log.1, and if files log.log.1, log.log.2, etc. 
 
mylogging.py

    import logging
    from logging.handlers import RotatingFileHandler

    def set_loggers(config):
        s_handler = logging.StreamHandler()
        f_handler = RotatingFileHandler(
            config["logger"]["path_to_logs"], maxBytes=26214400, backupCount=1
        )

        s_format = logging.Formatter(
            "%(name)s - %(levelname)s - %(message)s"
        )
        f_format = logging.Formatter(
            "%(name)s - %(asctime)s - %(message)s"
        )
        s_handler.setFormatter(s_format)
        f_handler.setFormatter(f_format)

        if config["logger"]["show_level"] == "DEBUG":
            s_handler.setLevel(logging.DEBUG)
        elif config["logger"]["show_level"] == "INFO":
            s_handler.setLevel(logging.INFO)
        elif config["logger"]["show_level"] == "WARNING":
            s_handler.setLevel(logging.WARNING)
        else:
            s_handler.setLevel(logging.ERROR)

        if config["logger"]["file_level"] == "DEBUG":
            f_handler.setLevel(logging.DEBUG)
        elif config["logger"]["file_level"] == "INFO":
            f_handler.setLevel(logging.INFO)
        elif config["logger"]["file_level"] == "WARNING":
            f_handler.setLevel(logging.WARNING)
        else:
            f_handler.setLevel(logging.ERROR)
            
        
        return s_handler, f_handler
        
    def set_logger(config):
        logger = logging.getLogger(config["logger"]["rootname"])
        if config["logger"]["base_level"] == "DEBUG":
            logger.setLevel(logging.DEBUG)
        elif config["logger"]["base_level"] == "INFO":
            logger.setLevel(logging.INFO)
        elif config["logger"]["base_level"] == "WARNING":
            logger.setLevel(logging.WARNING)
        else:
            logger.setLevel(logging.ERROR)
            
        s_handler, f_handler = set_loggers(config)
        logger.addHandler(s_handler)
        logger.addHandler(f_handler)

        return logger

liba.py

    import configparser
    import logging

    config = configparser.ConfigParser()
    config.read("config/config.ini")
    module_logger = logging.getLogger(config["logger"]["rootname"] + "." + __name__)

    def calc_smth():
        module_logger.error("calc_smth: x")
        module_logger.warning("calc_smth: x")
        module_logger.info("calc_smth: x")
        module_logger.debug("calc_smth: x")
        pass
        
parser.py

    import configparser
    import sys

    sys.path.insert(1, 'lib')
    import mylogging
    import liba

    config = configparser.ConfigParser()
    config.read("config/config.ini")

    logger = mylogging.set_logger(config)
    print(logger)

    x = liba.calc_smth()
    logger.error("i am in the parser")
    logger.warning("i am in the parser")
    logger.info("i am in the parser")
    logger.debug("i am in the parser")
