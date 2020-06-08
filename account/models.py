from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    )

    HAND_CHOICES = (
        ('left', 'Left'),
        ('right', 'Right')
    )

    BATTING_ORDER_CHOICES = (
        ('opener' , 'Opener'),
        ('middle', 'Middle Order'),
        ('finish', 'Finisher'),
        ('tail', 'Tail Ender')
    )

    BOWLING_TYPE_CHOICES = (
        ('RAF', 'Right Arm Fast'),
        ('RAM', 'Right Arm Medium'),
        ('LAF', 'Left Arm Fast'),
        ('LAM', 'Left Arm Medium'),
        ('RAFS', 'Right Arm Finger Spin'),
        ('RAWS', 'Right Arm Wrist Spin'),
        ('LAFS', 'Left Arm Finger Spin'),
        ('LAWS', 'Left Arm Wrist Spin')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Not Mentioned', null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    batting_hand = models.CharField(max_length=5, choices=HAND_CHOICES, default='Not Mentioned', null=True, blank=True)
    batting_order = models.CharField(max_length=6, choices=BATTING_ORDER_CHOICES, default='Not Mentioned', null=True, blank=True)
    bowling_hand = models.CharField(max_length=5, choices=HAND_CHOICES, null=True, default='Not Mentioned', blank=True)
    bowling_type = models.CharField(max_length=5, choices=BOWLING_TYPE_CHOICES, default='Not Mentioned', null=True, blank=True)
    image = models.ImageField(default='default.png', upload_to='profile_pictures')

    def __str__(self):
        return f'{self.user.username} Profile'