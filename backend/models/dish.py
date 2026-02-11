from extensions import db
from datetime import datetime
from sqlalchemy import DECIMAL

class Dish(db.Model):
    __tablename__ = 'dishes'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # 汤品/点心/肉菜/蔬菜等
    description = db.Column(db.Text)
    ingredients = db.Column(db.Text)  # 食材组成
    restrictions = db.Column(db.Text)  # 禁忌食材
    suitable_for = db.Column(db.Text)  # 适合人群
    not_suitable_for = db.Column(db.Text)  # 禁忌人群
    service_taboo = db.Column(db.Text)  # 服务禁忌
    lactation_risk = db.Column(db.Integer)  # 回奶风险等级
    post_partum_suitability = db.Column(db.Text)  # 产后时期适配性
    calories = db.Column(db.Integer)  # 卡路里
    price = db.Column(DECIMAL(10, 2))  # 价格
    status = db.Column(db.String(20), default='active')  # active/inactive
    
    def __repr__(self):
        return f'<Dish {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'description': self.description,
            'ingredients': self.ingredients,
            'restrictions': self.restrictions,
            'suitable_for': self.suitable_for,
            'not_suitable_for': self.not_suitable_for,
            'service_taboo': self.service_taboo,
            'lactation_risk': self.lactation_risk,
            'post_partum_suitability': self.post_partum_suitability,
            'calories': self.calories,
            'price': self.price,
            'status': self.status
        }
