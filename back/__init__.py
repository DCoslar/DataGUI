from util.Objects import Receipt
from util.Objects import Product
from util.Objects import Base

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from decimal import Decimal

Engine = create_engine("sqlite://", echo=True, future=True)
Base.metadata.create_all(Engine)

with Session(Engine) as session:
    P = Product(name="Yogurt", price=Decimal(1.09), bonus=Decimal(0.1), quantity=1)
    P2 = Product(name="Banana", price=Decimal(0.85), bonus=Decimal(0.0), quantity=1)
    P3 = Product(name='Cornflakes', price=Decimal(2.85), bonus=Decimal(0.0), quantity=1)
    R = Receipt(date="2022-12-10", bonus=Decimal(0.10), total=Decimal(4.79), store="AH", products=[P, P2, P3])

    P4 = Product(name='Donuts', price=Decimal(1.50), bonus=Decimal(0.0), quantity=1)
    P5 = Product(name='Toothpaste', price=Decimal(3.15), bonus=Decimal(0.0), quantity=1)
    R2 = Receipt(date="2022-12-13", bonus=Decimal(0.0), total=Decimal(1.1), products=[P4, P5])

    P6 = Product(name='Yogurt', price=Decimal(1.14), bonus=Decimal(0.0), quantity=2)
    R3 = Receipt(date="2023-01-04", bonus=Decimal(0.0), total=Decimal(2.28), store="Jumbo", products=[P6])

    session.add_all([R, R2, R3])
    session.commit()
