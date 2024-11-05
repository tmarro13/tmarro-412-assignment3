from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Profile, StatusMessage
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

class ShowAllProfilesView(ListView):
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

class ShowProfileView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html' 
    context_object_name = 'profile'  

class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)
        if user_form.is_valid():
            user = user_form.save()
            form.instance.user = user
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

class CreateStatusMessageView(CreateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_pk = self.kwargs.get('pk')
        profile = get_object_or_404(Profile, pk=profile_pk)
        context['profile'] = profile
        return context

    def form_valid(self, form):
        profile_pk = self.kwargs.get('pk')
        profile = get_object_or_404(Profile, pk=profile_pk)
        form.instance.profile = profile
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})
    
class UpdateProfileView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

class DeleteStatusMessageView(DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})

class UpdateStatusMessageView(UpdateView):
    model = StatusMessage
    fields = ['message']
    template_name = 'mini_fb/update_status_form.html'
    def get_success_url(self):
        # Redirect back to the profile page of the user after the status message is updated
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})

class CreateFriendView(View):
    def dispatch(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        other_profile = get_object_or_404(Profile, pk=self.kwargs['other_pk'])
        profile.add_friend(other_profile)
        return redirect('show_profile', pk=profile.pk)

class ShowFriendSuggestionsView(DetailView):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        # Use your get_friend_suggestions method to get suggestions
        context['friend_suggestions'] = profile.get_friend_suggestions()
        return context


class ShowNewsFeedView(DetailView):
    model = Profile
    template_name = 'mini_fb/news_feed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()  # Get the current profile
        context['news_feed'] = profile.get_news_feed()  # Get the news feed data
        return context

