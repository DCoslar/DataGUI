from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base

from datetime import datetime

from enum import Enum

Base = declarative_base()


class Receipt(Base):
    __tablename__ = "receipt"

    id = Column(Integer, primary_key=True)
    _date = Column(String(10), nullable=False)
    _bonus = Column(Integer, nullable=False)
    _total = Column(Integer, nullable=False)

    products = relationship(
        "Product", back_populates="receipt", cascade="all, delete-orphan"
    )

    def __str__(self):
        return f'{(self._total - self._bonus)/100:.2f}€ spend on {self.date}'

    def __repr__(self):
        return f'Receipt({self.date!r}, {self.bonus!r}, {self.total!r})'

    @property
    def total(self):
        return round(self._total/100, 2)

    @total.setter
    def total(self, new_val: float):
        if isinstance(new_val, float):
            self._total = int(new_val*100)

        else:
            raise TypeError("total needs to be a float!")

    @property
    def bonus(self):
        return round(self._bonus/100, 2)

    @bonus.setter
    def bonus(self, new_val: float):
        if isinstance(new_val, float):
            self._bonus = int(new_val*100)

        else:
            raise TypeError("bonus needs to be a float!")

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, new_date: str):
        test_date = datetime.strptime(new_date, "%Y-%m-%d")
        self._date = new_date


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    _bonus = Column(Integer, nullable=False)
    _price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    receipt_id = Column(Integer, ForeignKey("receipt.id"), nullable=False)
    receipt = relationship("Receipt", back_populates="products")

    def __str__(self):
        return f'{self.quantity}x {self.name.upper()} for {(self._price - self._bonus)/100:.2f}€'

    def __repr__(self):
        return f'Product("{self.name.upper()}", {self.price}, {self.bonus}, {self.quantity})'

    @property
    def price(self):
        return round(self._price/100, 2)

    @price.setter
    def price(self, new_val):
        if isinstance(new_val, float):
            self._price = int(new_val*100)

        else:
            raise TypeError("price needs to be a float!")

    @property
    def bonus(self):
        return round(int(self._bonus)/100, 2)

    @bonus.setter
    def bonus(self, new_val):
        if isinstance(new_val, float):
            self._bonus = int(new_val*100)

        else:
            raise TypeError("bonus needs to be a float!")


class RecIds(Enum):
    DATE = 1
    TOTAL = 2
    BONUS = 3


class ProdIds(Enum):
    NAME = 1
    PRICE = 2
    BONUS = 3
    QUANTITY = 4


if __name__ == "__main__":
    P = Product("Yogurt", 1.10, 0.1, 1)
    print(P)

    R = Receipt("2022-12-10", 0.15, 1.1)
    print(R)
