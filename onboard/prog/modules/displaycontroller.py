class Form():
    def __init__(self, lcd, X, Y, width, active=False, height=None,
                 entries=None):
        (self.__lcd, self.__entries, self.__label_len) = (lcd, [], 0)
        (self.__X, self.__Y) = (X, Y)
        (self.__width, self.__height) = (width, height)
        self.__active = active
        self.__auto_height = (self.__height is None)
        for entry in entries:
            self.add_entry(entry)

    def add_entry(self, label, value="", upd_width=True, upd_height=True):
        self.__entries.append([label, value])
        self.__label_len = max(self.__label_len, len(label))
        self.__height += 1 if self.__auto_height else 0

    def set_entry(self, label, value):
        for entry in self.__entries:
            if entry[0] == label:
                entry[1] = value
                return True
        return False

    def set_size(self, width, height):
        (self.__width, self.__height) = (width, height)

    def get_size(self):
        return (self.__width, self.__height)

    def show(self):
        if not self.__active:
            pass
        (x, y) = (self.__X, self.__Y)
        self.__lcd.gotoXY(x, y)
        for entry in self.__entries:
            x = self.__X
            self.__lcd.printXY(entry[0], X=x, Y=y, scroll=False)
            x += self.__label_len + 1
            ln = self.__width - (self.__label_len + 1)
            self.__lcd.printXY(entry[1][:ln], X=x, Y=y, scroll=False)
            y += 1
            if y == self.__Y + self.__height:
                break


class Screen():
    def __init__(self, displaycontroller, width=None, height=None,
                 entries=None):
        (self.__displaycontroller, self.__forms) = (displaycontroller, [])
        (self.__X, self.__Y) = (0, 0)
        (x, y, cols, rows) = displaycontroller.__lcd.get_size()
        self.__width = width if width is not None else cols
        self.__height = height if height is not None else rows
        if entries is not None:
            self.add_form(entries=entries)

    def add_form(self, active=True, X=None, Y=None, width=None,
                 height=None, entries=None):
        if X is None:
            X = self.__X
        if Y is None:
            Y = self.__Y
        if width is None:
            width = self.__width
        if height is None:
            height = self.__height
        form = Form(self.__displaycontroller.__lcd, active=active, X=X, Y=Y,
                    width=width, height=height, entries=entries)
        if height is None:
            (width, height) = form.get_size()
        Y += height
        self.__forms.append(form)
        return form

    def set_entry(self, label, value):
        for form in self.__forms:
            if form.set_entry(label, value):
                return True
        return False

    def show(self):
        for form in self.__forms:
            form.show()
        self.__displaycontroller.__lcd.flush()


class DisplayController():
    def __init__(self, controller):
        self.__lcd = controller.board.lcd
        self.__screens = []
        self.__active = None

    def new_screen(self, active=False, entries=None):
        screen = Screen(displaycontroller=self, entries=entries)
        self.__screens.append(screen)
        if active:
            self.__active = screen
        return screen

    def activate(self, screen):
        if screen in self.__screens:
            self.__active = screen

    def show(self):
        if self.__active:
            self.__active.show()

    def test(self):
        screen = Screen(displaycontroller=self, entries=("X", "Y", "Z"))
        screen.set_entry(label="X", value="4")
        screen.set_entry(label="Y", value="6")
        screen.set_entry(label="Z", value="8")
        screen.show()
