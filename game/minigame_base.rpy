
init -10:
    define MINIGAME_WINDOW_WIDTH = 1000
    define MINIGAME_WINDOW_HEIGHT = 800
    define MINIGAME_WINDOW_X = (renpy.config.screen_width - MINIGAME_WINDOW_WIDTH) // 2
    define MINIGAME_WINDOW_Y = (renpy.config.screen_height - MINIGAME_WINDOW_HEIGHT) // 2

transform WaveBackground:
    function WaveShader(amp=6, speed=0.03, period=8, repeat="mirror")

screen window_frame(x=0, y=0, width=800, height=600):
    add Frame("gui/window frame.png", 9, 39) xpos x ypos y xoffset -8 yoffset -8 xsize width + 12 ysize height + 12
    add "gui/window x button.png" xpos x + width - 30 ypos y + 2

screen streamer_window:
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
        background "#583051ff"
        add "robot" crop (20, -50, window_width, window_height)
        use window_frame(width=window_width, height=window_height)

screen minigame(game):
    tag minigame

    add Tile("minigame background") at WaveBackground
    
    add game:
        xalign 0.5
        yalign 0.5
    use window_frame(x=MINIGAME_WINDOW_X, y=MINIGAME_WINDOW_Y, width=MINIGAME_WINDOW_WIDTH, height=MINIGAME_WINDOW_HEIGHT)

    use streamer_window