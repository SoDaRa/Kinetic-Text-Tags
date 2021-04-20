"""
 Kinetic Text Tags Ren'Py Module
 2021 Daniel Westfall <SoDaRa2595@gmail.com>

 http://twitter.com/sodara9
 I'd appreciate being given credit if you do end up using it! :D Would really
 make my day to know I helped some people out!
 Really hope this can help the community create some really neat ways to spice
 up their dialogue!
 http://opensource.org/licenses/mit-license.php
 Forum Post: https://lemmasoft.renai.us/forums/viewtopic.php?f=51&t=60527&sid=75b4eb1aa5212a33cbfe9b0354e5376b
 Github: https://github.com/SoDaRa/Kinetic-Text-Tags
 itch.io: https://wattson.itch.io/kinetic-text-tags
"""
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


init python:
    ##### Made these ones just for fun. Leaving them in here just in case anyone wants
    ##### to use them. Probably will not add them to the Omega tag or to DispTextStyle

    # Takes in two colors, a range and an index and interpolates a new color
    # between the start and end points based on the range and index.
    # color_1: (String of hex color in #rrggbb format) Start of the gradient
    # color_2: (Same as above) End of the gradient
    # range: (int) The number of elements in the gradient
    # id:    (int) The offset into the gradient's range
    # Return: String of interpolated hex color in rrggbb format
    def color_gradient(color_1, color_2, range, index):
        if index == 0:
            return color_1
        if range == index:
            return color_2
        start_col = Color(color_1)
        end_col = Color(color_2)
        return start_col.interpolate(end_col, index * 1.0/range).hexcode

    # Applies a static gradient over text
    # Note: Hex Color = A string giving a hexadecimal color, in the form "#rrggbb".
    # color_1: (Hex Color) The starting color
    # color_2: (Hex Color) The ending color
    # Args are separated by an '-'
    # Example: {gradient=[color_1]-[color_2]}{/gradient}
    def gradient_tag(tag, argument, contents):
        new_list = [ ]
        if argument == "":
            return
        else: # Note: all arguments must be supplied
            col_1, _, col_2 = argument.partition('-')
        # Get a count of all the letters we will be applying colors to
        count = 0
        for kind,text in contents:
            if kind == renpy.TEXT_TEXT:
                for char in text:
                    if char == ' ':
                        continue
                    count += 1
        count -= 1
        my_index = 0
        my_style = DispTextStyle()
        for kind,text in contents:
            if kind == renpy.TEXT_TEXT:
                for char in text:
                    if char == ' ':
                        new_list.append((renpy.TEXT_TEXT, ' '))
                        continue
                    new_list.append((renpy.TEXT_TAG, "color=" + color_gradient(col_1, col_2, count, my_index)))
                    new_list.append((renpy.TEXT_TEXT, char))
                    new_list.append((renpy.TEXT_TAG, "/color"))
                    my_index += 1
            elif kind == renpy.TEXT_TAG:
                if not my_style.add_tags(text):
                    new_list.append((kind, text))
            else:
                new_list.append((kind,text))
        return new_list

    # A custom displayable that applies a gradient over a letter of text.
    # Honestly didn't test this works with other text tags since was just for fun
    class GradientText(renpy.Displayable):
        def __init__(self, char, col_list, id, list_end, **kwargs):
            """
            col_list format
                (color_1, color_2, end_id)
            list_end should be the number of gradients in the list
            """
            super(GradientText, self).__init__(**kwargs)

            self.char = char
            self.child = Text(char)
            self.col_list = col_list # Calling it grad_list for gradient might be more appropriate.
            self.id = id
            self.list_end = list_end
            # Figure out which gradient we are in
            for i, element in enumerate(col_list):
                if self.id < element[2]:
                    self.curr_grad = i
                    break
            # Determine the current range (for color_gradient func later)
            if self.curr_grad is 0:
                self.curr_range = self.col_list[0][2]
            else:
                self.curr_range = self.col_list[self.curr_grad][2] - self.col_list[self.curr_grad - 1][2]

        def render(self, width, height, st, at):
            my_style = DispTextStyle()
            # Get the color to apply to the text
            if self.curr_grad == 0:
                my_style.add_tags("color=" + color_gradient(self.col_list[self.curr_grad][0], self.col_list[self.curr_grad][1], self.curr_range, self.id))
            else: # color_gradient() expects id to be within the range given. So must reduce to that if exceeding it.
                my_style.add_tags("color=" + color_gradient(self.col_list[self.curr_grad][0], self.col_list[self.curr_grad][1], self.curr_range, self.id - self.col_list[self.curr_grad - 1][2]))

            # Usual retrieval and drawing of child render
            self.child.set_text(my_style.apply_style(self.char))
            child_render = renpy.render(self.child, width, height, st, at)
            self.width, self.height = child_render.get_size()
            render = renpy.Render(self.width, self.height)
            render.subpixel_blit(child_render, (0, 0))
            renpy.redraw(self, 0)

            # Iterate id for next render
            self.id += 1
            # If we are at the end of the range update gradient
            if self.id > self.col_list[self.curr_grad][2]:
                self.curr_grad += 1
                # If at the end of our color list, reset back to 0
                if self.curr_grad == self.list_end:
                    self.curr_grad = 0
                    self.id = 0
                    self.curr_range = self.col_list[0][2]
                # Otherwise just update the range
                else:
                    self.curr_range = self.col_list[self.curr_grad][2] - self.col_list[self.curr_grad - 1][2]

            return render

        def visit(self):
            return [ self.child ]

    # Applies gradients that smoothly rolls over the letters
    # Argument Notes:
    # Args are seperated by '-'
    # num_of_grad: (int) The number of gradients in the tag. This is to help the function
    #                    know how many gradients it's looking for.
    # The following repeat for the number of gradients specified above
    # grad_col_1: (Hex Color) The starting color of a gradient
    # grad_col_2: (Hex Color) The ending color of a gradient
    # grad_length:      (int) How many values are interpolated in the gradient.
    #                         Can think of this as how many characters the gradient
    #                         spans before the next one starts.
    # Example: {gradient2=[num_of_grad]-[grad_col_1]-[grad_col_2]-[grad_length]-[grad_col_1]-[grad_col_2]-[grad_length]-...} {/gradient2}
    def gradient2_tag(tag, argument, contents):
        new_list = [ ]
        if argument == "":
            return
        else: # Note: All arguments must be supplied
            arg_num, _, argument = argument.partition('-') # Number of gradients to read
        arg_num = int(arg_num)
        # Get all arguments
        col_list = []
        end_num = 0
        for i in range(arg_num):
            col_1, _, argument = argument.partition('-')   # Color 1
            col_2, _, argument = argument.partition('-')   # Color 2
            end_num_arg, _, argument = argument.partition('-') # Gradient Length
            end_num += int(end_num_arg) # Converts gradient length into it's ending position
            col_list.append((col_1, col_2, end_num))

        my_index = 0
        my_style = DispTextStyle()
        for kind,text in contents:
            if kind == renpy.TEXT_TEXT:
                for char in text:
                    if char == ' ':
                        new_list.append((renpy.TEXT_TEXT, ' '))
                        continue
                    char_disp = GradientText(my_style.apply_style(char), col_list, my_index, arg_num)
                    new_list.append((renpy.TEXT_DISPLAYABLE, char_disp))
                    my_index += 1
                    # Wrap around if reached the end of the gradient list.
                    if my_index >= col_list[arg_num-1][2]:
                        my_index = 0
            elif kind == renpy.TEXT_TAG:
                if not my_style.add_tags(text):
                    new_list.append((kind, text))
            else:
                new_list.append((kind,text))
        return new_list

    config.custom_text_tags["gradient"] = gradient_tag
    config.custom_text_tags["gradient2"] = gradient2_tag
