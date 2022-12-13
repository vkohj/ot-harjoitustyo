from tkinter import ttk


class TkinterWidgetTemplate:
    def __init__(self, widget, column, row, sticky):
        self.widget = widget
        self.column = column
        self.row = row
        self.sticky = sticky


class TkinterGUITemplate:
    def __init__(self, window, service, handler):
        self._window = window
        self._service = service
        self._handler = handler

        #self._framestyle = ttk.Style()
        #self._framestyle.configure('My.TFrame', background='white')

        # Status
        self._hidden = False

        # Elementit
        self.__elem = []
        self.__elem_named = {}

    def destroy(self):
        for elem in self.__elem:
            elem.widget.destroy()

        for elem in self.__elem_named.values():
            elem.widget.destroy()

        self.__elem.clear()
        self.__elem_named.clear()

    def _reinitialize(self):
        raise NotImplementedError("Must override in child class")

    def rebuild(self):
        self.destroy()
        self._initialize()

    def hide(self):
        if self._hidden:
            return

        for elem in self.__elem:
            elem.widget.grid_forget()

        for elem in self.__elem_named.values():
            elem.widget.grid_forget()

        self._hidden = True

    def show(self):
        if not self._hidden:
            return

        self._reinitialize()

        for elem in self.__elem:
            elem.widget.grid(column=elem.column,
                             row=elem.row, sticky=elem.sticky)

        for elem in self.__elem_named.values():
            elem.widget.grid(column=elem.column,
                             row=elem.row, sticky=elem.sticky)

        self._hidden = False

    def _initialize(self):
        self._window.minsize(800, 400)

    def _add_elem(self, elem, column, row, sticky="", name=""):
        to_append = TkinterWidgetTemplate(elem, column, row, sticky)

        if name == "":
            self.__elem.append(to_append)
        else:
            if name in self.__elem_named.keys():
                raise IndexError(f"Element already exists in [{name}]")
            self.__elem_named[name] = to_append

        if not self._hidden:
            elem.grid(row=row, column=column, sticky=sticky)

    def _get_elem(self, name):
        if name in self.__elem_named:
            return self.__elem_named[name].widget
        return None

    def _exit(self):
        self._handler.pop_menu()
