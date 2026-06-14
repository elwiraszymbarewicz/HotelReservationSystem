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