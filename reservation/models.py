from django.db import models
from reservation.enums import ViewType, RoomType, Status, AmenityType, FacilityType


class Amenity(models.Model):
    name = models.CharField(
        max_length=50,
        choices=AmenityType.choices,
    )

    def __str__(self):
        return self.name


class Facility(models.Model):
    name = models.CharField(
        max_length=50,
        choices=FacilityType.choices,
    )

    def __str__(self):
        return self.name


class Listing(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    amenities = models.ManyToManyField(Amenity, blank=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    number = models.CharField(max_length=10)
    capacity = models.IntegerField()
    room_type = models.CharField(
        max_length=20,
        choices=RoomType.choices,
        default=RoomType.SINGLE,
    )
    view = models.CharField(
        max_length=20,
        choices=ViewType.choices,
        default=ViewType.LAKE,
    )
    listing = models.ForeignKey(
        Listing,
        related_name='rooms',
        on_delete=models.CASCADE,
    )
    facilities = models.ManyToManyField(Facility, blank=True)

    def __str__(self):
        return f"Room {self.number} - {self.listing.name}"


class Reservation(models.Model):
    name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    room = models.ForeignKey(
        Room,
        related_name='reservations',
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.CONFIRMED,
    )
    adults = models.IntegerField(default=1)
    children = models.IntegerField(default=0)

    @property
    def nights(self):
        return (self.end_time.date() - self.start_time.date()).days

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['room', 'start_time', 'end_time'],
                name='unique_reservation',
            )
        ]

    def __str__(self):
        return f"Reservation for {self.name} in room {self.room.number}"
