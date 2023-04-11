#!/usr/bin/python3
"""
test client application
sends id and xml_b64
"""
import codecs
import configparser
import requests
import sys

config = configparser.ConfigParser()
config.read("../config/config.ini")

def get_content(fname):
    content = codecs.open(fname, "r", "utf-8").read()
    
    if config['server']['is_xml_b64'] == 1:
        b = base64.b64encode(bytes(content, 'utf-8')) # bytes
        base64_str = b.decode('utf-8') # convert bytes to string    
        
        return base64_str
    else:
        return content
        
def get_id():
    """
    gets id
    """
    return "2-12-85-06"

def send_file(server_url, fname):
    """
    b64_flag = True => in fname b64
    """
    content = get_content(fname)
    data = {
        'id': get_id(),
        'data': content
    }

    r = requests.post(server_url, json=data)

    if r.status_code == 200:
        with codecs.open("result.txt", "w", "utf-8") as fout:
            print(r.json(), file = fout)
    else:
        print(r.text)
            


basefname = sys.argv[1]
server_url = f"http://{config['server']['host']}:{config['server']['port']}/{config['server']['path']}"
b64_flag = True

send_file(server_url, basefname)