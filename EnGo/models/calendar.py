from calendar import Calendar
from datetime import timedelta
from EnGo.models.product import SoldProduct, FinishedProduct
from EnGo.models.receipt import Receipt
from EnGo.models.expense import Expense

weekday_heads = {
    0: "Lunes",
    1: "Martes",
    2: "Miércoles",
    3: "Jueves",
    4: "Viernes",
    5: "Sábado",
    6: "Domingo"
}


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
    
    def get_all_day_events(date):
        all_events = MyCalendar.get_all_events()
        day_events = {}
        for selected_category in all_events:
            events = all_events[selected_category]
            day_events[selected_category] = [event for event in events if event.date.isocalendar() == date.isocalendar()]

        return day_events

    def get_weekday_dates(date):
        current_weekday = date.weekday()
        weekday_dates = {current_weekday: date}
        for day in range(current_weekday):
            previous_day = timedelta(days=current_weekday - day)
            weekday_dates[day] = date - previous_day 
        for day in range(current_weekday, 7):
            weekday_dates[day] = date + timedelta(days=day - current_weekday)

        return weekday_dates