from datetime import date
from src.hotel_manager import HotelManager
from src.models import Guest, Room
from src.invoices import Invoice
def test_full_reservation_flow_and_conflict_integration() -> None:
    """INTEGRACJA: Symulacja pełnej ścieżki i blokady konfliktu terminów.
    Sprawdza współpracę klas: HotelManager -> Guest -> Room -> Reservation.
    """
    manager = HotelManager("Grand Central")
    room = Room(202, "Suite", 500.0)
    guest1 = Guest(1, "Olek", "olek@wp.pl", "111", "DOC1")
    guest2 = Guest(2, "Marek", "marek@wp.pl", "222", "DOC2")
    manager.add_room(room)
    manager.register_guest(guest1)
    manager.register_guest(guest2)
    # 1. Pierwsza rezerwacja (1-5 września) - powinna się udać
    res1 = manager.create_reservation(101, guest1, room, date(2026, 9, 1), date(2026, 9, 5))
    assert res1 is not None
    assert len(manager.reservations) == 1
    # 2. Druga rezerwacja (3-4 września) - KOLIZJA! Powinna zostać odrzucona (None)
    res2 = manager.create_reservation(102, guest2, room, date(2026, 9, 2), date(2026, 9, 4))
    assert res2 is None
    # 3. Trzecia rezerwacja w bezpiecznym terminie (5-10 września) - powinna się udać
    res3 = manager.create_reservation(103, guest2, room, date(2026, 9, 5), date(2026, 9, 10))
    assert res3 is not None
def test_reservation_to_invoice_integration() -> None:
    """INTEGRACJA: Sprawdza pełną ścieżkę od rezerwacji do wystawienia faktury finansowej.
    Sprawdza współpracę klas: HotelManager -> Reservation -> Invoice.
    """
    manager = HotelManager("Grand Central")
    room = Room(301, "Standard", 200.0)
    guest = Guest(1, "Kasia", "kasia@wp.pl", "333", "DOC3")
    # Tworzymy rezerwację na 3 noce (kwota: 600.00 PLN)
    res = manager.create_reservation(201, guest, room, date(2026, 10, 1), date(2026, 10, 4))
    # Przekazujemy utworzoną w menedżerze rezerwację bezpośrednio do modułu finansowego 
    invoice = Invoice(777, res, date(2026, 10, 4))
    assert invoice.is_paid is False
    assert "Kwota całkowita: 600.00 PLN" in invoice.generate_summary()