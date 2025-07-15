label day3:
    scene garden with fade
    play music "yuri waltz.mp3"
    show screen day_title(3)
    show daisy exsasperated at left with fastdissolve
    daisy "Tulong, when I'm through trimming these rose bushes I am going to need those hedge clippers."
    
    daisy "And I can't use them if they're in your stomach."
    
    show tulong at right with fastdissolve
    tulong "SNIP! SNIP SNIP! NOT TOO LONG!"
    
    # Tulong leaves.
    hide tulong with fastdissolve
    show daisy frustrated
    daisy "Tulong, what did I say about running with-"
    
    show daisy suprised
    daisy "Eek!"
    
    show batta normal shocked at right with fastdissolve
    batta "Oh!"
    
    show batta normal sultry
    batta "Well Darling Bug, it seems as though you've fallen for me once again~"
    
    show daisy flustered
    daisy "M-my Lady? What are you doing out here?"
    
    show batta relaxed haughty
    batta "Hm. I am the Villainous Countess of this Evil Keep- do I need a {i}reason{/i} to be anywhere within my own home?"
    
    show daisy confused
    daisy "No, My Lady. It's just..."
    
    daisy "Why choose right below me while I'm standing on a ladder? It doesn't seem the most... picturesque. Or safe."
    
    show batta normal sultry
    batta "On the contrary, up there's a view like no other..."
    
    daisy "Say that again, My Lady?"
    
    show batta relaxed haughty
    batta "Merely keeping an Evil Eye on you after your... disappointing performance yesterday morning, DAISY-BOT. To see if your... current state of disrepair gets any worst before I can see my wicked plans though by week's end."
    
    batta "I certainly don't need anything else holding me back."
    
    show daisy neutral
    daisy "...I see. I understand, My Lady. Please, resume your monitoring as you see fit."
    
    batta "I don't need your permission to do so!"
    
    daisy "..."
    
    batta "..."
    
    show batta normal neutral
    batta "..."
    
    batta "DAISY? Darling Bug, have I ever told you why I asked you to plant these specific types of flowers here in my Wicked Garden of Horrific Horticulture?"
    
    show daisy confused
    daisy "?"
    
    daisy "No, My Lady... you simply ordered me to plant them, and I followed suit."
    
    show batta normal shocked
    batta "Well, you could've asked at any point!"
    
    daisy "..."
    
    daisy "Are you... would you like me to ask you know?"
    
    batta "Only if... only if you want to."
    
    show batta relaxed haughty
    batta "Which you should! As keeper of these grounds, I put a lot of time and consideration into my choices! Everything has a reason!"
    
    show daisy happy
    daisy "Okay, My Lady. Tell me about..."

    default good_choice = False
    
    menu:
        "Tell me about..."
        "\"TELL ME ABOUT THE VIOLETS\"":
            show batta normal happy
            batta "Those are one of my favorites, you know."
            
            batta "Once there lived an ancient poet who wrote verse after verse about beautiful women who wreathed themselves in garlands of violets, who wore them in their hair..."
            
            batta "...here. Just like that."
            
            show daisy flustered
            daisy "My Lady?!"
            
            show batta normal sultry
            batta "It suits you, DAISY-BOT. I suppose I can understand what all the fuss is about."

            $ good_choice = True
        
        "\"TELL ME ABOUT THE WHITE LILIES\"":
            show batta normal happy
            batta "Those are one of my favorites, you know."
            
            batta "Long ago, there was an ancient land far to the east where the white lily was said to have symbolized the beauty and purity of women."
            
            batta "Even becoming a symbol for the of the lost, mythical art of YURI."
            
            show daisy confused
            daisy "What is YURI-"
            
            show daisy suprised
            daisy "!!!"
            
            daisy "My Lady, my hair-"
            
            show batta normal sultry
            batta "Keep it there. It suits you."

            $ good_choice = True
            
        "\"TELL ME ABOUT THE BLACK ROSES\"":
            play sound "item miss!.mp3"
            show batta normal shocked
            batta "Alright, well, to be honest DAISY-BOT, my Darling, I was sort of hoping you would ask about some of the other flowers..."
            
            batta "I had just chosen these because I thought they looked cool."
            
            show daisy exsasperated
            daisy "They are notably less cool whenever they wedge into the cracks of my metal casing and jam up my finger servos, My Lady."
            
            show batta normal embarrassed
            batta "I don't recall making you so delicate, DAISY-BOT."
            
            show batta relaxed angry
            batta "Maybe you really are broken after all if all it takes to keep you from doing your job are a few measly thorns."
            
            show daisy neutral
            daisy "..."

            $ good_choice = False
    
    daisy "My Lady, I-"
    
    show batta normal neutral
    batta "Get back to work, DAISY."
    
    batta "And take care not to fall again. I may not be around to catch you next time."
    
    # Batta leaves.
    hide batta with fastdissolve
    daisy "..."

    if good_choice:
        "You find a laser weedwhacker on the ground."
        $ try_add_inventory_item("Laser weedwhacker", "A tool for trimming plants with lasers.", "gui/item weedwhacker.png", 1)
        $ folder_open = True
        "Picked up the weedwhacker. It seems quite dangerous the more you look at it."
        $ folder_open = False
        
    show tulong at right with fastdissolve

    daisy "Tulong, please pass me those hedge clippers."
    
    tulong "SCISSOR! YOU WANT TO SCISSOR?"
    
    show daisy flustered
    daisy "Tulong-"
    
    jump day4
