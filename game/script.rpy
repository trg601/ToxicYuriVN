label start:

    jump day1

    scene castle

    show robot at left

    # These display lines of dialogue.

    daisy "wow.. I sure have been waiting a long while for DeVila to come back."
    daisy "I hope she comes back soon.."

    # call screen rice_counting_game

    show devila at right
    batta "Robot! I'm back!"
    batta "I have some great news!"
    daisy "DeVila! You're back!\nDid you beat them this time?"
    batta "Er, I have some bad news, actually.\nI didn't beat them. But... I got you a present!"
    
    # show robot blush
    daisy "A present? For me?"
    batta "Yes! I got you a checklist, so now you can keep track of all the things you need to do!"

    # show robot annoyed
    daisy "Oh.. Thank you"
    hide devila
    "At least it's something..."

    menu:
        "Throw the checklist away?"

        "Yes":
            daisy "I don't need this. It's all in my head anyway."
            "You throw the checklist away."
        "No":
            daisy "I guess I can keep it for now."

    return
