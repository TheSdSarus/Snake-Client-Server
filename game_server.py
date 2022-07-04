
import time
import random
import socket
import pygame
from threading import Thread

game_over = False
clock = pygame.time.Clock()

IP = "127.0.0.1"
PORT = 12000
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket.bind((IP, PORT))
print('El servidor esta escuchando, se espera que un jugador se conecte {}'.format(socket.getsockname()))

#Se espera
messageBytes, address = socket.recvfrom(2048)
execute_program = messageBytes.decode('utf-8')
if(execute_program != 'conect'):
    exit()


class Snake():
    

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.snakeList = []
        snake_Head = []
        snake_Head.append(x)
        snake_Head.append(y)
        self.snakeList.append(snake_Head)
        self.xChange = 0
        self.yChange = 0
        self.snakeLength = 1

    def updateValueChange(self,x,y):
        self.xChange = x
        self.yChange = y
    def updatePosition(self):
        self.x = self.x + self.xChange
        self.y = self.y + self.yChange

        snake_Head = []
        snake_Head.append(self.x)
        snake_Head.append(self.y)
        self.snakeList.append(snake_Head)
        if len(self.snakeList) > self.snakeLength:
            del self.snakeList[0]
        for x in self.snakeList[:-1]:
            if x == snake_Head:
                game_close = True
                print("asd" + str(game_close))

    def verify(self, dis_width, dis_height):
        if self.x >= dis_width or self.x < 0 or self.y >= dis_height or self.y < 0:
            print("entro al if")
            return True
        else:    
            return False    



a = Snake(200,200)
#b = Point(100,100)

foodx = round(random.randrange(0, 600 - 20) / 20.0) * 20.0
foody = round(random.randrange(0, 600 - 20) / 20.0) * 20.0

game_over = False


socket.settimeout(0)

#Aca estaba iniciado el socket

def task1():
    while True:
        try:
            messageBytes, address = socket.recvfrom(2048)
            messageString = messageBytes.decode('utf-8')
            print('Received from client {} : {}'.format(address, messageString))
            if messageString == 'left':
                a.updateValueChange(-20,0)
            if messageString == 'right':
                a.updateValueChange(20,0)
            if messageString == 'up':
                a.updateValueChange(0,-20)
            if messageString == 'down':
                a.updateValueChange(0,20)          
            #messageString = messageString.split(", ")
        except:
            asd = 1+1
    print("Hola")

def task2():
    while not game_over:
        if a.verify(600,600): #or b.verify(dis_width,dis_height):
            game_over = True    

        #b.updatePosition()
        #x1 += x1_change
        #y1 += y1_change

        a.updatePosition()

        #pygame.draw.rect(dis, black, [b.x, b.y, 20, 20])

        if a.x == foodx and a.y == foody:
            foodx = round(random.randrange(0, 600 - 20) / 20.0) * 20.0
            foody = round(random.randrange(0, 600 - 20) / 20.0) * 20.0
            a.snakeLength += 1

        clock.tick(5)



def task3():
    while True:
        result = str(foodx)+ "," + str(foody)

        for i in a.snakeList:
            result += "/" + str(i[0]) + "," + str(i[1])

        socket.sendto(str(result).encode(), address) 
    
print("EMPEZARA EJECUTAR LOS THREAD")

t1 = Thread(target=task1)
t2 = Thread(target=task2)
t3 = Thread(target=task3)

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()