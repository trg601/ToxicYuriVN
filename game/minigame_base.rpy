
init -5 python:
    def reset_minigame_screen_vars():
        global MINIGAME_WINDOW_WIDTH, MINIGAME_WINDOW_HEIGHT, MINIGAME_WINDOW_X, MINIGAME_WINDOW_Y
        global STREAMER_WINDOW_WIDTH, STREAMER_WINDOW_HEIGHT, STREAMER_WINDOW_X, STREAMER_WINDOW_Y
        MINIGAME_WINDOW_WIDTH = 1000
        MINIGAME_WINDOW_HEIGHT = 800
        MINIGAME_WINDOW_X = (renpy.config.screen_width - MINIGAME_WINDOW_WIDTH) // 2
        MINIGAME_WINDOW_Y = (renpy.config.screen_height - MINIGAME_WINDOW_HEIGHT) // 2

        STREAMER_WINDOW_WIDTH = 400
        STREAMER_WINDOW_HEIGHT = 300
        STREAMER_WINDOW_X = 20
        STREAMER_WINDOW_Y = renpy.config.screen_height - STREAMER_WINDOW_HEIGHT - 40
    reset_minigame_screen_vars()

transform WaveBackground:
    function WaveShader(amp=6, speed=0.03, period=8, repeat="mirror")

screen window_frame(x=0, y=0, width=800, height=600):
    add Frame("gui/window frame.png", 75, 75) xpos x ypos y xoffset -8 yoffset -8 xsize width + 12 ysize height + 12

default show_streamer_text = False
default streamer_text = "Maybe I should take some..."

screen streamer_window(game):
    # Lil "streamer" view of daisy bot
    tag streamer_window

    on "show" action SetVariable("show_streamer_text", False)

    frame:
        xpos STREAMER_WINDOW_X
        ypos STREAMER_WINDOW_Y
        xsize STREAMER_WINDOW_WIDTH
        ysize STREAMER_WINDOW_HEIGHT
        button action Function(game.click_inventory)
        background "#583051ff"
        add "daisy neutral" crop (200, 260, STREAMER_WINDOW_WIDTH, STREAMER_WINDOW_HEIGHT)
        use window_frame(x=-2, width=STREAMER_WINDOW_WIDTH, height=STREAMER_WINDOW_HEIGHT)
    
    if show_streamer_text:
        vbox:
            xpos STREAMER_WINDOW_X + 20
            ypos STREAMER_WINDOW_Y - 130
            xsize STREAMER_WINDOW_WIDTH - 40
            ysize 100
            text streamer_text:
                color COLOR_TEXT_MENU
                size 25
                yalign 1.0
                at streamer_text_fade

transform streamer_text_fade:
    alpha 0.0
    ease 1.0 alpha 1.0
    ease 3.0 alpha 1.0
    ease 1.0 alpha 0.0

screen minigame(game, title="", background_color="#290b48ff"):
    tag minigame

    add Tile("minigame background") at WaveBackground

    on "show" action SetVariable("default_mouse", "hand")
    on "hide" action SetVariable("default_mouse", None)

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
    ease 2.0 alpha 1.0
    ease 1.0 alpha 0.0