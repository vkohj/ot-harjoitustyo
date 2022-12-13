from tkinter import ttk, constants
from ui.interfaces.template import TkinterGUITemplate
from ui.interfaces.pack import TkinterGUIPack


class TkinterGUIOpen(TkinterGUITemplate):

    def __init__(self, window, service, handler):
        super().__init__(window, service, handler)
        self._initialize()

    def _reinitialize(self):
        self._window.grid_rowconfigure(0, weight=1)
        self._window.grid_columnconfigure(0, weight=1)

    def _initialize(self):
        super()._initialize()
        self._reinitialize()

        frame = ttk.Frame(master=self._window, padding=(20, 20, 20, 20))
        self._add_elem(frame, 0, 0, sticky="NSEW")

        label = ttk.Label(frame, text=f"Korttipakat kansiossa /{self._service.packfolder}/", font=self._handler.font_h1)
        self._add_elem(label, 0, 0)

        # Listan frame
        listframe = ttk.Frame(frame)

        # Pakkalista
        files = self._service.get_files_in_folder()
        for i, file in enumerate(files):
            label = ttk.Label(listframe, text=file,
                              font=self._handler.font_p)
            label.file = file

            self._add_elem(label, 0, i, sticky="NW")
            label.bind("<Enter>", lambda e: e.widget.config(
                font=self._handler.font_p_underline))
            label.bind("<Leave>", lambda e: e.widget.config(
                font=self._handler.font_p))
            label.bind("<Button-1>", self._handle_listframe_elem_click)

        self._add_elem(listframe, 0, 1, sticky="NW")

    def _handle_listframe_elem_click(self, args):
        path = self._service.packfolder + "/" + args.widget.file
        self._handler.add_menu(TkinterGUIPack(
            self._window, self._service, self._handler, path))
