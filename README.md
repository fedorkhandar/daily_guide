# daily_guide
Notes and guidelines for bad memory guy

# Table of Contents

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
4.5 [aiohttp](#4.5)
4.6. [b64](#4.6)
4.7. [Timer](#4.6)
5. [Utilities](#5)
5.1. [Anydesk](#5.1)
5.2. [CURL](#5.2)
5.3. [](#5.3)
6. [PostgreSQL](#6)
6.1. [Cyrillic encoding Windows in Psql](#6.1)
6.2. [Extensions](#6.2)
7. [Pytest](#7)
8. [The Process](#8)
8.1. [Steps](#8.1)
9. [Hardware](#9)
9.0. [Test 0](#9.0)
9.1. [Port Forwarding (D-link 615)](#9.1)
9.2. [Test](#9.2)
10. [Docker](#10)
10.1 [Installation on Windows](#10.1)
11. [Notepad +](#11)
11.1. [Execution Python scripts from the Notepad ++](#11.1)
11.2. [JSON and XML plugins](#11.2)

### Table of contents finishes

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

Change Git Owner on local machine

### 2.2. Credentials
    
    On Windows PC simply use OS's interface:
    1. Go to Credential Manager (Диспетчер учетных данных)
    2. Windows Credentials
    3. Delete entries under the Generic Credentials
    

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

[A Complete Guide to Python Virtual Environments](https://www.dataquest.io/blog/a-complete-guide-to-python-virtual-environments/)

### 4.5 aiohttp send post request <a name="4.5"></a>

Send smth as:
    
    async def send_smth(url, headers, data):
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data) as response:
                return response.text
                
    url = ''
    headers = ''
    data = ''
    send_smth(url, headers, data)
    
### 4.6. b64 <a name="4.6"></a>

    encoding

### 4.7. Timer <a name="4.6"></a>
    
    import time
    start = time.time()
    print(time.time()-start())
    
### 4.8. aiohttp handler <a name="4.8"></a>

#### config/config.ini

    [server]
    port = 9161
    path = my_service
    host=localhost
    ;http://localhost:9161/my_service

#### server.py

    def main():
        app = web.Application(client_max_size=4096**2)
        app.add_routes([web.post("/" + config["server"]["path"], handler)])
        web.run_app(app, port=config["server"]["port"])

    if __name__ == "__main__":
        main()

#### client/client.py
    
    import configparser
    
    config = configparser.ConfigParser()
    config.read("../data/config.ini")
    
    basefname = sys.argv[1]
    server_url = f"http://{config['server']['host']}:{config['server']['port']}/{config['server']['path']}"




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

### 6.2. Extensions <a name="6.2"></a>
    
Psql:

    DROP EXTENSION "uuid-ossp";
    SET SCHEMA 'schema_name';
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    \df

It would show:

    ...
    uuid_generate_v4
    ...
    
in Python script creating DB structure use :
    
    f"message_id UUID NOT NULL DEFAULT {schema_name}.uuid_generate_v4(),"
    

## 7. Pytest <a name="7"></a>

## 8. The Process <a name="8"></a>

### 8.1. Steps <a name="8.1"></a>
[The Good way to structure a Python Project](https://towardsdatascience.com/the-good-way-to-structure-a-python-project-d914f27dfcc9)
1. Create separate **virtual environment**

    * WARNING! **venv** doesn't work in 'Far Manager' on Windows

2. Create separate **tests** folder
3. Use **project template**
4. **Document** everything immediately
4.1. **Comment** code
4.2. Make notes to **daily guide**
5. Use **Git**

    * WARNING! Don't work inside **Cloud Storage Folders**

## 9. Hardware <a name="9"></a>

### 9.0. Test 0 <a name="9.0"></a>

### 9.1. Port Forwarding (D-link 615) <a name="9.1"></a>

[Enable port forwarding for the D-Link DIR-615
](https://www.cfos.de/en/cfos-personal-net/port-forwarding/d-link-dir-615.htm)

### 9.2. Test <a name="9.2"></a>

## 10. Docker <a name="10"></a>

### 10.1 Installation on Windows <a name="10.1"></a>

## 11. Notepad ++<a name="11"></a>

### 11.1. Execution Python scripts from the Notepad ++ <a name="11.1"></a>

We assumed:
- *Python is in PATH*
- *It's not about VENV*

SETTINGS AND USE:

1. Install plugin 'NppExec'
2. Configure it - mark just these 3 menu items:
    - Show NppExec Console
    - No internal messages
    - Follow $(CURRENT DIRECTORY)
3. Use it:
    - Press F6 on Python script tab
    - Write and Save command "Python $(FILE_NAME)"


### 11.2. JSON and XML plugins <a name="11.2"></a>

### 12. Decorators <a name="12"></a>
Python decorators are a powerful feature that can help you become a more efficient and productive Python developer. Here are some compelling examples of benefits of using Python decorators:

1. Code Reusability: Python decorators allow you to reuse code across multiple functions. Instead of writing the same code for multiple functions, you can use a decorator to add the desired functionality to each function. This avoids code duplication and makes your code more maintainable.

2. Functionality Extension: Python decorators allow you to extend the functionality of a function, method, or class without modifying the original code. This means that you can add new features to your code without changing the existing behavior of the code. For example, you can use a decorator to add logging, caching, or performance testing to a function.

3. Separation of Concerns: Python decorators allow you to separate concerns in your code. You can use a decorator to add cross-cutting concerns such as logging or error handling to your code, without cluttering the code with these concerns. This makes your code more modular and easier to maintain.

4. Easy to Use: Python decorators are easy to use and require minimal code changes. You simply define a decorator function and apply it to the desired function using the `@decorator` syntax. This makes it easy to add new functionality to your code.

5. Readability: Python decorators can improve the readability of your code. By using decorators, you can separate concerns and make your code more modular. This makes it easier to understand the code and reduces the cognitive load on the reader.

6. Clean Code: Python decorators can help you write clean code. By separating concerns and reusing code, you can reduce code duplication and make your code more maintainable. This makes it easier to add new features and fix bugs in your code.

Overall, Python decorators are a powerful feature that can help you write more efficient, modular, and maintainable code. They allow you to separate concerns, reuse code, and extend the functionality of your code without modifying the original code.

Here are 5 best practices of using Python decorators:

1. Use functools.wraps() to preserve function metadata: When creating a decorator, it's important to preserve the metadata of the original function such as its name and docstring. This can be done using the `functools.wraps()` decorator. This ensures that the original function can still be identified properly, even after it has been decorated.

```python
import functools

def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Do something before the function is called
        result = func(*args, **kwargs)
        # Do something after the function is called
        return result
    return wrapper
```

2. Use class-based decorators for complex functionality: For complex functionality, it may be better to use a class-based decorator instead of a function-based decorator. This allows you to encapsulate the decorator logic in a separate class, making the code more modular.

```python
class MyDecorator:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        # Do something before the function is called
        result = self.func(*args, **kwargs)
        # Do something after the function is called
        return result

@MyDecorator
def my_function():
    pass
```

3. Document your decorators: It's important to document your decorators so that other developers can understand how they work and how to use them. Use docstrings to provide clear and concise documentation for your decorators.

```python
def my_decorator(func):
    """
    This is a decorator that does something.
    """
    def wrapper(*args, **kwargs):
        # Do something before the function is called
        result = func(*args, **kwargs)
        # Do something after the function is called
        return result
    return wrapper
```

4. Use decorators sparingly: While decorators can be a powerful tool, it's important to use them sparingly. Overuse of decorators can make the code hard to read and understand. Use decorators only when they provide a clear benefit to the code.

5. Use the @wraps decorator for debugging: When debugging code that uses decorators, it can be helpful to use the `@wraps` decorator. This will ensure that the original function's metadata is preserved, making it easier to identify the function during debugging.

```python
import functools

def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Do something before the function is called
        result = func(*args, **kwargs)
        # Do something after the function is called
        return result
    return wrapper
```

Sources:
- [RealPython](https://realpython.com/primer-on-python-decorators/)
- [The Digital Cat](https://www.thedigitalcatonline.com/blog/2015/04/23/python-decorators-metaprogramming-with-style/)
- [CodeMentor](https://www.codementor.io/@sheena/advanced-use-python-decorators-class-function-du107nxsv)
- [FreeCodeCamp](https://www.freecodecamp.org/news/python-decorators-explained-with-examples/)
- [Python Documentation](https://docs.python.org/3/library/functools.html#functools.wraps)
