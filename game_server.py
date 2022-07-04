
import time
import random
import socket
import pygame
from threading import Thread

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
class Food:
    def __init__(self, x=round(random.randrange(0, 600 - 20) / 20.0) * 20.0, y=round(random.randrange(0, 600 - 20) / 20.0) * 20.0):
        self.x = x
        self.y = y

    def setNewCoordinate(self):
        self.x = round(random.randrange(0, 600 - 20) / 20.0) * 20.0 
        self.y = round(random.randrange(0, 600 - 20) / 20.0) * 20.0
        print("Hola")
class Game:
    def __init__(self, width=600, height=600):
        self.width = width
        self.height = height
        self.clock = pygame.time.Clock()
        self.IP = "127.0.0.1"
        self.PORT = 12000
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.IP, self.PORT))
        print("Se inicio el socket correctamente")
        self.addressplayer = None
        self.snake = Snake(200,200)
        self.food = Food()
        #self.foodx = round(random.randrange(0, 600 - 20) / 20.0) * 20.0
        #self.foody = round(random.randrange(0, 600 - 20) / 20.0) * 20.0
        self.game_over = False

    def waitPlayer(self):
        messageBytes, self.addressplayer = self.socket.recvfrom(2048)
        execute_program = messageBytes.decode('utf-8')
        if(execute_program != 'conect'):
            exit()

    def rungame(self):
        self.socket.settimeout(0)
        print("EMPEZARA EJECUTAR LOS THREAD")
        t1 = Thread(target=self.task1)
        t2 = Thread(target=self.task2)
        t3 = Thread(target=self.task3)

        t1.start()
        t2.start()
        t3.start()

        t1.join()
        t2.join()
        t3.join()
        print("CORRIO LOS THREAD")

    def task1(self):
        while True:
            try:
                messageBytes, self.addressplayer = self.socket.recvfrom(2048)
                messageString = messageBytes.decode('utf-8')
                print('Received from client {} : {}'.format(self.addressplayer, messageString))
                if messageString == 'left':
                    self.snake.updateValueChange(-20,0)
                if messageString == 'right':
                    self.snake.updateValueChange(20,0)
                if messageString == 'up':
                    self.snake.updateValueChange(0,-20)
                if messageString == 'down':
                    self.snake.updateValueChange(0,20)          
                #messageString = messageString.split(", ")
            except:
                asd = 1+1

    def task2(self):
        while True:

            self.snake.updatePosition()

            #pygame.draw.rect(dis, black, [b.x, b.y, 20, 20])

            if self.snake.x == self.food.x and self.snake.y == self.food.y:
                self.food.setNewCoordinate()
                self.snake.snakeLength += 1

            self.clock.tick(5)
    
    def task3(self):
        while True:
            
            result = str(self.food.x)+ "," + str(self.food.y)

            for i in self.snake.snakeList:
                result += "/" + str(i[0]) + "," + str(i[1])

            self.socket.sendto(str(result).encode(), self.addressplayer)
            time.sleep(0.01)            


    
print("EMPEZARA EJECUTAR EL JUEGO")

juego = Game()
print("SE ESPERAN A LOS JUGADORES")
juego.waitPlayer()
print("SE CORRE EL JUEGO")
juego.rungame()
