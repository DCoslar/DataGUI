import sqlite3


def get_str_products(products, rec_id):
    fin_str = ""
    for idx in range(len(products) - 1):
        product = products[idx]
        fin_str += f'"{product["name"].upper()}", {product["price"]}, {product["bonus"]}, {product["quantity"]}, {rec_id},\n'

    product = products[-1]
    fin_str += f'"{product["name"].upper()}", {product["price"]}, {product["bonus"]}, {product["quantity"]}, {rec_id}'

    return fin_str


def get_str_receipt(receipt):
    return f'"{receipt["buy_date"]}", {receipt["total_sum"]}, {receipt["coupon"]}'


def add_entry(products, receipt):
    con = sqlite3.connect("C:\\Users\\David\\DataGripProjects\\DatabaseSpending\\test.sqlite")
    with con:
        cursor = con.cursor()
        rec_quer = f'INSERT INTO receipts(buy_date, sum_spent, coupon) VALUES ({get_str_receipt(receipt)});'
        cursor.execute(rec_quer)
        last_id = cursor.lastrowid
        prod_quer = f'INSERT INTO products(name, price, bonus, quantity, RECEIPT_ID) VALUES ({get_str_products(products, last_id)});'
        cursor.execute(prod_quer)


if __name__ == "__main__":
    receipt = {
        "buy_date": "2022-09-22",
        "total_sum": 1.79,
        "coupon": 0
    }

    product1 = {
        "name": "apetina",
        "price": 2.39,
        "bonus": 0.60,
        "quantity": 1
    }

    products = [product1]

    add_entry(products, receipt)
