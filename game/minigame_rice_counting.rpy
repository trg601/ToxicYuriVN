
init python:
    import math
    import random
    import pygame

    RICE_COLORS = ["#ffffff", "#cccccc", "#999999"]
    CELL_SIZE = 10.0
    CELL_RADIUS = CELL_SIZE * 0.7

    class RiceCountingGame(renpy.Displayable):
        def __init__(self, **kwargs):
            super(RiceCountingGame, self).__init__(**kwargs)
            self.width = MINIGAME_WINDOW_WIDTH
            self.height = MINIGAME_WINDOW_HEIGHT
            self.x = MINIGAME_WINDOW_X
            self.y = MINIGAME_WINDOW_Y
            self.process_timer = 0.0
            self.prev_st = None

            self.bin_x = self.x + self.width + 50
            self.bin_y = self.y + self.height - 300

            # Initialize a grid with random rice counts
            self.grid_width = self.width // int(CELL_SIZE)
            self.grid_height = self.height // int(CELL_SIZE)
            self.min_process_y = 0
            # self.rice_grid = [[
            #     random.choice([0, 0, 0, 0, 1, 2, 3]) * (1 if y < 50 and ( 25 < x < 75) else 0) for x in range(self.grid_width)]
            #     for y in range(self.grid_height)]
            self.rice_grid = [[0 for x in range(self.grid_width)] for y in range(self.grid_height)]
            self.total_rice = 0
            self.rice_held = 0
            self.rice_grab_radius = 7
            self.rice_counted = 0

            for _ in range(10):
                rx = random.randint(5, self.grid_width - 6)
                ry = random.randint(self.grid_height // 2, self.grid_height - 6)
                radius = random.randint(4, 6)
                self.add_circle(rx, ry, radius)

            self.rice_ball_grid_size = self.rice_grab_radius * 2
            self.rice_ball_grid = [[0 for x in range(self.rice_ball_grid_size + 1)] for y in range(self.rice_ball_grid_size + 1)]
            self.rice_ball_x = None
            self.rice_ball_y = None
            self.rice_falling_count = 0

        def in_bounds(self, x: int, y: int) -> bool:
            return 0 <= x < self.grid_width and 0 <= y < self.grid_height

        def check(self, x: int, y: int) -> int:
            if self.in_bounds(x, y):
                return self.rice_grid[y][x]
            return 0

        def try_add(self, x: int, y: int) -> bool:
            if self.in_bounds(x, y) and not self.rice_grid[y][x]:
                self.rice_grid[y][x] = random.randint(1, 3)
                self.total_rice += 1
                return True
            return False
    
        def try_remove(self, x: int, y: int):
            if self.in_bounds(x, y) and self.rice_grid[y][x]:
                self.rice_grid[y][x] = 0
                self.total_rice -= 1

        def add_circle(self, x: int, y: int, radius: int, from_held: bool = False):
            for dy in range(-radius, radius + 1):
                for dx in range(-radius, radius + 1):
                    if dx * dx + dy * dy <= radius * radius:
                        if self.try_add(x + dx, y + dy) and from_held:
                            self.rice_held -= 1
                            if self.rice_held <= 0:
                                return

        def remove_circle(self, x: int, y: int, radius: int):
            for dy in range(-radius, radius + 1):
                for dx in range(-radius, radius + 1):
                    if dx * dx + dy * dy <= radius * radius:
                        self.try_remove(x + dx, y + dy)

        def create_rice_ball(self, radius: int):
            for y in range(self.rice_ball_grid_size):
                for x in range(self.rice_ball_grid_size):
                    self.rice_ball_grid[y][x] = 0
            x = y = self.rice_ball_grid_size // 2
            
            for dy in range(-radius, radius + 1):
                for dx in range(-radius, radius + 1):
                    if self.rice_held <= 0:
                        return
                    if dx * dx + dy * dy <= radius * radius:
                        self.rice_ball_grid[y + dy][x + dx] = random.randint(1, 3)
                        self.rice_held -= 1

        def process(self, st):
            """Process game step"""
            for y in reversed(range(self.grid_height)):
                for x in range(self.grid_width):
                    if (value := self.check(x, y)) and y < self.grid_height - 1:
                        if not self.check(x, y + 1):
                            self.rice_grid[y][x] = 0
                            self.rice_grid[y + 1][x] = value
                        elif not self.check(x + 1, y + 1) and not self.check(x + 1, y) and x < self.grid_width - 1:
                            self.rice_grid[y][x] = 0
                            self.rice_grid[y + 1][x + 1] = value
                        elif not self.check(x - 1, y + 1) and not self.check(x - 1, y) and x > 0:
                            self.rice_grid[y][x] = 0
                            self.rice_grid[y + 1][x - 1] = value
            
            if self.rice_ball_x is not None and self.rice_ball_y is not None:
                self.rice_ball_y += CELL_SIZE
                if self.rice_ball_y > self.bin_y + 100:
                    self.rice_ball_x = None
                    self.rice_ball_y = None
                    self.rice_counted += self.rice_falling_count
                    renpy.restart_interaction()  # Ensure the label updates after rice is counted

        def render(self, width, height, st, at):
            """Render the game"""
            render = renpy.Render(width, height)
            canvas = render.canvas()
            canvas.rect("#290b48ff", (self.x, self.y, self.width, self.height))

            delta_time = st - (self.prev_st or st)
            self.prev_st = st
            self.process_timer += delta_time

            if self.process_timer > 0.01:
                for _ in range(3):
                    self.process(st)
                self.process_timer = 0.0
                
            # Draw the rice grid
            for y in range(self.grid_height):
                for x in range(self.grid_width):
                    if value := self.rice_grid[y][x]:
                        canvas.circle(
                            RICE_COLORS[value - 1],
                            (self.x + (x * CELL_SIZE), self.y + (y * CELL_SIZE)),
                            CELL_RADIUS, CELL_RADIUS
                        )
            
            # Draw the rice ball
            if self.rice_ball_x is not None and self.rice_ball_y is not None:
                for y in range(self.rice_ball_grid_size):
                    for x in range(self.rice_ball_grid_size):
                        if value := self.rice_ball_grid[y][x]:
                                canvas.circle(
                                    RICE_COLORS[value - 1],
                                    (self.rice_ball_x + (x * CELL_SIZE), self.rice_ball_y + (y * CELL_SIZE)),
                                    CELL_RADIUS, CELL_RADIUS
                                )

            # Draw trash bin
            bin_img = renpy.load_image("gui/trash bin.png")
            render.blit(bin_img, (self.bin_x, self.bin_y))

            renpy.redraw(self, 0)
            return render

        def event(self, ev, x, y, st):
            global default_mouse
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                mx = int(x - self.x) // int(CELL_SIZE)
                my = int(y - self.y) // int(CELL_SIZE)
                if self.rice_held:
                    deposit_radius = max(2, math.ceil((self.rice_held / math.pi) ** 0.5))
                    if x > self.bin_x:
                        self.add_to_bin(y, deposit_radius)
                    else:
                        self.add_circle(mx, my, deposit_radius, from_held=True)
                else:
                    rice_before = self.total_rice
                    self.remove_circle(mx, my, self.rice_grab_radius)
                    self.rice_held = rice_before - self.total_rice
                default_mouse = "grab" if self.rice_held > 0 else None

            # If all rice is collected, game over
            if self.total_rice <= 0 and self.rice_held == 0 and self.rice_ball_x is None:
                renpy.notify("All rice collected!")
                return 1
                
        def add_to_bin(self, y: int, deposit_radius: int):
            if self.rice_falling_count > 0:
                self.rice_counted += self.rice_falling_count
                self.rice_falling_count = 0

            if y < self.bin_y:
                rice_radius_size = self.rice_grab_radius * CELL_SIZE
                self.rice_ball_x = self.bin_x + 140 - rice_radius_size
                self.rice_ball_y = y - rice_radius_size
                self.rice_falling_count = self.rice_held
                self.create_rice_ball(deposit_radius)
            else:
                self.rice_counted += self.rice_held
            self.rice_held = 0
            renpy.restart_interaction()  # Ensure the label updates after rice is counted

screen rice_counting_game:
    # custom mouse cursor
    on "show" action SetField(config, "mouse_displayable", MouseDisplayable("gui/hand open.png", 50, 50).add("grab", "gui/hand grab.png", 50, 50))
    on "hide" action SetField(config, "mouse_displayable", None)

    default game = RiceCountingGame()
    use minigame(game, "Collect the Rice!")

    text "[game.rice_counted] grains of rice" xpos MINIGAME_WINDOW_X + MINIGAME_WINDOW_WIDTH + 50 ypos MINIGAME_WINDOW_Y + MINIGAME_WINDOW_HEIGHT + 20 color "#ffffff" size 32
