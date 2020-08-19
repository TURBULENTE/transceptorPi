### Transceptor Madre ###

#Funciones por ejecutar:
    #1.- Streaming de video/audio

    #2. Escuchar a WEB (/head, num), (/back, num), (/r_arm, num), (/l_arm, num), (/r_foot, num), (/l_foot, num)
    #2.1 Enviar argumento por OSC a RPi's determinadas

    #3. Escuchar WEB, palabras clave
    #3.1 Enviar a bluetooth audio de palabras por tts



#para hacer el stream #
import os

# -----  CLAVES YOUTUBE
clave = 'v8e5-byf4-q5kw-k9jv-6cg2' #canal_1 Madre / M_Front
#clave = '9rg2-6dfa-8bc0-xk7w-b3b0' #canal_2 H_Back
#clave = 'gs6t-2y8f-g5mf-cezu-2j22' #canal_3 H_RArm
#clave = '75f8-0ytd-vp6y-ufka-23py' #canal_4 H_LArm
#clave = '07s5-u308-bc2z-c5hs-cbzk' #canal_5 H_RLeg
#clave = 'k3yk-xj6s-1a0m-wd7z-1f1f' #canal_6 H_LLeg


### STREAMING
def stream():
    #os.system('raspivid -o - -t 0 -vf -hf -w 854 -h 480 -fps 25 -b 1200000 | ffmpeg -re -ar 44100 -ac 2 -acodec pcm_s16le -f s16le -ac 2 -i /dev/zero -f h264 -i - -vcodec copy -acodec aac -ab 128k -g 50 -strict experimental -f flv rtmp://a.rtmp.youtube.com/live2/jvuh-aeuk-me5j-tzxt-8mvc')

    #codigo para emitir con microfono
    #os.system('/opt/vc/bin/raspivid --nopreview -md 4 -w 854 -h 480 -fps 25 -t 0 -b 200000 -g 50 -n -o - | ffmpeg -y -xerror -thread_queue_size 32K -f h264 -r 15 -itsoffset 5.5 -i - -f alsa -ar 11025 -itsoffset 5.5 -async 1 -ac 1 -thread_queue_size 32K -i plughw:0 -c:a aac -b:a 32k -async 1 -c:v copy -f flv -flags:v +global_header -rtmp_buffer 10000 -r 15 -async 1 rtmp://a.rtmp.youtube.com/live2/' + clave )
    #print("streaming with audio now")

    #codigo para emitir sin microfono
    os.system('/opt/vc/bin/raspivid --nopreview -md 4 -vf -hf -w 854 -h 480 -fps 25 -t 0 -b 2000000 -g 50 -n -o - | ffmpeg -re -ar 44100 -ac 2 -acodec pcm_s16le -f s16le -ac 2 -i /dev/zero -f h264 -i - -vcodec copy -acodec aac -ab 128k -g 50 -strict experimental -f flv rtmp://a.rtmp.youtube.com/live2/' + clave)
    print("streaming with NO audio now")


### ------------------------------------------------



### MANDAR MENSAJES OSC-----------------------------
import argparse
import random
import time

from pythonosc import udp_client



###  Enviar mensajes OSC
def cliente():
#if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip", default="192.168.1.109",
      help="The ip of the OSC server")
  parser.add_argument("--port", type=int, default=5005,
      help="The port the OSC server is listening on")
  args = parser.parse_args()

  client = udp_client.SimpleUDPClient(args.ip, args.port)

  varclient = True
  if varclient:
  #for x in range(10):
    client.send_message("/likeFront", 1)
    client.send_message("/likeBack", 1)
    client.send_message("/likeRArm", 1)
    client.send_message("/likeFLArm", 1)
    client.send_message("/likeRLeg", 1)
    client.send_message("/likeLLeg", 1)
    time.sleep(1)


### TEXT TO SPEECH

from subprocess import call #texttospeech
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

host_name = '192.168.1.111' #navasoak IP MADRE
#host_name = '192.168.8.101'    # modem transceptor
host_port = 8000 #Puerto a escuchar




class MyServer(BaseHTTPRequestHandler):
    """ A special implementation of BaseHTTPRequestHander for reading data from
        and control GPIO of a Raspberry Pi
    """

    def do_HEAD(self):
        """ do_HEAD() can be tested use curl command
            'curl -I http://server-ip-address:port'
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self): #hacer un array de palabras posibles y comparar en un solo if !!!
        self.do_HEAD()
        status = ''
        if self.path=='/':
            print("Path Vacio")

        elif (self.path=='/edgar,se,cae'):
            print("Edgar se cae")

        elif (self.path=='/duck,face'):
            print("duckface")

        elif (self.path=='/hide,the,pain,harold'):
            print("duckface")

        elif (self.path=='/dramatic,chipmunk'):
            print("Dramatic Chipmunk")

        elif (self.path=='/double,rainbow'):
            print("Double Rainbow")


            #ESPEAK LO QUE SEA
            texto = self.path[1:]
            os.system("espeak "+ "."+ texto +" -ven -k5 -s140 --stdout | aplay -D bluealsa")

        elif (self.path!='/' and self.path !='/favicon.ico'):

            print(self.path == '/favicon.ico')
            #texto = self.path[1:] #variable para leer lo que hay después del slash /, quitándole el slash (lo añadió to)
            #os.system("espeak " + texto +" -ven -k5 -s140 --stdout | aplay -D bluealsa") #Aquí damos formato de espeak

### --------------------------------------------

#### PROGRAMA MADRE ##############################
# ¿cómo hacer para que las tres funciones suceda de manera sumultánea? osc, stream(), cliente ()
#leer url webserver
if __name__ == '__main__':
    http_server = HTTPServer((host_name, host_port), MyServer)
    print("Server Starts - %s:%s" % (host_name, host_port))

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()

    #programita osc
    varC= True
    if varC:
        #stream()
        #cliente()



#### --------------------------------------------
