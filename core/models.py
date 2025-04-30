# models.py

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import datetime

# Mood Entry Model

class MoodEntry(models.Model):
    MOOD_CHOICES = [
        ('Happy', 5),
        ('Calm', 4),
        ('Neutral', 3),
        ('Anxious', 2),
        ('Sad', 1),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES)
    mood_value = models.IntegerField(default=3)  # Neutral mood as default
    gratitude = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.mood} on {self.date}"

# Journal Entry Model

class JournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Wellness Plan Model

class WellnessPlan(models.Model):
    goal = models.CharField(max_length=255)
    time_commitment = models.CharField(max_length=50)
    daily_routine = models.TextField()
    diet_tips = models.TextField(default="Stay hydrated and eat nutritious foods 🥗")
    relaxation_activities = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wellness Plan for {self.goal} - {self.time_commitment}"

# User Profile Model

class UserProfile(models.Model):
    """Extended user profile model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    last_activity = models.DateTimeField(default=timezone.now)
    streak_start = models.DateField(null=True, blank=True)
    total_mindful_minutes = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def calculate_streak(self):
        """Calculate the user's current streak in days"""
        if not self.streak_start:
            return 0
            
        today = timezone.now().date()
        delta = today - self.streak_start
        return delta.days + 1
    
    def get_total_mindful_minutes(self):
        """Get total minutes spent meditating"""
        return self.total_mindful_minutes

# Create and save profile automatically
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a profile when a new user is created"""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the profile when the user is updated"""
    instance.profile.save()

# Badge Model

class Badge(models.Model):
    """Model for user achievement badges"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges')
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50)  # Material Design Icon class
    unlocked = models.BooleanField(default=False)
    progress = models.IntegerField(default=0)  # Progress percentage toward unlocking
    date_unlocked = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.user.username})"

# Activity Model

class Activity(models.Model):
    """Model for tracking user activities"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50)  # Material Design Icon class
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name_plural = "Activities"
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"

# Meditation Session Model

class MeditationSession(models.Model):
    """Model to track user meditation sessions"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meditation_sessions')
    duration = models.IntegerField(help_text="Duration in minutes")
    date = models.DateField(default=timezone.now)
    completed = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.duration} minutes on {self.date}"

# Daily Challenge Model

class DailyChallenge(models.Model):
    """Model for storing daily challenges"""
    text = models.TextField()
    date = models.DateField(default=timezone.now)
    
    def __str__(self):
        return f"Challenge for {self.date}: {self.text[:30]}..."
    
    class Meta:
        verbose_name_plural = "Daily Challenges"

# User Challenge Model

class UserChallenge(models.Model):
    """Model to track which challenges a user has completed"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='completed_challenges')
    challenge = models.ForeignKey(DailyChallenge, on_delete=models.CASCADE)
    completed_date = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ('user', 'challenge')
    
    def __str__(self):
        return f"{self.user.username} completed '{self.challenge.text[:20]}...' on {self.completed_date}"

