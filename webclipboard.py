import clipboard
import yaml
import requests
from notifypy import Notify
import sys
import time
import base64
import signal



def outro(signal,frame):
    print("\bExiting...")
    sys.exit(0)

signal.signal(signal.SIGINT, outro)


CONF=yaml.safe_load(open('conf.yml').read())

DWEET_SEND_URL = f'https://dweet.io/dweet/for/{CONF["dweetthing"]}'
DWEET_RECV_URL = f'https://dweet.io:443/get/latest/dweet/for/{CONF["dweetthing"]}'

notification = Notify()
def notify(msg,title='WebClip'):
    notification.message = msg
    notification.title = title
    notification.send()



def recvclip(debug=False):
    try:
        __clip = requests.get(DWEET_RECV_URL).json()['with'][0]['content']['clip']
        __clip = base64.b64decode(__clip) if CONF['encoding']=='base64' else base64.b32decode(__clip)
        __clip = __clip.decode()
    except Exception as e:
        print(f'recvclip exception -> {e}\n')
        __clip = ''
    if debug: print(f'Received -> {__clip}')
    return __clip
    


def sendclip(__clip,debug=False):
    if debug: print(f'Sending -> {__clip[:5]}...')

    __clip = __clip.encode()

    encoded_clip = base64.b64encode(__clip) if CONF['encoding']=='base64' else base64.b32encode(__clip)
    if requests.get(DWEET_SEND_URL,params={'clip':encoded_clip}).status_code == 200:
        notify(f'Sent')
    else:
        notify('Sending Failed')



def intro():
    print('\n\t----------------------------------\n\tA big thanks to - http://dweet.io\n\t----------------------------------')
    print(f'\nSENDING AT -> {DWEET_SEND_URL}')
    print(f'RECEIVING AT -> {DWEET_RECV_URL}\n')


if __name__ == '__main__':

    USAGE = f'\nUsage : \n\t python {sys.argv[0]} master[,slave] [debug]\n'
    DEBUG = 0
    
    if len(sys.argv) < 2:
        print(USAGE)
        sys.exit()
    else:
        runmode = sys.argv[1]
        if len(sys.argv)>2:
            DEBUG=1 if sys.argv[2]=='debug' else 0
    
    INTERVAL = CONF['pollrate']


    intro()

    if runmode=='master':

        notify(f"Sensing clipboard every {INTERVAL} seconds")        

        LAST_CLIP = clipboard.paste()
        
        while True:
            clip = clipboard.paste()
            if clip != LAST_CLIP:
                LAST_CLIP = clip
                sendclip(clip,debug=DEBUG)
            time.sleep(INTERVAL)

    elif runmode=='slave':
        notify(f"Listening every {INTERVAL} seconds")

        LAST_CLIP = recvclip()
        
        while True:
            clip = recvclip(debug=DEBUG)
            if clip != LAST_CLIP:
                LAST_CLIP = clip
                clipboard.copy(clip)
                notify(f'Recieved')
            time.sleep(INTERVAL)

    else: 
        print (USAGE)
