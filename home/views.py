from django.shortcuts import render
from cart.models import Item
from django.db.models import Count
import moviesstore.settings as settings

# Create your views here.
def index(request):
    template_data = {}
    template_data['title'] = 'Movies Store'
    template_data["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY
    state_movie_stats = (
        Item.objects
        .values('order__state', 'movie__name')
        .annotate(num_purchases=Count('id'))
        .exclude(order__state__isnull=True)
        .exclude(order__state__exact='')
        .order_by('-num_purchases')
    )

    top_movie_per_state = {}
    for entry in state_movie_stats:
        state = entry['order__state']
        movie = entry['movie__name']
        if state not in top_movie_per_state:
            top_movie_per_state[state] = movie

    template_data['map_data'] = top_movie_per_state
    return render(request, 'home/index.html', {
        'template_data': template_data})
def about(request):
    template_data = {}
    template_data['title'] = 'About'
    return render(request, 'home/about.html',
        {'template_data': template_data})