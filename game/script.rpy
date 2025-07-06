# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define r = Character("Robot", color="#008db0")
define e = Character("DeVila Batteus", color="#b00d0d")
define config.nearest_neighbor = True

# The game starts here.

label start:

    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    scene castle

    # This shows a character sprite. A placeholder is used, but you can
    # replace it by adding a file named "eileen happy.png" to the images
    # directory.

    show robot at left

    # These display lines of dialogue.

    r "wow.. I sure have been waiting a long while for DeVila to come back."
    r "I hope she comes back soon.."

    # call screen rice_counting_game

    show devila at right with moveinright
    e "Robot! I'm back!"
    e "I have some great news!"
    r "DeVila! You're back!\nDid you beat them this time?"
    e "Er, I have some bad news, actually.\nI didn't beat them. But... I got you a present!"
    
    # show robot blush
    r "A present? For me?"
    e "Yes! I got you a checklist, so now you can keep track of all the things you need to do!"

    # show robot annoyed
    r "Oh.. Thank you"
    hide devila with moveoutright
    "At least it's something..."

    menu:
        "Throw the checklist away?"

        "Yes":
            r "I don't need this. It's all in my head anyway."
            "You throw the checklist away."
        "No":
            r "I guess I can keep it for now."

    return
