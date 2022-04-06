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
define e_3d = Character("Eileen3D", show_layer="threeD_text")
default playername = "player"
label start:

    scene bg room

    show eileen happy

    e "Wanna see some new text effects I've been making?"
    e "Here's one {atl=bounce}ATL based text tag in use.{/atl}"
    e "Here's one using {atl=rotate_text~0.5, bounce_text~10}ATL to do the bounce effect.{/atl}"
    e "Here's a rotate using {atl=0.1,rotate_text~0.8}ATL as a tag thingy.{/atl}"
    e "Here's a {atl=0.3,drop_text~#~ 1.5, bounce_text~10}dripping text ATL example.{/atl}"
    camera threeD_text:
        perspective True
    e_3d "Here's a {atl=-0.1, text_rotate_3d}3D ATL text effect.{/atl}"
    "Here's a normal line with an override to {atl=-0.1, text_rotate_3d}allow for 3D Text.{/atl}" (show_layer="threeD_text")
    camera threeD_text
    e "Here's a fade in {atl=-#,#,fade_in_text~1.0}atl text tag along with another atl text tag{/atl}"
    e "Here's some {explode}exploding text.{/explode} Just give it a sec."
    e "Here's some {explodehalf=2-2.0}position exploding text{/explodehalf}."
    e "Here's a {glitch=1.1}{color=#0f0}{b}Glitch{/b}{/color} Tag{/glitch}"
    # I know these first couple are a bit of an eye sore but wanted to show here how to apply styles to the effects.
    # And how previous styling won't be applied through them...
    eb "Here is some {bt=h10-s0.5-p10.0}wavy bouncey{/bt} text"
    e "Here is some {sc}{b}{i}{font=FOT-PopJoyStd-B.otf}{=test_style}scared{/b} sha{/font}key{/i}{/=test_style}{/sc} text"
    e "Here is some {rotat}spinning rotation{/rotat} text"
    e "Here is a {gradient=#ff0000-#00ff00}fancy gradient{/gradient} {gradient=#00ff00-#0000ff}with every color{/gradient} {gradient=#0000ff-#ff0000}of the rainbow{/gradient}!!"
    e "Here is a {gradient2=6-#ff0000-#ffff00-10-#ffff00-#00ff00-10-#00ff00-#00ffff-10-#00ffff-#0000ff-10-#0000ff-#ff00ff-10-#ff00ff-#ff0000-10}fancy gradient with every color of the rainbow{/gradient2}!!"
    e "{fi=0-0.5}Here is some fade in text{/fi}"
    e "Here is some more selective {fi=13-1.5-20}fade in{/fi} text"
    e "Here is some {move}{b}moveable sliding{/move} text. Move your mouse near it to see!!"
    e "I'm having conflicting feelings about this..."
    e "{bt=2}There still seems to be some bugs. Like if I just keep typing this, this text will continue off the screen and you won't be able to read it.{/bt}"
    e "{bt=2}But if we insert a paragraph tag into our line, we'll be able to tell \nthe text displayable to make a new paragraph to avoid the issue! \nHuzzah!!{/bt}"
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
