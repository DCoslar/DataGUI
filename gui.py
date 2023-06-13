from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo

from util import Engine, Receipt, Product, GraphPage, MPLGraph
from util.frames.TreeFrame import TreeFrame
from util.frames.ReceiptEntry import receipt_entry

from sqlalchemy import select
from sqlalchemy.orm import Session

root = Tk()
root.option_add('*tearOff', FALSE)
root.title("Money overview | Currency: €")
root.geometry("1150x500")


## MAIN FRAME
mainframe = ttk.Frame(root, padding=(3, 5))
mainframe.grid(column=0, row=0, sticky="NWES")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)


## RECIEPT FRAME
rec_tree_frame = TreeFrame(root=mainframe,
                           cols=['date', 'total', 'bonus'],
                           text=["Date", "Total (€)", "Bonus (€)"],
                           width=[80, 50, 60])
rec_frame = rec_tree_frame.frame
rec_frame.grid(column=0, row=0, sticky="NWS", rowspan=2)
mainframe.columnconfigure(0, weight=0)
mainframe.rowconfigure(0, weight=1)
rec_frame.rowconfigure(0, weight=1)

rec_tree = rec_tree_frame.tree

with Session(Engine) as session:
    receipts = select(Receipt).order_by(Receipt.id)

    for idx, rec in enumerate(session.scalars(receipts)):
        val_str = (f'{rec.date}', f'{rec.total:.2f}€', f'{rec.bonus:.2f}€')
        rec_tree.insert(parent='', index='end', text=rec.id, values=val_str)

## PRODUCTS FRAME

last_selection = None

prod_tree_frame = TreeFrame(root=mainframe,
                            cols=['name', 'price', 'bonus', 'quantity', 'total'],
                            text=['Name', 'Price', 'Bonus', 'Quantity', 'Total'],
                            width=[150, 60, 60, 60, 60])

prod_frame = prod_tree_frame.frame
prod_frame.grid(column=1, row=0, sticky="NWS", rowspan=2)
mainframe.columnconfigure(1, weight=0)
prod_frame.rowconfigure(0, weight=1)

prod_tree = prod_tree_frame.tree


def item_selected(event):
    if len(rec_tree.selection()) > 1:
        showinfo(title='Error', message='Please only select one Item at a time.')

    else:
        item = rec_tree.item(rec_tree.selection()[0])
        cur_id = item['text']

        global last_selection

        if last_selection == cur_id:
            return

        prod_tree.delete(*prod_tree.get_children())
        last_selection = cur_id

        with Session(Engine) as session:
            products = select(Product).where(Product.receipt_id == cur_id).order_by(Product.id)

            for idx, prod in enumerate(session.scalars(products)):
                val_str = (f'{prod.name}', f'{prod.price:.2f}€', f'{prod.bonus:.2f}€', f'{prod.quantity}',
                           f'{(prod.price * prod.quantity)-prod.bonus:.2f}€')
                prod_tree.insert(parent='', index='end', iid=str(idx), values=val_str)


rec_tree.bind('<<TreeviewSelect>>', item_selected)

## PLOT FRAME
plot_frame = ttk.Frame(mainframe)
plot_frame.grid(column=2, row=0, sticky="NWES")
mainframe.columnconfigure(2, weight=1)
mainframe.rowconfigure(0, weight=1)
graph_frame = GraphPage(plot_frame)
graph_frame.canvas = MPLGraph((500, 100))
graph_frame.grid(row=0, column=0, sticky="NEWS")

root.bind("<Control-r>", graph_frame.redraw)

## DATA ABOUT PLOT FRAME
plot_details_frame = ttk.Frame(mainframe)
plot_details_frame.grid(column=2, row=1, sticky="WES", padx=10, pady=10)
plot_details = ttk.Notebook(plot_details_frame)
plot_details.grid(column=0, row=0, sticky="NWES")

plot_settings = ttk.Frame(plot_details)
plot_settings.grid(column=0, row=0, sticky="NWES")

plot_title_label = ttk.Label(plot_settings, text="Plot Title: ")
plot_title_label.grid(row=0, column=0, sticky="W")
plot_title = ttk.Entry(plot_settings, textvariable=StringVar(), width=20)
plot_title.grid(row=0, column=1, sticky="W")

y_axis_title_label = ttk.Label(plot_settings, text="Y-Axis Label: ")
y_axis_title_label.grid(row=1, column=0, sticky="W")
y_axis_title = ttk.Entry(plot_settings, textvariable=StringVar(), width=20)
y_axis_title.grid(row=1, column=1, sticky="W")

x_axis_title_label = ttk.Label(plot_settings, text="X-Axis Label: ")
x_axis_title_label.grid(row=2, column=0, sticky="W")
x_axis_title = ttk.Entry(plot_settings, textvariable=StringVar(), width=20)
x_axis_title.grid(row=2, column=1, sticky="W")


plot_details.add(plot_settings, text="General")



## NEW ENTRY
new_window = receipt_entry(root)
root.bind("<Control-n>", new_window)

## MENUS
menubar = Menu(mainframe)

### File Menu
menu_file = Menu(menubar, tearoff=False)
menubar.add_cascade(menu=menu_file, label='File')
menu_file.add_command(label="New Database", accelerator='Ctrl+Shift+N')
menu_file.add_command(label="Open Database", accelerator='Ctrl+O')
menu_file.add_separator()

### Edit Menu
menu_edit = Menu(menubar, tearoff=False)
menubar.add_cascade(menu=menu_edit, label='Edit')
menu_edit.add_command(label="New Receipt Entry", accelerator='Ctrl+N')

### View Menu
menu_view = Menu(menubar, tearoff=False)
menubar.add_cascade(menu=menu_view, label='View')
menu_view.add_command(command=graph_frame.redraw, label='Redraw', accelerator='Ctrl+R')


root.config(menu=menubar)
root.mainloop()
