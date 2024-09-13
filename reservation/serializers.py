from rest_framework import serializers

from .enums import RoomType, ViewType
from .models import Room, Reservation, Listing, Amenity, Facility


class RoomAvailabilitySerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()

    def validate(self, data):
        """
        Ensure that the end date is after the start date.
        """
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if start_date and end_date and start_date >= end_date:
            raise serializers.ValidationError("End date must be after start date.")

        return data


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ['id', 'name']


class RoomSerializer(serializers.ModelSerializer):
    room_type = serializers.ChoiceField(choices=RoomType.choices)
    view = serializers.ChoiceField(choices=ViewType.choices)
    facilities = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = [
            'number',
            'capacity',
            'room_type',
            'view',
            'facilities',
        ]

    def get_facilities(self, obj):
        return [facility.name for facility in obj.facilities.all()]


class ReservationSerializer(serializers.ModelSerializer):
    listing = serializers.PrimaryKeyRelatedField(queryset=Listing.objects.all(), write_only=True)

    class Meta:
        model = Reservation
        fields = [
            'listing',
            'room',
            'name',
            'start_time',
            'end_time',
            'adults',
            'children',
        ]

    def validate(self, data):
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("End time must be after start time.")
        return data

    def create(self, validated_data):
        listing = validated_data.pop('listing')
        room = validated_data['room']
        start_time = validated_data['start_time']
        end_time = validated_data['end_time']

        if room.listing != listing:
            raise serializers.ValidationError("Selected room does not belong to the chosen listing.")

        if Reservation.objects.filter(
                room=room,
                start_time__lt=end_time,
                end_time__gt=start_time
        ).exists():
            raise serializers.ValidationError("This room is already reserved for the selected dates.")

        return Reservation.objects.create(**validated_data)


class ListingSerializer(serializers.ModelSerializer):
    amenities = AmenitySerializer(many=True, read_only=True)

    class Meta:
        model = Listing
        fields = ['id', 'name', 'location', 'amenities']
