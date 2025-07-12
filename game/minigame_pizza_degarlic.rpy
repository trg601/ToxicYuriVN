
init python:
    import pygame
    import random
    import math

    class GarlicPiece:
        def __init__(self, x, y, angle):
            self.x = x
            self.y = y
            self.stuck_x = x
            self.stuck_y = y
            self.target_x = x
            self.target_y = y
            self.velocity_x = 0
            self.velocity_y = 0
            self.stuck = True
            self.active = True
            self.angle = angle
    
    garlic_size = 90

    class PizzaDegarlickingGame(renpy.Displayable):
        def __init__(self, **kwargs):
            super(PizzaDegarlickingGame, self).__init__(**kwargs)
            self.width = MINIGAME_WINDOW_WIDTH
            self.height = MINIGAME_WINDOW_HEIGHT
            self.x = MINIGAME_WINDOW_X
            self.y = MINIGAME_WINDOW_Y
            self.process_timer = 0.0
            self.prev_st = None

            center_x = self.x + (self.width // 2)
            center_y = self.y + (self.height // 2)
            
            self.held_garlic: GarlicPiece | None = None
            self.garlic = []
            self.garlic_remaining = 1
            self.fill_garlic(30)

        def fill_garlic(self, count):
            self.garlic.clear()
            self.garlic_remaining = count
            self.held_garlic = None
            center_x = self.x + (self.width // 2)
            center_y = self.y + (self.height // 2)
            for _ in range(count):
                angle = random.uniform(0, 2 * 3.141592653589793)
                radius = random.uniform(0, self.height // 2)
                garlic_x = int(center_x + radius * math.cos(angle)) - 50
                garlic_y = int(center_y + radius * math.sin(angle)) * 0.75 + 70
                garlic_angle = random.uniform(0, 360)
                self.garlic.append(GarlicPiece(garlic_x, garlic_y, garlic_angle))

        def get_garlic_at_position(self, x, y):
            """Get garlic piece at the given position."""
            for garlic_piece in self.garlic:
                if garlic_piece.active and (garlic_piece.x <= x <= garlic_piece.x + garlic_size and
                    garlic_piece.y <= y <= garlic_piece.y + garlic_size):
                    return garlic_piece

        def process(self, st):
            """Process game step"""
            for garlic_piece in self.garlic:
                if not garlic_piece.active:
                    continue
                
                garlic_piece.x += (garlic_piece.target_x - garlic_piece.x) * 0.4
                garlic_piece.y += (garlic_piece.target_y - garlic_piece.y) * 0.4

                if garlic_piece != self.held_garlic and not garlic_piece.stuck:
                    garlic_piece.velocity_y += 0.5
                
                garlic_piece.target_x += garlic_piece.velocity_x
                garlic_piece.target_y += garlic_piece.velocity_y

                if (garlic_piece.x + garlic_size < 0 or garlic_piece.x > renpy.config.screen_width
                or garlic_piece.y + garlic_size < 0 or garlic_piece.y > renpy.config.screen_height):
                    garlic_piece.active = False
                    self.garlic_remaining -= 1
                    renpy.restart_interaction()

        def render(self, width, height, st, at):
            """Render the game"""
            render = renpy.Render(width, height)
            canvas = render.canvas()

            delta_time = st - (self.prev_st or st)
            self.prev_st = st
            self.process_timer += delta_time

            if self.process_timer > 0.01:
                self.process(st)
                self.process_timer = 0.0
            
            pizza_img = renpy.load_image("images/pizza.png")
            render.blit(pizza_img, (self.x, self.y + 50))
            
            # draw garlic pieces
            for garlic_piece in self.garlic:
                if not garlic_piece.active:
                    continue
                t = Transform(child="images/garlic.png", rotate=garlic_piece.angle, subpixel=True)
                child_render = renpy.render(t, width, height, st, at)
                render.blit(child_render, (garlic_piece.x, garlic_piece.y))

            renpy.redraw(self, 0)
            return render

        def event(self, ev, x, y, st):
            global default_mouse
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if not self.held_garlic:
                    self.held_garlic = self.get_garlic_at_position(x, y)
                    if self.held_garlic and self.held_garlic.stuck:
                        self.held_garlic.stuck_x = x
                        self.held_garlic.stuck_y = y
                default_mouse = "grab"
            elif ev.type == pygame.MOUSEMOTION:
                if self.held_garlic:
                    if self.held_garlic.stuck:
                        dx = x - self.held_garlic.stuck_x
                        dy = y - self.held_garlic.stuck_y
                        distance = math.hypot(dx, dy)
                        if distance > 0:
                            move_x = self.held_garlic.stuck_x + dx * 0.25
                            move_y = self.held_garlic.stuck_y + dy * 0.25
                            self.held_garlic.target_x = move_x - garlic_size // 2
                            self.held_garlic.target_y = move_y - garlic_size // 2
                            if distance > 150:
                                self.held_garlic.stuck = False
                    else:
                        self.held_garlic.target_x = x - garlic_size // 2
                        self.held_garlic.target_y = y - garlic_size // 2
            elif ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                default_mouse = None
                if self.held_garlic:
                    if not self.held_garlic.stuck:
                        dx = x - self.held_garlic.x
                        dy = y - self.held_garlic.y
                        if abs(dx) > 50:
                            self.held_garlic.velocity_x = dx * 0.15
                        if abs(dy) > 50:
                            self.held_garlic.velocity_y = dy * 0.25
                    self.held_garlic = None
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_LEFT:
                    self.fill_garlic(500)
            
            if self.garlic_remaining <= 0:
                renpy.notify("All garlic removed!")
                return 1  # End the game when all garlic is removed

        def click_inventory(self):
            """Handle clicking on the inventory icon."""
            global default_mouse
            if self.held_garlic and try_add_inventory_item("Garlic", "A peeled garlic clove.", "gui/item garlic.png"):
                self.held_garlic.active = False
                self.garlic_remaining -= 1
                default_mouse = None
                renpy.restart_interaction()
            
screen pizza_degarlicking_game:
    tag minigame

    default game = PizzaDegarlickingGame()
    use minigame(game, "Remove all the garlic!", background_color="#6c0141ff")
    text "[game.garlic_remaining] garlic pieces remaining":
        style "outline_text"
        xpos MINIGAME_WINDOW_X + 20
        ypos MINIGAME_WINDOW_Y
        size 32
