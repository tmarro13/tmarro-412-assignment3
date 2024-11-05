from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    
    # data attributes of a Profile
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    firstname = models.TextField(blank=False)
    lastname = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.TextField(blank=False)
    image_url = models.URLField(blank=True)

    def __str__(self):
        '''Return a string representation of this object.'''

        return f'{self.firstname} {self.lastname}' 
    def __str__(self):
        '''Return a string representation of this Profile object.'''
        return f'{self.firstname} {self.lastname}'

    def get_status_messages(self):
        '''Return all status messages related to this profile, ordered by timestamp descending.'''
        return self.status_messages.all().order_by('-timestamp')

    def get_absolute_url(self):
        '''Return the URL to access a particular profile instance.'''
        return reverse('show_profile', kwargs={'pk': self.pk})
    
    def get_friends(self):
        """Retrieve a list of friends for the current profile."""
        friends = Friend.objects.filter(
            Q(profile1=self) | Q(profile2=self)
        )
        # Extract friend profiles based on whether they are profile1 or profile2
        friend_profiles = [f.profile1 if f.profile2 == self else f.profile2 for f in friends]
        return friend_profiles
    
    def add_friend(self, other):
        if self != other:
            if not Friend.objects.filter(
                models.Q(profile1=self, profile2=other) | 
                models.Q(profile1=other, profile2=self)
            ).exists():
                Friend.objects.create(profile1=self, profile2=other)

    def get_friend_suggestions(self):
    # Get a list of current friends' IDs for this profile
        current_friends = self.get_friends()
        current_friend_ids = [friend.id for friend in current_friends]

    # Include the current profile's ID in the list to exclude from suggestions
        exclude_ids = current_friend_ids + [self.id]

    # Query for profiles that are not friends with the current profile and exclude the profile itself
        suggestions = Profile.objects.exclude(id__in=exclude_ids)

        return suggestions
    
    def get_news_feed(self):
        # Fetching status messages for the user and their friends
        friend_profiles = self.get_friends()
        # Include user's own status messages
        friends_and_self = friend_profiles + [self]
        # Use a filter to get all status messages from user's friends and the user
        news_feed = StatusMessage.objects.filter(profile__in=friends_and_self).order_by('-timestamp')
        return news_feed



class StatusMessage(models.Model):
    '''Model representing a user's status message.'''
    timestamp = models.DateTimeField(default=timezone.now)
    message = models.TextField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='status_messages')
    
    def get_images(self):
        return self.image_set.all()

class Image(models.Model):
    image_file = models.ImageField(upload_to='status_images')
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class Friend(models.Model):
    profile1 = models.ForeignKey('Profile', related_name='profile1', on_delete=models.CASCADE)
    profile2 = models.ForeignKey('Profile', related_name='profile2', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.profile1.firstname} & {self.profile2.firstname}'
    
    def get_friends(self):
        friends_as_profile1 = Friend.objects.filter(profile1=self).values_list('profile2', flat=True)
        friends_as_profile2 = Friend.objects.filter(profile2=self).values_list('profile1', flat=True)
        friend_ids = set(friends_as_profile1) | set(friends_as_profile2)
        return Profile.objects.filter(id__in=friend_ids)