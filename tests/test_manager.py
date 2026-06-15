from src.hotel_manager import HotelManager
from src.models import Room
def test_add_room_to_manager() -> None:
    """Testuje poprawne dodawanie pokoju do wewnętrznej listy menedżera."""
    manager = HotelManager("Hotel Blue")
    room = Room(101, "Standard", 150.0)
    manager.add_room(room)
    assert len(manager.rooms) == 1
    assert manager.rooms[0].room_number == 101