from datetime import datetime, timedelta

from tests.e2e.conftest import Context


def test_navigating_to_previous_months(context: Context) -> None:
    context.pages.calendar_page.open()
    context.pages.calendar_page.choose_event('wesele')
    context.pages.calendar_page.go_to_month(5, 2024)
    has_correct_month, displayed_title = context.pages.calendar_page.check_displayed_calendar_title('MAJ 2024')
    assert has_correct_month, f'The {displayed_title=} is different than expected: "MAJ 2024"'


def test_navigating_to_future_months(context: Context) -> None:
    context.pages.calendar_page.open()
    context.pages.calendar_page.choose_event('wesele')
    year = datetime.now().year + 1
    context.pages.calendar_page.go_to_month(5, year)
    has_correct_month, displayed_title = context.pages.calendar_page.check_displayed_calendar_title(f'MAJ {year}')
    assert has_correct_month, f'The {displayed_title=} is different than expected: "MAJ {year}"'


def test_book_the_wedding(context: Context) -> None:
    context.pages.calendar_page.open()
    context.pages.calendar_page.choose_event('wesele')
    date = datetime.now().date() + timedelta(days=10)
    context.pages.calendar_page.go_to_month(date.month, date.year)
    context.pages.calendar_page.choose_date(date)

    context.pages.form_page.switch_to_form()
    data = {'name': 'Test', 'email': 'Test@gmail.com', 'location': 'Zamojska 20, Lublin'}
    context.pages.form_page.book_event(**data)
    assert context.pages.success_page.is_success_header_displayed()
