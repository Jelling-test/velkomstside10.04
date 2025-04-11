from flask import render_template, redirect, url_for, flash, request, session, g, jsonify, current_app
from app.main import bp
from app.main.forms import BakeryOrderForm, PromotionOrderForm, EventRegistrationForm
from app.models import MenuItem, CafeHours, BakeryItem, Event, Promotion, BakeryOrder, BakeryOrderItem, PromotionOrder, EventRegistration, PoolHours
from app import db
from flask_login import current_user, login_required
from datetime import datetime, date, timedelta, time
import os
from werkzeug.utils import secure_filename
import uuid

@bp.route('/')
@bp.route('/index')
def index():
    promotions = Promotion.query.filter(
        Promotion.is_active == True,
        Promotion.end_date >= datetime.now()
    ).order_by(Promotion.start_date).all()
    
    events = Event.query.filter(
        Event.is_active == True,
        Event.end_date >= datetime.now()
    ).order_by(Event.start_date).limit(3).all()
    
    cafe_hours = {}
    for day in range(7):  
        hours = CafeHours.query.filter_by(day=day).first()
        if not hours:
            hours = CafeHours(day=day, is_closed=False, open_time=time(10, 0), close_time=time(21, 0))
            db.session.add(hours)
            db.session.commit()
        
        cafe_hours[day] = hours
    
    pool_hours = PoolHours.query.filter(
        PoolHours.is_active == True,
        PoolHours.end_date >= date.today()
    ).order_by(PoolHours.order_index, PoolHours.start_date).all()
    
    return render_template('main/index.html', 
                           title='Velkommen til Jelling Camping',
                           promotions=promotions,
                           events=events,
                           cafe_hours=cafe_hours,
                           pool_hours=pool_hours)

@bp.route('/set_language/<lang>')
def set_language(lang):
    if lang in current_app.config['LANGUAGES']:
        session['language'] = lang
    return redirect(request.referrer or url_for('main.index'))

@bp.route('/cafe')
def cafe():
    menu_items = MenuItem.query.filter_by(is_active=True).order_by(MenuItem.name_da).all()
    
    cafe_hours = {}
    for day in range(7):  
        hours = CafeHours.query.filter_by(day=day).first()
        if hours:
            cafe_hours[day] = hours
    
    return render_template('main/cafe.html', 
                           title='Café og Restaurant',
                           menu_items=menu_items,
                           cafe_hours=cafe_hours)

@bp.route('/bakery')
def bakery():
    bakery_items = BakeryItem.query.filter_by(is_active=True).order_by(BakeryItem.name_da).all()
    
    # Tilføj variabler, der er nødvendige for skabelonen
    form = BakeryOrderForm()
    
    # Tjek bestillingstid
    current_hour = datetime.now().hour
    start_time = current_app.config.get('BAKERY_ORDER_START_TIME', 10)
    end_time = current_app.config.get('BAKERY_ORDER_END_TIME', 5)
    
    if end_time < start_time:
        order_time_valid = current_hour >= start_time or current_hour < end_time
    else:
        order_time_valid = current_hour >= start_time and current_hour < end_time
    
    # Tjek om brugeren allerede har bestilt
    already_ordered = False
    if current_user.is_authenticated:
        tomorrow = date.today() + timedelta(days=1)
        existing_order = BakeryOrder.query.filter_by(
            user_id=current_user.id,
            delivery_date=tomorrow
        ).first()
        already_ordered = existing_order is not None
    
    return render_template('main/bakery.html', 
                          title='Rundstykker og Bageri',
                          bakery_items=bakery_items,
                          form=form,
                          order_time_valid=order_time_valid,
                          bakery_order_start_time=f"{start_time}:00",
                          bakery_order_end_time=f"{end_time}:00",
                          already_ordered=already_ordered)

@bp.route('/calendar')
def calendar():
    events = Event.query.filter(
        Event.is_active == True,
        Event.end_date >= datetime.now()
    ).order_by(Event.start_date).all()
    
    return render_template('main/calendar.html', 
                           title='Aktiviteter og Events',
                           events=events)

@bp.route('/promotions')
def promotions():
    promotions = Promotion.query.filter(
        Promotion.is_active == True,
        Promotion.end_date >= datetime.now()
    ).order_by(Promotion.start_date).all()
    
    return render_template('main/promotions.html', 
                           title='Tilbud fra Caféen',
                           promotions=promotions,
                           now=datetime.now())

@bp.route('/order_bakery', methods=['GET', 'POST'])
@login_required
def order_bakery():
    form = BakeryOrderForm()
    
    current_hour = datetime.now().hour
    start_time = current_app.config['BAKERY_ORDER_START_TIME']
    end_time = current_app.config['BAKERY_ORDER_END_TIME']
    
    if end_time < start_time:
        is_order_time = current_hour >= start_time or current_hour < end_time
    else:
        is_order_time = current_hour >= start_time and current_hour < end_time
    
    if not is_order_time:
        flash('Rundstykker kan kun bestilles mellem kl. 10:00 og 05:00.', 'warning')
        return redirect(url_for('main.bakery'))
    
    bakery_items = BakeryItem.query.filter_by(is_active=True).order_by(BakeryItem.name_da).all()
    
    if form.validate_on_submit():
        order = BakeryOrder(
            user_id=current_user.id,
            pickup_date=date.today() + timedelta(days=1),
            email=form.email.data,
            mac_address=request.remote_addr,
            is_confirmed=True
        )
        db.session.add(order)
        db.session.flush()  
        
        has_items = False
        for item in bakery_items:
            quantity = request.form.get(f'quantity_{item.id}', type=int)
            if quantity and quantity > 0:
                order_item = BakeryOrderItem(
                    order_id=order.id,
                    bakery_item_id=item.id,
                    quantity=quantity
                )
                db.session.add(order_item)
                has_items = True
        
        if not has_items:
            flash('Du skal vælge mindst én vare.', 'danger')
            return render_template('main/order_bakery.html', 
                                title='Bestil Rundstykker',
                                form=form,
                                bakery_items=bakery_items)
        
        db.session.commit()
        
        flash('Din bestilling er modtaget. Du vil modtage en bekræftelsesmail.', 'success')
        return redirect(url_for('main.bakery'))
    
    if not form.email.data and current_user.email:
        form.email.data = current_user.email
    
    return render_template('main/order_bakery.html', 
                           title='Bestil Rundstykker',
                           form=form,
                           bakery_items=bakery_items)

@bp.route('/order_promotion/<int:id>', methods=['GET', 'POST'])
@login_required
def order_promotion(id):
    promotion = Promotion.query.get_or_404(id)
    
    if not promotion.is_active or promotion.end_date < datetime.now():
        flash('Dette tilbud er ikke længere tilgængeligt.', 'warning')
        return redirect(url_for('main.promotions'))
    
    form = PromotionOrderForm()
    
    if form.validate_on_submit():
        order = PromotionOrder(
            user_id=current_user.id,
            promotion_id=promotion.id,
            quantity=form.quantity.data,
            email=form.email.data,
            mac_address=request.remote_addr,
            comment=form.comment.data,
            is_confirmed=True
        )
        db.session.add(order)
        db.session.commit()
        
        flash('Din bestilling er modtaget. Du vil modtage en bekræftelsesmail.', 'success')
        return redirect(url_for('main.promotions'))
    
    if not form.email.data and current_user.email:
        form.email.data = current_user.email
    
    return render_template('main/order_promotion.html', 
                           title='Bestil Tilbud',
                           form=form,
                           promotion=promotion)

@bp.route('/register_event/<int:id>', methods=['GET', 'POST'])
@login_required
def register_event(id):
    event = Event.query.get_or_404(id)
    
    if not event.is_active or event.end_date < datetime.now():
        flash('Dette arrangement er ikke længere tilgængeligt.', 'warning')
        return redirect(url_for('main.calendar'))
    
    form = EventRegistrationForm()
    
    if form.validate_on_submit():
        registration = EventRegistration(
            user_id=current_user.id,
            event_id=event.id,
            num_participants=form.num_participants.data,
            email=form.email.data,
            mac_address=request.remote_addr,
            is_confirmed=True
        )
        db.session.add(registration)
        db.session.commit()
        
        flash('Din tilmelding er modtaget. Du vil modtage en bekræftelsesmail.', 'success')
        return redirect(url_for('main.calendar'))
    
    if not form.email.data and current_user.email:
        form.email.data = current_user.email
    
    return render_template('main/register_event.html', 
                           title='Tilmeld Arrangement',
                           form=form,
                           event=event)

@bp.route('/info')
def info():
    pool_hours = PoolHours.query.filter(
        PoolHours.is_active == True,
        PoolHours.end_date >= date.today()
    ).order_by(PoolHours.order_index, PoolHours.start_date).all()
    
    return render_template('main/info.html', 
                           title='Information',
                           pool_hours=pool_hours)

@bp.route('/pool_hours')
def pool_hours():
    # Hent friluftsbadet åbningstider
    pool_hours = PoolHours.query.filter(
        PoolHours.is_active == True,
        PoolHours.end_date >= date.today()
    ).order_by(PoolHours.order_index).all()

    return render_template('main/pool_hours.html',
                           title='Friluftsbadets Åbningstider',
                           pool_hours=pool_hours)
