class Guest:
    """Reprezentuje gościa hotelowego z pełnymi danymi rejestracyjnymi."""

    def __init__(self, guest_id: int, name: str, email: str, phone: str, document_id: str):
        self.guest_id: int = guest_id
        self.name: str = name
        self.email: str = email
        self.phone: str = phone
        self.document_id: str = document_id

    def is_data_complete(self) -> bool:
        """Sprawdza, czy wszystkie wymagane pola zostały wypełnione (brak pustych stringów)."""
        return all([self.name.strip(), self.email.strip(), self.phone.strip(), self.document_id.strip()])

    def is_email_valid(self) -> bool:
        """Sprawdza, czy podany adres email zawiera znak '@'."""
        return "@" in self.email


class Room:
    """Reprezentuje pokój hotelowy."""

    def __init__(self, room_number: int, room_type: str, price_per_night: float):
        self.room_number: int = room_number
        self.room_type: str = room_type
        self.price_per_night: float = price_per_night
        self.is_clean: bool = True

    def mark_as_dirty(self) -> None:
        self.is_clean = False

    def mark_as_clean(self) -> None:
        self.is_clean = True

from datetime import date

class Reservation:
    """Reprezentuje rezerwację konkretnego pokoju przez gościa hotelowego."""

    def __init__(self, reservation_id: int, guest: 'Guest', room: 'Room', start_date: date, end_date: date):
        self.reservation_id: int = reservation_id
        self.guest: 'Guest' = guest
        self.room: 'Room' = room
        self.start_date: date = start_date
        self.end_date: date = end_date
        self.is_active: bool = True

    def calculate_total_cost(self) -> float:
        """Oblicza całkowity koszt rezerwacji na podstawie liczby nocy i ceny pokoju.
        
        Zwraca 0.0, jeśli daty są niepoprawne (np. data końcowa przed początkową).
        """
        nights = (self.end_date - self.start_date).days
        if nights <= 0:
            return 0.0
        return nights * self.room.price_per_night

    def cancel_reservation(self) -> None:
        """Anuluje rezerwację, zmieniając jej status na nieaktywny."""
        self.is_active = False