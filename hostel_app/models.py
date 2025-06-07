from django.db import models
from django.contrib.auth.models import User

class Hostel(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.name

class Room(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=10)
    capacity = models.IntegerField()
    current_occupancy = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.hostel.name} - Room {self.room_number}"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20)
    department = models.CharField(max_length=50)
    year = models.IntegerField()
    assigned_room = models.ForeignKey(Room, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.user.username

class BookingRequest(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    preferred_room = models.ForeignKey(Room, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Approved", "Approved"), ("Rejected", "Rejected")],
        default="Pending"
    )

    def __str__(self):
        return f"Request by {self.student.user.username} for {self.preferred_room}"

class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.FloatField()
    status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Paid", "Paid")],
        default="Pending"
    )
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.amount} - {self.status}"
