from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from movies.models import Movie
from .utils import calculate_cart_total
from .models import Order, Item
from django.contrib.auth.decorators import login_required
from django.db.models import Count

def index(request):
    cart_total = 0
    movies_in_cart = []
    cart = request.session.get('cart', {})
    movie_ids = list(cart.keys())
    if (movie_ids != []):
        movies_in_cart = Movie.objects.filter(id__in=movie_ids)
        cart_total = calculate_cart_total(cart, movies_in_cart)
    template_data = {}
    template_data['title'] = 'Cart'
    template_data['movies_in_cart'] = movies_in_cart
    template_data['cart_total'] = cart_total
    return render(request, 'cart/index.html',{'template_data': template_data})

def add(request, id):
    get_object_or_404(Movie, id=id)
    cart = request.session.get('cart', {})
    cart[id] = request.POST['quantity']
    request.session['cart'] = cart
    return redirect('cart.index')

def clear(request):
    request.session['cart'] = {}
    return redirect('cart.index')

@login_required
def purchase(request):
    cart = request.session.get('cart', {})
    movie_ids = list(cart.keys())
    if (movie_ids == []):
        return redirect('cart.index')
    movies_in_cart = Movie.objects.filter(id__in=movie_ids)
    cart_total = calculate_cart_total(cart, movies_in_cart)

    if request.method != 'POST':
        return render(request, 'cart/state_form.html')
    
    state = request.POST.get('state')

    order = Order()
    order.user = request.user
    order.total = cart_total
    order.state = state
    order.save()
    for movie in movies_in_cart:
        item = Item()
        item.movie = movie
        item.price = movie.price
        item.order = order
        item.quantity = cart[str(movie.id)]
        item.save()
    request.session['cart'] = {}
    template_data = {}
    template_data['title'] = 'Purchase confirmation'
    template_data['order_id'] = order.id
    return render(request, 'cart/purchase.html', {'template_data': template_data})

def map_view(request):
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

    return render(request, 'home/index.html', {'top_movie_per_state': top_movie_per_state})