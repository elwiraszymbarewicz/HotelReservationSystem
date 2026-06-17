import pytest
from src.models import Guest, Room

def test_guest_extended_registration() -> None:
    """Testuje tworzenie gościa z pełnymi danymi oraz walidację pól."""
    guest = Guest(1, "Elwira Szymbarewicz", "elwira@example.com", "+48 123 456 789", "ABC123456")
    
    assert guest.document_id == "ABC123456"
    assert guest.is_data_complete() is True
    assert guest.is_email_valid() is True

def test_guest_incomplete_data() -> None:
    """Testuje zachowanie systemu przy brakujących danych."""
    incomplete_guest = Guest(2, "Jan Kowalski", "jan@wp.pl", " ", "")
    assert incomplete_guest.is_data_complete() is False

def test_guest_invalid_email_format() -> None:
    """Dodatkowy test: Sprawdza całkowicie błędny format e-maila (brak znaku małpy)."""
    invalid_guest = Guest(99, "Jan", "jan_at_wp.pl", "123", "DOC")
    assert invalid_guest.is_email_valid() is False

def test_room_initial_state_is_clean() -> None:
    """Dodatkowy test: Upewnia się, że każdy nowo utworzony pokój jest domyślnie czysty."""
    new_room = Room(555, "Suite", 600.0)
    assert new_room.is_clean is True

def test_room_toggle_cleanliness_multiple_times() -> None:
    """Dodatkowy test: Sprawdza wielokrotną zmianę statusu czystości pokoju."""
    room = Room(202, "Standard", 150.0)
    room.mark_as_dirty()
    room.mark_as_clean()
    room.mark_as_dirty()
    assert room.is_clean is False