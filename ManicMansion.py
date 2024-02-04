# Importerer nødvendige bibloteker
import pygame, sys, random

# Bredde og høyde på vindu
WIDTH = 700
HEIGHT = 500

#Bredde og høyde midtre del
ZONE_WIDTH = 450
ZONE_HEIGHT = HEIGHT

# Størrelse på vindu
SIZE = (WIDTH, HEIGHT)

#Frames per seconds
FPS = 120

# Farger
GHOST_COLOR = (100, 100, 100)
GREEN = (80, 255, 80)
PLAYER_COLOR = (255, 0, 50)
WHITE = (255, 255, 255)
GRAY = (170, 170, 170)

#Poeng variabel
points = 0

# Initialiserer pygame
pygame.init()

# Lager overflaten til å tegne på
surface = pygame.display.set_mode(SIZE)

# Lager en klokke
clock = pygame.time.Clock()

#Felles bredde på alle objektene
object_width, object_height = 40, 40

#Klasse som lager tilfeldig y posisjon til senere objekter
class GameObject:
    def __init__(self):
        self.y_position = random.randint(object_height, HEIGHT - object_height)

    def placement(self):
        # Oppdaterer x og y posisjonene
        self.rect.x = self.x_position
        self.rect.y = self.y_position


#Klasse for sauene som arver fra GameObject klassen
class Sheep(GameObject):
    def __init__(self):
        super().__init__()
        #Setter tilfeldig x posisjon på frisonen på høyre side
        self.x_position = random.randint(WIDTH - ((WIDTH - ZONE_WIDTH) / 2), WIDTH - object_width)
        self.rect = pygame.Rect(self.x_position, self.y_position, object_width, object_height) #Lager sauen

    def placement(self):
        super().placement()

#Klasse for hindrene som skal befinne seg i midten av vinduet, arver fra GameObject
class Obstacle(GameObject):
    def __init__(self):
        super().__init__()
        self.x_position = random.randint((WIDTH - ZONE_WIDTH) / 2, (WIDTH - ((WIDTH - ZONE_WIDTH) / 2)) - object_width)
        self.rect = pygame.Rect(self.x_position, self.y_position, object_width, object_height)

    def placement(self):
        super().placement()

#Klasse for spilleren
class Human(GameObject):
    def __init__(self):
        super().__init__()
        #Tilfeldig x-posisjon i venstre frisone
        self.x_position = random.randint(0, ((WIDTH - ZONE_WIDTH) / 2 - object_width))
        self.rect = pygame.Rect(self.x_position, self.y_position, object_width, object_height)
        #Setter fart horisontalt og vertikalt til null
        self.vx = 0
        self.vy = 0

    def placement(self):
        #Oppdaterer posisjonen til spiller rektangelet men tar og sjekker etter bevegelse
        super().placement()
        
        #Legger til eventuell bevegelse i ulike retninger
        self.x_position += self.vx
        self.y_position += self.vy

        # Henter nedtrykkede knapper
        keys = pygame.key.get_pressed()

        # Sjekker etter trykk på WASD eller piltastene og beveger på spilleren ut ifra dette
        if not(player_with_sheep):
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player.vx = -1.3
            elif keys[pygame.K_RIGHT or keys[pygame.K_d]]:
                player.vx = 1.3
            else:
                player.vx = 0

            if keys[pygame.K_UP] or keys[pygame.K_w]:
                player.vy = -1.3
            elif keys[pygame.K_DOWN or keys[pygame.K_s]]:
                player.vy = 1.3
            else:
                player.vy = 0
        else:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player.vx = -0.8
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player.vx = 0.8
            else:
                player.vx = 0

            if keys[pygame.K_UP] or keys[pygame.K_w]:
                player.vy = -0.8
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                player.vy = 0.8
            else:
                player.vy = 0

#Spøkelsesklassen som arver fra GameObject
class Ghost(GameObject):
    def __init__(self):
        super().__init__()
        #Tilfeldig x-posisjon i midten
        self.x_position = random.randint((WIDTH - ZONE_WIDTH) / 2, (WIDTH - ((WIDTH - ZONE_WIDTH) / 2)) - object_width)
        self.rect = pygame.Rect(self.x_position, self.y_position, object_width, object_height)
        
        #Setter fast fart på spøkelset
        self.vx = -1
        self.vy = 1

    def placement(self):
        super().placement()

        self.x_position += self.vx
        self.y_position += self.vy

    def change_direction(self):
        #Sjekker om spøkelset beveger seg ut av det grønne området og endrer retningen hvis det er tilfellet
        if (ghost.x_position + object_width >= ZONE_WIDTH + (WIDTH - ZONE_WIDTH) / 2):
            self.vx *= -1
        
        if ghost.x_position <= (WIDTH - ZONE_WIDTH) / 2:
            self.vx *= -1

        if ghost.y_position + object_height >= HEIGHT:
            self.vy *= -1

        if ghost.y_position <= 0:
            self.vy *= -1

#Opretter spiller-objektet
player = Human()

# Lager tomme lister for sauene, hindringene og spøkelsene
sheep_list = []
obstacle_list = []
ghost_list = []

#Lager funksjoner som opretter spøkelses-, hindrings-, og saueobjekter og legger til de aktuelle lister
def add_sheep():
    sheep = Sheep()
    sheep_list.append(sheep)


def add_obstacle():
    obstacle = Obstacle()
    obstacle_list.append(obstacle)


def add_ghost():
    ghost = Ghost()
    ghost_list.append(ghost)


#Legger til tre saue- og hindringsobjekter
for i in range(3):
    add_sheep()
    add_obstacle()

# Legger til et spøkelsesobjekt
add_ghost()

#Lager font og skriftstørrelse for score-telleren
font = pygame.font.SysFont('Arial', 26)

# Funksjon som viser antall poeng
def display_points():
    text_img = font.render(f"Score: {points}", True, WHITE)
    surface.blit(text_img, (20, 10))

# Variabel som kontrollerer om spillet skal kjøre
run_program = True

# Variabel som viser om spiller holder sau eller ikke
player_with_sheep = False

# Spill-løkke
while run_program:
    #Henter nedtrykkede knapper
    keys = pygame.key.get_pressed()

    # Passer på at løkken går i riktig tempo
    clock.tick(FPS)
    
    #Fyller vinduet med grått
    surface.fill(GRAY)

    # Begrens menneskets posisjon innenfor vinduet
    player.x_position = min(max(player.x_position, 0), WIDTH - object_width)
    player.y_position = min(max(player.y_position, 0), HEIGHT - object_height)
    
    #Tegner grønne midtområdet
    pygame.draw.rect(surface, GREEN, [(WIDTH - ZONE_WIDTH) / 2, 0, ZONE_WIDTH, ZONE_HEIGHT])

    # Tegner spilleren
    pygame.draw.rect(surface, PLAYER_COLOR, [player.x_position, player.y_position, object_width, object_height])

    # Tegner hindringer
    for obstacle in obstacle_list:
        # Løkke som sjekker om hindringene kolliderer med hverandre
        for another_obstacle in obstacle_list:
            if obstacle != another_obstacle:
                if obstacle.rect.colliderect(another_obstacle.rect):
                    # Oppdaterer x og y posisjonene til de ikke koliderer
                    while obstacle.rect.colliderect(another_obstacle.rect):
                        obstacle.x_position = random.randint((WIDTH - ZONE_WIDTH) / 2, (WIDTH - ((WIDTH - ZONE_WIDTH) / 2)) - object_width)
                        obstacle.y_position = random.randint(object_height, HEIGHT - object_height)
                        obstacle.placement() #Opddaterer posisjonene
        
        #If-løkke som gjør at spilleren ikke kan bevege seg gjennom hindringene
        if player.rect.colliderect(obstacle.rect):
            if player.x_position < obstacle.x_position:
                if keys[pygame.K_RIGHT]:
                    player.vx = 0
            if player.x_position > obstacle.x_position:
                if keys[pygame.K_LEFT]:
                    player.vx = 0
            if player.y_position > obstacle.y_position:
                if keys[pygame.K_UP]:
                    player.vy = 0
            if player.y_position < obstacle.y_position:
                if keys[pygame.K_DOWN]:
                    player.vy = 0

        # Tegner hindringen
        pygame.draw.rect(surface, GRAY, [obstacle.x_position, obstacle.y_position, object_width, object_height])

    # Tegner spøkelsene
    for ghost in ghost_list:
        # Løkke som sjekker om spøkelsene kolliderer
        for another_ghost in ghost_list:
            if ghost != another_ghost:
                if ghost.rect.colliderect(another_ghost.rect):
                    # Oppdatere x og y posisjonene til de ikke lenger kolliderer
                    while not ghost.rect.colliderect(another_ghost.rect):
                        ghost.x_position = random.randint((WIDTH - ZONE_WIDTH) / 2, (WIDTH - ((WIDTH - ZONE_WIDTH) / 2)) - object_width)
                        ghost.y_position = random.randint(object_height, HEIGHT - object_height)
                        ghost.placement() #Oppdaterer posisjonen

        # Tegner spøkelsene
        pygame.draw.rect(surface, GHOST_COLOR, [ghost.x_position, ghost.y_position, object_width, object_height])

        # Oppdatereer posisjonen og sjekker etter kollisjon med "veggene"
        ghost.placement()
        ghost.change_direction()

    # Tegner sauene
    for sheep in sheep_list:
        # Løkke som sjekker om sauene kolliderer
        for another_sheep in sheep_list:
            if sheep != another_sheep:
                if sheep.rect.colliderect(another_sheep.rect):
                    #  Oppdatere x og y posisjonene til de ikke lenger kolliderer
                    while sheep.rect.colliderect(another_sheep.rect):
                        sheep.x_position = random.randint(WIDTH - ((WIDTH - ZONE_WIDTH) / 2), WIDTH - object_width)
                        sheep.y_position = random.randint(object_height, HEIGHT - object_height)
                        sheep.placement() #Oppdaterer posisjonen

        #Tegner sauen
        pygame.draw.rect(surface, WHITE, [sheep.x_position, sheep.y_position, object_width, object_height])
        
        #Sjekker om spilleren har kollidert med en sau
        if sheep.rect.colliderect(player.rect):
            #Dersom de ikke har kollidert enda så fjerner man sauen, og endrer farge på spilleren og oppdaterer variabelen
            if not(player_with_sheep):
                sheep_list.remove(sheep)
                PLAYER_COLOR = WHITE
                player_with_sheep = True
            #Dersom spilleren allerede har en sau så skal spille avsluttes
            else:
                run_program = False
    
    #Sjekker om spileren har en sau og kommer seg til venstre frisone
    if player_with_sheep and (player.x_position <= ((WIDTH - ZONE_WIDTH) / 2) - object_width):
        #Legger til ett poeng, en ny hindring, ny sau og nytt spøkelse
        points += 1
        add_ghost()
        add_sheep()
        add_obstacle()
        PLAYER_COLOR = (255, 0, 50) #Setter fargen tilbake
        player_with_sheep = False #Sier at spilleren ikke lenger har en sau
    
    for ghost in ghost_list:
        #Sjekker etter kollisjon mellom spøkelse og spiller
        if ghost.rect.colliderect(player.rect):
            run_program = False #Dersom kolliderer avsluttes program

    #Håndterer "events"
    for events in pygame.event.get():
        # Sjekker om vi vil lukke vinduet
        if events.type == pygame.QUIT:
            run_program = False  
    
    #Oppdaterer spillerens posisjon
    player.placement()
    
    #Oppdaterer antall poeng
    display_points()
    
    #  "Snur" vindu vi har tegnet på så det blir synlig
    pygame.display.flip()

# Avslutter spillet dersom ferdig
pygame.quit()

print(f"Du fikk {points} poeng")

"""
Spilleren setter seg litt fast på hindringenenår de kolliderer, det er ikke helt optimalt,
men jeg hadde ikke tid til å finne en bedre løsning. Dette er da noe jeg kommer til å prøve å endre på i etterkant.

Kunne kanskje også vært mulig å ha alle listene med objektene i en ny liste siden jeg hadde tre forløkker som
sjekket om de overlappet og da gjorde det samme.
"""