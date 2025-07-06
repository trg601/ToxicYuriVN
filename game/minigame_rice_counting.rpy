
init python:
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

            # Initialize a grid with random rice counts
            self.grid_width = self.width // int(CELL_SIZE)
            self.grid_height = self.height // int(CELL_SIZE)
            # self.rice_grid = [[
            #     random.choice([0, 0, 0, 0, 1, 2, 3]) * (1 if y < 50 and ( 25 < x < 75) else 0) for x in range(self.grid_width)]
            #     for y in range(self.grid_height)]
            self.rice_grid = [[0 for x in range(self.grid_width)] for y in range(self.grid_height)]
            self.total_rice = 0
            self.rice_held = 0
            self.rice_counted = 0

            for _ in range(10):
                rx = random.randint(5, self.grid_width - 6)
                ry = random.randint(self.grid_height // 2, self.grid_height - 6)
                radius = random.randint(4, 6)
                self.add_circle(rx, ry, radius)

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

            renpy.redraw(self, 0)
            return render

        def event(self, ev, x, y, st):
            global default_mouse
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                x = int(x - self.x) // int(CELL_SIZE)
                y = int(y - self.y) // int(CELL_SIZE)
                if self.rice_held:
                    self.add_circle(x, y, 5, from_held=True)
                else:
                    rice_before = self.total_rice
                    self.remove_circle(x, y, 5)
                    self.rice_held = rice_before - self.total_rice
                default_mouse = "grab" if self.rice_held > 0 else None

            # If all rice is collected, game over
            if self.total_rice <= 0 and self.rice_held == 0:
                renpy.notify("All rice collected!")
                return 1
                
        def add_to_bin(self):
            self.rice_counted += self.rice_held
            self.rice_held = 0
            renpy.notify("Rice added to bin!")

screen rice_counting_game:
    # custom mouse cursor
    on "show" action SetField(config, "mouse_displayable", MouseDisplayable("gui/hand open.png", 50, 50).add("grab", "gui/hand grab.png", 50, 50))
    on "hide" action SetField(config, "mouse_displayable", None)

    default game = RiceCountingGame()
    use minigame(game)

    imagebutton:
        idle "gui/trash bin.png"
        hover "gui/trash bin.png"
        xpos MINIGAME_WINDOW_X + MINIGAME_WINDOW_WIDTH + 50
        ypos MINIGAME_WINDOW_Y + MINIGAME_WINDOW_HEIGHT - 300
        action [Function(game.add_to_bin), SetVariable("default_mouse", None)]
    text "[game.rice_counted] grains of rice" xpos MINIGAME_WINDOW_X + MINIGAME_WINDOW_WIDTH + 50 ypos MINIGAME_WINDOW_Y + MINIGAME_WINDOW_HEIGHT + 20 color "#ffffff" size 32
