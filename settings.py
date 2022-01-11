class Settings:
    def __init__(self):
        # Screen Settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_colour = (50,50,50)

        # Ship Settings
        self.ship_speed = 1.5

        # Bullet Settings
        self.bullet_speed = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_colour = (124, 252, 0)
        self.bullets_allowed = 5

        # Alien Settings
        self.alien_speed = 0.5
        self.fleet_drop_speed = 10
        self.fleet_direction = 1