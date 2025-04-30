from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required
from .models import MoodEntry, JournalEntry, UserProfile, Activity, Badge, DailyChallenge, MeditationSession, WellnessPlan
from .forms import MoodEntryForm, JournalEntryForm, ProfileUpdateForm
from django.utils.timezone import now
from django.utils import timezone
from django.contrib import messages
import random

def home(request):
    return render(request, 'home.html')


@login_required
def home_view(request):
    if request.method == 'POST':
        form = MoodEntryForm(request.POST)
        if form.is_valid():
            mood_entry = form.save(commit=False)
            mood_entry.user = request.user
            mood_entry.save()
            return redirect('home')

    else:
        form = MoodEntryForm()

    # Fetch mood data for the chart
    mood_entries = MoodEntry.objects.filter(user=request.user).order_by('date')
    mood_dates = [entry.date.strftime('%b %d') for entry in mood_entries]
    mood_values = [entry.mood_value for entry in mood_entries]  # Ensure this matches your model field

    return render(request, 'home.html', {
        'form': form,
        'mood_dates': mood_dates,
        'mood_values': mood_values,
    })


def track_mood(request):
    if request.method == 'POST':
        mood = request.POST.get('mood')
        gratitude = request.POST.get('gratitude')

        mood_mapping = {
            'Happy': 5,
            'Calm': 4,
            'Neutral': 3,
            'Anxious': 2,
            'Sad': 1,
        }
        
        mood_value = mood_mapping.get(mood, 3)  # Default to Neutral

        MoodEntry.objects.create(user=request.user, mood=mood, mood_value=mood_value, gratitude=gratitude)
        return redirect('home')


@login_required
def track_mood_view(request):
    if request.method == 'POST':
        form = MoodEntryForm(request.POST)
        if form.is_valid():
            mood_entry = form.save(commit=False)

            # Map the mood to a numerical value
            mood_mapping = {
                'Happy': 5,
                'Calm': 4,
                'Neutral': 3,
                'Anxious': 2,
                'Sad': 1,
            }

            mood_entry.mood_value = mood_mapping.get(mood_entry.mood, 3)  # Default to Neutral

            mood_entry.user = request.user
            mood_entry.save()
            return redirect('track_mood')
    else:
        form = MoodEntryForm()

    # Fetch mood data for the chart
    mood_entries = MoodEntry.objects.filter(user=request.user).order_by('date')
    mood_dates = [entry.date.strftime('%b %d') for entry in mood_entries]
    mood_values = [entry.mood_value for entry in mood_entries]

    return render(request, 'track_mood.html', {
        'form': form,
        'mood_dates': mood_dates,
        'mood_values': mood_values,
    })


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def assessment_view(request):
    if request.method == 'POST':
        overwhelmed = int(request.POST.get('overwhelmed', 3))
        joy = int(request.POST.get('joy', 3))
        sleep = int(request.POST.get('sleep', 3))

        score = overwhelmed + joy + sleep

        # Simple feedback logic
        if score >= 12:
            result = "You're doing well! Keep nurturing your mental health. 🌟"
        elif score >= 8:
            result = "You're balancing things, but there's room for self-care. ✨"
        else:
            result = "It might be a good time to seek support. Remember, help is available. 💙"

        return render(request, 'assessment.html', {'result': result})

    return render(request, 'assessment.html')


def book_appointment(request):
    if request.method == 'POST':
        # Handle form data here
        name = request.POST.get('name')
        email = request.POST.get('email')
        date = request.POST.get('date')
        message = request.POST.get('message')
        
        # Save or process the appointment
        # Example: Save to the database or send an email
        
        return redirect('assessment')  # Redirect back to assessment page

    return render(request, 'book_appointment.html')


@login_required
def journal_view(request):
    if request.method == "POST":
        form = JournalEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect('journal')  # Refresh the page to show the new entry
    else:
        form = JournalEntryForm()

    # Get the user's journal entries, sorted by date (newest first)
    entries = JournalEntry.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'journal.html', {
        'form': form,
        'entries': entries,
    })


def resources_view(request):
    return render(request, 'resources.html')


def wellness_plan_view(request):
    wellness_plan = None

    if request.method == "POST":
        stress_level = int(request.POST.get("stress", 0))
        sleep_hours = int(request.POST.get("sleep", 0))
        joy_activities = request.POST.get("joy_activities", "").lower()
        goals = request.POST.get("goals", "").strip()
        self_care_time = int(request.POST.get("self_care_time", 0))

        # Build the personalized plan
        daily_routine = "🌅 **Morning Routine:**\n"
        daily_routine += "- Start with 5 minutes of deep breathing 🧘‍♀️\n"
        daily_routine += "- Stretch or do light yoga for flexibility 🧎‍♂️\n"

        # Sleep-based suggestions
        if sleep_hours < 6:
            daily_routine += "- Take a 20-minute power nap in the afternoon 💤\n"
        else:
            daily_routine += "- Go for a short morning walk for energy 🌞\n"

        # Stress-based activities
        relaxation_activities = "✨ **Recommended Relaxation Activities:**\n"
        if stress_level >= 4:
            relaxation_activities += "- Try progressive muscle relaxation 🧠\n"
            relaxation_activities += "- Listen to calming nature sounds 🌊\n"
            relaxation_activities += "- Journaling for emotional release 📓\n"
        else:
            relaxation_activities += "- Enjoy creative hobbies like painting 🎨\n"

        # Joy-based activities
        if "music" in joy_activities:
            relaxation_activities += "- Curate a calming playlist 🎵\n"
        if "reading" in joy_activities:
            relaxation_activities += "- Read uplifting books or poetry 📚\n"
        if "walk" in joy_activities:
            daily_routine += "- Take a mindful nature walk after lunch 🚶‍♀️\n"

        # Goal-based recommendations
        if "anxiety" in goals.lower():
            relaxation_activities += "- Try grounding exercises (like 5-4-3-2-1) 🌿\n"
        if "focus" in goals.lower():
            relaxation_activities += "- Use Pomodoro technique for work ⏲️\n"
        if "energy" in goals.lower():
            relaxation_activities += "- Do short HIIT workouts to boost energy ⚡\n"

        # Self-care time adjustments
        if self_care_time < 30:
            relaxation_activities += "- Do quick 10-minute meditations 🧘‍♂️\n"
        else:
            relaxation_activities += "- Explore longer activities like yoga or journaling ✍️\n"

        # Diet tips
        diet_tips = "🥗 **Healthy Eating Tips:**\n"
        diet_tips += "- Eat nutrient-rich foods (leafy greens, berries, nuts) 🥬\n"
        diet_tips += "- Drink plenty of water — hydration boosts mood 💧\n"
        if "energy" in goals.lower():
            diet_tips += "- Include protein-rich snacks for sustained energy 🍳\n"

        # Save the generated plan
        wellness_plan = WellnessPlan.objects.create(
            goal=goals if goals else "General Wellness",
            time_commitment=f"{self_care_time} minutes/day",
            daily_routine=daily_routine,
            diet_tips=diet_tips,
            relaxation_activities=relaxation_activities
        )

    return render(request, 'wellness_plan.html', {'wellness_plan': wellness_plan})


@login_required
def dashboard_view(request):
    # Calculate streak
    streak_days = calculate_user_streak(request.user)
    
    # Get journal entries count
    journal_count = JournalEntry.objects.filter(user=request.user).count()
    
    # Get mindful minutes
    mindful_minutes = calculate_mindful_minutes(request.user)
    
    # Get user badges
    user_badges = get_user_badges(request.user)
    
    # Get daily challenge
    daily_challenge = get_daily_challenge()
    
    # Get mood data for chart
    mood_entries = MoodEntry.objects.filter(user=request.user).order_by('date')
    mood_dates = [entry.date.strftime('%b %d') for entry in mood_entries]
    mood_values = [entry.mood_value for entry in mood_entries]
    
    context = {
        'streak_days': streak_days,
        'journal_count': journal_count,
        'mindful_minutes': mindful_minutes,
        'user_badges': user_badges,
        'daily_challenge': daily_challenge,
        'mood_dates': mood_dates,
        'mood_values': mood_values,
    }
    
    return render(request, 'dashboard.html', context)


def calculate_user_streak(user):
    """
    Calculate the user's current streak in days
    """
    try:
        profile = UserProfile.objects.get(user=user)
        
        if not profile.streak_start:
            return 0
            
        today = timezone.now().date()
        delta = today - profile.streak_start
        return delta.days + 1
    except UserProfile.DoesNotExist:
        return 0
    except Exception:
        return 0


def calculate_mindful_minutes(user):
    """
    Calculate the total mindful minutes for a user based on their meditation sessions
    
    Args:
        user: User object
        
    Returns:
        int: Total minutes spent meditating
    """
    try:
        # Try to get the total from the profile first (for efficiency)
        profile = UserProfile.objects.get(user=user)
        return profile.total_mindful_minutes
    except (UserProfile.DoesNotExist, AttributeError):
        # If profile doesn't exist or doesn't have this field, calculate from sessions
        try:
            # Sum up the duration of all meditation sessions
            sessions = MeditationSession.objects.filter(user=user)
            total_minutes = sum(session.duration for session in sessions)
            return total_minutes
        except Exception:
            # If there's any error, return 0 as a fallback
            return 0


def get_user_badges(user):
    """
    Get all badges for a user, both unlocked and locked
    
    Args:
        user: User object
        
    Returns:
        QuerySet: User's badges with unlock status
    """
    try:
        # Get all badges assigned to the user
        badges = Badge.objects.filter(user=user)
        
        # If user has no badges yet, create default ones
        if not badges.exists():
            default_badges = [
                {
                    "name": "First Journal",
                    "description": "Write your first journal entry",
                    "icon": "mdi-notebook-outline",
                    "unlocked": False,
                    "progress": 0
                },
                {
                    "name": "Mindfulness Beginner",
                    "description": "Complete 10 minutes of meditation",
                    "icon": "mdi-meditation",
                    "unlocked": False,
                    "progress": 0
                },
                {
                    "name": "Week Streak",
                    "description": "Maintain a 7-day login streak",
                    "icon": "mdi-calendar-check",
                    "unlocked": False,
                    "progress": 0
                },
                {
                    "name": "Challenge Accepted",
                    "description": "Complete 5 daily challenges",
                    "icon": "mdi-trophy-outline",
                    "unlocked": False,
                    "progress": 0
                }
            ]
            
            for badge_data in default_badges:
                Badge.objects.create(user=user, **badge_data)
            
            # Fetch the newly created badges
            badges = Badge.objects.filter(user=user)
        
        return badges
    except Exception:
        # Return an empty list if there's an error
        return []


def get_daily_challenge():
    """
    Get a daily challenge for the user
    
    Returns:
        str: A daily challenge text
    """
    try:
        # Try to get today's challenge from the database
        today = timezone.now().date()
        challenge = DailyChallenge.objects.filter(date=today).first()
        
        if challenge:
            return challenge.text
        
        # If no challenge for today, get a random one or create a default
        challenge = DailyChallenge.objects.order_by('?').first()
        
        if challenge:
            return challenge.text
        
        # Default challenges if none exist in the database
        default_challenges = [
            "Take 5 minutes to practice deep breathing",
            "Write down three things you're grateful for today",
            "Compliment someone today and notice how it makes you both feel",
            "Go for a 10-minute walk outside and observe nature",
            "Drink at least 8 glasses of water today",
            "Practice active listening in a conversation today",
            "Try a 5-minute meditation session",
            "Reach out to someone you haven't spoken to in a while",
            "Take a break from social media today",
            "Write down one positive thing that happened today"
        ]
        
        return random.choice(default_challenges)
    except Exception:
        # Return a default challenge if there's an error
        return "Take a moment to breathe deeply and appreciate the present moment"


@login_required
def meditation_view(request):
    return render(request, 'meditation.html')


def mood_tracker(request):
    return render(request, 'track_mood.html')


@login_required
def profile_view(request):
    """View for displaying user profile page"""
    # Get user profile data
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    # Get user statistics
    streak_days = calculate_user_streak(user)
    
    # FIXED: Use JournalEntry.objects.filter instead of user.journal_entries
    journal_count = JournalEntry.objects.filter(user=user).count()
    
    mindful_minutes = calculate_mindful_minutes(user)
    achievements_count = Badge.objects.filter(user=user, unlocked=True).count()
    
    # Get user's badges
    user_badges = Badge.objects.filter(user=user)
    
    # Get recent activities
    recent_activities = Activity.objects.filter(user=user).order_by('-timestamp')[:10]
    
    context = {
        'user': user,
        'profile': profile,
        'streak_days': streak_days,
        'journal_count': journal_count,
        'mindful_minutes': mindful_minutes,
        'achievements_count': achievements_count,
        'user_badges': user_badges,
        'recent_activities': recent_activities,
    }
    
    return render(request, 'profile.html', context)


@login_required
def update_profile(request):
    """View for updating user profile"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            
            # Create activity for profile update
            Activity.objects.create(
                user=request.user,
                title="Profile Updated",
                description="You updated your profile information",
                icon="mdi-account-edit"
            )
            
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    
    return redirect('profile')