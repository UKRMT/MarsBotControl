import pygame
import pygame.camera
import datetime
import time
import re
import os

pygame.camera.init()
pygame.camera.list_cameras()
fcam = pygame.camera.Camera("/dev/frontcam", (1024,768))
bcam = pygame.camera.Camera("/dev/backcam", (1024,768))
fcam.start()
bcam.start()
while(1):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    os.rename("/var/www/html/f-current.png", "/home/pi/marsbotcontrol/stills/f-{}{}".format(timestr, ".png"))
    os.rename("/var/www/html/b-current.png", "/home/pi/marsbotcontrol/stills/b-{}{}".format(timestr, ".png"))
    
    i = fcam.get_image()
    i = pygame.transform.rotate(i, 180)
    pygame.image.save(i, "/var/www/html/f-current-loading.png")
    print('saved front image')
    j = bcam.get_image()
    j = pygame.transform.rotate(j, -90)
    pygame.image.save(j, "/var/www/html/b-current-loading.png")
    print('saved back image\n')
    os.rename("/var/www/html/f-current-loading.png", "/var/www/html/f-current.png")
    os.rename("/var/www/html/b-current-loading.png", "/var/www/html/b-current.png")
    time.sleep(0.5)
