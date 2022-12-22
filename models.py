from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from database import Base, engine


class CUProducts(Base):
    __tablename__ = 'cu_products'
    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    store_id = Column(String, nullable=False)
    sku = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    category = Column(String, nullable=False)
    descriptions = Column(String, nullable=False)
    images = Column(String, nullable=False)

    prices = relationship('CUPrices', back_populates='product')


class CUPrices(Base):
    __tablename__ = 'cu_prices'
    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    price = Column(String, nullable=False)
    discount = Column(String)
    product_id = Column(Integer, ForeignKey(CUProducts.id))

    product = relationship('CUProducts', back_populates='prices')


Base.metadata.create_all(engine)
