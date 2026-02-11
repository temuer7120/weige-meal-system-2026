from extensions import db
from datetime import datetime

class TabooRule(db.Model):
    __tablename__ = 'taboo_rules'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rule_name = db.Column(db.String(255), nullable=False)
    rule_type = db.Column(db.String(50), nullable=False)  # 如饮食禁忌、服务禁忌等
    description = db.Column(db.Text)
    severity_level = db.Column(db.Integer)  # 1-5级
    applicable_period = db.Column(db.String(100))  # 如产后1周、哺乳期等
    related_ingredients = db.Column(db.Text)  # JSON格式存储
    related_dishes = db.Column(db.Text)  # JSON格式存储
    exception_conditions = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<TabooRule {self.rule_name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'rule_name': self.rule_name,
            'rule_type': self.rule_type,
            'description': self.description,
            'severity_level': self.severity_level,
            'applicable_period': self.applicable_period,
            'related_ingredients': self.related_ingredients,
            'related_dishes': self.related_dishes,
            'exception_conditions': self.exception_conditions,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class TabooRuleDetail(db.Model):
    __tablename__ = 'taboo_rule_details'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rule_id = db.Column(db.Integer, db.ForeignKey('taboo_rules.id'), nullable=False)
    detail_type = db.Column(db.String(50))  # 如具体禁忌、注意事项等
    content = db.Column(db.Text)
    reference_source = db.Column(db.String(255))  # 如医学指南、专家建议等
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    rule = db.relationship('TabooRule', backref=db.backref('details', lazy=True))
    
    def __repr__(self):
        return f'<TabooRuleDetail {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'rule_id': self.rule_id,
            'detail_type': self.detail_type,
            'content': self.content,
            'reference_source': self.reference_source,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class RuleIngredientMapping(db.Model):
    __tablename__ = 'rule_ingredient_mappings'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rule_id = db.Column(db.Integer, db.ForeignKey('taboo_rules.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    rule = db.relationship('TabooRule', backref=db.backref('ingredient_mappings', lazy=True))
    ingredient = db.relationship('Ingredient', backref=db.backref('rule_mappings', lazy=True))
    
    def __repr__(self):
        return f'<RuleIngredientMapping {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'rule_id': self.rule_id,
            'ingredient_id': self.ingredient_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class RuleDishMapping(db.Model):
    __tablename__ = 'rule_dish_mappings'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rule_id = db.Column(db.Integer, db.ForeignKey('taboo_rules.id'), nullable=False)
    dish_id = db.Column(db.Integer, db.ForeignKey('dishes.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    rule = db.relationship('TabooRule', backref=db.backref('dish_mappings', lazy=True))
    dish = db.relationship('Dish', backref=db.backref('rule_mappings', lazy=True))
    
    def __repr__(self):
        return f'<RuleDishMapping {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'rule_id': self.rule_id,
            'dish_id': self.dish_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
