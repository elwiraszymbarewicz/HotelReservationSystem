from datetime import date
import pytest
from src.models import Guest, Room, Reservation
from src.invoices import Invoice
def test_invoice_creation_and_defaults() -> None:
    """Testuje poprawne inicjalizowanie obiektu faktury i jej domyślny status."""
    guest = Guest(1, "Anna Nowak", "anna@nowak.pl", "+48555666777", "ID888999")
    room = Room(202, "Deluxe", 400.0)
    reservation = Reservation(10, guest, room, date(2026, 8, 1), date(2026, 8, 3))
    invoice = Invoice(1, reservation, date(2026, 8, 3))
    assert invoice.invoice_id == 1
    assert invoice.reservation.reservation_id == 10
    assert invoice.is_paid is False
def test_invoice_generate_summary_content() -> None:
    """Testuje, czy generowane podsumowanie zawiera kluczowe dane finansowe i osobowe."""
    guest = Guest(1, "Anna Nowak", "anna@nowak.pl", "+48555666777", "ID888999")
    room = Room(202, "Deluxe", 400.0)
    reservation = Reservation(10, guest, room, date(2026, 8, 1), date(2026, 8, 3)) 
    # 2 noce * 400 = 800
    invoice = Invoice(1, reservation, date(2026, 8, 3))
    summary = invoice.generate_summary()
    assert "FV/1" in summary
    assert "Anna Nowak" in summary
    assert "Pokój nr: 202" in summary
    assert "Kwota całkowita: 800.00 PLN" in summary
def test_invoice_payment_status_toggle() -> None:
    """Testuje poprawność zmiany statusu opłacenia faktury."""
    guest = Guest(1, "Anna Nowak", "anna@nowak.pl", "123", "DOC1")
    room = Room(202, "Deluxe", 400.0)
    reservation = Reservation(10, guest, room, date(2026, 8, 1), date(2026, 8, 2))
    invoice = Invoice(1, reservation, date(2026, 8, 2))
    assert invoice.is_paid is False
    invoice.mark_as_paid()
    assert invoice.is_paid is True