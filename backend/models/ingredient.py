from extensions import db
from datetime import datetime
from sqlalchemy import DECIMAL

class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    current_stock = db.Column(DECIMAL(10, 2), default=0)
    minimum_stock = db.Column(DECIMAL(10, 2), default=0)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))
    price = db.Column(DECIMAL(10, 2))
    expiry_date = db.Column(db.Date)
    nutrition_info = db.Column(db.Text)
    calories = db.Column(DECIMAL(8, 2))
    restrictions = db.Column(db.Text)
    suitable_for = db.Column(db.Text)  # 适合人群
    not_suitable_for = db.Column(db.Text)  # 禁忌人群
    is_lactation_affecting = db.Column(db.Boolean, default=False)  # 是否影响回奶
    post_partum_period_restrictions = db.Column(db.Text)  # 产后时期禁忌
    purchaser = db.Column(db.String(50))
    origin = db.Column(db.Text)  # 食材溯源
    
    def __repr__(self):
        return f'<Ingredient {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'unit': self.unit,
            'current_stock': self.current_stock,
            'minimum_stock': self.minimum_stock,
            'supplier_id': self.supplier_id,
            'price': self.price,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'nutrition_info': self.nutrition_info,
            'calories': self.calories,
            'restrictions': self.restrictions,
            'suitable_for': self.suitable_for,
            'not_suitable_for': self.not_suitable_for,
            'is_lactation_affecting': self.is_lactation_affecting,
            'post_partum_period_restrictions': self.post_partum_period_restrictions,
            'purchaser': self.purchaser,
            'origin': self.origin
        }
