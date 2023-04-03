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

 sudo pm2 start my_job` &mdash; start job
 
sudo pm2 stop my_job` &mdash; stop job

