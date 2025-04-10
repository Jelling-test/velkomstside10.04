from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, time


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_number = db.Column(db.String(20), unique=True, index=True)
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    is_admin = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_da = db.Column(db.String(100))
    name_en = db.Column(db.String(100))
    name_de = db.Column(db.String(100))
    name_nl = db.Column(db.String(100))
    name_fi = db.Column(db.String(100))
    name_no = db.Column(db.String(100))
    name_sv = db.Column(db.String(100))
    description_da = db.Column(db.Text)
    description_en = db.Column(db.Text)
    description_de = db.Column(db.Text)
    description_nl = db.Column(db.Text)
    description_fi = db.Column(db.Text)
    description_no = db.Column(db.Text)
    description_sv = db.Column(db.Text)
    price = db.Column(db.Float)
    image = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)


class BakeryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_da = db.Column(db.String(100))
    name_en = db.Column(db.String(100))
    name_de = db.Column(db.String(100))
    name_nl = db.Column(db.String(100))
    name_fi = db.Column(db.String(100))
    name_no = db.Column(db.String(100))
    name_sv = db.Column(db.String(100))
    price = db.Column(db.Float)
    image = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)


class BakeryOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    pickup_date = db.Column(db.Date)
    email = db.Column(db.String(120), nullable=False)
    mac_address = db.Column(db.String(20))
    is_confirmed = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref='bakery_orders')
    items = db.relationship('BakeryOrderItem', backref='order', cascade='all, delete-orphan')


class BakeryOrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('bakery_order.id'))
    bakery_item_id = db.Column(db.Integer, db.ForeignKey('bakery_item.id'))
    quantity = db.Column(db.Integer, default=1)

    bakery_item = db.relationship('BakeryItem')


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title_da = db.Column(db.String(100))
    title_en = db.Column(db.String(100))
    title_de = db.Column(db.String(100))
    title_nl = db.Column(db.String(100))
    title_fi = db.Column(db.String(100))
    title_no = db.Column(db.String(100))
    title_sv = db.Column(db.String(100))
    description_da = db.Column(db.Text)
    description_en = db.Column(db.Text)
    description_de = db.Column(db.Text)
    description_nl = db.Column(db.Text)
    description_fi = db.Column(db.Text)
    description_no = db.Column(db.Text)
    description_sv = db.Column(db.Text)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    location = db.Column(db.String(100))
    image = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)


class Promotion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title_da = db.Column(db.String(100))
    title_en = db.Column(db.String(100))
    title_de = db.Column(db.String(100))
    title_nl = db.Column(db.String(100))
    title_fi = db.Column(db.String(100))
    title_no = db.Column(db.String(100))
    title_sv = db.Column(db.String(100))
    description_da = db.Column(db.Text)
    description_en = db.Column(db.Text)
    description_de = db.Column(db.Text)
    description_nl = db.Column(db.Text)
    description_fi = db.Column(db.Text)
    description_no = db.Column(db.Text)
    description_sv = db.Column(db.Text)
    price = db.Column(db.Float)
    original_price = db.Column(db.Float)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    image = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)


class PromotionOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    promotion_id = db.Column(db.Integer, db.ForeignKey('promotion.id'))
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    quantity = db.Column(db.Integer, default=1)
    email = db.Column(db.String(120), nullable=False)
    mac_address = db.Column(db.String(20))
    is_confirmed = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref='promotion_orders')
    promotion = db.relationship('Promotion')


class EventRegistration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    num_participants = db.Column(db.Integer, default=1)
    email = db.Column(db.String(120), nullable=False)
    mac_address = db.Column(db.String(20))
    is_confirmed = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref='event_registrations')
    event = db.relationship('Event')


class CafeHours(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Integer)  # 0=Mandag, 1=Tirsdag, osv.
    is_closed = db.Column(db.Boolean, default=False)
    open_time = db.Column(db.Time, default=time(10, 0))  # 10:00
    close_time = db.Column(db.Time, default=time(21, 0))  # 21:00


class PoolHours(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_da = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100))
    name_de = db.Column(db.String(100))
    name_nl = db.Column(db.String(100))
    description_da = db.Column(db.Text)
    description_en = db.Column(db.Text)
    description_de = db.Column(db.Text)
    description_nl = db.Column(db.Text)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    weekday_open_time = db.Column(db.Time)
    weekday_close_time = db.Column(db.Time)
    weekend_open_time = db.Column(db.Time)
    weekend_close_time = db.Column(db.Time)
    special_note_da = db.Column(db.Text)
    special_note_en = db.Column(db.Text)
    special_note_de = db.Column(db.Text)
    special_note_nl = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    order_index = db.Column(db.Integer, default=0)  # For at sortere åbningstider i den rigtige rækkefølge


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
