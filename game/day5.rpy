label day5:
    # After yesterday's garlic pizza incident, all of Batta's Minions are sick from eating the poisoned pizza.
    # Minions are strewn about the castle's pristine floors, either hunched over or laid on top of each other.
    # Batta is angrily lounging in her chaise lounge chair, death gripping her phone with one hand.
    scene hallway with fade
    show batta relaxed angry at right with fastdissolve
    show screen day_title(5)
    batta "Yes. Tony's Pizza & Wings? This is {i}THE{/i} Evil Vampiric Mistress of the Da-Hello-?! Hello? HELLO?!"
    
    # The line goes dead.
    batta "Tony S. Pizza- if you think for a singular moment of your pathetic existence that you can get away with hanging up on THE Batta S. Devila then you are sorely mis-"
    
    show helloworld at center with fastdissolve
    helloworld "0W. 0UCH. 0WIE. 0W. 0W. 0W. 0W- 000101010011-"
    
    # The noise breaks Batta's concentration.
    show batta relaxed angry
    batta "Would you cease your incessant whining?"
    
    # It's hard to concentrate on villainy with the sound of everyone suffering echoing through the room.
    helloworld ": ("
    hide batta with fastdissolve
    
    # DAISY is knelt between HELL O. WORLD and Candlestein, completing a vitals scan on the two of them.
    show daisy exsasperated at left with fastdissolve
    daisy "My scan indicates that the remainder of the poison should be expelled from your body by the end of this evening."
    
    show candlestein at center with fastdissolve
    candlestein "I'm gonna be honest with you. I don't think I'll make it till then."
    
    daisy "..."
    
    candlestein "Thankfully I'm like a doctor without the license, so lemme tell you how to make a tonic that should speed this process up."
    
    show daisy suprised
    daisy "You have an antidote recipe?"
    
    candlestein "Yep."

    candlestein "You'll just need to mix these three ingredients: Unicorn dust, wasp's honey, and a newt's eye"
    
    show daisy exsasperated
    daisy "{i}    Why{/i} didn't you mention this sooner?"
    
    # Batta slams her phone on the receiver. The line's gone dead again. She sees the scene in front of her, and storms over.
    show batta relaxed angry at right with fastdissolve
    batta "DAISY-BOT, I hope the next words out of your mouth are {i}\"Yes, Mistress.\"{/i}"
    
    # DAISY finishes making notes in her processor for the GUT-ROT TONIC.
    show daisy suprised
    daisy "Of course My Lady. What do you ask of me?"
    
    show batta relaxed angry
    batta "Have you found a way to fix this mess?!"
    
    show daisy happy
    daisy "Y-Yes My Lady. We have an antidote recipe ready for preparation!"
    
    show batta normal happy
    batta "..."
    
    batta "{i}    HAHAHAHAHAHAHA-{/i} PERFECT! DAISY, my incredibly intelligent Darling Bug. Of course you'd find a work around."
    
    show daisy flustered
    daisy "It was no trouble at all My Lady. I was merely following up on your orders."
    
    batta "Don't sell yourself short, my Dear. There's no poison stronger than the one brewed up by Yours Truly. It was a tantalizing mixtures of the MOST foul, devilish components imaginable."
    
    show daisy neutral
    daisy "Of course. Your devilish schemes never cease to amaze me."
    
    candlestein "Hey I helped too."
    
    daisy "I just need a bit of time and the antidote will be completed."
    
    # DAISY begins to walk off.
    hide daisy with moveoutleft
    show batta normal neutral
    batta "Where do you think you're going? I have a FIVE- no {i}EIGHT{/i} - step plan in motion to be enacted within the next day or so and I WILL NOT stand to have any more setbacks."
    
    show daisy suprised at left with moveinleft
    daisy "My Lady, I can only work so quickly-"
    
    batta "In order to get these schemes back on track, I will be overseeing this."
    
    daisy "!!!"
    
    show batta relaxed haughty
    batta "Yes, yes, yes. A woman of {i}my{/i} stature and incredibly busy schedule overseeing something as simple as brewing an antidote? My generosity knows no bounds."
    
    show daisy neutral
    daisy "... I see. We are eternally grateful for your generosity, My Lady."
    
    # Batta and DAISY make their way to the kitchen. It's incredibly well stocked with a plethora of ingredients both magical and not. Shelves line the walls with pristine cooking equipment and a large assortment of knives and other household objects fashioned to be weapons.
    # Batta pulls jars of unicorn dust, wasp's honey and newt's eye from the shelves. DAISY appears shocked at how efficient her process is.
    # Batta notices that DAISY is staring, and makes a face at her.
    batta "Yes?!"
    
    daisy "My apologies, Mistress. I meant no ill intent, I was simply marveling at your culinary prowess."
    
    show batta normal neutral
    batta "..."
    
    show batta normal happy
    batta "WHY YES! Of course! My culinary expertise."
    
    # DAISY begins setting the stove and ingredients together. Batta notes a container of wasp's honey on the table.
    show batta normal neutral
    batta "I see this has mostly gone unused. I remember I quite enjoyed the last time you used it to make that vanilla cake."
    
    # DAISY beams.
    show daisy happy
    daisy "I'm happy it was to your liking, Mistress."
    
    batta "How could they not be? The taste was nothing short of divine."
    
    # DAISY's gaze darts to Batta.
    batta "Perhaps it was nice to see you so elated to make something for me. The joy in your eyes, the way you walked about the castle, how diligent you were in everything you did- the way you would stop for nothing short of perfection."
    
    # As Batta speaks, her tone seems different. Reminiscient, almost, of a time she clearly thinks back to fondly.
    show batta normal sultry
    batta "It was no shock of course. You were made in my image, an image of perfection. An image that fits you perfectly."
    show daisy flustered
    daisy "..."
    
    show daisy neutral
    # MINI GAME START: COMPLETE THE THREE STEP TONIC!
    menu: 
        "What ingredients are needed for the tonic?"
        
        "Unicorn dust, Dragonscale powder, and Newt's Eye":
            jump wrong_tonic
        "Dragonscale powder, Newt's Eye, and Wasp's Honey":
            jump wrong_tonic

        "Wasp's honey, Newt's Eye, and Unicorn Dust":
            jump right_tonic
        "Unicorn Dust, Wormswood, and Dragonscale powder":
            jump wrong_tonic

label right_tonic:
    # The timer goes off. The antidote is complete!
    daisy "I-it's complete, my Lady."
    
    # Batta takes a whiff. She takes a spoon from the drawer.
    batta "Finally. Here. Taste."
    # She holds the spoon up to DAISY's mouth.
    daisy "It's perfect."

    hide candlestein with fastdissolve
    hide helloworld with fastdissolve
    
    # RIGHT ANSWER/ MINI-GAME SUCCESS:
    # With the antidote's success, the rest of the Minions were back in fighting form! Later that evening, Batta stops DAISY in the kitchen as she is cleaning up.
    show batta normal happy
    batta "DAISY, my Darling?"
    
    show daisy suprised
    daisy "Oh?"
    
    show batta normal neutral
    batta "I'm impressed. Everyone is in top form, even better it seems. Perhaps we make a better team than I anticipated, my dear."
    
    show daisy happy
    daisy "Thank you for your praise, My Lady."
    
    # It is quiet for a moment as DAISY continues to clean. Batta closes the kitchen door behind her.
    show batta normal happy
    batta "Everything is back on schedule, as it should be. And...as I said before-"
    
    # She walks over to her side, leaning closer to DAISY until her voice is barely above a whisper.
    show batta normal sultry
    batta "I seek to reward hard work when I see it."

    batta "..."

    batta "Also, please put back the vomit bucket when you go, we won't be needing it."

    hide batta

    menu:
        "Take the bucket?":
            $ try_add_inventory_item("Vomit bucket", "A bucket used to collect vomit.", "gui/item bucket.png", 3)
            $ folder_open = True
            "Picked up the bucket."
            $ folder_open = False
        "Leave the bucket":
            daisy "I'll get it later."

    jump day6
    
label wrong_tonic:
    # The timer goes off. The antidote is complete!
    daisy "I-it's complete, my Lady."
    
    # Batta takes a whiff. She takes a spoon from the drawer.
    batta "Finally. Here. Taste."

    show daisy flustered
    # daisy "!!! WRONG ANSWER/mini-game failed:"
    daisy "Hmm... I don't think it worked, My Lady."

    play sound "item miss!.mp3"
    
    # The castle walls are silent. With the antidote's failure, the rest of the Minion's have taken to somehow making it through the night in relative silence, more sick than ever.
    show batta relaxed angry
    batta "It eludes me, DAISY, that even with my guidance you STILL can't complete a SIMPLE antidote. I have given you time in and time out to prove yourself to me-"
    
    daisy "I-it was your carelessness- that-"
    
    # Even DAISY is shocked by her outburst.
    show daisy suprised
    daisy "!"
    show batta normal shocked
    batta "..."
    
    show batta relaxed angry
    batta "How DARE you even {i}assume{/i} that I could even be capable of such mediocrity. I create you in {i}my{/i} image and you stand her, blaspheming right in front of me?"
    
    show daisy sheepish
    daisy "My Lady, I assure you that I intended no disrespect but I-"
    
    # Batta begins to walk away.
    show batta relaxed haughty
    batta "Get to work DAISY. I will not have my plans setback any further."
    
    jump day6
