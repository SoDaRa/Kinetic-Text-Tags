init python:
    class ExplodeText(renpy.Displayable):
        def __init__(self, child, timer=2, **kwargs):
            super(ExplodeText, self).__init__(**kwargs)
            self.child = child
            self.curr_x = 0
            self.curr_y = 0
            self.timer = timer
            self.gravity = 300
            self.v0_x = (renpy.random.random() - 0.5) * 800.0
            self.v0_y = renpy.random.random() * -700.0

        def render(self, width, height, st, at):
            curr_x = 0
            curr_y = 0
            if st > self.timer:
                st -= self.timer
                curr_x = self.v0_x * st
                curr_y = self.v0_y * st + self.gravity * pow(st,2)
            child_render = renpy.render(self.child, width, height, st, at)

            self.width, self.height = child_render.get_size()
            render = renpy.Render(self.width, self.height)

            # This will position our child's render. Replacing our need for an offset Transform
            render.subpixel_blit(child_render, (curr_x, curr_y))
            if curr_y < 2000:
                renpy.redraw(self, 0) # This lets it know to redraw this indefinitely
            return render

        def visit(self):
            return [ self.child ]

    class ExplodeHalfText(renpy.Displayable):
        def __init__(self, child, length, id, explode_point, timer=2, **kwargs):
            super(ExplodeHalfText, self).__init__(**kwargs)
            self.child = child
            self.curr_x = 0
            self.curr_y = 0
            self.timer = timer
            self.length = length
            self.id = id
            self.gravity = 300
            self.v0_x = (id - explode_point) * 100
            self.v0_y = math.cos((id - explode_point) * math.pi * (1.0/(2.0 * length))) * -900
            # self.v0_y = (-abs(id - explode_point) + length) * -35

        def render(self, width, height, st, at):
            curr_x = 0
            curr_y = 0
            if st > self.timer:
                st -= self.timer
                curr_x = self.v0_x * st
                curr_y = self.v0_y * st + self.gravity * pow(st,2)
            child_render = renpy.render(self.child, width, height, st, at)

            self.width, self.height = child_render.get_size()
            render = renpy.Render(self.width, self.height)

            # This will position our child's render. Replacing our need for an offset Transform
            render.subpixel_blit(child_render, (curr_x, curr_y))
            if curr_y < 2000:
                renpy.redraw(self, 0) # This lets it know to redraw this indefinitely
            return render

        def visit(self):
            return [ self.child ]


    # Explodes text out after a certain amount of time
    # timer: (float) How long till the text explodes
    # Example: {explode=[timer]}Text{/explode}
    def explode_tag(tag, argument, contents):
        new_list = [ ]
        if argument == "":
            argument = 2
        else:
            argument = float(argument)
        my_style = DispTextStyle()
        for kind,text in contents:
            if kind == renpy.TEXT_TEXT:
                for char in text:
                    char_text = Text(my_style.apply_style(char))
                    char_disp = ExplodeText(char_text, argument)
                    new_list.append((renpy.TEXT_DISPLAYABLE, char_disp))
            elif kind == renpy.TEXT_TAG:
                if text.find("image") != -1:
                    tag, _, value = text.partition("=")
                    my_img = renpy.displayable(value)
                    img_disp = ExplodeText(my_img, argument)
                    new_list.append((renpy.TEXT_DISPLAYABLE, img_disp))
                elif not my_style.add_tags(text):
                    new_list.append((kind, text))
            else:
                new_list.append((kind,text))
        return new_list

    # Explodes text out from a point after a certain amount of time
    # center: (int) Position in the string the explosion will be centered on.
    # timer: (float) How long till the text explodes
    # Example: {explode=[center]-[timer]}Text{/explode}
    def explodehalf_tag(tag, argument, contents):
        new_list = [ ]
        if argument == "":
            time_arg = 2
            center_arg = -1
        else:
            center_arg, _, time_arg = argument.partition("-")
            time_arg = float(time_arg)
            center_arg = int(center_arg)
        my_style = DispTextStyle()
        total_length = 0
        for kind,text in contents:
            if kind == renpy.TEXT_TEXT:
                total_length += len(text)
            elif kind == renpy.TEXT_TAG:
                if text.find("image") != -1:
                    curr_id += 1
        curr_id = 0
        if center_arg == -1:
            center_arg = total_length / 2
        for kind,text in contents:
            if kind == renpy.TEXT_TEXT:
                for char in text:
                    char_text = Text(my_style.apply_style(char))
                    char_disp = ExplodeHalfText(char_text, total_length, curr_id, center_arg, time_arg)
                    new_list.append((renpy.TEXT_DISPLAYABLE, char_disp))
                    curr_id += 1
            elif kind == renpy.TEXT_TAG:
                if text.find("image") != -1:
                    tag, _, value = text.partition("=")
                    my_img = renpy.displayable(value)
                    img_disp = ExplodeHalfText(my_img, total_length, curr_id, center_arg, time_arg)
                    new_list.append((renpy.TEXT_DISPLAYABLE, img_disp))
                    curr_id += 1
                elif not my_style.add_tags(text):
                    new_list.append((kind, text))
            else:
                new_list.append((kind,text))
        return new_list

    config.custom_text_tags["explode"] = explode_tag
    config.custom_text_tags["explodehalf"] = explodehalf_tag
