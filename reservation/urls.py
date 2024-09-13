from django.urls import path
from reservation.views import CreateReservationView, CheckAvailabilityView, booked_rooms_report, ListingView, \
    RoomListView

urlpatterns = [
    path('listings/', ListingView.as_view(), name='listings'),
    path('listings/<int:listing_id>/rooms/', RoomListView.as_view(), name='listing-rooms'),
    path('create-reservation/', CreateReservationView.as_view(), name='create-reservation'),
    path('check-availability/', CheckAvailabilityView.as_view(), name='check-availability'),
    path('report/<str:report_type>/', booked_rooms_report, name='booked_rooms_report'),
]
