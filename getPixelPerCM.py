from encodings import utf_8
import json
import sys
from turtle import width
import pygame
# 导入配置文件
with open("config.json","r",encoding="utf-8") as f:
    str = f.read()
    settings = json.loads(str)
    WIDTH =settings["MONITOR"][0]
    HEIGHT = settings["MONITOR"][1]
    distanceOfSubject = settings["distanceOfSubject"]
    AngleLowerBound = settings["angleRange"][0]
    AngleUpperBound = settings["angleRange"][1]
    pixelPerCM = settings["pixelPerCM"]
    blackCrossDiameter = settings["BlackCrossDiameter"]
    FontSize = 25
# 初始化
pygame.init()
# 设置主屏幕
screen = pygame.display.set_mode((WIDTH,HEIGHT))
screen.fill((255,255,255)) # 填充白色背景
# 设置窗口标题
pygame.display.set_caption("欢迎校正本系统")
# 输出必要指导性文字
font = pygame.font.SysFont(pygame.font.get_fonts(),FontSize) 
text1 = font.render("Please make sure the distance between two red lines is 5cm to Calibrate the system.",True,(0,0,0))
text2 = font.render("After that, type ENTER button on the keyboard to SAVE the settings and quit!",True,(0,0,0))

LineLocation = 0 # 第二条红线的坐标
clock = pygame.time.Clock()
while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN: # 鼠标按下更新坐标
            LineLocation = event.pos[0]
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN: # 按下Enter后更新测量长度到文件，并推出脚本
                settings["pixelPerCM"] = abs(WIDTH/4 - LineLocation) / 5
                print("The new pixelPerCM is {}.".format(settings["pixelPerCM"]))
                with open("config.json","w",encoding="utf-8") as f:
                    f.write(json.dumps(settings))
                sys.exit()
    # 初始填充            
    screen.fill((255,255,255)) # 填充白色背景
    screen.blit(text1,(10,10))
    screen.blit(text2,(10,10 + FontSize))
    pygame.draw.rect(screen,(255,0,0),(WIDTH/4,0,1,HEIGHT),0)
    pygame.draw.rect(screen,(255,0,0),(LineLocation,0,1,HEIGHT),0)
    pygame.display.flip()
pygame.quit()
