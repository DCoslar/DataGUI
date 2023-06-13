from .Objects import Receipt
from .Objects import Product
from .Objects import Base
from .Objects import RecIds, ProdIds

from util.frames.PlotFrame import GraphPage, MPLGraph

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

Engine = create_engine("sqlite://", echo=True, future=True)
Base.metadata.create_all(Engine)

with Session(Engine) as session:
    P = Product(name="Yogurt", price=1.09, bonus=0.1, quantity=1)
    P2 = Product(name="Yogurt", price=1.10, bonus=0.1, quantity=1)
    P3 = Product(name='Yogurt', price=1.11, bonus=0.1, quantity=1)
    P4 = Product(name='Yogurt', price=1.12, bonus=0.1, quantity=1)
    P5 = Product(name='Yogurt', price=1.13, bonus=0.1, quantity=1)
    P6 = Product(name='Yogurt', price=1.14, bonus=0.1, quantity=1)
    P7 = Product(name='Yogurt', price=1.15, bonus=0.1, quantity=1)
    P8 = Product(name='Yogurt', price=1.16, bonus=0.1, quantity=1)
    P9 = Product(name='Yogurt', price=1.17, bonus=0.1, quantity=1)
    P10 = Product(name='Yogurt', price=1.18, bonus=0.1, quantity=1)
    P11 = Product(name='Yogurt', price=1.19, bonus=0.1, quantity=1)
    P12 = Product(name='Yogurt', price=1.20, bonus=0.1, quantity=1)
    P13 = Product(name='Yogurt', price=1.21, bonus=0.1, quantity=1)
    P14 = Product(name='Yogurt', price=1.22, bonus=0.1, quantity=1)
    P15 = Product(name='Yogurt', price=1.23, bonus=0.1, quantity=1)
    P16 = Product(name='Yogurt', price=1.24, bonus=0.1, quantity=1)
    P17 = Product(name='Yogurt', price=1.25, bonus=0.1, quantity=1)
    P18 = Product(name='Yogurt', price=1.26, bonus=0.1, quantity=1)
    P19 = Product(name='Yogurt', price=1.27, bonus=0.1, quantity=1)
    P20 = Product(name='Yogurt', price=1.28, bonus=0.1, quantity=1)
    P21 = Product(name='Yogurt', price=1.29, bonus=0.1, quantity=1)
    P22 = Product(name='Yogurt', price=1.30, bonus=0.1, quantity=1)
    R = Receipt(date="2022-12-10", bonus=0.15, total=1.1, products=[P, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12,
                                                                    P13, P14, P15, P16, P17, P18, P19, P20, P21, P22])
    R2 = Receipt(date="2022-12-10", bonus=0.15, total=1.1, products=[])
    R3 = Receipt(date="2022-12-10", bonus=0.15, total=1.1, products=[])
    R4 = Receipt(date="2022-12-10", bonus=0.15, total=1.1, products=[])
    R5 = Receipt(date="2022-12-10", bonus=0.15, total=1.1, products=[])
    R6 = Receipt(date="2022-12-10", bonus=0.15, total=1.1, products=[])
    R7 = Receipt(date="2022-12-10", bonus=0.15, total=1.1, products=[])
    R8 = Receipt(date="2022-12-10", bonus=0.15, total=1.1, products=[])
    R9 = Receipt(date="2022-12-10", bonus=0.15, total=1.1, products=[])
    R10 = Receipt(date="2022-12-10", bonus=0.15, total=1.1, products=[])
    R11 = Receipt(date="2022-12-10", bonus=0.15, total=1.1, products=[])
    R12 = Receipt(date="2022-12-10", bonus=0.15, total=1.1, products=[])
    R13 = Receipt(date="2022-12-10", bonus=0.15, total=1.1, products=[])
    R14 = Receipt(date="2022-12-10", bonus=0.15, total=1.1, products=[])
    R15 = Receipt(date="2022-12-10", bonus=0.15, total=1.1, products=[])
    R16 = Receipt(date="2022-12-10", bonus=0.15, total=1.1, products=[])
    R17 = Receipt(date="2022-12-10", bonus=0.15, total=1.1, products=[])
    R18 = Receipt(date="2022-12-10", bonus=0.15, total=1.1, products=[])
    R19 = Receipt(date="2022-12-10", bonus=0.15, total=1.1, products=[])
    R20 = Receipt(date="2022-12-10", bonus=0.15, total=1.1, products=[])
    R21 = Receipt(date="2022-12-10", bonus=0.15, total=1.1, products=[])


    session.add_all([P, R, P2, R2])
    session.commit()
