import os
import time
import logging
import threading
import codecs
import requests



def setlog():
    # set stdout
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)

    # log
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    log.addHandler(ch)

    return log
 
logger = setlog()

def parse(idname, text):
    text = text.strip()
    data = {}
    for t in text.split('\n'):
        key = t.split(':')[0]
#        logger.debug(key)
        value = ':'.join(t.split(':')[1:])
#        logger.debug(value)
        if key in ['Location', 'Duration']:
            value = int(value.split('.')[0])
        if key in ['UserId']:
            value = idname
        data[key] = value
#   logger.debug('data:',data)
    print('data:',data)
    return data

def load(idname, filename='data1.txt'):
    with open(filename) as f:
        text = f.read()
        print(text)
        datas = [parse(idname, t) for t in text.split('-')]
 #       logger.debug(datas)
        return datas
  

def heartbeat(url, data):
    return requests.post(url, data=data)

def loop(data):
    url = 'http://47.104.182.113/adks-spcrm/rest/AddCourse'
    while data['Location'] <= data['Duration']:
        r = heartbeat(url, data)
        logger.debug(r.status_code)
        time.sleep(5)
        data['Location'] += 5

def main():
    idname = input('please enter your id: ')
    logger.debug(idname)
    datas = load(idname)
    threads = []
  
    for data in datas:
#        os.system('pause')
        t = threading.Thread(target=loop, args=(data, ))
        threads.append(t)
        t.start()
        logger.debug(t, 'Thread start')

if __name__ == '__main__':
    main()