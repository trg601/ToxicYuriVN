
init -10:
    define MINIGAME_WINDOW_WIDTH = 1000
    define MINIGAME_WINDOW_HEIGHT = 800
    define MINIGAME_WINDOW_X = (renpy.config.screen_width - MINIGAME_WINDOW_WIDTH) // 2
    define MINIGAME_WINDOW_Y = (renpy.config.screen_height - MINIGAME_WINDOW_HEIGHT) // 2

transform WaveBackground:
    function WaveShader(amp=6, speed=0.03, period=8, repeat="mirror")

screen window_frame(x=0, y=0, width=800, height=600):
    add Frame("gui/window frame.png", 75, 75) xpos x ypos y xoffset -8 yoffset -8 xsize width + 12 ysize height + 12

screen streamer_window(game):
    # Lil "streamer" view of daisy bot
    tag streamer_window

    $ window_width = 400
    $ window_height = 300

    frame:
        xalign 0.0
        yalign 1.0
        xoffset 20
        yoffset -40
        xsize window_width
        ysize window_height
        button action Function(game.click_inventory)
        background "#583051ff"
        add "robot" crop (20, -50, window_width, window_height)
        use window_frame(width=window_width, height=window_height)

screen minigame(game, title="", background_color="#290b48ff"):
    tag minigame

    add Tile("minigame background") at WaveBackground
    
    on "show" action SetField(config, "mouse_displayable", MouseDisplayable("gui/hand open.png", 50, 50).add("grab", "gui/hand grab.png", 50, 50))
    on "hide" action SetField(config, "mouse_displayable", None)

    add Solid(background_color):
        xpos MINIGAME_WINDOW_X
        ypos MINIGAME_WINDOW_Y
        xsize MINIGAME_WINDOW_WIDTH
        ysize MINIGAME_WINDOW_HEIGHT

    use streamer_window(game)

    use window_frame(x=MINIGAME_WINDOW_X, y=MINIGAME_WINDOW_Y, width=MINIGAME_WINDOW_WIDTH, height=MINIGAME_WINDOW_HEIGHT)
    add game:
        xalign 0.5
        yalign 0.5

    text title:
        style "outline_text"
        size 90
        xalign 0.5
        yalign 0.5
        at fadeout

transform fadeout:
    ease 1.0 alpha 1.0
    ease 1.0 alpha 0.0