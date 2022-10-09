from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from .models import Movie, Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm':searchTerm, 'movies':movies, 'name':request.user.username})


def signup(request):
    signupMail = request.GET.get('email')
    return render(request, 'signup.html', {'signup':signupMail})


def detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    reviews = Review.objects.filter(movie=movie)
    return render(request, 'detail.html', {'movie':movie, 'reviews':reviews})

@login_required
def createreview(request, movie_id):
    #We first get the movie object from the database
    movie = get_object_or_404(Movie, pk=movie_id) #gets the movie (row based on movie_id primary key)
    if request.method == 'GET':
        #we render createreview.html and pass in the review form for the user to create the review:
        return render(request, 'createreview.html', {'form': ReviewForm(), 'movie':movie})
    else:
        try:
            #form accepts all data subitted to ReviewFrom present in createreview.html
            form = ReviewForm(request.POST)
            #We create and save a new review object from the form's values but do not yet put it into the database (commit=False) because we want to specify the user and movie relationships for the review:
            newReview = form.save(commit=False)
            newReview.user = request.user
            newReview.movie = movie
            newReview.save()
            return redirect('detail', newReview.movie.id)
        except:
            return render(request, 'createreview.html', {'form': ReviewForm(), 
                                                         'error':'Bad data passed in the form.'})

@login_required
def updatereview(request, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    if request.method == 'GET':
        form = ReviewForm(instance=review)
        return render(request, 'updatereview.html', {'review':review, 'form':form})
    else:
        try:
            form = ReviewForm(request.POST, instance=review)
            form.save()
            return redirect('detail', review.movie.id)
        except ValueError:
            return render(request, 'updatereview.html', {'review':review ,'form': form, 
                                                         'error':'Bad data passed in the form.'})

@login_required
def deletereview(request, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    review.delete()
    return redirect('detail', review.movie.id)