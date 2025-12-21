from .availability import AvailabilityManager

def availability_status(request):
    """
    Context processor to add availability status to all templates.
    """
    return {
        'availability': AvailabilityManager.get_status_data()
    }
