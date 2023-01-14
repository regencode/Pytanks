import pygame

class GUI():
    def __init__(self, game):

        # Initialize game variables for easy access
        self.game = game
        self.screen = game.screen
        self.screen_rect = game.screen_rect
        self.clock = game.clock
        self.settings = game.settings
        self.player = game.player.sprite

        # Initialize font
        self.font = pygame.font.Font("resources\Game\GothamRoundedMedium.ttf", 50)

        # Initialize score
        self.score = 0

        # Initialize current player level
        self.currentPlayerLevel = 0



    def displayCurrentPlayerLevel(self):
        self.currentPlayerLevel = self.player.level
        
        self.levelDisplay = self.font.render(f"Level {self.currentPlayerLevel}", True, "Black")
        self.levelDisplay_rect = self.expSide.get_rect(midbottom = self.player.rect.midtop)
        self.screen.blit(self.levelDisplay, self.levelDisplay_rect)

    def displayPlayerHealthBar(self):
        self.currentHealth = self.player.health
        self.maxHealth = self.settings.player_maxHealth

        # Get number of health bars and draw on screen (each bar represents 10% exp, and takes up a space of 40px including margin)
        self.numHealthBars = int(round(((self.currentHealth/self.maxHealth)/0.10)))
        for x in range(400, 400+(self.numHealthBars*40), 40):
            redBar = pygame.draw.rect(self.screen, "Red",(x, 700, 35, 35))
        self.healthBar = pygame.draw.rect(self.screen, "Gray", (400, 700, 400, 35), 5)

        # To indicate that the bar is for health points
        self.hpSide = self.font.render("HP", True, "Black", "Gray")
        self.hpSide_rect = self.hpSide.get_rect(midright = self.healthBar.midleft)
        self.screen.blit(self.hpSide, self.hpSide_rect)


    def updateScore(self):
        self.score += 1

    def displayExpBar(self):
        # Get current player exp from player
        self.playerExp = self.player.exp
        self.currentExpThreshold = self.settings.expThresholds[self.currentPlayerLevel]

        # Get number of exp bars and draw on screen (each bar represents 10% exp, and takes up a space of 40px including margin)
        self.numExpBars = int(round(((self.playerExp/self.currentExpThreshold)/0.10)))
        for x in range(400, 400+(self.numExpBars*40), 40):
            yellowBar = pygame.draw.rect(self.screen, "Yellow",(x, 750, 35, 20))
        self.expBar = pygame.draw.rect(self.screen, "Gray", (400, 750, 400, 20), 5)

    
        # To indicate that the bar is for health points
        self.expSide = self.font.render("EXP", True, "Black", "Gray")
        self.expSide_rect = self.expSide.get_rect(midright = self.expBar.midleft)
        self.screen.blit(self.expSide, self.expSide_rect)


        # Display numeric value of exp
        self.expCounter = self.font.render(f"EXP: {str(round(self.playerExp))}xp/{str(self.currentExpThreshold)}xp", True, "Black")
        self.expCounter_rect = self.expCounter.get_rect(midbottom = self.screen_rect.midbottom)
        self.expCounter_rect.y -= 30
        self.screen.blit(self.expCounter, self.expCounter_rect)


    def displayTime(self):
        self.timeboard = self.font.render(f"Time alive: {str(self.game.global_tick//1000)}s", True, "Black")
        self.timeboard_rect = self.timeboard.get_rect( midtop = self.screen_rect.midtop )
        self.timeboard_rect.y += 30
        self.screen.blit(self.timeboard, self.timeboard_rect)

    def displayScore(self):

        # Scoreboard
        self.scoreboard = self.font.render(f"Kills: {str(self.score)} ", True, "Black")
        self.scoreboard_rect = self.scoreboard.get_rect( midtop = self.screen_rect.midtop )
        self.scoreboard_rect.y += 10
        self.screen.blit(self.scoreboard, self.scoreboard_rect)

    def displayFramesPerSecond(self):
        self.frames_now = self.clock.get_fps()
        self.font = pygame.font.Font("resources\Game\GothamRoundedMedium.ttf", 25)
        self.fps_counter = self.font.render(f"FPS: {str(self.frames_now//1)}", True, "red")
        self.fps_counter_rect = self.fps_counter.get_rect( topleft = self.screen_rect.topleft )
        self.screen.blit(self.fps_counter, self.fps_counter_rect)

    def update(self):
        # Updates
        pass


    def custom_draw(self):
        # Updates and gets

        # Displays
        self.displayScore()
        self.displayTime()
        self.displayExpBar()
        self.displayCurrentPlayerLevel()
        self.displayPlayerHealthBar()
        self.displayFramesPerSecond()  

