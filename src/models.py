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