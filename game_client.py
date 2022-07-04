import socket
import pygame

IP = "127.0.0.1"
PORT = 12000
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

a = input("Desea usted conectarse: ")
print('Usted indico que se: ' + a + "\n")
socket.sendto(a.encode('utf-8'), (IP, PORT))
print("SE MANDO EL MENSAJE")

pygame.init()
 
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

dis_width = 600
dis_height  = 600

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Jugando')

def our_snake(snake_block, a):
    for x in a.snakeList:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

socket.settimeout(0)

def updateBoard(messageString): 
    dis.fill(white)
    aux = 0
    print("entra al update board")
    print(messageString)

    for x in messageString:
        coordenada = x.split(",")
        a = coordenada[0]
        print("holii" + a)
        if aux == 0:
            pygame.draw.rect(dis, green, [int(float(coordenada[0])), int(float(coordenada[1])), 20, 20])
        else:
            pygame.draw.rect(dis, black, [int(coordenada[0]), int(coordenada[1]), 20, 20])
        aux = aux + 1

    
    print("------------")
hola = ['0','1']

dis.fill(white)
pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                message = 'left'
                socket.sendto(message.encode('utf-8'), (IP, PORT))

            elif event.key == pygame.K_RIGHT:
                message = 'right'
                socket.sendto(message.encode('utf-8'), (IP, PORT))

            elif event.key == pygame.K_UP:
                message = 'up'
                socket.sendto(message.encode('utf-8'), (IP, PORT))
            elif event.key == pygame.K_DOWN:
                message = 'down'
                socket.sendto(message.encode('utf-8'), (IP, PORT))


    try:
        messageBytes, address = socket.recvfrom(2048)
        messageString = messageBytes.decode('utf-8')
        print('Received from server {} : {}'.format(address, messageString))
        messageString = messageString.split("/")
        hola = messageString[0].split(",")
        
        #print("asd " + asd[0])

        updateBoard(messageString)
        print("se actualizo")
        pygame.display.update()
    except Exception as inst:
        asd = 1+1
        #print(type(inst))    # the exception instance
        #print(inst.args)     # arguments stored in .args
        #print(inst)  

pygame.quit()
quit()

