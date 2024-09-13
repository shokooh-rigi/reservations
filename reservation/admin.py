from django.contrib import admin
from .models import Room, Reservation, Listing


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'number',
        'listing',
        'capacity',
        'room_type',
        'get_facilities',
        'view',
    )
    search_fields = (
        'number',
        'listing__name',
    )
    list_filter = (
        'listing',
        'room_type',
        'facilities',
    )
    ordering = ('number',)
    filter_horizontal = ('facilities',)

    def get_facilities(self, obj):
        return ", ".join([facility.name for facility in obj.facilities.all()])
    get_facilities.short_description = 'Facilities'


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        'room',
        'name',
        'start_time',
        'end_time',
        'nights',
        'adults',
        'children',
        'status',
    )
    search_fields = (
        'room__number',
        'name',
    )
    list_filter = (
        'room',
        'status',
        'start_time',
        'end_time',
    )
    ordering = ('start_time',)


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'get_amenities')
    search_fields = ('name', 'location')
    ordering = ('name',)
    filter_horizontal = ('amenities',)

    def get_amenities(self, obj):
        return ", ".join([amenity.name for amenity in obj.amenities.all()])
    get_amenities.short_description = 'Amenities'
