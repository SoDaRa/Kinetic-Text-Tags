style test_style:
    color "#aa0000"
    size 25
    font "TurretRoad-Medium.ttf"
style es_style:
    color "#9933ff"
    size 30

define e = Character("Eileen")
define es = Character("{swap=Eileen@Lienee@1.0}{=es_style}Eileen{/swap}")
define eb = Character("{bt}Eileen{/bt}", what_outlines=[ (.5, "#aFbFAA") ], what_color="#aa0000")

default playername = "Player"

label start:

    scene bg room

    show eileen happy

    e "Wanna see some new text effects I've been making?"
    # I know these first couple are a bit of an eye sore but wanted to show here how to apply styles to the effects.
    # And how previous styling won't be applied through them...
    eb "Here is some {bt=10}wavy bouncey{/bt} text"
    e "Here is some {sc}{b}{i}{font=FOT-PopJoyStd-B.otf}{=test_style}scared{/b} sha{/font}key{/i}{/=test_style}{/sc} text"
    e "Here is some {rotat}spinning rotation{/rotat} text"
    e "Here is a {gradient=#ff0000-#00ff00}fancy gradient{/gradient} {gradient=#00ff00-#0000ff}with every color{/gradient} {gradient=#0000ff-#ff0000}of the rainbow{/gradient}!!"
    e "Here is a {gradient2=6-#ff0000-#ffff00-10-#ffff00-#00ff00-20-#00ff00-#00ffff-30-#00ffff-#0000ff-40-#0000ff-#ff00ff-50-#ff00ff-#ff0000-60}fancy gradient with every color of the rainbow{/gradient2}!!"
    e "{fi=0-0.5}Here is some fade in text{/fi}"
    e "Here is some more selective {fi=13-1.5}fade in{/fi} text"
    e "Here is some {move}{b}moveable sliding{/move} text. Move your mouse near it to see!!"
    e "I'm having conflicting feelings about this..."
    e "{fi=0-0.5}There still seems to be some bugs. Like if I just keep typing this, this text will continue off the screen and you won't be able to read it.{/fi}"
    e "{fi=0-0.5}But if we insert a paragraph tag into our line, we'll be able to tell {para}the text displayable to make a new paragraph to avoid the issue! {para}Huzzah!!{/fi}"
    es "I want to {swap=love@hate@1.0}{bt}feel{/bt}{/swap} it."
    e "And I feel something bad is about to {chaos}happen...{/chaos}"
    e "{chaos}Helllllp Mmeeeee!!!{/chaos}"
    # This is mostly to demonstrate that the tags can stack. However this does cause lag the more you apply
    # If you wish to apply this many, I advise you make a single Class that does all the effects itself or...
    e "{bt}{sc}{rotat}{chaos}Oh god NOooooo{/rotat}{/sc}{/bt}"
    # You could do this. Have them nest directly without as many render callbacks through Text displayables
    e "{omega=BT=5@SC=10@FI=20-0.5@ROT=400@CH}Oh god NOooooo{/omega}"
    e "{bt=20}{fi=20-1.5}Must{/fi} {rotat}gain{/rotat} {sc=10}control!!! For [playername]!!!{/sc}{/bt}"
    # They can be applied to menu options as well
    menu:
        "{bt}Breath{/bt}":
            e "*breathe*"
            e "{bt=3}*breathe*...{/bt}"
        "{chaos}Panic More{/chaos}":
            e "{sc=10}That probably won't help.{/sc}"
            e "{sc=3}I'ma just {/sc}{sc=1}calm down{/sc} now..."
    e "How did you like them?"
    e "I hope you can come up with even more clever ones!"
    e "If you do, be sure to share them! I'd {bt=4}love{/bt} to see them~"

    return
