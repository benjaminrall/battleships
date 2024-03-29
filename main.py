import pygame
import os
from network import Network
from ship import Ship
from tray import Tray
from game import Game
from sprite_loader import Spritesheet
from personallib.camera import Camera
from personallib.canvas import *

# Constants
WIN_WIDTH = 1000
WIN_HEIGHT = 650
FRAMERATE = 120
GRID_SIZE = 400
SCALE = GRID_SIZE // 10
ICON_IMG = pygame.image.load(os.path.join("imgs", "icon.png"))
DEFAULT_IP = ""
COLOURS = [None, (255, 0, 0), (200, 200, 200)]

# Pygame Setup
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Battleships")
pygame.display.set_icon(ICON_IMG)
clock = pygame.time.Clock()

# Objects
cam = Camera(win, 0, 0, 1)
playerSurface = pygame.Surface((GRID_SIZE, GRID_SIZE))
opponentSurface = pygame.Surface((GRID_SIZE, GRID_SIZE))
sprites = Spritesheet("imgs/sprites/", SCALE)
tray = Tray(40, -195, GRID_SIZE, GRID_SIZE // 4 + SCALE * 4)

# Variables
running = True
heldShip = None
heldShipOrientation = 0
playerShips = []
enemyShips = []
network = None
playerID = None
ready = False
enemyReady = False
playing = False
game = None
won = None
turn = -1

# Methods
def draw_board(surface):
    surface.fill((0, 0, 60))
    for y in range(10):
        for x in range(10):
            pygame.draw.rect(surface, (0, 0, 200), (x * SCALE + 1, y * SCALE + 1, SCALE - 2, SCALE - 2))

def draw_hits(surface, board):
    for y in range(10):
        for x in range(10):
            colour = COLOURS[board[y][x]]
            if colour:
                shift = SCALE // 2
                pygame.draw.circle(surface, colour, ((x * SCALE) + shift, (y * SCALE) + shift), shift / 2)

def draw_sunken_ships(surface, ships, board):
    for ship in ships:
        sunk = True
        if not ship.sunk:
            for position in ship.get_positions():
                if board[position[1]][position[0]] == 0:
                    sunk = False
        if sunk:
            (start, end) = ship.get_bounds()
            shift = SCALE // 2
            pygame.draw.line(
                surface, COLOURS[1], ((start[0] * SCALE) + shift, (start[1] * SCALE) + shift), 
                ((end[0] * SCALE) + shift, (end[1] * SCALE) + shift), shift + (1 if shift % 2 == 0 else 0)
            )
            ship.sunk = True

def draw_player_board(cam, surface, ships, heldShip, board = None):
    draw_board(surface)
    for ship in ships:
        if ship != heldShip:
            surface.blit(sprites[(ship.type * 2) + ship.orientation], (ship.root[0] * SCALE, ship.root[1] * SCALE))
    if board is not None:
        draw_hits(surface, board)
        draw_sunken_ships(surface, ships, board)
    cam.blit(surface, (-440, -265))
    if heldShip is not None:
        mousePos = cam.get_world_coord(pygame.mouse.get_pos())
        sprite = sprites[(heldShip.type * 2) + heldShip.orientation]
        cam.blit(sprite, (mousePos[0] - SCALE // 2, mousePos[1] - SCALE // 2))
    

def draw_opponent_board(cam, surface, pos, ships, board, showHover):
    draw_board(surface)
    draw_hits(surface, board)
    if ships is not None and len(ships) > 0:
        draw_sunken_ships(surface, ships, board)
    cam.blit(surface, pos)
    if showHover:
        hoverSurface = pygame.Surface(surface.get_size())
        hoverSurface.set_alpha(80)
        mousePos = cam.get_world_coord(pygame.mouse.get_pos())
        relX = mousePos[0] - pos[0]
        relY = mousePos[1] - pos[1]
        if 0 <= relX < GRID_SIZE and 0 <= relY < GRID_SIZE:
            x = relX // SCALE
            y = relY // SCALE
            pygame.draw.rect(hoverSurface, (200, 200, 200), (x * SCALE + 1, y * SCALE + 1, SCALE - 2, SCALE - 2))
        cam.blit(hoverSurface, pos)

def connect():
    textBox = connectMenu.find_element("ipTextBox")
    errorText = connectMenu.find_element("connectionErrorMessage")
    address = textBox.get_text()
    # Check it's not empty
    if len(address) == 0:
        textBox.clear_text()
        errorText.render("IP address must be specified.")
        return
    # Check it contains valid characters
    for char in address:
        if char not in ['.', '0', '1', '2', '3', '4', '5' ,'6', '7', '8', '9']:
            textBox.clear_text()
            errorText.render("Invalid character in address.")
            return
    # Attempt connection
    global network, playerID
    network = Network(address)
    if network.connected:
        playerID = int(network.getP())
        if playerID is not None and playerID < 0:
            errorText.render("Server full.")
        else:
            network.send("unready")
    else:
        network = None
        textBox.clear_text()
        errorText.render("Invalid IP address or no server found.")

def readyButton():
    global network, playerID, ready
    if network is None or playerID < 0:
        return
    if not ready:
        lobbyMenu.find_element("readyButton").text.render("Unready")
        lobbyMenu.find_element(f"ready{playerID}").set_path("imgs/ready.png")
        network.send("ready")
    else:
        lobbyMenu.find_element("readyButton").text.render("Ready")
        lobbyMenu.find_element(f"ready{playerID}").set_path("imgs/not_ready.png")
        network.send("unready")
    ready = not ready

def resetButton():
    global won
    won = None
    lobbyMenu.find_element("readyButton").set_enabled(True)
    resetMenu.set_visible(False)

def quitButton():
    global running
    running = False
    pygame.quit()
    exit()

# Canvas
connectMenu = Canvas(WIN_WIDTH, WIN_HEIGHT)
connectMenu.add_element(Button("connectButton", (340, 500), (120, 50), Text("connectButtonText", (0, 0), "georgia", 24, "Connect"), (200, 200, 200), (150, 150, 150), (100, 100, 100), onClick=connect))
connectMenu.add_element(TextBox("ipTextBox", (60, 500), (240, 50), Text("ipTextBoxText", (0, 0), "georgia", 24), DEFAULT_IP, (0, 0, 0), (250, 250, 250), "Enter IP...", (150, 150, 150), (0, 0, 0), 1, (230, 230, 230), (210, 210, 210), onEnter=connect))
connectMenu.add_element(Text("connectionErrorMessage", (60, 560), "georgia", 14, "", (255, 0, 0)))
connectMenu.set_visible(False)

waitingMenu = Canvas(WIN_WIDTH, WIN_HEIGHT)
waitingMenu.add_element(Text("waitingText", (260, 500), "georgia", 30, "Waiting for players...", (255, 255, 255), "centre"))
waitingMenu.set_visible(False)

lobbyMenu = Canvas(WIN_WIDTH, WIN_HEIGHT)
lobbyMenu.add_element(Button("readyButton", (100, 500), (160, 50), Text("readyButtonText", (0, 0), "georgia", 24, "Ready"), (200, 200, 200), (150, 150, 150), (100, 100, 100), onClick=readyButton))
lobbyMenu.add_element(Image("ready0", (300, 500), "imgs/not_ready.png"))
lobbyMenu.add_element(Image("ready1", (360, 500), "imgs/not_ready.png"))
lobbyMenu.set_visible(False)

resetMenu = Canvas(WIN_WIDTH, WIN_HEIGHT)
resetMenu.add_element(Fill("fade", (0, 0, 0), 0.7))
resetMenu.add_element(Text("winText", (500, 300), "georgia", 72, "You Win!", (255, 255, 255), "centre"))
resetMenu.add_element(Button("resetButton", (400, 400), (200, 60), Text("resetButtonText", (0, 0), "georgia", 24, "Play Again"), (200, 200, 200), (150, 150, 150), (100, 100, 100), onClick=resetButton))
resetMenu.set_visible(False)


# Main Loop
if __name__ == '__main__':
    while running:

        clock.tick(FRAMERATE)

        win.fill((50, 50, 50))

        if not playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    connectMenu.run_method_on_type(TextBox, "input_key_event", [event])
                    if event.key == pygame.K_r and heldShip is not None:
                        heldShip.orientation = (heldShip.orientation + 1) % 2
                elif event.type == pygame.MOUSEMOTION:
                    screenMousePos = pygame.mouse.get_pos()
                    connectMenu.run_method_on_type(Button, "hover", [screenMousePos])
                    connectMenu.run_method_on_type(TextBox, "hover", [screenMousePos])
                    lobbyMenu.run_method_on_type(Button, "hover", [screenMousePos])
                    resetMenu.run_method_on_type(Button, "hover", [screenMousePos])
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        screenMousePos = pygame.mouse.get_pos()
                        connectMenu.run_method_on_type(Button, "click", [screenMousePos])
                        connectMenu.run_method_on_type(TextBox, "click", [screenMousePos])
                        lobbyMenu.run_method_on_type(Button, "click", [screenMousePos])
                        resetMenu.run_method_on_type(Button, "click", [screenMousePos])
                        if not ready and won is None:
                            mousePos = cam.get_world_coord(screenMousePos)
                            gridPos = (-440, -265)
                            relX = mousePos[0] - gridPos[0]
                            relY = mousePos[1] - gridPos[1]
                            if tray.contains_pos(mousePos):
                                index = tray.get_tray_index(mousePos)
                                if index < len(tray.ships):
                                    heldShip = tray[index]
                            elif 0 <= relX < GRID_SIZE and 0 <= relY < GRID_SIZE:
                                newPos = (relX // SCALE, relY // SCALE)
                                for ship in playerShips:
                                    bounds = ship.get_bounds()
                                    if bounds[0][0] <= newPos[0] <= bounds[1][0] and bounds[0][1] <= newPos[1] <= bounds[1][1]:
                                        heldShip = ship
                                        break
                            if heldShip is not None:
                                heldShipOrientation = heldShip.orientation
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1: 
                        screenMousePos = pygame.mouse.get_pos()
                        connectMenu.run_method_on_type(Button, "hover", [screenMousePos])
                        lobbyMenu.run_method_on_type(Button, "hover", [screenMousePos])
                        resetMenu.run_method_on_type(Button, "hover", [screenMousePos])
                        if heldShip is not None:
                            validDrop = False
                            mousePos = cam.get_world_coord(screenMousePos)
                            gridPos = (-440, -265)
                            relX = mousePos[0] - gridPos[0]
                            relY = mousePos[1] - gridPos[1]
                            if 0 <= relX < GRID_SIZE and 0 <= relY < GRID_SIZE:
                                newPos = (int(relX // SCALE), int(relY // SCALE))
                                newBounds = heldShip.get_bounds(newPos)
                                if 0 <= newBounds[1][0] < 10 and 0 <= newBounds[1][1] < 10 and not heldShip.overlaps(playerShips, newPos):
                                    heldShip.root = newPos
                                    validDrop = True
                                    if heldShip.inTray:
                                        playerShips.append(heldShip)
                                        tray.ships.remove(heldShip)
                                        heldShip.inTray = False
                                        if len(tray.ships) == 0:
                                            connectMenu.set_visible(True)
                            if not validDrop:
                                heldShip.orientation = heldShipOrientation
                            heldShip = None

            tray.draw(cam, heldShip, sprites)

            draw_player_board(cam, playerSurface, playerShips, heldShip)

            connectMenu.run_method_on_type(TextBox, "update_cursor")

            connectMenu.update(cam)
            waitingMenu.update(cam)
            lobbyMenu.update(cam)

            if network:
                playerData = network.send("get:players").split(":")
                connectMenu.set_visible(False)
                if playerData[0] == "False":
                    waitingMenu.set_visible(True)
                    lobbyMenu.set_visible(False)
                else:
                    waitingMenu.set_visible(False)
                    lobbyMenu.set_visible(True)

                    draw_board(opponentSurface)
                    cam.blit(opponentSurface, (40, -265))
                    resetMenu.update(cam)

                    if playerData[1] == "False":
                        if enemyReady:
                            lobbyMenu.find_element(f"ready{(playerID + 1) % 2}").set_path("imgs/not_ready.png")
                            enemyReady = False
                    else:
                        if not enemyReady:
                            lobbyMenu.find_element(f"ready{(playerID + 1) % 2}").set_path("imgs/ready.png")
                            enemyReady = True
                if ready and enemyReady or playerData[2] == "True":
                    if playerID == 0:
                        network.send("start")
                    lobbyMenu.set_visible(False)
                    playing = True
                    game = network.send("get:game")
                    while game == "None":
                        game = network.send("get:game")
                    game = Game(game)
                    turn = int(network.send("get:turn"))
                    if playerData[2] == "True" and not (ready and enemyReady):
                        (playerShips, enemyShips) = network.pickle_receive("get:ships")
                    else:
                        network.send("pickle")
                        network.pickle_send(playerShips)
                    ready = True
            
                        
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and turn == playerID:
                        mousePos = cam.get_world_coord(pygame.mouse.get_pos())
                        gridPos = (40, -265)
                        relX = mousePos[0] - gridPos[0]
                        relY = mousePos[1] - gridPos[1]
                        if 0 <= relX < GRID_SIZE and 0 <= relY < GRID_SIZE:
                            shotPos = (int(relX // SCALE), int(relY // SCALE))
                            network.send(f"play:{shotPos[0]}:{shotPos[1]}")

            if not False in [ship.sunk for ship in playerShips]:
                network.send(f"end:{(playerID + 1) % 2}")

            getUpdate = network.send("get:update")
            if getUpdate == "True":
                game = Game(network.send("get:game"))
                turn = game.turn
            if enemyShips is None or len(enemyShips) == 0:
                enemyShips = network.pickle_receive("get:ships")[(playerID + 1) % 2]

            draw_player_board(cam, playerSurface, playerShips, heldShip, game.boards[playerID])
            
            draw_opponent_board(cam, opponentSurface, (40, -265), enemyShips, game.boards[(playerID + 1) % 2], turn == playerID)

            if game.winner >= 0:
                playing = False
                readyButton()
                won = game.winner == playerID
                resetMenu.find_element("winText").render("You Win!" if won else "You Lose!")
                resetMenu.set_visible(True)
                lobbyMenu.find_element("readyButton").set_enabled(False)
                for ship in playerShips:
                    ship.sunk = False
                enemyShips = None
                network.send("reset")

        pygame.display.update()