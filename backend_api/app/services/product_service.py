from typing import Optional
from ..extensions import db
from ..models import Product

class ProductService:
    """Service for Product entity CRUD."""
    def get(self, id_: int) -> Optional[Product]:
        return db.session.get(Product, id_)

    def create(self, **data) -> Product:
        product = Product(**data)
        db.session.add(product)
        db.session.commit()
        return product

    def update(self, product: Product, **data) -> Product:
        for k, v in data.items():
            setattr(product, k, v)
        db.session.commit()
        return product

    def delete(self, product: Product) -> None:
        db.session.delete(product)
        db.session.commit()
