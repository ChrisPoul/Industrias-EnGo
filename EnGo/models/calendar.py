from calendar import Calendar
from EnGo.models.product import SoldProduct, FinishedProduct
from EnGo.models.receipt import Receipt
from EnGo.models.expense import Expense

event_categories = dict(
    selecting="Seleccionar Categoría",
    all="Todos",
    sold_product="Productos Vendidos",
    finished_product="Productos Terminados",
    receipt="Recibos",
    expense="Gastos"
)
update_views = dict(
    all="admin.admin",
    sold_product="receipt.update",
    finished_product="warehouse.update_product",
    receipt="receipt.update",
    expense="expense.update"
)


class MyCalendar:

    def get_months(date):
        calendar = Calendar()
        month_rows = calendar.yeardatescalendar(date.year, 1)
        months = [month_row[0] for month_row in month_rows]

        return months

    def get_all_events():
        return dict(
            selecting=[],
            all=[],
            sold_product=SoldProduct.query.all(),
            finished_product=FinishedProduct.query.all(),
            receipt=Receipt.query.all(),
            expense=Expense.query.all()
        )
    
    def get_day_events(date):
        try:
            filter_date = date.date()
        except AttributeError:
            filter_date = date

        def filter_events_by_day(events):
            return [event for event in events if event.date.date() == filter_date]

        all_events = MyCalendar.get_all_events()
        day_events = {}
        for selected_category in all_events:
            events = all_events[selected_category]
            day_events[selected_category] = filter_events_by_day(events)

        return day_events