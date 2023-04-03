# daily_guide
Notes and guidelines for bad memory guy

#Table of Contents
1. [Syntax notes](#1)
1.1. [Markdown](#1.1)
2. [Git and Github](#2)
2.1. [Repos](#2.1)
3. [Linux notes](#3)
3.1. [Screen](#3.1)
3.2. [Users](#3.2)
3.3. [Python installation](#3.3)
3.4. [Ports](#3.4)
3.5. [Executable python script](#3.5)
3.6. [pm2](#3.6)
4. [Python](#4)
4.1. [Linters](#4.1)
4.2. [Files and config](#4.2)
4.3. [Logging](#4.3)
4.4. [Virtual environment](#4.4)
5. [Utilities](#5)
5.1. [Anydesk](#5.1)
5.2. [CURL](#5.2)
5.3. [](#5.3)
6. [PostgreSQL](#6)
6.1. [Cyrillic encoding Windows in Psql](#6.1)
7. [Pytest](#7)

## 1. Syntax notes <a name="1"></a>

### 1.1. Markdown <a name="1.1"></a>

The reference [markdownguide.org](https://www.markdownguide.org/basic-syntax/).

## 2. Git and Github <a name="2"></a>

### 2.1. Repos <a name="2.1"></a>

Clone Repo

    git clone https://github.com/fedorkhandar/daily_guide
    
Full update Repo from **Gihtub**

    git pull origin main
    
Update Github from local repo
    
    git push origin main
    
## 3. Linux notes <a name="3"></a> 

### 3.1. Screen <a name="3.1"></a> 

The reference [Screen Manual](https://www.gnu.org/software/screen/manual/html_node/index.html)

Screen has sessions. Every session has windows.

Sessions

`screen -ls` &mdash; session list

`screen -r 'session_name'` &mdash; connection after break

`screen -D -r 'session_name'` &mdash; connection after break

`screen -S session_name` &mdash; rename current session

Windows

`CTRL + A "` &mdash; Windows list

`CTRL + A K` &mdash; Windows list

`CTRL + A A` &mdash; rename window

### 3.2. Users <a name="3.2"></a> 

поменять пользователя

    su - username
    sudo su - root

добавление пользователя в группу sudo

    usermod -a -G sudo имя_пользователя

    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get update && sudo apt-get upgrade

установить ssh

    sudo apt-get install ssh
    sudo apt install mc


### 3.3. Python installation <a name="3.3"></a>

[tgz on Python.org](https://www.python.org/ftp/python/3.11.1/Python-3.11.1.tgz)


УСТАНОВКА Python3.10

    sudo apt update && sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev pkg-config -y

    sudo apt-get install --reinstall ca-certificates
    sudo apt install software-properties-comm   on -y
    sudo -E add-apt-repository -y 'ppa:deadsnakes/ppa'

    deb http://ppa.launchpad.net/deadsnakes/ppa/ubuntu YOUR_UBUNTU_VERSION_HERE main

    # add deadsnake repo (default or nightly)
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt install python3.10

    git clone https://github.com/pypa/setuptools.git && cd setuptools && sudo python3.10 setup.py install
    sudo apt install python3.10-distutils
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10
    sudo apt install python3.10-venv

    sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.6 2
    sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1
    sudo update-alternatives --config python
    sudo update-alternatives --config python


### 3.4. Ports <a name="3.4"></a>

`sudo fuser -vn tcp`**`<PORT>`** &mdash; find who occupies the port

`kill -9`**`<PID>`** &mdash; kill it

### 3.5. Executable python script <a name="3.5"></a>

0. Write `#!/usr/bin/python3` in the first line of the `<my_script.py>`
1. `dos2unix my_script.py` &mdash; format the file
2. `chmod ugo+x my_script.py` &mdash; set the rights
3. `./my_script.py` &mdash; run it 

`sudo apt-get install dos2unix` &mdash; install **dos2unix**

### 3.6. pm2 <a name="3.6"></a>

`pm2 start myscript.py --name my_job --interpreter python3 --restart-delay 10000` &mdash; create job

`sudo pm2 restart my_job` &mdash; restart job

`sudo pm2 logs my_job` &mdash; show logs

`sudo pm2 start my_job` &mdash; start job
 
`sudo pm2 stop my_job` &mdash; stop job

## 4. Python <a name="4"></a>

### 4.1. Linters <a name="4.1"></a>

`vulture my_script.py >> _1.txt` &mdash; detects unused code (with probability)

`black my_script.py` &mdash; autoformat (changes file)

`pylint my_script.py >> _1.txt` &mdash; large linter

`flake8 my_script.py >> _1.txt` &mdash; large linter

### 4.2. Files and config <a name="4.2"></a>

Typical used file structure

    logs/log.log
    config/config.ini
    lib/mylibrary.py
    main.py
    
<details>

<summary>main.py, config/config.ini</summary>

#### main.py

    import configparser
    import logging
    import sys
    sys.path.insert(1, 'lib')
    import mylibrary

    config = configparser.ConfigParser()
    config.read("config/config.ini")
    
#### config/config.ini

    [logger]
    rootname=parser
    base_level=DEBUG
    show_level=DEBUG
    file_level=ERROR
    path_to_logs=logs/log.log
    maxbytes=26214400
    backupcount=5
    
</details>

### 4.3. Logging <a name="4.3"></a>

Filetree as in Section 4.2

<details>

<summary>config/config.ini, lib/mylogging.py, lib/mylibrary.py, parser.py</summary>
 
#### config/config.ini

    [logger]
    rootname=parser
    base_level=DEBUG
    show_level=DEBUG
    file_level=ERROR
    path_to_logs=logs/log.log
    maxbytes=26214400
    backupcount=5
    
When **backupcount** is non-zero, the system will save old log files by appending the extensions. When current logfile is filled, it is closed and renamed to log.log.1, and if files log.log.1, log.log.2, etc. 
 
#### lib/mylogging.py

    import logging
    from logging.handlers import RotatingFileHandler

    def set_loggers(config):
        s_handler = logging.StreamHandler()
        f_handler = RotatingFileHandler(
            config["logger"]["path_to_logs"], 
            maxBytes=int(config["logger"]["maxbytes"]), 
            backupCount=int(config["logger"]["backupcount"])
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

#### lib/mylibrary.py

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
        
#### parser.py

    import configparser
    import sys

    sys.path.insert(1, 'lib')
    import mylogging
    import mylibrary

    config = configparser.ConfigParser()
    config.read("config/config.ini")

    logger = mylogging.set_logger(config)
    print(logger)

    x = mylibrary.calc_smth()
    logger.error("i am in the parser")
    logger.warning("i am in the parser")
    logger.info("i am in the parser")
    logger.debug("i am in the parser")
 
 </details>

### 4.4. Virtual environment <a name="4.4"></a>


## 5. Utilities <a name="5"></a>

### 5.1. Anydesk <a name="5.1"></a>

[Howto](http://deb.anydesk.com/howto.html)

[Command line for Linux](https://support.anydesk.com/knowledge/command-line-interface-for-linux)

Run the following commands as root user:

    wget -qO - https://keys.anydesk.com/repos/DEB-GPG-KEY | apt-key add -
    echo "deb http://deb.anydesk.com/ all main" > /etc/apt/sources.list.d/anydesk-stable.list
    apt update
    apt install anydesk
    echo <password> | anydesk --set-password
    anydesk --get-id
    nano /etc/gdm3/custom.conf
        WaylandEnable=false
        [daemon]
        # Enabling automatic login
        AutomaticLoginEnable=true
        AutomaticLogin=$USERNAME

### 5.2. CURL <a name="5.2"></a>

[Конвертер CURL-запросов](https://curlconverter.com/)

### 5.3. <a name="5.3"></a>


## 6. PostgreSQL <a name="6"></a>

### 6.1. Cyrillic encoding Windows in Psql <a name="6.1"></a>
    
    Запустить cmd.exe, нажать мышью в правом левом верхнем углу окна, там Свойства - Шрифт - выбрать Lucida Console. Нажать ОК.
    
    Выполнить команду: chcp 1251
    В ответ выведет: Текущая кодовая страница: 1251
    
    Запустить psql;
    psql -d ВАШАБАЗА -U ВАШЛОГИН
    
    Кстати, обратите внимание - теперь предупреждения о несовпадении кодировок нет.
    Выполнить: set client_encoding='win1251';
    Он выведет: SET

## 7. Pytest <a name="7"></a>
