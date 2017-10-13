from datetime import date
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import generic
from django.utils import timezone
from django.db.models import Count

from .models import Artist, Event, Venue
from .forms import ArtistForm, EventForm, VenueForm


class IndexView(generic.ListView):
    model = Artist
    template_name = 'event/index.html'
    discover_count = 5
    trending_count = 8
    recommend_count = 10

    def get_context_data(self, **kwargs):
        """
        Return the discover, trending, new,
        recommended artists and events
        """
        context = super(IndexView, self).get_context_data(**kwargs)
        # Get all artists, but exclude artists without images
        context['discover'] = Artist.objects.exclude(image_url__exact='', thumb_url__exact='')
        # Exclude artists already followed by a current user
        context['discover'] = context['discover'].exclude(users__in=[self.request.user.id])[:self.discover_count]
        context['trending'] = Artist.objects.annotate(user_count=Count('users')).order_by('-user_count')[:self.trending_count]
        if self.request.user.is_authenticated():
            # Get upcoming events by a user's favorite artists
            context['recommend'] = Event.objects.filter(artists__in=self.request.user.artists.all(), datetime__gte=timezone.now())
            # Exclude events already followed by a current user
            context['recommend'] = context['recommend'].exclude(users__in=[self.request.user.id]).annotate(
                                                                user_count=Count('users')).order_by(
                                                                'datetime', '-user_count')[:self.recommend_count]
            context['event_count'] = self.request.user.events.filter(datetime__gte=timezone.now()).count()
        return context


class SearchView(generic.ListView):
    model = Event
    template_name = 'event/search.html'


class ArtistView(generic.ListView):
    model = Artist
    count = 12
    template_name = 'event/artist.html'
    context_object_name = 'artists'

    def get_queryset(self):
        """
        Return the first twelve artists
        """
        return super().get_queryset()[:self.count]


class ArtistDetailView(generic.DetailView):
    model = Artist

    def get_context_data(self, **kwargs):
        """
        Return the artist detail information
        """
        now = timezone.now()
        today = date.today()
        year = today.year
        week = today.isocalendar()[1]
        month = today.month
        events = self.object.events

        context = super(ArtistDetailView, self).get_context_data(**kwargs)

        context['upcoming_events'] = {}
        context['upcoming_events'].update({'week':  events.filter(datetime__gte=now, datetime__week=week).order_by('datetime')})
        context['upcoming_events'].update({'month': events.filter(datetime__gte=now, datetime__month=month).order_by('datetime')})
        context['upcoming_events'].update({'year':  events.filter(datetime__gte=now, datetime__year=year).order_by('datetime')})
        context['upcoming_events'].update({'all':   events.filter(datetime__gte=now).order_by('datetime')})

        context['past_events'] = {}
        context['past_events'].update({'week':  events.filter(datetime__lte=now, datetime__week=week).order_by('-datetime')})
        context['past_events'].update({'month': events.filter(datetime__lte=now, datetime__month=month).order_by('-datetime')})
        context['past_events'].update({'year':  events.filter(datetime__lte=now, datetime__year=year).order_by('-datetime')})
        context['past_events'].update({'all':   events.filter(datetime__lte=now).order_by('-datetime')})
        return context


class ArtistCreateView(generic.CreateView):
    model = Artist
    form_class = ArtistForm
    success_url = reverse_lazy('user:profile')

    def form_valid(self, form):
        """
        Create the artist
        """
        self.request.user.artists.add(form.save())
        return super(ArtistCreateView, self).form_valid(form)


class ArtistUpdateView(generic.UpdateView):
    model = Artist
    form_class = ArtistForm
    success_url = reverse_lazy('user:profile')


class ArtistDeleteView(generic.DeleteView):
    model = Artist
    success_url = reverse_lazy('user:profile')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class EventView(generic.ListView):
    model = Event
    template_name = 'event/event.html'
    context_object_name = 'events'

    def get_context_data(self, **kwargs):
        """
        Return the upcoming events
        """
        now = timezone.now()
        today = date.today()
        year = today.year
        week = today.isocalendar()[1]
        month = today.month
        events = Event.objects

        context = super(EventView, self).get_context_data(**kwargs)

        context['events'] = {}
        context['events'].update({'week':  events.filter(datetime__gte=now, datetime__week=week).order_by('datetime')})
        context['events'].update({'month': events.filter(datetime__gte=now, datetime__month=month).order_by('datetime')})
        context['events'].update({'year':  events.filter(datetime__gte=now, datetime__year=year).order_by('datetime')})
        context['events'].update({'all':   events.filter(datetime__gte=now).order_by('datetime')})
        return context


class EventDetailView(generic.DetailView):
    model = Event


class EventCreateView(generic.CreateView):
    model = Event
    form_class = EventForm
    success_url = reverse_lazy('user:profile')

    def form_valid(self, form):
        """
        Create the event
        """
        self.request.user.events.add(form.save())
        form.instance.artists.set(form.cleaned_data['artists'])
        return super(EventCreateView, self).form_valid(form)


class EventUpdateView(generic.UpdateView):
    model = Event
    form_class = EventForm
    success_url = reverse_lazy('user:profile')

    def form_valid(self, form):
        """
        Update the event
        """
        form.instance.artists.set(form.cleaned_data['artists'])
        return super(EventUpdateView, self).form_valid(form)


class EventDeleteView(generic.DeleteView):
    model = Event
    success_url = reverse_lazy('user:profile')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class VenueView(generic.ListView):
    model = Venue
    count = 12
    template_name = 'event/venue.html'
    context_object_name = 'venues'

    def get_queryset(self):
        """
        Return the first twelve venues
        """
        return super().get_queryset()[:self.count]


class VenueCreateView(generic.CreateView):
    model = Venue
    form_class = VenueForm
    success_url = reverse_lazy('user:profile')

    def form_valid(self, form):
        """
        Create the venue
        """
        self.request.user.venues.add(form.save())
        return super(VenueCreateView, self).form_valid(form)


class VenueUpdateView(generic.UpdateView):
    model = Venue
    form_class = VenueForm
    success_url = reverse_lazy('user:profile')


class VenueDeleteView(generic.DeleteView):
    model = Venue
    success_url = reverse_lazy('user:profile')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


def bookmark_artist(request, pk):
    if request.user.is_authenticated():
        if request.user.artists.filter(id=pk):
            request.user.artists.remove(pk)
        else:
            request.user.artists.add(pk)

        return JsonResponse({
            'pk': pk,
            'id': 'artists',
            'user_count': Artist.objects.get(pk=pk).users.count(),
            'artist_count': request.user.artists.count(),
        })


def bookmark_event(request, pk):
    if request.user.is_authenticated():
        if request.user.events.filter(id=pk):
            request.user.events.remove(pk)
        else:
            request.user.events.add(pk)

        return JsonResponse({
            'pk': pk,
            'id': 'events',
            'user_count': Event.objects.get(pk=pk).users.count(),
            'event_count': request.user.events.count(),
        })


def bookmark_venue(request, pk):
    if request.user.is_authenticated():
        if request.user.venues.filter(id=pk):
            request.user.venues.remove(pk)
        else:
            request.user.venues.add(pk)

        return JsonResponse({
            'pk': pk,
            'id': 'venues',
            'user_count': Venue.objects.get(pk=pk).users.count(),
            'venue_count': request.user.venues.count(),
        })
