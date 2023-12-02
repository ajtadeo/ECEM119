""" Source: https://www.geeksforgeeks.org/create-a-pong-game-in-python-pygame/ """
import pygame
import threading, json
from http.server import SimpleHTTPRequestHandler, HTTPServer
from queue import Queue, Empty
 
pygame.init()
 
# Font that is used to render the text
font20 = pygame.font.Font('freesansbold.ttf', 20)
 
# RGB values of standard colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
 
# Basic parameters of the screen
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
 
clock = pygame.time.Clock()    
FPS = 30

# Global queues for player movement
player1Queue = Queue()
player2Queue = Queue()

# HTTP server params, ipconfig getifaddr en0
HOST = '172.20.10.2'
PORT = 9000
server_address = (HOST, PORT)

""" HTTP Request Handler """
class RequestHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/p1":
            # get args
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8')
                json_data = json.loads(post_data)
                # print(json_data)
                
                if json_data.get("move", None):
                    direction = json_data["move"]
                    player1Queue.put(direction)
                    self.send_response(200)
                    self.end_headers()
                else:
                    self.send_error(400, "No move data found.")
                    self.end_headers()
            else:
                self.send_error(400, "No content found.")
                self.end_headers()
        else:
            self.send_error(404, "Path not found.")
        
# httpd must be defined after RequestHandler
httpd = HTTPServer(server_address, RequestHandler)
        
""" HTTP Server """   
def start_server():
	print(f"HTTP server started on {HOST}:{PORT}")
	httpd.serve_forever()
        
 
""" Striker Class """
class Striker:
        # Take the initial position, dimensions, speed and color of the object
    def __init__(self, posx, posy, width, height, speed, color):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        # Rect that is used to control the position and collision of the object
        self.geekRect = pygame.Rect(posx, posy, width, height)
        # Object that is blit on the screen
        self.geek = pygame.draw.rect(screen, self.color, self.geekRect)
 
    # Used to display the object on the screen
    def display(self):
        self.geek = pygame.draw.rect(screen, self.color, self.geekRect)
 
    def update(self, yFac):
        self.posy = self.posy + self.speed*yFac
 
        # Restricting the striker to be below the top surface of the screen
        if self.posy <= 0:
            self.posy = 0
        # Restricting the striker to be above the bottom surface of the screen
        elif self.posy + self.height >= HEIGHT:
            self.posy = HEIGHT-self.height
 
        # Updating the rect with the new values
        self.geekRect = (self.posx, self.posy, self.width, self.height)
 
    def displayScore(self, text, score, x, y, color):
        text = font20.render(text+str(score), True, color)
        textRect = text.get_rect()
        textRect.center = (x, y)
 
        screen.blit(text, textRect)
 
    def getRect(self):
        return self.geekRect
 
 
""" Ball Class """
class Ball:
    def __init__(self, posx, posy, radius, speed, color):
        self.posx = posx
        self.posy = posy
        self.radius = radius
        self.speed = speed
        self.color = color
        self.xFac = 1
        self.yFac = -1
        self.ball = pygame.draw.circle(
            screen, self.color, (self.posx, self.posy), self.radius)
        self.firstTime = 1
 
    def display(self):
        self.ball = pygame.draw.circle(
            screen, self.color, (self.posx, self.posy), self.radius)
 
    def update(self):
        self.posx += self.speed*self.xFac
        self.posy += self.speed*self.yFac
 
        # If the ball hits the top or bottom surfaces, 
        # then the sign of yFac is changed and 
        # it results in a reflection
        if self.posy <= 0 or self.posy >= HEIGHT:
            self.yFac *= -1
 
        if self.posx <= 0 and self.firstTime:
            self.firstTime = 0
            return 1
        elif self.posx >= WIDTH and self.firstTime:
            self.firstTime = 0
            return -1
        else:
            return 0
 
    def reset(self):
        self.posx = WIDTH//2
        self.posy = HEIGHT//2
        self.xFac *= -1
        self.firstTime = 1
 
    # Used to reflect the ball along the X-axis
    def hit(self):
        self.xFac *= -1
 
    def getRect(self):
        return self.ball

 
""" Game Loop """
def game_loop():
    running = True
 
    # Defining the objects
    player1 = Striker(20, 0, 10, 100, 10, GREEN)
    player2 = Striker(WIDTH-30, 0, 10, 100, 10, GREEN)
    ball = Ball(WIDTH//2, HEIGHT//2, 7, 7, WHITE)
 
    listOfGeeks = [player1, player2]
 
    # Initial parameters of the players
    player1Score, player2Score = 0, 0
    player1YFac, player2YFac = 0, 0
 
    while running:
        screen.fill(BLACK)
 
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # keyboard based movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player2YFac = -1
                if event.key == pygame.K_DOWN:
                    player2YFac = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player2YFac = 0
                
        # arduino based movement
        if player1Queue.empty():
            player1YFac = 0
        else:
            player1Direction = player1Queue.get_nowait()
            # print(player1Direction)
            # player2Directions = player2Queue.get_nowait()
            if player1Direction == 'up':
                player1YFac = -1
            elif player1Direction == 'down':
                player1YFac = 1
 
        # Collision detection
        for geek in listOfGeeks:
            if pygame.Rect.colliderect(ball.getRect(), geek.getRect()):
                ball.hit()
 
        # Updating the objects
        player1.update(player1YFac)
        player2.update(player2YFac)
        point = ball.update()
 
        # -1 -> Geek_1 has scored
        # +1 -> Geek_2 has scored
        #  0 -> None of them scored
        if point == -1:
            player1Score += 1
        elif point == 1:
            player2Score += 1
 
        # Someone has scored
        # a point and the ball is out of bounds.
        # So, we reset it's position
        if point:   
            ball.reset()
 
        # Displaying the objects on the screen
        player1.display()
        player2.display()
        ball.display()
 
        # Displaying the scores of the players
        player1.displayScore("Player 1 (Arduino) : ", 
                           player1Score, 100, 20, WHITE)
        player2.displayScore("Player 2 : ", 
                           player2Score, WIDTH-100, 20, WHITE)
 
        pygame.display.update()
        clock.tick(FPS)     


""" Main Thread """
def main():
	server_thread = threading.Thread(target=start_server)
	server_thread.start()
	game_loop()

	pygame.quit()
	httpd.shutdown()
	server_thread.join() # wait for server thread to close
 
if __name__ == "__main__":
    main()
