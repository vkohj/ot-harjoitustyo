from tkinter import ttk, constants
from tkinter.font import Font
from ui.interfaces.template import TkinterGUITemplate
from ui.interfaces.pack import TkinterGUIPack


class TkinterGUIOpen(TkinterGUITemplate):

    def __init__(self, window, service, handler):
        # Fontit
        self._font_packlist_li = Font(size=11)
        self._font_packlist_li_hover = Font(size=11, underline=1)

        super().__init__(window, service, handler)
        self.__initialize()

    def _reinitialize(self):
        self._window.grid_rowconfigure(0, weight=1)
        self._window.grid_columnconfigure(0, weight=1)

    def __initialize(self):
        self._reinitialize()

        frame = ttk.Frame(master=self._window, padding=(20, 20, 20, 20))
        self._add_elem(frame, 0, 0, sticky="NW")

        label = ttk.Label(
            frame, text=f"Korttipakat kansiossa /{self._service.packfolder}/", font=self._font_h1)
        self._add_elem(label, 0, 0)

        # Listan frame
        listframe = ttk.Frame(frame)

        # Pakkalista
        files = self._service.get_files_in_folder()
        for i, file in enumerate(files):
            label = ttk.Label(listframe, text=file,
                              font=self._font_packlist_li)
            label.file = file

            self._add_elem(label, 0, i, sticky="NW")
            label.bind("<Enter>", lambda e: e.widget.config(
                font=self._font_packlist_li_hover))
            label.bind("<Leave>", lambda e: e.widget.config(
                font=self._font_packlist_li))
            label.bind("<Button-1>", self._handle_listframe_elem_click)

        self._add_elem(listframe, 0, 1, sticky="NW")

    def _handle_listframe_elem_click(self, args):
        path = self._service.packfolder + "/" + args.widget.file
        self._handler.add_menu(TkinterGUIPack(
            self._window, self._service, self._handler, path))
