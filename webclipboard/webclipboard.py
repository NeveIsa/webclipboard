import clipboard
import yaml
import requests
from notifypy import Notify
import beepy
import sys
import time
import base64
import signal



def outro(signal,frame):
    print("\bExiting...")
    sys.exit(0)

signal.signal(signal.SIGINT, outro)

def intro():
    asciiart=''' 
                     _            _  _         _                             _
                    | |          | |(_)       | |                           | |
     __      __ ___ | |__    ___ | | _  _ __  | |__    ___    __ _  _ __  __| |
     \ \ /\ / // _ \| '_ \  / __|| || || '_ \ | '_ \  / _ \  / _` || '__|/ _` |
      \ V  V /|  __/| |_) || (__ | || || |_) || |_) || (_) || (_| || |  | (_| |
       \_/\_/  \___||_.__/  \___||_||_|| .__/ |_.__/  \___/  \__,_||_|   \__,_|
                                       | |
                                       |_| ❤ ❤ ❤ USC MATH499 FALL2020  ❤ ❤ ❤
    '''
    print(asciiart)
    print('\n\t\t\t----------------------------------\n\t\t\tA big thanks to - http://dweet.io\n\t\t\t----------------------------------')



class Webclipboard:

    CONF={'encoding':'base64','pollrate':5}
    
    def __init__(self,dweetthing='webclipboard'):
        self.DWEET_SEND_URL = f'https://dweet.io/dweet/for/{dweetthing}'
        self.DWEET_RECV_URL = f'https://dweet.io:443/get/latest/dweet/for/{dweetthing}'
        self.notification = Notify()



    def notify(self,msg,title='WEBCLIPBOARD'):
        self.notification.message = msg
        self.notification.title = title
        self.notification.send()
        



    def recvclip(self,debug=False):
        try:
            __clip = requests.get(self.DWEET_RECV_URL).json()['with'][0]['content']['clip']
            __clip =  base64.b64decode(__clip) if self.CONF['encoding']=='base64' else base64.b32decode(__clip)
            __clip = __clip.decode()
        except Exception as e:
            print(f'recvclip exception -> {e}\n')
            __clip = ''
        #if debug: print(f'Received -> {__clip}')
        return __clip



    def sendclip(self,__clip,debug=False):
        if debug: print(f'Sending -> {__clip[:10]}...')

        __clip = __clip.encode()

        encoded_clip = base64.b64encode(__clip) if self.CONF['encoding']=='base64' else base64.b32encode(__clip)

        if requests.get(self.DWEET_SEND_URL,params={'clip':encoded_clip}).status_code == 200:
            self.notify(f'Sent')
        else:
            self.notify('Sending Failed')


    def getconf(self):
        with open('conf.yml') as f:
            conf=f.read()
        print(conf)

    def loadconf(self,filename):
        pass


    def run(self,runmode,debug):

        INTERVAL = self.CONF['pollrate']

        if runmode=='master':

            print(f'\n\t\tSENDING AT -> {self.DWEET_SEND_URL}\n')
            self.notify(f"Sensing clipboard every {INTERVAL} seconds")        

            LAST_CLIP = clipboard.paste()
            
            while True:
                clip = clipboard.paste()
                if clip != LAST_CLIP:
                    LAST_CLIP = clip
                    self.sendclip(clip,debug=debug)
                time.sleep(INTERVAL)

        elif runmode=='slave':
            print(f'\n\t\tRECEIVING AT -> {self.DWEET_RECV_URL}\n')
            self.notify(f"Acting on clipboard every {INTERVAL} seconds")

            LAST_CLIP = self.recvclip()
            
            while True:
                clip = self.recvclip(debug=debug)
                if clip != LAST_CLIP:
                    LAST_CLIP = clip
                    clipboard.copy(clip)

                    if debug: print(f'Received -> {clip[:10]}')
                    self.notify(f'Recieved')

                time.sleep(INTERVAL)

def get_cmdline_args(USAGE=None):

    if not USAGE:
        USAGE = f'\nUsage : \n\t python {sys.argv[0].split("/")[0]} --mode=master,slave  --channel=yourUniqueChannelName [--debug]\n'
    DEBUG = 0

    if len(sys.argv) < 3:
        print(USAGE)
        sys.exit(-1)
    else:
        RUNMODE = sys.argv[1].split('=')[-1]
        DWEETTHING = sys.argv[2].split('=')[-1]
        if len(sys.argv)>3:
            DEBUG=1 if sys.argv[3]=='--debug' else 0

    


    if RUNMODE in ['master','slave']:pass
    else:
        print(USAGE)
        sys.exit(-1)

    return RUNMODE,DWEETTHING,DEBUG



if __name__ == '__main__':

    runmode,dweetthing,debug = get_cmdline_args()
    intro()

    wcb = Webclipboard(dweetthing)
    wcb.run(runmode,debug)

