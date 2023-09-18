from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo

from back import Engine, Receipt, Product

from util.frames.TreeFrame import TreeFrame
from util.frames.ReceiptEntry import receipt_entry
from util.frames.PlotFrame import PlotFrameFill, InfoNotebook

from sqlalchemy import select
from sqlalchemy.orm import Session

# Declare root window, title and size
root = Tk()
root.option_add('*tearOff', FALSE)
root.title("Money overview | Currency: €")
root.geometry("1350x600")


## MAIN FRAME
mainframe = ttk.Frame(root, padding=(3, 5))
mainframe.grid(column=0, row=0, sticky="NWES")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)


## RECIEPT FRAME
# Create a TreeView that will keep date, store, total and bonus
rec_tree_frame = TreeFrame(root=mainframe,
                           cols=['date', 'store', 'total', 'bonus'],
                           text=["Date", "Store", "Total (€)", "Bonus (€)"],
                           width=[80, 80, 50, 60])
rec_frame = rec_tree_frame.frame
rec_frame.grid(column=0, row=0, sticky="NWS", rowspan=2)
mainframe.columnconfigure(0, weight=0)
mainframe.rowconfigure(0, weight=1)
rec_frame.rowconfigure(0, weight=1)

rec_tree = rec_tree_frame.tree

# Populate the tree with all receipts in the database
with Session(Engine) as session:
    receipts = select(Receipt).order_by(Receipt.id)

    for idx, rec in enumerate(session.scalars(receipts)):
        val_str = (f'{rec.date}', f'{rec.store}', f'{rec.total:.2f}€', f'{rec.bonus:.2f}€')
        rec_tree.insert(parent='', index='end', text=rec.id, values=val_str)

## PRODUCTS FRAME
last_selection = None

# Create a TreeView with name, proce, bonus, quantity and total (of products)
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
    """Populates a TreeView prod_tree with elements belonging to a receipt selected in the TreeView rec_tree.

    :param event:
    :return:
    """
    if len(rec_tree.selection()) > 1:
        showinfo(title='Error', message='Please only select one Item at a time.')

    else:
        global last_selection

        try:
            item = rec_tree.item(rec_tree.selection()[0])
        except IndexError:
            # The entry we are referring to has been deleted.
            # Clear all selections
            prod_tree.delete(*prod_tree.get_children())
            last_selection = None
            return

        cur_id = item['text']

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


def refresh_db(event=None):
    """Empties and populates the receipt tree.

    :param event:
    :return:
    """
    rec_tree.selection_clear()
    prod_tree.delete(*prod_tree.get_children())
    rec_tree.delete(*rec_tree.get_children())
    # Populate the tree with all receipts in the database
    with Session(Engine) as session:
        receipts = select(Receipt).order_by(Receipt.id)

        for idx, rec in enumerate(session.scalars(receipts)):
            val_str = (f'{rec.date}', f'{rec.store}', f'{rec.total:.2f}€', f'{rec.bonus:.2f}€')
            rec_tree.insert(parent='', index='end', text=rec.id, values=val_str)

## PLOT FRAME
plot_frame = ttk.Frame(mainframe)
plot_frame.grid(column=2, row=0, sticky="NWES")
mainframe.columnconfigure(2, weight=1)
mainframe.rowconfigure(0, weight=1)

## DATA ABOUT PLOT FRAME
# Generate a plot frame
plot_details_frame = ttk.Frame(mainframe)
plot_details_frame.grid(column=2, row=1, sticky="WES", padx=10, pady=10)

plot_notebook = InfoNotebook(plot_details_frame)
plot = PlotFrameFill(
        plot_frame,
        (500, 400),
        plot_notebook
    )

## NEW ENTRY
new_window = receipt_entry(root, refresh_db)
root.bind("<Control-n>", new_window)
root.bind("<Control-r>", plot.draw)


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
menu_edit.add_command(label="New Receipt Entry", accelerator='Ctrl+N', command=new_window)

### View Menu
menu_view = Menu(menubar, tearoff=False)
menubar.add_cascade(menu=menu_view, label='View')
menu_view.add_command(label="Reload Plot", accelerator='Ctrl+R', command=lambda: plot.draw(x_title_var.get()))

root.config(menu=menubar)
root.mainloop()
