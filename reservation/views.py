from datetime import datetime, time

from django.http import HttpResponse
from django.shortcuts import render
from django.utils.timezone import make_aware, is_naive
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Room, Reservation, Listing
from .serializers import ReservationSerializer, RoomAvailabilitySerializer, ListingSerializer, RoomSerializer


class ListingView(APIView):
    def get(self, request):
        listing_name = request.query_params.get('name', None)
        listing_location = request.query_params.get('location', None)

        listings = Listing.objects.all()

        if listing_name:
            listings = listings.filter(name__icontains=listing_name)
        if listing_location:
            listings = listings.filter(location__icontains=listing_location)

        serializer = ListingSerializer(listings, many=True)
        return Response(serializer.data)


class RoomListView(APIView):
    def get(self, request, listing_id):
        try:
            listing = Listing.objects.get(id=listing_id)
        except Listing.DoesNotExist:
            return Response({'error': 'Listing not found'}, status=status.HTTP_404_NOT_FOUND)

        rooms = Room.objects.filter(listing=listing)
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)


class CreateReservationView(CreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            room = serializer.validated_data['room']
            start_time = serializer.validated_data['start_time']
            end_time = serializer.validated_data['end_time']

            if is_naive(start_time):
                start_time = make_aware(start_time)
            if is_naive(end_time):
                end_time = make_aware(end_time)

            if Reservation.objects.filter(
                    room=room,
                    start_time__lt=end_time,
                    end_time__gt=start_time
            ).exists():
                return Response(
                    {'error': 'This room is already reserved for the selected dates.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            self.perform_create(serializer)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class CheckAvailabilityView(APIView):
    def post(self, request):
        listing_id = request.data.get('listing_id')
        if not listing_id:
            return Response(
                {'error': 'Listing ID is required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            listing = Listing.objects.get(id=listing_id)
        except Listing.DoesNotExist:
            return Response(
                {'error': 'Invalid listing ID.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = RoomAvailabilitySerializer(data=request.data)
        if serializer.is_valid():
            start_date = serializer.validated_data['start_date']
            end_date = serializer.validated_data['end_date']
            check_in_time = make_aware(datetime.combine(start_date, time(14, 0)))
            check_out_time = make_aware(datetime.combine(end_date, time(12, 0)))

            available_rooms = Room.objects.filter(listing=listing).exclude(
                reservations__start_time__lt=check_out_time,
                reservations__end_time__gt=check_in_time
            ).distinct()

            available_rooms_data = [{
                'room number': room.number,
                'listing name': listing.name,
                'listing location': listing.location,
                'room capacity': room.capacity,
                'room type': room.room_type,
                 } for room in available_rooms]
            return Response(
                {'available_rooms': available_rooms_data},
                status=status.HTTP_200_OK,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


def booked_rooms_report(request, report_type):
    reservations = Reservation.objects.select_related('room').all()

    if not reservations:
        return HttpResponse("No reservations found.", status=404)

    if report_type == 'html':
        return render(
            request,
            'reservation/report.html',
            {'reservations': reservations}
        )
    elif report_type == 'text':
        text_report = "\n".join(
            [
                f"Room Number: {res.room.number}, "
                f"Room Type: {res.room.room_type}, "
                f"Guest Name: {res.name}, "
                f"View: {res.room.view}, " 
                f"Amenities: {', '.join([amenity.name for amenity in res.room.listing.amenities.all()])}, "
                f"Facilities: {', '.join([facility.name for facility in res.room.facilities.all()])}, "
                f"Check-In: {res.start_time.strftime('%Y-%m-%d')}, "
                f"Check-Out: {res.end_time.strftime('%Y-%m-%d')}, "
                f"Nights: {res.nights}, "
                f"Status: {res.status}"
                for res in reservations
            ]
        )

        return HttpResponse(text_report, content_type='text/plain')

    else:
        return HttpResponse("Invalid report type", status=400)
