"""
Создание базы данных для приложения такси.

Используется подключение к postgres.
"""
from sqlalchemy import Column, create_engine, INT, VARCHAR, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy_utils import ChoiceType

engine = create_engine('postgresql://postgres:12345@127.0.0.1:5432/taxi')

Model = declarative_base()


class Driver(Model):  # type: ignore
    """Модель таблицы Водители."""

    __tablename__ = 'drivers'  # имя таблицы

    # Атрибуты класса описывают колонки таблицы, их типы данных и ограничения
    id = Column(INT, primary_key=True, autoincrement=True, comment="Идентификатор водителя")
    name = Column(VARCHAR(50), nullable=False, comment="Имя водителя")
    car = Column(VARCHAR(50), nullable=False, comment="Машина водителя")

    @property
    def serialize(self) -> dict:
        """Переопределение метода сериализации."""
        return {
            "id": self.id,
            "name": self.name,
            "car": self.car
        }


class Client(Model):  # type: ignore
    """Модель таблицы Клиенты."""

    __tablename__ = 'clients'  # имя таблицы

    # Атрибуты класса описывают колонки таблицы, их типы данных и ограничения
    id = Column(INT, primary_key=True, autoincrement=True, comment="Идентификатор клиента")
    name = Column(VARCHAR(50), nullable=False, comment="Имя клиента")
    is_vip = Column(Boolean, nullable=False, comment="VIP клиент")

    @property
    def serialize(self) -> dict:
        """Переопределение метода сериализации."""
        return {
            "id": self.id,
            "name": self.name,
            "is_vip": self.is_vip
        }


class Order(Model):  # type: ignore
    """Модель таблицы Заказы."""

    __tablename__ = 'orders'  # имя таблицы

    # Атрибуты класса описывают колонки таблицы, их типы данных и ограничения
    id = Column(INT, primary_key=True, autoincrement=True, comment="Идентификатор заказа")
    address_from = Column(VARCHAR(50), nullable=False, comment="Точка отправки")
    address_to = Column(VARCHAR(50), nullable=False, comment="Точка прибытия")
    client_id = Column(INT, ForeignKey('clients.id', ondelete='CASCADE'), nullable=False,
                       comment="идентификатор клиента")
    driver_id = Column(INT, ForeignKey('drivers.id', ondelete='CASCADE'), nullable=False,
                       comment="идентификатор водителя")
    date_created = Column(TIMESTAMP, nullable=False, comment="Дата создания заказа")
    status = Column(ChoiceType([("not_accepted", "not_accepted"), (" in_progress", " in_progress"),
                                ("done", "done"), ("cancelled", "cancelled")], impl=VARCHAR()), nullable=False,
                    comment="Статус заказа")
    clients = relationship("Client")
    drivers = relationship("Driver")

    @property
    def serialize(self) -> dict:
        """Переопределение метода сериализации."""
        return {
            "id": self.id,
            "address_from": self.address_from,
            "address_to": self.address_to,
            "client_id": self.client_id,
            "driver_id": self.driver_id,
            "date_created": self.date_created,
            "status": self.status
        }


if __name__ == "__main__":
    Model.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    session.commit()
    session.close()


