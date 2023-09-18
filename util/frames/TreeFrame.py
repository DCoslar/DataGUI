from tkinter import ttk
from tkinter import VERTICAL, CENTER, NO


class TreeFrame:
    def __init__(self, root: ttk.Frame, cols: list, text: list, width: list):
        # Get a frame for the treeview
        self.frame = ttk.Frame(root)

        # Copy lists so that we can modify them
        cols_copy = cols[:]
        text_copy = text[:]
        width_copy = width[:]

        # Get a tree
        self.tree = ttk.Treeview(self.frame)
        self.tree['columns'] = tuple(cols)

        # Set the invisible column
        self.tree.column('#0', width=0, stretch=NO)
        self.tree.heading('#0', text='', anchor=CENTER)

        # Create first col seperately because it sticks to the west, not east
        cur_col = cols_copy.pop(0)
        self.tree.column(cur_col, width=width_copy.pop(0), anchor='w')
        self.tree.heading(cur_col, text=text_copy.pop(0))

        # For the remaining columns, go off the instructions provided
        for col, text, width in zip(cols_copy, text_copy, width_copy):
            self.tree.column(col, width=width, anchor='e')
            self.tree.heading(col, text=text)

        # Create a vertical scrollbar
        scrollbar = ttk.Scrollbar(self.frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='nsw')

        self.tree.grid(column=0, row=0, sticky="NWS")


