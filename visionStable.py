from math import pi, tan,cos,sin
from encodings import utf_8
import json
from multiprocessing.connection import wait
import sys
from turtle import width
import pygame
import random

from scipy import rand
# 导入配置文件

def cross(surface,color,location,size):
    scaleRate = 0.1
    barWidth = scaleRate * size
    pygame.draw.rect(surface,color,(location[0]-barWidth/2,location[1]-size/2,barWidth,size),0)
    pygame.draw.rect(surface,color,(location[0]-size/2,location[1]-barWidth/2,size,barWidth),0)
with open("config.json","r",encoding="utf-8") as f:
    str = f.read()
    settings = json.loads(str)
    # 显示器参数
    WIDTH =settings["MONITOR"][0]
    HEIGHT = settings["MONITOR"][1]
    # 受试者距离
    distanceOfSubject = settings["distanceOfSubject"]
    # 干扰因素视角范围
    AngleLowerBound = settings["angleRange"][0]
    AngleUpperBound = settings["angleRange"][1]
    # 每厘米有几个像素，需要先用getPixelPerCM校正
    pixelPerCM = settings["pixelPerCM"]
    # 黑十字大小参数
    blackCrossDiameter = settings["BlackCrossDiameter"]
    # 中央黑点视角
    blackPointDiameterAngle = settings["blackPointDiameterAngle"]

# 利用给定的参数实现视角到像素的转换
def angle2Pixel(angle):
    return tan(angle * 2 * pi / 360) * distanceOfSubject * pixelPerCM

blackPointWidth = int(angle2Pixel(blackPointDiameterAngle)) # 计算黑点直径
# 绘制中央黑点
def drawCenterPoint(surface):
    pygame.draw.circle(surface,(0,0,0),(WIDTH/2,HEIGHT/2),blackPointWidth/2)

# 绘制干扰点
def drawDistract(surface):
    starSclale = 2.5
    starSize = int(blackPointWidth * starSclale)
    starCorrection = -0.2 * starSize,-0.4 * starSize # 用于控制字符星号本身会“偏心”的问题
    font = pygame.font.SysFont(pygame.font.get_fonts(),starSize) 
    star = font.render("*",True,(0,0,0))
    # 随机生成一个新的点（利用极坐标）
    innerRadius = angle2Pixel(AngleLowerBound)
    outterRadius = angle2Pixel(AngleUpperBound)
    ranLength = random.random() * (outterRadius - innerRadius) + innerRadius
    ranAngle = random.random() * 2 * pi
    dx = ranLength * cos(ranAngle) + starCorrection[0]
    dy = ranLength * sin(ranAngle) + starCorrection[1]
    starLocation =  WIDTH/2 + dx, HEIGHT/2 + dy
    surface.blit(star,starLocation)
          
def DistractVision(surface):
    timeArray = [random.random()*5 for i in range(20)]
    timeArray.sort()
    step = [(timeArray[x], timeArray[x+1]) for x in range(0,len(timeArray),2)]
    endTime = 0
    for i in step:
        pygame.time.wait(int((i[0] - endTime) * 1000))
        drawDistract(surface)
        pygame.display.flip()
        pygame.time.wait(int((i[1]-i[0]) * 1000))
        screen.fill((255,255,255)) 
        drawCenterPoint(surface)
        pygame.display.flip()
        endTime = i[1]
# 管理整个15000s流程
def theWholeProcess(surface):
    # 先展示5秒十字
    cross(surface,(0,0,0),(WIDTH/2,HEIGHT/2),blackCrossDiameter * pixelPerCM)
    pygame.display.flip()
    pygame.time.wait(5000)
    # 展示5s黑点
    surface.fill((255,255,255))
    drawCenterPoint(surface)
    pygame.display.flip()
    pygame.time.wait(5000)
    # 展示混淆
    DistractVision(surface)
    pygame.time.wait(5000)
    exit(0)
# 初始化
pygame.init()
# 设置主屏幕
screen = pygame.display.set_mode((WIDTH,HEIGHT))
screen.fill((255,255,255))
# 设置窗口标题
pygame.display.set_caption("欢迎来到本测试")

clock = pygame.time.Clock()
while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    # pygame.draw.circle(screen, (0,0,0), (WIDTH/2, HEIGHT/2), pixelPerCM * blackCircleDiameter / 2, width=0)        
    
    # cross(screen,(0,0,0),(WIDTH/2, HEIGHT/2), pixelPerCM * blackCrossDiameter)
    theWholeProcess(screen) 
pygame.quit()
