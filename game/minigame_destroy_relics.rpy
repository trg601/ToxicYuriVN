
init python:
    import pygame
    import random
    import math

    class Relic:
        def __init__(self, x, y, scale):
            self.x = x
            self.y = y
            self.angle = 0
            self.scale = scale
            self.index = 0
            self.shake_timer = 0.0
            self.hp = math.ceil(10 * scale)
            self.stage_hp = self.hp
        
        def split(self, relics):
            """Split the relic into smaller parts."""
            distance = 200 * self.scale
            for i in range(3):
                new_relic = Relic(self.x, self.y, self.scale / 2)
                angle = i * (2 * math.pi / 3) + 22.5
                new_relic.x += int(distance * math.cos(angle))
                new_relic.y += int(distance * math.sin(angle))
                new_relic.index = 0
                relics.append(new_relic)
        
        def in_bounds(self, x, y):
            return (x >= self.x - 300 * self.scale and x <= self.x + 300 * self.scale
                    and y >= self.y - 350 * self.scale and y <= self.y + 350 * self.scale)

    class DestroyRelicsGame(renpy.Displayable):
        def __init__(self, **kwargs):
            super(DestroyRelicsGame, self).__init__(**kwargs)
            reset_minigame_screen_vars()
            self.width = MINIGAME_WINDOW_WIDTH
            self.height = MINIGAME_WINDOW_HEIGHT
            self.x = MINIGAME_WINDOW_X
            self.y = MINIGAME_WINDOW_Y
            self.process_timer = 0.0
            self.prev_st = None
            self.center_x = self.x + (self.width // 2)
            self.center_y = self.y + (self.height // 2)
            self.drag_offset_x = 0
            self.drag_offset_y = 0
            self.drag_relic = None

            self.relics = [Relic(self.center_x, self.center_y, 1)]

            self.cross_images = [renpy.displayable("cross 1"), renpy.displayable("cross 2"), renpy.displayable("cross 3")]
            
        def process(self, st):
            """Process game step"""
            for relic in self.relics:
                if relic.shake_timer > 0:
                    relic.shake_timer -= 1
                    relic.angle = random.uniform(-5, 5)
                    if relic.shake_timer <= 0:
                        relic.angle = 0

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

            for relic in self.relics:
                cross_trans = Transform(child=self.cross_images[relic.index], rotate=relic.angle, zoom=relic.scale)
                cross_render = renpy.render(cross_trans, width, height, st, at)
                render.blit(cross_render, (relic.x - 500 * relic.scale, relic.y - 500 * relic.scale))

            renpy.redraw(self, 0)
            return render

        def event(self, ev, x, y, st):
            global default_mouse
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                for relic in self.relics:
                    if relic.in_bounds(x, y):
                        relic.shake_timer = 5
                        relic.hp -= 1
                        if relic.hp <= 0:
                            relic.index += 1
                            relic.hp = relic.stage_hp
                            if relic.index >= len(self.cross_images):
                                self.relics.remove(relic)
                                if relic.scale > 0.25:
                                    relic.split(self.relics)
                                if relic.scale == 0.5:
                                    global show_streamer_text, streamer_text
                                    show_streamer_text = True
                                    streamer_text = "Maybe I should take a relic shard... For later..."
                                    renpy.restart_interaction()
                        elif relic.scale < 0.5:
                            self.drag_relic = relic
                            self.drag_offset_x = relic.x - x
                            self.drag_offset_y = relic.y - y
            if ev.type == pygame.MOUSEMOTION:
                default_mouse = "hand"
                for relic in self.relics:
                    if relic.in_bounds(x, y):
                        default_mouse = "grab"
                if self.drag_relic:
                    self.drag_relic.x = min(max(x + self.drag_offset_x, 50), renpy.config.screen_width - 50)
                    self.drag_relic.y = min(max(y + self.drag_offset_y, 50), renpy.config.screen_height - 50)
            if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                self.drag_relic = None

            if len(self.relics) == 0:
                renpy.notify("Relic(s) destroyed!")
                default_mouse = None
                close_inventory()
                return 1

        def click_inventory(self):
            """Handle clicking on the inventory icon."""
            if not self.drag_relic:
                for relic in self.relics:
                    if (relic.x >= STREAMER_WINDOW_X and relic.x <= STREAMER_WINDOW_X + STREAMER_WINDOW_WIDTH and
                        relic.y >= STREAMER_WINDOW_Y and relic.y <= STREAMER_WINDOW_Y + STREAMER_WINDOW_HEIGHT):
                        self.drag_relic = relic
                        break
            if self.drag_relic and try_add_inventory_item("Relic", "A shard of a relic.", "gui/item relic.png", 4):
                self.relics.remove(self.drag_relic)
                self.drag_relic = None
                renpy.restart_interaction()
            
screen destroy_relics_game:
    tag minigame

    default game = DestroyRelicsGame()
    use minigame(game, "Destroy the relic(s)!", background_color="#341b3bff")

    text "crucibuster.exe":
        style "outline_text"
        xpos MINIGAME_WINDOW_X + 20
        ypos MINIGAME_WINDOW_Y
        size 32
