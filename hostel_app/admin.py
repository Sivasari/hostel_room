from django.contrib import admin
from .models import Hostel, Room, Student, BookingRequest, Payment

admin.site.register(Hostel)
admin.site.register(Room)
admin.site.register(Student)
admin.site.register(BookingRequest)
admin.site.register(Payment)
