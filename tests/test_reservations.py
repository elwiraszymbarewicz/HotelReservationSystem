from datetime import date
import pytest
from src.models import Guest, Room, Reservation

def test_reservation_creation_and_defaults() -> None:
    """Testuje poprawne tworzenie obiektu rezerwacji i jej domyślny status."""
    guest = Guest(1, "Jan Kowalski", "jan@wp.pl", "+48111222333", "XYZ123")
    room = Room(101, "Standard", 200.0)
    reservation = Reservation(1, guest, room, date(2026, 7, 1), date(2026, 7, 5))

    assert reservation.reservation_id == 1
    assert reservation.guest.name == "Jan Kowalski"
    assert reservation.room.room_number == 101
    assert reservation.is_active is True

def test_calculate_total_cost_multiple_nights() -> None:
    """Testuje poprawne wyliczanie kosztu dla kilkudniowego pobytu."""
    guest = Guest(1, "Jan", "jan@wp.pl", "123", "DOC1")
    room = Room(101, "Standard", 250.0)
    # 4 noce: od 1 do 5 lipca
    reservation = Reservation(1, guest, room, date(2026, 7, 1), date(2026, 7, 5))

    assert reservation.calculate_total_cost() == 1000.0

def test_calculate_total_cost_invalid_dates() -> None:
    """Testuje, czy system zwraca 0.0 przy błędnych lub takich samych datach."""
    guest = Guest(1, "Jan", "jan@wp.pl", "123", "DOC1")
    room = Room(101, "Standard", 250.0)

    # Ta sama data (0 nocy)
    res_same_day = Reservation(2, guest, room, date(2026, 7, 1), date(2026, 7, 1))
    # Data końcowa przed początkową
    res_wrong_order = Reservation(3, guest, room, date(2026, 7, 5), date(2026, 7, 1))

    assert res_same_day.calculate_total_cost() == 0.0
    assert res_wrong_order.calculate_total_cost() == 0.0

def test_cancel_reservation() -> None:
    """Testuje poprawność procesu anulowania rezerwacji."""
    guest = Guest(1, "Jan", "jan@wp.pl", "123", "DOC1")
    room = Room(101, "Standard", 200.0)
    reservation = Reservation(1, guest, room, date(2026, 7, 1), date(2026, 7, 2))

    reservation.cancel_reservation()
    assert reservation.is_active is False