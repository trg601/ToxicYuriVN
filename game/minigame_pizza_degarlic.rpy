
init python:
    import pygame
    import random
    import math

    class GarlicPiece:
        def __init__(self, x, y, angle):
            self.x = x
            self.y = y
            self.start_x = x
            self.start_y = y
            self.target_x = x
            self.target_y = y
            self.velocity_x = 0
            self.velocity_y = 0
            self.stuck = True
            self.active = True
            self.angle_velocity = 0
            self.angle = angle
        
        def in_bounds(self, bx, by, width, height):
            return (self.x + garlic_size > bx and self.x < bx + width and
                    self.y + garlic_size > by and self.y < by + height)

    garlic_size = 90
    garlic_per_pizza = 10

    class PizzaDegarlickingGame(renpy.Displayable):
        def __init__(self, **kwargs):
            super(PizzaDegarlickingGame, self).__init__(**kwargs)
            reset_minigame_screen_vars()
            self.width = MINIGAME_WINDOW_WIDTH
            self.height = MINIGAME_WINDOW_HEIGHT
            self.x = MINIGAME_WINDOW_X
            self.y = MINIGAME_WINDOW_Y
            self.process_timer = 0.0
            self.prev_st = None
            self.drag_offset_x = 0
            self.drag_offset_y = 0
            self.drag_x = 0
            self.drag_y = 0

            self.center_x = self.x + (self.width // 2)
            self.center_y = self.y + (self.height // 2)
            self.pizza_offset = -renpy.config.screen_width
            self.pizza_target = 0
            self.pizza_remaining = 2
            
            self.held_garlic: GarlicPiece | None = None
            self.garlic = []
            self.garlic_remaining = 1
            self.fill_garlic(garlic_per_pizza)

        def fill_garlic(self, count):
            self.garlic.clear()
            self.garlic_remaining = count
            self.held_garlic = None
            for _ in range(count):
                for _ in range(5):
                    angle = random.uniform(0, 2 * 3.141592653589793)
                    radius = random.uniform(50, self.height * 0.45)
                    garlic_x = int(self.center_x + radius * math.cos(angle)) - 60
                    garlic_y = int(self.center_y + radius * math.sin(angle)) * 0.70 + 90
                    if not self.get_garlic_at_position(garlic_x + garlic_size, garlic_y + garlic_size):
                        break
                garlic_angle = random.uniform(0, 360)
                self.garlic.append(GarlicPiece(garlic_x, garlic_y, garlic_angle))

        def get_garlic_at_position(self, x, y):
            """Get garlic piece at the given position."""
            found = None
            x -= garlic_size // 2
            y -= garlic_size // 2
            for i, garlic_piece in enumerate(self.garlic):
                if garlic_piece.active and (garlic_piece.x <= x <= garlic_piece.x + garlic_size and
                    garlic_piece.y <= y <= garlic_piece.y + garlic_size):
                    found = garlic_piece
            return found

        def process(self, st):
            """Process game step"""
            if self.pizza_offset != self.pizza_target:
                self.pizza_offset += (self.pizza_target - self.pizza_offset) * 0.1
                if abs(self.pizza_offset - self.pizza_target) < 5:
                    self.pizza_offset = self.pizza_target
                    if self.pizza_target >= renpy.config.screen_width:
                        self.pizza_offset = -renpy.config.screen_width
                        self.pizza_target = 0
                        self.fill_garlic(garlic_per_pizza)
                        renpy.restart_interaction()
                return

            for garlic_piece in self.garlic:
                if not garlic_piece.active:
                    continue
                
                garlic_piece.x += (garlic_piece.target_x - garlic_piece.x) * 0.4
                garlic_piece.y += (garlic_piece.target_y - garlic_piece.y) * 0.4

                if garlic_piece != self.held_garlic and not garlic_piece.stuck:
                    garlic_piece.velocity_y += 0.5
                
                garlic_piece.target_x += garlic_piece.velocity_x
                garlic_piece.target_y += garlic_piece.velocity_y

                if self.held_garlic == garlic_piece:
                    continue

                if not garlic_piece.in_bounds(0, 0, renpy.config.screen_width, renpy.config.screen_height):
                    garlic_piece.active = False
                    self.garlic_remaining -= 1
                    renpy.restart_interaction()
                elif garlic_piece.in_bounds(STREAMER_WINDOW_X, STREAMER_WINDOW_Y, STREAMER_WINDOW_WIDTH, STREAMER_WINDOW_HEIGHT):
                    if not self.try_give_garlic(garlic_piece):
                        center_x = STREAMER_WINDOW_X + STREAMER_WINDOW_WIDTH / 2
                        center_y = STREAMER_WINDOW_Y + STREAMER_WINDOW_HEIGHT / 2
                        dx = garlic_piece.x + garlic_size / 2 - center_x
                        dy = garlic_piece.y + garlic_size / 2 - center_y
                        distance = max(math.hypot(dx, dy), 1)
                        garlic_piece.velocity_x = (dx / distance) * 30
                        garlic_piece.velocity_y = (dy / distance) * 30

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
            render.blit(pizza_img, (self.x + self.pizza_offset, self.y + 50))
            
            # draw garlic pieces
            for garlic_piece in self.garlic:
                if not garlic_piece.active:
                    continue
                t = Transform(child="garlic", xcenter=0.5, ycenter=0.5, rotate=garlic_piece.angle, subpixel=True)
                child_render = renpy.render(t, width, height, st, at)
                render.blit(child_render, (garlic_piece.x + self.pizza_offset, garlic_piece.y))

            renpy.redraw(self, 0)
            return render

        def event(self, ev, x, y, st):
            global default_mouse
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if not self.held_garlic:
                    self.held_garlic = self.get_garlic_at_position(x, y)
                    if self.held_garlic:
                        self.drag_offset_x = self.held_garlic.x - x
                        self.drag_offset_y = self.held_garlic.y - y
                        self.drag_x = x
                        self.drag_y = y
                        self.held_garlic.velocity_x = 0
                        self.held_garlic.velocity_y = 0
                default_mouse = "grab"
            elif ev.type == pygame.MOUSEMOTION:
                if self.held_garlic:
                    if self.held_garlic.stuck:
                        dx = x - self.drag_x
                        dy = y - self.drag_y
                        distance = math.hypot(dx, dy)
                        if distance > 0:
                            move_x = self.drag_x + dx * 0.25
                            move_y = self.drag_y + dy * 0.25
                            self.held_garlic.target_x = move_x + self.drag_offset_x
                            self.held_garlic.target_y = move_y + self.drag_offset_y
                            if distance > 200:
                                self.held_garlic.stuck = False
                    else:
                        self.held_garlic.target_x = x + self.drag_offset_x
                        self.held_garlic.target_y = y + self.drag_offset_y
            elif ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                default_mouse = "hand"
                if self.held_garlic:
                    if self.held_garlic.stuck:
                        self.held_garlic.target_x = self.held_garlic.start_x
                        self.held_garlic.target_y = self.held_garlic.start_y
                    else:
                        dx = x - self.held_garlic.x
                        dy = y - self.held_garlic.y
                        if abs(dx) > 90:
                            self.held_garlic.velocity_x = dx * 0.15
                        if abs(dy) > 90:
                            self.held_garlic.velocity_y = dy * 0.15
                    self.held_garlic = None
            # elif ev.type == pygame.KEYDOWN:
            #     if ev.key == pygame.K_LEFT:
            #         self.fill_garlic(500)
            
            if self.garlic_remaining <= 0 and self.pizza_target == self.pizza_offset:
                if self.pizza_remaining > 0:
                    self.pizza_remaining -= 1
                    self.pizza_target = renpy.config.screen_width
                    renpy.notify(f"Pizza {2 - self.pizza_remaining} complete!")
                else:
                    renpy.notify("All pizzas de-garlicked!")
                    close_inventory()
                    return 1  # End the game when all garlic on all pizzas are removed
        
        def try_give_garlic(self, garlic_piece) -> bool:
            global default_mouse
            if garlic_piece and try_add_inventory_item("Garlic", "A peeled garlic clove.", "gui/item garlic.png", 2):
                garlic_piece.active = False
                self.garlic_remaining -= 1
                if self.held_garlic == garlic_piece:
                    self.held_garlic = None
                    default_mouse = "hand"
                renpy.restart_interaction()
                return True
            return False
            
        def click_inventory(self):
            """Handle clicking on the inventory icon."""
            self.try_give_garlic(self.held_garlic)
            
screen pizza_degarlicking_game:
    tag minigame

    default game = PizzaDegarlickingGame()
    use minigame(game, "Remove all the garlic!", background_color="#6c0141ff")
    text "degarlicking.exe - [game.garlic_remaining] garlic pieces remaining":
        style "outline_text"
        xpos MINIGAME_WINDOW_X + 20
        ypos MINIGAME_WINDOW_Y
        size 32
