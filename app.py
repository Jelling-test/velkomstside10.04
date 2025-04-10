from app import create_app, db
from app.models import User, Admin, MenuItem, CafeHours, BakeryItem, BakeryOrder, BakeryOrderItem, Event, EventRegistration, Promotion, PromotionOrder

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db, 
        'User': User, 
        'Admin': Admin, 
        'MenuItem': MenuItem, 
        'CafeHours': CafeHours, 
        'BakeryItem': BakeryItem, 
        'BakeryOrder': BakeryOrder, 
        'BakeryOrderItem': BakeryOrderItem, 
        'Event': Event, 
        'EventRegistration': EventRegistration, 
        'Promotion': Promotion, 
        'PromotionOrder': PromotionOrder
    }

if __name__ == '__main__':
    app.run(debug=True)
