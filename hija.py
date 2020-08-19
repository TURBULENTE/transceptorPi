
### Transceptor Hijas ###

#Funciones por realizar de manera simultánea

    #1. If recibir mensaje OSC /like
        #mover Motor

    #2. If (algo/ buton On) Streaming de video y audio






### OSC setup --------



from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import osc_message_builder #loañadi
import argparse
import math

### -------------

#import keyboard
#para hacer el stream #
import os


# -----  CLAVES YOUTUBE
clave = 'v8e5-byf4-q5kw-k9jv-6cg2' #canal_1
#clave = '9rg2-6dfa-8bc0-xk7w-b3b0' #canal_2
#clave = 'gs6t-2y8f-g5mf-cezu-2j22' #canal_3
#clave = '75f8-0ytd-vp6y-ufka-23py' #canal_4
#clave = '07s5-u308-bc2z-c5hs-cbzk' #canal_5
#clave = 'k3yk-xj6s-1a0m-wd7z-1f1f' #canal_6
## ----

#GPIO setup
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)
Motor1A = 32
GPIO.setup(Motor1A, GPIO.OUT)
## ----

### Mover Motor
def mover_motor(unused_addr, args):
    #if cuemotor:
        for  x in range ( 0, 3):
            print ("Turning motor on")
            GPIO.output(Motor1A, GPIO.HIGH)
            sleep(0.5)
            print ("Stopping motor")
            GPIO.output(Motor1A, GPIO.LOW)
            sleep(0.5)


def streaming():
    #os.system('raspivid -o - -t 0 -vf -hf -w 854 -h 480 -fps 25 -b 1200000 | ffmpeg -re -ar 44100 -ac 2 -acodec pcm_s16le -f s16le -ac 2 -i /dev/zero -f h264 -i - -vcodec copy -acodec aac -ab 128k -g 50 -strict experimental -f flv rtmp://a.rtmp.youtube.com/live2/jvuh-aeuk-me5j-tzxt-8mvc')

    #codigo para emitir con microfono
    #print("streaming with audio now")
    #os.system('/opt/vc/bin/raspivid --nopreview -md 4 -w 854 -h 480 -fps 25 -t 0 -b 200000 -g 50 -n -o - | ffmpeg -y -xerror -thread_queue_size 32K -f h264 -r 15 -itsoffset 5.5 -i - -f alsa -ar 11025 -itsoffset 5.5 -async 1 -ac 1 -thread_queue_size 32K -i plughw:0 -c:a aac -b:a 32k -async 1 -c:v copy -f flv -flags:v +global_header -rtmp_buffer 10000 -r 15 -async 1 rtmp://a.rtmp.youtube.com/live2/' + clave )


    #codigo para emitir sin microfono
    print("streaming with NO audio now")
    os.system('/opt/vc/bin/raspivid --nopreview -md 4 -vf -hf -w 854 -h 480 -fps 25 -t 0 -b 2000000 -g 50 -n -o - | ffmpeg -re -ar 44100 -ac 2 -acodec pcm_s16le -f s16le -ac 2 -i /dev/zero -f h264 -i - -vcodec copy -acodec aac -ab 128k -g 50 -strict experimental -f flv rtmp://a.rtmp.youtube.com/live2/' + clave)



#stream = True
#while stream:
#    try:
#        if keyboard.is_pressed('q'):
#            print ('Tecla presionada, comenzando stream')
#            streaming()
#    except:
#        break
#        print ('stream terminado')
#else:
#    print('Sin stream')
    # Do anything else you want to do here



### PROGRAMA HIJAS

#OSC --------------------------
if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip",
      default="192.168.1.109", help="The ip to listen on")
  parser.add_argument("--port",
      type=int, default=5005, help="The port to listen on")
  args = parser.parse_args()

#AQUÍ ES EN DONDE "CACHA" LOS MENSAJES
  dispatcher = dispatcher.Dispatcher()
  dispatcher.map("/likeFront", mover_motor)
  server = osc_server.ThreadingOSCUDPServer(
      (args.ip, args.port), dispatcher)
  print("Serving on {}".format(server.server_address))
  server.serve_forever()
 #OSC FIN---------------------

print('Fin del programa')

### ----------------------------------------------------------
