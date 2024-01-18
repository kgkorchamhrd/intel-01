import pygame
import time

#알람 설정
pygame.mixer.init()
pygame.mixer.music.load("IU.mp3")

#알람 실행
pygame.mixer.music.play()
time.sleep(3)
