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
counter = 0
while(1):
    timestr = time.strftime("%Y%m%d-%H%M%S")   
    i = fcam.get_image()
	j = bcam.get_image()
    i = pygame.transform.rotate(i, 180)
	j = pygame.transform.rotate(j, -90)
    pygame.image.save(i, "/var/www/html/img/f-loading.png")
	pygame.image.save(j, "/var/www/html/img/b-loading.png")
    print('Saved images.\n')
    os.rename("/var/www/html/img/f-loading.png", "/var/www/html/img/f-" + str(counter) + ".png")
    os.rename("/var/www/html/img/b-loading.png", "/var/www/html/img/b-" + str(counter) + ".png")
	if(counter > 5):
		os.rename("/var/www/html/img/f-" + str(counter - 5) + ".png", "/home/pi/marsbotcontrol/stills/f-{}{}".format(timestr, ".png"))
		os.rename("/var/www/html/img/f-" + str(counter - 5) + ".png", "/home/pi/marsbotcontrol/stills/b-{}{}".format(timestr, ".png"))
		print("Moved old images to stills.")
    time.sleep(0.5)
	couter += 1
