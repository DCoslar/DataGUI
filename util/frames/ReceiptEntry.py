from tkinter import ttk

from datetime import datetime

from back import Engine, Receipt, Product
from util.windows.SingleWindow import generate_window_function

from sqlalchemy.orm import Session
from sqlalchemy import text
from tkinter import *

from decimal import Decimal


@generate_window_function
def receipt_entry(entry_window, close_window):
    entry_window.title("New Receipt | Currency: €")
    entry_window.resizable(FALSE, FALSE)

    ## FRAMES
    entry_frame = ttk.Frame(entry_window)
    entry_frame.grid(row=0, column=0, sticky="NWES")
    entry_window.columnconfigure(0, weight=1)
    entry_window.rowconfigure(0, weight=1)

    ### Products so far
    entry_frame.rowconfigure(0, weight=1)
    prod_frame = ttk.Frame(entry_frame)
    prod_frame.grid(row=0, column=0, sticky="NWS")
    prod_tree = ttk.Treeview(prod_frame)
    prod_tree.grid(row=0, column=0, sticky="NWES")
    prod_frame.rowconfigure(0, weight=1)
    prod_frame.columnconfigure(0, weight=0)

    ### New Data entry
    right_frame = ttk.Frame(entry_frame)
    right_frame.grid(row=0, column=1, sticky="NWS")

    #### Receipts
    ttk.Label(right_frame, text="Please enter the receipt data: ").grid(row=0, column=0, sticky="NW")
    receipt_frame = ttk.Frame(right_frame)
    receipt_frame.grid(row=1, column=0, sticky="NW")

    #### New Entry
    ttk.Label(right_frame, text="Please enter the new product's data: ").grid(row=2, column=0, sticky="NW")
    new_product_frame = ttk.Frame(right_frame)
    new_product_frame.grid(row=3, column=0, sticky="NW")
    general_prod_problem = StringVar()
    general_prod_problem.set("")
    general_prod_problem_label = ttk.Label(right_frame, textvariable=general_prod_problem)
    general_prod_problem_label.grid(row=4, column=0, sticky="W")

    ### Buttons
    button_frame = ttk.Frame(right_frame)
    button_frame.grid(row=5, column=0, sticky="NW")

    entry_frame['padding'] = (5, 10)

    ## PRODUCTS SO FAR TREE VIEW
    prod_tree['columns'] = ('name', 'price', 'bonus', 'quantity', 'total')

    prod_tree.column('#0', width=0, stretch=NO)
    prod_tree.column('name', width=150, anchor='w')
    prod_tree.column('price', width=60, anchor='e')
    prod_tree.column('bonus', width=60, anchor='e')
    prod_tree.column('quantity', width=60, anchor='e')
    prod_tree.column('total', width=60, anchor='e')

    prod_tree.heading('#0', text='', anchor=CENTER)
    prod_tree.heading('name', text='Name')
    prod_tree.heading('price', text='Price')
    prod_tree.heading('bonus', text='Bonus')
    prod_tree.heading('quantity', text='Quantity')
    prod_tree.heading('total', text='Total')

    scrollbar_2 = ttk.Scrollbar(prod_frame, orient=VERTICAL, command=prod_tree.yview)
    prod_tree.configure(yscroll=scrollbar_2.set)
    scrollbar_2.grid(row=0, column=1, sticky='nsw')

    ## RECEIPT FRAME
    rec_date_label = ttk.Label(receipt_frame, text="Date: ", width=10)
    rec_date_label.grid(row=0, column=0, sticky="W")
    rec_total_label = ttk.Label(receipt_frame, text="Total: ")
    rec_total_label.grid(row=1, column=0, sticky="W")
    rec_bonus_label = ttk.Label(receipt_frame, text="Bonus: ")
    rec_bonus_label.grid(row=2, column=0, sticky="W")
    rec_store_label = ttk.Label(receipt_frame, text="Store: ")
    rec_store_label.grid(row=3, column=0, sticky="W")

    rec_date = ttk.Entry(receipt_frame, textvariable=StringVar(), width=10)
    rec_date.grid(row=0, column=1, sticky="W")
    rec_total = ttk.Entry(receipt_frame, textvariable=DoubleVar(), width=10)
    rec_total.grid(row=1, column=1, sticky="W")
    rec_bonus = ttk.Entry(receipt_frame, textvariable=DoubleVar(), width=10)
    rec_bonus.grid(row=2, column=1, sticky="W")

    with Session(Engine) as session:
        store_names = session.execute(text("SELECT DISTINCT store FROM receipt;"))

    store_names = [str(store[0]) for store in store_names]
    store_names.sort(reverse=False)

    rec_store = ttk.Combobox(receipt_frame, textvariable=StringVar(), width=30, values=store_names)
    rec_store.grid(row=3, column=1, sticky="W")

    correct_date = StringVar()
    correct_date.set('Use format YYYY-MM-DD')

    correct_total = StringVar()
    correct_total.set('Items are missing!')

    correct_bonus = StringVar()
    correct_bonus.set('Bonus incorrect')

    ttk.Label(receipt_frame, textvariable=correct_date, width=25).grid(row=0, column=2, sticky="W")
    ttk.Label(receipt_frame, textvariable=correct_total, width=25).grid(row=1, column=2, sticky="W")
    ttk.Label(receipt_frame, textvariable=correct_bonus, width=25).grid(row=2, column=2, sticky="W")

    ## NEW PRODUCT
    ### New Product labels
    product_name_label = ttk.Label(new_product_frame, text="Name:")
    product_name_label.grid(row=0, column=0, sticky="W")
    product_price_label = ttk.Label(new_product_frame, text="Price:")
    product_price_label.grid(row=1, column=0, sticky="W")
    product_bonus_label = ttk.Label(new_product_frame, text="Bonus:")
    product_bonus_label.grid(row=2, column=0, sticky="W")
    product_quant_label = ttk.Label(new_product_frame, text="Quantity:", width=10)
    product_quant_label.grid(row=3, column=0, sticky="W")
    product_total_label = ttk.Label(new_product_frame, text="Total:")
    product_total_label.grid(row=4, column=0, sticky="W")
    ### New Product Entry boxes
    with Session(Engine) as session:
        product_names = session.execute(text("SELECT DISTINCT name FROM product;"))

    product_names = [prod_name[0] for prod_name in product_names]
    product_names.sort(reverse=False)

    prod_name = ttk.Combobox(new_product_frame, textvariable=StringVar(), width=20, values=product_names)
    prod_name.grid(row=0, column=1, sticky="W")


    prod_price = ttk.Entry(new_product_frame, textvariable=DoubleVar(), width=8)
    prod_price.grid(row=1, column=1, sticky="W")
    prod_bonus = ttk.Entry(new_product_frame, textvariable=DoubleVar(), width=8)
    prod_bonus.grid(row=2, column=1, sticky="W")
    prod_quantity = ttk.Entry(new_product_frame, textvariable=StringVar(), width=5)
    prod_quantity.grid(row=3, column=1, sticky="W")
    prod_total = ttk.Entry(new_product_frame, textvariable=DoubleVar(), width=10)
    prod_total.grid(row=4, column=1, sticky="W")
    ### New Product Error Messages
    correct_prod_name = StringVar()
    correct_prod_name.set('')
    correct_prod_price = StringVar()
    correct_prod_price.set('Price incorrect')
    correct_prod_bonus = StringVar()
    correct_prod_bonus.set('Bonus incorrect')
    correct_prod_quant = StringVar()
    correct_prod_quant.set('Quantity incorrect')
    correct_prod_total = StringVar()
    correct_prod_total.set('Total incorrect')

    ttk.Label(new_product_frame, textvariable=correct_prod_name, width=25).grid(row=0, column=2, sticky="W")
    ttk.Label(new_product_frame, textvariable=correct_prod_price, width=25).grid(row=1, column=2, sticky="W")
    ttk.Label(new_product_frame, textvariable=correct_prod_bonus, width=25).grid(row=2, column=2, sticky="W")
    ttk.Label(new_product_frame, textvariable=correct_prod_quant, width=25).grid(row=3, column=2, sticky="W")
    ttk.Label(new_product_frame, textvariable=correct_prod_total, width=25).grid(row=4, column=2, sticky="W")

    def check_entry():
        try:
            str(prod_name.get())
        except ValueError:
            correct_prod_name.set("Name invalid")
            product_name_label.config(foreground="red")
        else:
            if len(str(prod_name.get())) > 30:
                correct_prod_name.set("The name is too long")
                product_name_label.config(foreground="red")
            else:
                correct_prod_name.set('')
                product_name_label.config(foreground="green")

        invalid_price = True
        try:
            Decimal(prod_price.get())
        except ValueError:
            correct_prod_price.set("Price invalid")
            product_price_label.config(foreground="red")
        else:
            if not (Decimal(prod_price.get()) > 0):
                correct_prod_price.set("Price must be > 0")
                product_price_label.config(foreground="red")
            else:
                invalid_price = False
                correct_prod_price.set('')
                product_price_label.config(foreground="green")

        invalid_bonus = True
        try:
            Decimal(prod_bonus.get())
        except ValueError:
            correct_prod_bonus.set("Bonus invalid")
            product_bonus_label.config(foreground="red")
        else:
            if Decimal(prod_bonus.get()) < 0:
                correct_prod_bonus.set("Bonus must be >= 0")
                product_bonus_label.config(foreground="red")
            else:
                invalid_bonus = False
                correct_prod_bonus.set('')
                product_bonus_label.config(foreground="green")

        invalid_total = True
        try:
            Decimal(prod_total.get())
        except ValueError:
            correct_prod_total.set("Total invalid")
            product_total_label.config(foreground="red")
        else:
            if not (Decimal(prod_total.get()) > 0):
                correct_prod_total.set("Total must be > 0")
                product_total_label.config(foreground="red")
            else:
                invalid_total = False
                correct_prod_total.set('')
                product_total_label.config(foreground="green")

        invalid_quant = True
        try:
            int(prod_quantity.get())
        except ValueError:
            correct_prod_quant.set("Quantity invalid")
            product_quant_label.config(foreground="red")
        else:
            if int(prod_quantity.get()) < 1:
                correct_prod_quant.set("Quantity must be > 0")
                product_quant_label.config(foreground="red")
            else:
                invalid_quant = False
                correct_prod_quant.set('')
                product_quant_label.config(foreground="green")

        if any([invalid_bonus, invalid_total, invalid_price, invalid_quant]):
            return False

        if (Decimal(prod_price.get()) * Decimal(prod_quantity.get())) - Decimal(prod_bonus.get()) != Decimal(prod_total.get()):
            general_prod_problem.set("(Price * Quantity) - Bonus =/= Total")
            general_prod_problem_label.config(foreground="red")
            return False
        else:
            general_prod_problem.set("")
            general_prod_problem_label.config(foreground="black")
            return True

    def add_entry():
        if not check_entry():
            return

        val_str = (prod_name.get(), prod_price.get(), prod_bonus.get(), prod_quantity.get(), prod_total.get())
        prod_tree.insert(parent='', index='end', values=val_str)

    def check_receipt():
        res = []
        cur_date = rec_date.get()
        try:
            test_date = datetime.strptime(cur_date, "%Y-%m-%d")
        except ValueError:
            correct_date.set('Use format YYYY-MM-DD')
            rec_date_label.config(foreground='red')
            res.append(False)
        else:
            correct_date.set('')
            rec_date_label.config(foreground='green')
            res.append(True)

        invalid_rec_total = True
        try:
            Decimal(rec_total.get())
        except ValueError:
            correct_total.set('Total invalid')
            rec_total_label.config(foreground='red')
        else:
            if not (Decimal(rec_total.get()) >= 0):
                correct_total.set('Total must be >= 0')
                rec_total_label.config(foreground='red')
            else:
                invalid_rec_total = False
                correct_total.set('')
                rec_total_label.config(foreground='green')

        invalid_rec_bonus = True
        try:
            Decimal(rec_bonus.get())
        except ValueError:
            correct_bonus.set("Bonus invalid")
            rec_bonus_label.config(foreground="red")
        else:
            if not (Decimal(rec_bonus.get()) >= 0):
                correct_bonus.set("Bonus must be >= 0")
                rec_bonus_label.config(foreground="red")
            else:
                invalid_rec_bonus = False
                correct_total.set("")
                rec_total_label.config(foreground="green")

        if any([invalid_rec_bonus, invalid_rec_total]):
            return False

        total_amount = sum(list(map(Decimal, map(lambda x: x['values'][4], [prod_tree.item(id) for id in prod_tree.get_children()]))))
        if Decimal(rec_total.get()) == total_amount:
            correct_total.set('')
            rec_total_label.config(foreground='green')
            res.append(True)
        else:
            correct_total.set('Items are missing!')
            rec_total_label.config(foreground='red')
            res.append(False)

        total_bonus = sum(list(map(Decimal, map(lambda x: x['values'][2], [prod_tree.item(id) for id in prod_tree.get_children()]))))
        if Decimal(rec_bonus.get()) == total_bonus:
            correct_bonus.set('')
            rec_bonus_label.config(foreground='green')
            res.append(True)
        else:
            correct_bonus.set('Bonus incorrect')
            rec_bonus_label.config(foreground='red')
            res.append(False)

        return res

    def add_receipt():
        if not all(check_receipt()):
            return

        rec_list = []

        for item in [prod_tree.item(id) for id in prod_tree.get_children()]:
            rec_list.append(Product(name=str(item['values'][0]), price=Decimal(item['values'][1]),
                                    bonus=Decimal(item['values'][2]), quantity=int(item['values'][3])))

        receipt = Receipt(date=str(rec_date.get()), bonus=Decimal(rec_bonus.get()), total=Decimal(rec_total.get()),
                          store=rec_store.get(), products=rec_list)

        with Session(Engine) as session:
            session.add(receipt)
            session.commit()

        prod_tree.delete(*prod_tree.get_children())

    def next_receipt():
        add_receipt()

        correct_prod_name.set('')
        correct_prod_price.set('Price incorrect')
        correct_prod_bonus.set('Bonus incorrect')
        correct_prod_quant.set('Quantity incorrect')
        correct_prod_total.set('Total incorrect')
        correct_date.set('Use format YYYY-MM-DD')
        correct_total.set('Items are missing!')
        correct_bonus.set('Bonus incorrect')

    ttk.Button(button_frame, command=add_entry, text="Add Product").grid(row=0, column=0, sticky="W")
    ttk.Button(button_frame, command=check_entry, text="Check Product").grid(row=0, column=1, sticky="W")

    ttk.Button(button_frame, command=add_receipt, text="Add Receipt").grid(row=1, column=0, sticky="W")
    ttk.Button(button_frame, command=check_receipt, text="Check Receipt").grid(row=1, column=1, sticky="W")
    ttk.Button(button_frame, command=next_receipt, text="Next Receipt").grid(row=1, column=2, sticky="W")
