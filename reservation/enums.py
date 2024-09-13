from django.db import models


class AmenityType(models.TextChoices):
    WIFI = 'WiFi', 'WiFi'
    MINI_BAR = 'Mini Bar', 'Mini Bar'
    SWIMMING_POOL = 'Swimming Pool', 'Swimming Pool'
    GYM = 'Gym', 'Gym'


class FacilityType(models.TextChoices):
    SMART_TV = 'Smart TV', 'Smart TV'
    HAIR_DRYER = 'Hair Dryer', 'Hair Dryer'
    AIR_CONDITIONING = 'Air Conditioning', 'Air Conditioning'
    HEATING = 'Heating', 'Heating'


class RoomType(models.TextChoices):
    SINGLE = 'Single', 'Single Room'
    DOUBLE = 'Double', 'Double Room'
    SUITE = 'Suite', 'Suite Room'
    FAMILY = 'Family', 'Family Room'


class ViewType(models.TextChoices):
    SEA = 'SEA', 'SEA View'
    LAKE = 'Lake', 'Lake View'
    CITY = 'City', 'City View'
    MOUNTAIN = 'Mountain', 'Mountain View'
    JUNGLE = 'Jungle', 'Jungle View'


class Status(models.TextChoices):
    CONFIRMED = 'Confirmed', 'Confirmed'
    PENDING = 'Pending', 'Pending'
    CANCELLED = 'Cancelled', 'Cancelled'
