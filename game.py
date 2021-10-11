import pygame
from grid import Grid


pygame.init()

screen=pygame.display.set_mode((600,600))
pygame.display.set_caption('Tic-Tac-Toe')

import threading
def creatT(target):
    thread= threading.Thread(target=target)
    thread.daemon=True
    thread.start()


import socket

host='127.0.0.1'
port= 65432
connection_establised= False
conn, addr= None, None
sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host,port))
sock.listen(1)

def receive_data():
    global turn
    while True:
        data = conn.recv(1024).decode() # receive data from the client, it is a blocking method
        data = data.split('-') # the format of the data after splitting is: ['x', 'y', 'yourturn', 'playing']
        x, y = int(data[0]), int(data[1])
        if data[2] == 'yourturn':
            turn = True
        if data[3] == 'False':
            grid.game_over = True
        if grid.get_cell_value(x, y) == 0:
            grid.set_cell_value(x, y, 'O')

def waiting():
    global connection_established, conn, addr
    conn, addr = sock.accept() # wait for a connection, it is a blocking method
    print('client is connected')
    connection_established = True
    receive_data()


creatT(waiting)

grid = Grid()
running=True
player="X"
turn=True
play="True"



while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type == pygame.MOUSEBUTTONDOWN and not grid.game_over: #works for left mouse button only
            if pygame.mouse.get_pressed()[0]:
                if turn and not grid.game_over:
                    pos = pygame.mouse.get_pos()
                    cellX, cellY = pos[0] // 200, pos[1] // 200
                    grid.get_mouse(cellX, cellY, player)
                    if grid.game_over:
                        playing = 'False'
                    send_data = '{}-{}-{}-{}'.format(cellX, cellY, 'yourturn', play).encode()
                    conn.send(send_data)
                    turn = False

        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE and connection_establised:
                grid.clear()
                grid.game_over=False
                play="True"
            elif event.key==pygame.K_SPACE:
                running=False

    screen.fill((0,0,0))
    grid.draw(screen)

    pygame.display.flip()