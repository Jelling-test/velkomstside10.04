from flask import render_template, redirect, url_for, flash, request, session, g, current_app
from app.admin import bp
from app.admin.forms import MenuItemForm, BakeryItemForm, OpeningHoursForm, EventForm, PromotionForm, PoolHoursForm
from app.models import User, Admin, MenuItem, BakeryItem, Event, Promotion, CafeHours, PoolHours, BakeryOrder, PromotionOrder, EventRegistration, BakeryOrderItem
from app import db
from flask_login import login_required, current_user
from datetime import datetime, time
import os
from werkzeug.utils import secure_filename
import uuid

# Hjælpefunktion til at gemme uploadede billeder
def save_image(file, folder):
    if not file:
        return None
    
    filename = secure_filename(file.filename)
    random_prefix = uuid.uuid4().hex
    filename = f"{random_prefix}_{filename}"
    
    file_path = os.path.join(current_app.root_path, 'static', 'uploads', folder, filename)
    file.save(file_path)
    
    return filename

# Decorator til at tjekke om brugeren er admin
def admin_required(f):
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('Du har ikke adgang til denne side.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    
    # Bevar funktionens navn og dokumentation
    decorated_function.__name__ = f.__name__
    decorated_function.__doc__ = f.__doc__
    
    return decorated_function

@bp.route('/dashboard')
@admin_required
def dashboard():
    # Tæl antal bestillinger
    bakery_orders_count = BakeryOrder.query.count()
    promotion_orders_count = PromotionOrder.query.count()
    event_registrations_count = EventRegistration.query.count()
    
    # Hent de seneste bestillinger
    recent_bakery_orders = BakeryOrder.query.order_by(BakeryOrder.order_date.desc()).limit(5).all()
    recent_promotion_orders = PromotionOrder.query.order_by(PromotionOrder.order_date.desc()).limit(5).all()
    recent_event_registrations = EventRegistration.query.order_by(EventRegistration.registration_date.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                           title='Admin Dashboard',
                           bakery_orders_count=bakery_orders_count,
                           promotion_orders_count=promotion_orders_count,
                           event_registrations_count=event_registrations_count,
                           recent_bakery_orders=recent_bakery_orders,
                           recent_promotion_orders=recent_promotion_orders,
                           recent_event_registrations=recent_event_registrations)

# Café-menu administration
@bp.route('/menu')
@admin_required
def menu():
    menu_items = MenuItem.query.order_by(MenuItem.name_da).all()
    return render_template('admin/menu.html', title='Menukort', menu_items=menu_items)

@bp.route('/menu/create', methods=['GET', 'POST'])
@admin_required
def create_menu_item():
    form = MenuItemForm()
    
    if form.validate_on_submit():
        menu_item = MenuItem(
            name_da=form.name_da.data,
            name_en=form.name_en.data,
            name_de=form.name_de.data,
            name_nl=form.name_nl.data,
            description_da=form.description_da.data,
            description_en=form.description_en.data,
            description_de=form.description_de.data,
            description_nl=form.description_nl.data,
            price=form.price.data,
            is_active=form.is_active.data
        )
        
        if form.image.data:
            filename = secure_filename(str(uuid.uuid4()) + os.path.splitext(form.image.data.filename)[1])
            form.image.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], 'menu', filename))
            menu_item.image = filename
            
        db.session.add(menu_item)
        db.session.commit()
        
        flash('Menupunkt oprettet.', 'success')
        return redirect(url_for('admin.menu'))
        
    return render_template('admin/create_menu_item.html', title='Opret Menupunkt', form=form)

@bp.route('/menu/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_menu_item(id):
    menu_item = MenuItem.query.get_or_404(id)
    form = MenuItemForm(obj=menu_item)
    
    if form.validate_on_submit():
        menu_item.name_da = form.name_da.data
        menu_item.name_en = form.name_en.data
        menu_item.name_de = form.name_de.data
        menu_item.name_nl = form.name_nl.data
        menu_item.description_da = form.description_da.data
        menu_item.description_en = form.description_en.data
        menu_item.description_de = form.description_de.data
        menu_item.description_nl = form.description_nl.data
        menu_item.price = form.price.data
        menu_item.is_active = form.is_active.data
        
        if form.image.data:
            # Slet gammel fil hvis der er en
            if menu_item.image:
                try:
                    os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], 'menu', menu_item.image))
                except:
                    pass
                    
            filename = secure_filename(str(uuid.uuid4()) + os.path.splitext(form.image.data.filename)[1])
            form.image.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], 'menu', filename))
            menu_item.image = filename
            
        db.session.commit()
        
        flash('Menupunkt opdateret.', 'success')
        return redirect(url_for('admin.menu'))
        
    return render_template('admin/edit_menu_item.html', title='Rediger Menupunkt', form=form, menu_item=menu_item)

@bp.route('/menu/delete/<int:id>', methods=['POST'])
@admin_required
def delete_menu_item(id):
    menu_item = MenuItem.query.get_or_404(id)
    
    # Slet billedfil hvis der er en
    if menu_item.image:
        try:
            os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], 'menu', menu_item.image))
        except:
            pass
            
    db.session.delete(menu_item)
    db.session.commit()
    
    flash('Menupunkt slettet.', 'success')
    return redirect(url_for('admin.menu'))

# Café åbningstider
@bp.route('/cafe_hours', methods=['GET', 'POST'])
@admin_required
def cafe_hours():
    form = OpeningHoursForm()
    
    # Hent eksisterende åbningstider
    hours = {}
    for day in range(7):  # 0=Mandag, 1=Tirsdag, ..., 6=Søndag
        hours[day] = CafeHours.query.filter_by(day=day).first()
        if not hours[day]:
            # Opret standard åbningstider hvis de ikke findes
            hours[day] = CafeHours(day=day, is_closed=False, open_time=time(10, 0), close_time=time(21, 0))
            db.session.add(hours[day])
            db.session.commit()
    
    if form.validate_on_submit():
        # Opdater åbningstider for hver dag
        hours[0].is_closed = form.monday_is_closed.data
        hours[0].open_time = form.monday_open_time.data
        hours[0].close_time = form.monday_close_time.data
        
        hours[1].is_closed = form.tuesday_is_closed.data
        hours[1].open_time = form.tuesday_open_time.data
        hours[1].close_time = form.tuesday_close_time.data
        
        hours[2].is_closed = form.wednesday_is_closed.data
        hours[2].open_time = form.wednesday_open_time.data
        hours[2].close_time = form.wednesday_close_time.data
        
        hours[3].is_closed = form.thursday_is_closed.data
        hours[3].open_time = form.thursday_open_time.data
        hours[3].close_time = form.thursday_close_time.data
        
        hours[4].is_closed = form.friday_is_closed.data
        hours[4].open_time = form.friday_open_time.data
        hours[4].close_time = form.friday_close_time.data
        
        hours[5].is_closed = form.saturday_is_closed.data
        hours[5].open_time = form.saturday_open_time.data
        hours[5].close_time = form.saturday_close_time.data
        
        hours[6].is_closed = form.sunday_is_closed.data
        hours[6].open_time = form.sunday_open_time.data
        hours[6].close_time = form.sunday_close_time.data
        
        db.session.commit()
        
        flash('Åbningstider opdateret.', 'success')
        return redirect(url_for('admin.dashboard'))
    
    # Forudfyld formularen med eksisterende data
    form.monday_is_closed.data = hours[0].is_closed
    form.monday_open_time.data = hours[0].open_time
    form.monday_close_time.data = hours[0].close_time
    
    form.tuesday_is_closed.data = hours[1].is_closed
    form.tuesday_open_time.data = hours[1].open_time
    form.tuesday_close_time.data = hours[1].close_time
    
    form.wednesday_is_closed.data = hours[2].is_closed
    form.wednesday_open_time.data = hours[2].open_time
    form.wednesday_close_time.data = hours[2].close_time
    
    form.thursday_is_closed.data = hours[3].is_closed
    form.thursday_open_time.data = hours[3].open_time
    form.thursday_close_time.data = hours[3].close_time
    
    form.friday_is_closed.data = hours[4].is_closed
    form.friday_open_time.data = hours[4].open_time
    form.friday_close_time.data = hours[4].close_time
    
    form.saturday_is_closed.data = hours[5].is_closed
    form.saturday_open_time.data = hours[5].open_time
    form.saturday_close_time.data = hours[5].close_time
    
    form.sunday_is_closed.data = hours[6].is_closed
    form.sunday_open_time.data = hours[6].open_time
    form.sunday_close_time.data = hours[6].close_time
    
    return render_template('admin/cafe_hours.html', title='Café Åbningstider', form=form)

# Bager administration
@bp.route('/bakery_items')
@admin_required
def bakery_items():
    items = BakeryItem.query.order_by(BakeryItem.name_da).all()
    return render_template('admin/bakery_items.html', title='Bager Administration', items=items)

@bp.route('/create_bakery_item', methods=['GET', 'POST'])
@admin_required
def create_bakery_item():
    form = BakeryItemForm()
    
    if form.validate_on_submit():
        image_filename = save_image(form.image.data, 'bakery')
        
        bakery_item = BakeryItem(
            name_da=form.name_da.data,
            name_en=form.name_en.data,
            name_de=form.name_de.data,
            name_nl=form.name_nl.data,
            name_fi=form.name_fi.data,
            name_no=form.name_no.data,
            name_sv=form.name_sv.data,
            price=form.price.data,
            image=image_filename,
            is_active=form.is_active.data
        )
        
        db.session.add(bakery_item)
        db.session.commit()
        
        flash('Bager-produkt oprettet.', 'success')
        return redirect(url_for('admin.bakery_items'))
    
    return render_template('admin/create_bakery_item.html', title='Opret Bager-produkt', form=form)

@bp.route('/edit_bakery_item/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_bakery_item(id):
    bakery_item = BakeryItem.query.get_or_404(id)
    form = BakeryItemForm()
    
    if form.validate_on_submit():
        bakery_item.name_da = form.name_da.data
        bakery_item.name_en = form.name_en.data
        bakery_item.name_de = form.name_de.data
        bakery_item.name_nl = form.name_nl.data
        bakery_item.name_fi = form.name_fi.data
        bakery_item.name_no = form.name_no.data
        bakery_item.name_sv = form.name_sv.data
        bakery_item.price = form.price.data
        bakery_item.is_active = form.is_active.data
        
        if form.image.data:
            image_filename = save_image(form.image.data, 'bakery')
            bakery_item.image = image_filename
        
        db.session.commit()
        
        flash('Bager-produkt opdateret.', 'success')
        return redirect(url_for('admin.bakery_items'))
    
    # Forudfyld formularen med eksisterende data
    form.name_da.data = bakery_item.name_da
    form.name_en.data = bakery_item.name_en
    form.name_de.data = bakery_item.name_de
    form.name_nl.data = bakery_item.name_nl
    form.name_fi.data = bakery_item.name_fi
    form.name_no.data = bakery_item.name_no
    form.name_sv.data = bakery_item.name_sv
    form.price.data = bakery_item.price
    form.is_active.data = bakery_item.is_active
    
    return render_template('admin/edit_bakery_item.html', title='Rediger Bager-produkt', form=form, bakery_item=bakery_item)

@bp.route('/delete_bakery_item/<int:id>', methods=['POST'])
@admin_required
def delete_bakery_item(id):
    bakery_item = BakeryItem.query.get_or_404(id)
    
    # Slet billedet hvis det findes
    if bakery_item.image:
        try:
            image_path = os.path.join(current_app.root_path, 'static', 'uploads', 'bakery', bakery_item.image)
            if os.path.exists(image_path):
                os.remove(image_path)
        except Exception as e:
            # Fortsæt selvom billedet ikke kunne slettes
            pass
    
    db.session.delete(bakery_item)
    db.session.commit()
    
    flash('Bager-produkt slettet.', 'success')
    return redirect(url_for('admin.bakery_items'))

@bp.route('/bakery_orders')
@admin_required
def bakery_orders():
    orders = BakeryOrder.query.order_by(BakeryOrder.order_date.desc()).all()
    return render_template('admin/bakery_orders.html', title='Rundstykkebestillinger', orders=orders)

@bp.route('/bakery_order_details/<int:id>')
@admin_required
def bakery_order_details(id):
    order = BakeryOrder.query.get_or_404(id)
    return render_template('admin/bakery_order_details.html', title='Bestillingsdetaljer', order=order)

# Kalender administration
@bp.route('/events')
@admin_required
def events():
    events = Event.query.order_by(Event.start_date).all()
    return render_template('admin/events.html', title='Kalender Administration', events=events)

@bp.route('/create_event', methods=['GET', 'POST'])
@admin_required
def create_event():
    form = EventForm()
    
    if form.validate_on_submit():
        image_filename = save_image(form.image.data, 'events')
        
        event = Event(
            title_da=form.title_da.data,
            title_en=form.title_en.data,
            title_de=form.title_de.data,
            title_nl=form.title_nl.data,
            title_fi=form.title_fi.data,
            title_no=form.title_no.data,
            title_sv=form.title_sv.data,
            description_da=form.description_da.data,
            description_en=form.description_en.data,
            description_de=form.description_de.data,
            description_nl=form.description_nl.data,
            description_fi=form.description_fi.data,
            description_no=form.description_no.data,
            description_sv=form.description_sv.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            location=form.location.data,
            image=image_filename,
            is_active=form.is_active.data
        )
        
        db.session.add(event)
        db.session.commit()
        
        flash('Arrangement oprettet.', 'success')
        return redirect(url_for('admin.events'))
    
    return render_template('admin/create_event.html', title='Opret Arrangement', form=form)

@bp.route('/edit_event/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_event(id):
    event = Event.query.get_or_404(id)
    form = EventForm()
    
    if form.validate_on_submit():
        event.title_da = form.title_da.data
        event.title_en = form.title_en.data
        event.title_de = form.title_de.data
        event.title_nl = form.title_nl.data
        event.title_fi = form.title_fi.data
        event.title_no = form.title_no.data
        event.title_sv = form.title_sv.data
        event.description_da = form.description_da.data
        event.description_en = form.description_en.data
        event.description_de = form.description_de.data
        event.description_nl = form.description_nl.data
        event.description_fi = form.description_fi.data
        event.description_no = form.description_no.data
        event.description_sv = form.description_sv.data
        event.start_date = form.start_date.data
        event.end_date = form.end_date.data
        event.location = form.location.data
        event.is_active = form.is_active.data
        
        if form.image.data:
            image_filename = save_image(form.image.data, 'events')
            event.image = image_filename
        
        db.session.commit()
        
        flash('Arrangement opdateret.', 'success')
        return redirect(url_for('admin.events'))
    
    # Forudfyld formularen med eksisterende data
    form.title_da.data = event.title_da
    form.title_en.data = event.title_en
    form.title_de.data = event.title_de
    form.title_nl.data = event.title_nl
    form.title_fi.data = event.title_fi
    form.title_no.data = event.title_no
    form.title_sv.data = event.title_sv
    form.description_da.data = event.description_da
    form.description_en.data = event.description_en
    form.description_de.data = event.description_de
    form.description_nl.data = event.description_nl
    form.description_fi.data = event.description_fi
    form.description_no.data = event.description_no
    form.description_sv.data = event.description_sv
    form.start_date.data = event.start_date
    form.end_date.data = event.end_date
    form.location.data = event.location
    form.is_active.data = event.is_active
    
    return render_template('admin/edit_event.html', title='Rediger Arrangement', form=form, event=event)

@bp.route('/delete_event/<int:id>', methods=['POST'])
@admin_required
def delete_event(id):
    event = Event.query.get_or_404(id)
    
    # Slet billedet hvis det findes
    if event.image:
        try:
            image_path = os.path.join(current_app.root_path, 'static', 'uploads', 'events', event.image)
            if os.path.exists(image_path):
                os.remove(image_path)
        except Exception as e:
            # Fortsæt selvom billedet ikke kunne slettes
            pass
    
    db.session.delete(event)
    db.session.commit()
    
    flash('Arrangement slettet.', 'success')
    return redirect(url_for('admin.events'))

@bp.route('/event_registrations')
@admin_required
def event_registrations():
    registrations = EventRegistration.query.order_by(EventRegistration.registration_date.desc()).all()
    return render_template('admin/event_registrations.html', title='Arrangementtilmeldinger', registrations=registrations)

# Kampagne administration
@bp.route('/promotions')
@admin_required
def promotions():
    promotions = Promotion.query.order_by(Promotion.start_date).all()
    return render_template('admin/promotions.html', title='Kampagne Administration', promotions=promotions, now=datetime.now())

@bp.route('/create_promotion', methods=['GET', 'POST'])
@admin_required
def create_promotion():
    form = PromotionForm()
    
    if form.validate_on_submit():
        image_filename = save_image(form.image.data, 'posters')
        
        promotion = Promotion(
            title_da=form.title_da.data,
            title_en=form.title_en.data,
            title_de=form.title_de.data,
            title_nl=form.title_nl.data,
            title_fi=form.title_fi.data,
            title_no=form.title_no.data,
            title_sv=form.title_sv.data,
            description_da=form.description_da.data,
            description_en=form.description_en.data,
            description_de=form.description_de.data,
            description_nl=form.description_nl.data,
            description_fi=form.description_fi.data,
            description_no=form.description_no.data,
            description_sv=form.description_sv.data,
            price=form.price.data,
            original_price=form.original_price.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            image=image_filename,
            is_active=form.is_active.data
        )
        
        db.session.add(promotion)
        db.session.commit()
        
        flash('Kampagne oprettet.', 'success')
        return redirect(url_for('admin.promotions'))
    
    return render_template('admin/create_promotion.html', title='Opret Kampagne', form=form)

@bp.route('/edit_promotion/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_promotion(id):
    promotion = Promotion.query.get_or_404(id)
    form = PromotionForm()
    
    if form.validate_on_submit():
        promotion.title_da = form.title_da.data
        promotion.title_en = form.title_en.data
        promotion.title_de = form.title_de.data
        promotion.title_nl = form.title_nl.data
        promotion.title_fi = form.title_fi.data
        promotion.title_no = form.title_no.data
        promotion.title_sv = form.title_sv.data
        promotion.description_da = form.description_da.data
        promotion.description_en = form.description_en.data
        promotion.description_de = form.description_de.data
        promotion.description_nl = form.description_nl.data
        promotion.description_fi = form.description_fi.data
        promotion.description_no = form.description_no.data
        promotion.description_sv = form.description_sv.data
        promotion.price = form.price.data
        promotion.original_price = form.original_price.data
        promotion.start_date = form.start_date.data
        promotion.end_date = form.end_date.data
        promotion.is_active = form.is_active.data
        
        if form.image.data:
            image_filename = save_image(form.image.data, 'posters')
            promotion.image = image_filename
        
        db.session.commit()
        
        flash('Kampagne opdateret.', 'success')
        return redirect(url_for('admin.promotions'))
    
    # Forudfyld formularen med eksisterende data
    form.title_da.data = promotion.title_da
    form.title_en.data = promotion.title_en
    form.title_de.data = promotion.title_de
    form.title_nl.data = promotion.title_nl
    form.title_fi.data = promotion.title_fi
    form.title_no.data = promotion.title_no
    form.title_sv.data = promotion.title_sv
    form.description_da.data = promotion.description_da
    form.description_en.data = promotion.description_en
    form.description_de.data = promotion.description_de
    form.description_nl.data = promotion.description_nl
    form.description_fi.data = promotion.description_fi
    form.description_no.data = promotion.description_no
    form.description_sv.data = promotion.description_sv
    form.price.data = promotion.price
    form.original_price.data = promotion.original_price
    form.start_date.data = promotion.start_date
    form.end_date.data = promotion.end_date
    form.is_active.data = promotion.is_active
    
    return render_template('admin/edit_promotion.html', title='Rediger Kampagne', form=form, promotion=promotion)

@bp.route('/delete_promotion/<int:id>', methods=['POST'])
@admin_required
def delete_promotion(id):
    promotion = Promotion.query.get_or_404(id)
    
    # Slet billedet hvis det findes
    if promotion.image:
        try:
            image_path = os.path.join(current_app.root_path, 'static', 'uploads', 'posters', promotion.image)
            if os.path.exists(image_path):
                os.remove(image_path)
        except Exception as e:
            # Fortsæt selvom billedet ikke kunne slettes
            pass
    
    db.session.delete(promotion)
    db.session.commit()
    
    flash('Kampagne slettet.', 'success')
    return redirect(url_for('admin.promotions'))

@bp.route('/promotion_orders')
@admin_required
def promotion_orders():
    orders = PromotionOrder.query.order_by(PromotionOrder.order_date.desc()).all()
    return render_template('admin/promotion_orders.html', title='Kampagnebestillinger', orders=orders)

# Friluftsbad administration
@bp.route('/pool_hours_admin')
@admin_required
def pool_hours_admin():
    pool_hours = PoolHours.query.order_by(PoolHours.order_index, PoolHours.start_date).all()
    return render_template('admin/pool_hours.html', title='Friluftsbadets Åbningstider', pool_hours=pool_hours)

@bp.route('/create_pool_hours', methods=['GET', 'POST'])
@admin_required
def create_pool_hours():
    form = PoolHoursForm()
    
    if form.validate_on_submit():
        pool_hours = PoolHours(
            name_da=form.name_da.data,
            name_en=form.name_en.data,
            name_de=form.name_de.data,
            name_nl=form.name_nl.data,
            description_da=form.description_da.data,
            description_en=form.description_en.data,
            description_de=form.description_de.data,
            description_nl=form.description_nl.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            weekday_open_time=form.weekday_open_time.data,
            weekday_close_time=form.weekday_close_time.data,
            weekend_open_time=form.weekend_open_time.data,
            weekend_close_time=form.weekend_close_time.data,
            special_note_da=form.special_note_da.data,
            special_note_en=form.special_note_en.data,
            special_note_de=form.special_note_de.data,
            special_note_nl=form.special_note_nl.data,
            order_index=form.order_index.data,
            is_active=form.is_active.data
        )
        
        db.session.add(pool_hours)
        db.session.commit()
        
        flash('Åbningstider for friluftsbadet oprettet.', 'success')
        return redirect(url_for('admin.pool_hours_admin'))
    
    return render_template('admin/create_pool_hours.html', title='Opret Åbningstider', form=form)

@bp.route('/edit_pool_hours/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_pool_hours(id):
    pool_hours = PoolHours.query.get_or_404(id)
    form = PoolHoursForm()
    
    if form.validate_on_submit():
        pool_hours.name_da = form.name_da.data
        pool_hours.name_en = form.name_en.data
        pool_hours.name_de = form.name_de.data
        pool_hours.name_nl = form.name_nl.data
        pool_hours.description_da = form.description_da.data
        pool_hours.description_en = form.description_en.data
        pool_hours.description_de = form.description_de.data
        pool_hours.description_nl = form.description_nl.data
        pool_hours.start_date = form.start_date.data
        pool_hours.end_date = form.end_date.data
        pool_hours.weekday_open_time = form.weekday_open_time.data
        pool_hours.weekday_close_time = form.weekday_close_time.data
        pool_hours.weekend_open_time = form.weekend_open_time.data
        pool_hours.weekend_close_time = form.weekend_close_time.data
        pool_hours.special_note_da = form.special_note_da.data
        pool_hours.special_note_en = form.special_note_en.data
        pool_hours.special_note_de = form.special_note_de.data
        pool_hours.special_note_nl = form.special_note_nl.data
        pool_hours.order_index = form.order_index.data
        pool_hours.is_active = form.is_active.data
        
        db.session.commit()
        
        flash('Åbningstider for friluftsbadet opdateret.', 'success')
        return redirect(url_for('admin.pool_hours_admin'))
    
    # Forudfyld formularen med eksisterende data
    form.name_da.data = pool_hours.name_da
    form.name_en.data = pool_hours.name_en
    form.name_de.data = pool_hours.name_de
    form.name_nl.data = pool_hours.name_nl
    form.description_da.data = pool_hours.description_da
    form.description_en.data = pool_hours.description_en
    form.description_de.data = pool_hours.description_de
    form.description_nl.data = pool_hours.description_nl
    form.start_date.data = pool_hours.start_date
    form.end_date.data = pool_hours.end_date
    form.weekday_open_time.data = pool_hours.weekday_open_time
    form.weekday_close_time.data = pool_hours.weekday_close_time
    form.weekend_open_time.data = pool_hours.weekend_open_time
    form.weekend_close_time.data = pool_hours.weekend_close_time
    form.special_note_da.data = pool_hours.special_note_da
    form.special_note_en.data = pool_hours.special_note_en
    form.special_note_de.data = pool_hours.special_note_de
    form.special_note_nl.data = pool_hours.special_note_nl
    form.order_index.data = pool_hours.order_index
    form.is_active.data = pool_hours.is_active
    
    return render_template('admin/edit_pool_hours.html', title='Rediger Åbningstider', form=form, pool_hours=pool_hours)

@bp.route('/delete_pool_hours/<int:id>', methods=['POST'])
@admin_required
def delete_pool_hours(id):
    pool_hours = PoolHours.query.get_or_404(id)
    
    db.session.delete(pool_hours)
    db.session.commit()
    
    flash('Åbningstider for friluftsbadet slettet.', 'success')
    return redirect(url_for('admin.pool_hours_admin'))
