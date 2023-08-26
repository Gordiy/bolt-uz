from rest_framework.exceptions import ValidationError

from bolt_uz.celery import app

from .models import Ticket
from .services import CalculateDistanceService, ImageStationRecognitionService


# TODO: create better solution for image station recognition.
@app.task
def image_station_recognition(ticket_id: int) -> None:
    """Recognite image."""
    ticket = Ticket.objects.get(id=ticket_id)
    file = ticket.file
    user = ticket.user
    
    print(type(file))

    station_recognition_service = ImageStationRecognitionService(file)
    try:
        result = station_recognition_service.recognite()
    except ValidationError:
        ticket.delete()
        return None


    distance = 0
    for data in result:
        origin = data.get('origin').lower()
        destination = data.get('destination').lower()

        try:
            ticket_distance = CalculateDistanceService().calculate_distance(origin, destination)
            distance += ticket_distance
        except ValidationError:
            ticket.delete()
        
        ticket.origin = origin
        ticket.destination = destination
        ticket.save()

        user.update_distance(ticket_distance)
