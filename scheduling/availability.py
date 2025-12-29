import datetime
from django.utils import timezone

class AvailabilityManager:
    """
    Manages the service availability logic for Tecno Pronto.
    Schedule:
    - Monday to Friday: 18:00 - 00:00 (Midnight)
    - Saturday and Sunday: Available all day (24h)
    """
    SCHEDULE_TEXT = "Lun-Ven 18:00-24:00 & Weekend"

    @classmethod
    def is_available(cls, now=None):
        """
        Determines if the service is currently available based on the current time.
        """
        if now is None:
            # Get current local time in the configured TIME_ZONE
            now = timezone.localtime(timezone.now())
        
        weekday = now.weekday()  # 0 is Monday, 6 is Sunday
        hour = now.hour
        
        # Weekend (Saturday=5, Sunday=6)
        if weekday >= 5:
            return True
        
        # Weekday (Mon-Fri)
        # 18:00 to 24:00
        if 18 <= hour < 24:
            return True
            
        return False

    @classmethod
    def get_status_data(cls):
        """
        Returns a dictionary containing all availability-related data
        and Tailwind CSS classes for consistent styling.
        """
        is_avail = cls.is_available()
        return {
            'is_available': is_avail,
            'schedule': cls.SCHEDULE_TEXT,
            'status_text': "Disponibile Ora" if is_avail else "Attualmente Chiuso",
            'status_color': "green" if is_avail else "red",
            'status_bg': "green-500/10" if is_avail else "red-500/10",
            'status_border': "green-500/20" if is_avail else "red-500/20",
            'status_bullet': "green-500" if is_avail else "red-500",
            'status_bullet_ping': "green-400" if is_avail else "red-400",
            'status_text_color': "green-400" if is_avail else "red-400",
        }
