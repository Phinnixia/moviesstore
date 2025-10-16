from django.shortcuts import render, redirect, get_object_or_404 
from .models import Movie, Review, Petition, Rating
from django.contrib.auth.decorators import login_required

def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()
    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html', {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)
    ratings = Rating.objects.filter(movie =movie)
    score = 0
    total = 0
    for rating in ratings:
        score += rating.rating
        total += 1
    if total != 0:
        total = score / total
    #total = 5
    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    template_data['ratings'] = ratings
    template_data['total'] = total
    return render(request, 'movies/show.html', {'template_data': template_data})

#UPVOTE (copy for rating)
def comments(request):
    reviews = Review.objects.all()
    template_data = {}
    template_data['reviews'] = reviews.order_by('-upvote')
    return render(request, 'movies/comments.html', {'template_data': template_data})

def increment_upvote(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.upvote += 1
    review.save()
    return redirect('movies.show', id=id)

#PETITIONS
def petitions(request):
    petitions = Petition.objects.all()
    template_data = {}
    template_data['petitions'] = petitions
    return render(request, 'movies/petitions.html', {'template_data': template_data})

#RATINGS
@login_required
def create_rating(request, id):
    if request.method == 'POST':
        movie = Movie.objects.get(id=id)
        rating = Rating()
        rating.movie = movie
        rating.user = request.user
        rating.rating = request.POST['rating']
        rating.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def create_petition(request):
    if request.method == 'POST' and request.POST['movieTitle'] != '':
        petition = Petition()
        petition.movieTitle = request.POST['movieTitle']
        petition.description = request.POST['description']
        petition.save()

        petitions = Petition.objects.all()
        template_data = {}
        template_data['petitions'] = petitions

        return render(request, 'movies/petitions.html', {'template_data': template_data})
    else:
        return render(request, 'movies/petitions.html', {'template_data': template_data})

def vote(request, id):
    petition = get_object_or_404(Petition, id=id)
    petition.votes += 1
    petition.save()

    petitions = Petition.objects.all()
    template_data = {}
    template_data['petitions'] = petitions
    return render(request, 'movies/petitions.html', {'template_data': template_data})

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html', {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('movies.show', id=id)