from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter
from django.db.models import Count
import plotly.express as px
from plotly.io import to_html
from datetime import datetime

# Display a paginated list of voters with optional filtering
class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100  # Display 100 records per page

    def get_queryset(self):
        """Filter voter records based on query parameters."""
        queryset = super().get_queryset()
        # Retrieve filters from the GET request
        party = self.request.GET.get('party_affiliation')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')
        v20state = self.request.GET.get('v20state')
        v21town = self.request.GET.get('v21town')
        v21primary = self.request.GET.get('v21primary')
        v22general = self.request.GET.get('v22general')
        v23town = self.request.GET.get('v23town')

        # Apply filters to the queryset based on user input
        if party and party != 'All':
            queryset = queryset.filter(party_affiliation=party)
        if min_dob:
            queryset = queryset.filter(date_of_birth__gte=f'{min_dob}-01-01')
        if max_dob:
            queryset = queryset.filter(date_of_birth__lte=f'{max_dob}-12-31')
        if voter_score and voter_score != 'All':
            queryset = queryset.filter(voter_score=voter_score)
        if v20state == 'on':
            queryset = queryset.filter(v20state=True)
        if v21town == 'on':
            queryset = queryset.filter(v21town=True)
        if v21primary == 'on':
            queryset = queryset.filter(v21primary=True)
        if v22general == 'on':
            queryset = queryset.filter(v22general=True)
        if v23town == 'on':
            queryset = queryset.filter(v23town=True)

        return queryset

    def get_context_data(self, **kwargs):
        """Add filter options to context for template use."""
        context = super().get_context_data(**kwargs)
        context['party_choices'] = self.get_party_choices()
        context['year_choices'] = self.get_year_choices()
        context['voter_score_choices'] = self.get_voter_score_choices()
        return context

    def get_party_choices(self):
        """Retrieve distinct party affiliations."""
        parties = Voter.objects.values_list('party_affiliation', flat=True).distinct()
        return ['All'] + sorted([party.strip() for party in parties if party.strip()])

    def get_year_choices(self):
        """Generate unique years from date_of_birth fields."""
        years = Voter.objects.values_list('date_of_birth', flat=True)
        years = [dob.year for dob in years if dob]
        return sorted(set(years))

    def get_voter_score_choices(self):
        """Retrieve unique voter scores."""
        scores = Voter.objects.values_list('voter_score', flat=True).distinct()
        return ['All'] + sorted(scores)


# Display detailed information for a single voter
class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'


# Display graphs with data on voters, with optional filtering
class GraphsView(ListView):
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'
    
    def get_queryset(self):
        """Filter voters based on selected criteria for graph data."""
        queryset = Voter.objects.all()
        # Retrieve filters from the GET request
        party = self.request.GET.get('party_affiliation')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')
        elections = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']

        # Apply filters
        if party and party != 'All':
            queryset = queryset.filter(party_affiliation=party.strip())
        if min_dob:
            queryset = queryset.filter(date_of_birth__year__gte=int(min_dob))
        if max_dob:
            queryset = queryset.filter(date_of_birth__year__lte=int(max_dob))
        if voter_score and voter_score != 'All':
            queryset = queryset.filter(voter_score=int(voter_score))
        for election in elections:
            if self.request.GET.get(election):
                queryset = queryset.filter(**{election: True})

        return queryset

    def get_context_data(self, **kwargs):
        """Add graphs and filter options to context for template use."""
        context = super().get_context_data(**kwargs)
        
        # Filtered voter data
        voters = self.get_queryset()

        # Generate a histogram for Year of Birth
        birth_years = [voter.date_of_birth.year for voter in voters if voter.date_of_birth]
        if birth_years:
            birth_year_fig = px.histogram(
                x=birth_years,
                nbins=100,
                title="Voter Distribution by Year of Birth",
                labels={'x': 'Year of Birth', 'y': 'Count'}
            )
            context['year_of_birth_graph'] = to_html(birth_year_fig, full_html=False)
        else:
            context['year_of_birth_graph'] = "<p>No data available for Year of Birth chart.</p>"

        # Generate a pie chart for Party Affiliation
        party_counts = {}
        for voter in voters:
            party = voter.party_affiliation.strip() or 'Unknown'
            party_counts[party] = party_counts.get(party, 0) + 1
        if party_counts:
            party_fig = px.pie(
                names=list(party_counts.keys()),
                values=list(party_counts.values()),
                title="Voter Distribution by Party Affiliation"
            )
            context['party_affiliation_graph'] = to_html(party_fig, full_html=False)
        else:
            context['party_affiliation_graph'] = "<p>No data available for Party Affiliation chart.</p>"

        # Generate a bar chart for Election Participation
        participation_data = {
            '2020 State': sum(1 for voter in voters if voter.v20state),
            '2021 Town': sum(1 for voter in voters if voter.v21town),
            '2021 Primary': sum(1 for voter in voters if voter.v21primary),
            '2022 General': sum(1 for voter in voters if voter.v22general),
            '2023 Town': sum(1 for voter in voters if voter.v23town),
        }
        if any(participation_data.values()):
            election_fig = px.bar(
                x=list(participation_data.keys()),
                y=list(participation_data.values()),
                title="Voter Participation in Elections",
                labels={'x': 'Election', 'y': 'Number of Voters'}
            )
            context['election_participation_graph'] = to_html(election_fig, full_html=False)
        else:
            context['election_participation_graph'] = "<p>No data available for Election Participation chart.</p>"

        # Add filter options for graph page
        context['party_choices'] = ['All'] + list(Voter.objects.values_list('party_affiliation', flat=True).distinct())
        context['year_choices'] = sorted(set(
            voter.date_of_birth.year for voter in Voter.objects.all() if voter.date_of_birth
        ))
        context['voter_score_choices'] = ['All'] + sorted(set(
            Voter.objects.values_list('voter_score', flat=True).distinct()
        ))

        return context
