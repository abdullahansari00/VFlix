from django.shortcuts import render, redirect
from .models import MoviesList, MoviesSuggestions
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.

def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        passw = request.POST.get('passw')
        vpass = request.POST.get('vpass')

        if passw == vpass:
            if len(User.objects.filter(username = uname)) == 0:
                if len(User.objects.filter(email = email)) == 0:
                    user = User.objects.create_user(username = uname, email = email, first_name = name, password = passw)
                    #ulist = User_List(name = name, user_name = uname, email = email, password = passw)
                    #ulist.save()

                    movie = MoviesSuggestions(username = uname)
                    movie.save()

                else:
                    error = "Email already exists"
                    return render(request, 'front/error.html', {'error' : error})
            else:
                error = "Username already exists"
                return render(request, 'front/error.html', {'error' : error})

            return redirect('enter')

        else:
            error = "Password didn't match"
            return render(request, 'front/error.html', {'error' : error})

#return render(request, 'back/login.html')

def enter(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        passw = request.POST.get('passw')

        user = authenticate(username = uname, password = passw)

        if user:
            login(request, user)
            return redirect('home')

        else:
            error = "Incorreect username or password"
            return render(request, 'front/error.html', {'error' : error})

    return render(request, 'front/login.html')

def exit(request):
    logout(request)
    return redirect('enter')

def changepassword(request):
    username = request.user.username
    if not request.user.is_authenticated :
        return redirect('enter')

    if request.method == 'POST':
        uname = request.POST.get('uname')
        opass = request.POST.get('opass')
        npass = request.POST.get('npass')

        user = authenticate(username = uname, password = opass)

        if user:
            user = User.objects.get(username = request.user)
            user.set_password(npass)
            user.save()
            #ulst = User_List.objects.get(user_name = uname)
            #ulst.password = npass
            #ulst.save()
            return redirect('enter')

        else:
            error = "Incorrect username or password"
            return render(request, 'front/error.html', {'error' : error})

    return render(request, 'front/changep.html',{'username' : username.capitalize()})


username = None

def home(request):
    if not request.user.is_authenticated :
        return redirect('enter')

    username = request.user.username
    movies = MoviesList.objects.all().order_by('rank').exclude(rank = 0)
    watched_movie = MoviesSuggestions.objects.get(username = username)
    watched = list(map(int, watched_movie.watched_movies.split(',')))

    return render(request, 'front/home.html', {'movies' : movies, 'watched' : watched, 'username' : username.capitalize()})

def watched_movies(request):
    if not request.user.is_authenticated :
        return redirect('enter')

    username = request.user.username
    watched_movie = MoviesSuggestions.objects.get(username = username)
    watched_movie = list(map(int, watched_movie.watched_movies.split(',')))
    movies = MoviesList.objects.filter(rank__in = watched_movie).exclude(rank = 0)

    return render(request, 'front/watched.html', {'movies' : movies, 'username' : username.capitalize()})
    
def suggested_movies(request):
    def genre_count(genre):
        count = 0

        if 'Action' in genre:
            count = count + watched_movie.action

        if 'Adventure' in genre:
            count = count + watched_movie.adventure

        if 'Sci-Fi' in genre:
            count = count + watched_movie.scifi

        if 'Mystery' in genre:
            count = count + watched_movie.mystery

        if 'Horror' in genre:
            count = count + watched_movie.horror

        if 'Thriller' in genre:
            count = count + watched_movie.thriller

        if 'Animation' in genre:
            count = count + watched_movie.animation

        if 'Comedy' in genre:
            count = count + watched_movie.comedy

        if 'Family' in genre:
            count = count + watched_movie.family

        if 'Fantasy' in genre:
            count = count + watched_movie.fantasy

        if 'Drama' in genre:
            count = count + watched_movie.drama

        if 'Music' in genre:
            count = count + watched_movie.music

        if 'Biography' in genre:
            count = count + watched_movie.biography

        if 'Romance' in genre:
            count = count + watched_movie.romance

        if 'History' in genre:
            count = count + watched_movie.history

        if 'Crime' in genre:
            count = count + watched_movie.crime

        if 'Western' in genre:
            count = count + watched_movie.western

        if 'War' in genre:
            count = count + watched_movie.war

        if 'Musical' in genre:
            count = count + watched_movie.musical

        if 'Sport' in genre:
            count = count + watched_movie.sport

        return count

    username = request.user.username
    watched_movie = MoviesSuggestions.objects.get(username = username)
    watched_movie_list = list(map(int, watched_movie.watched_movies.split(',')))
    movies = MoviesList.objects.all().exclude(rank__in = watched_movie_list)
    movies_list = [[] for x in range(len(movies))]
    
    c = 0
    for x in movies:
        movies_list[c].append(genre_count(x.genre))
        movies_list[c].append(x.rank)
        movies_list[c].append(x.title)
        movies_list[c].append(x.genre)
        movies_list[c].append(x.description)
        movies_list[c].append(x.director)
        movies_list[c].append(x.actors)
        movies_list[c].append(x.year)
        movies_list[c].append(x.rating)
        c = c+1

    movies_list = sorted(sorted(movies_list, key = lambda x : x[1]), key = lambda x : x[0], reverse = True)

    return render(request, 'front/suggestions.html', {'movies' : movies_list, 'username' : username.capitalize()})

def search(request):
    if not request.user.is_authenticated :
        return redirect('enter')

    search = request.POST.get('search')
    username = request.user.username
    movies = MoviesList.objects.filter(title__contains = search).exclude(rank = 0)
    watched_movie = MoviesSuggestions.objects.get(username = username)
    watched = list(map(int, watched_movie.watched_movies.split(',')))

    return render(request, 'front/search.html', {'movies' : movies, 'watched' : watched, 'username' : username.capitalize()})

def add_movie(request, rank, var):
    if not request.user.is_authenticated :
        return redirect('enter')

    add_movie = MoviesSuggestions.objects.get(username = request.user.username)
    add_movie.watched_movies = add_movie.watched_movies+', '+str(rank)

    movie = MoviesList.objects.get(rank = rank)

    movie_genre = movie.genre

    if 'Action' in movie_genre:
    	add_movie.action = add_movie.action + 1

    if 'Adventure' in movie_genre:
    	add_movie.adventure = add_movie.adventure + 1

    if 'Sci-Fi' in movie_genre:
    	add_movie.scifi = add_movie.scifi + 1

    if 'Mystery' in movie_genre:
    	add_movie.mystery = add_movie.mystery + 1

    if 'Horror' in movie_genre:
    	add_movie.horror = add_movie.horror + 1

    if 'Thriller' in movie_genre:
    	add_movie.thriller = add_movie.thriller + 1

    if 'Animation' in movie_genre:
    	add_movie.animation = add_movie.animation + 1

    if 'Comedy' in movie_genre:
    	add_movie.comedy = add_movie.comedy + 1

    if 'Family' in movie_genre:
    	add_movie.family = add_movie.family + 1

    if 'Fantasy' in movie_genre:
    	add_movie.fantasy = add_movie.fantasy + 1

    if 'Drama' in movie_genre:
    	add_movie.drama = add_movie.drama + 1

    if 'Music' in movie_genre:
    	add_movie.music = add_movie.music + 1

    if 'Biography' in movie_genre:
    	add_movie.biography = add_movie.biography + 1

    if 'Romance' in movie_genre:
    	add_movie.romance = add_movie.romance + 1

    if 'History' in movie_genre:
    	add_movie.history = add_movie.history + 1

    if 'Crime' in movie_genre:
    	add_movie.crime = add_movie.crime + 1

    if 'Western' in movie_genre:
    	add_movie.western = add_movie.western + 1

    if 'War' in movie_genre:
    	add_movie.war = add_movie.war + 1

    if 'Musical' in movie_genre:
    	add_movie.musical = add_movie.musical + 1

    if 'Sport' in movie_genre:
    	add_movie.sport = add_movie.sport + 1
    
    add_movie.save()

    if int(var) == 0:
        return redirect('home')
    else:
        return redirect('suggested_movies')

def del_movie(request, rank, var):
    if not request.user.is_authenticated :
        return redirect('enter')

    del_movie = MoviesSuggestions.objects.get(username = request.user.username)
    del_movie_l = list(map(int, del_movie.watched_movies.split(',')))
    del_movie_l.remove(int(rank))

    if len(del_movie_l) == 0:
    	del_movie_l = [0]
    del_movie_l = sorted(del_movie_l)
    result = ', '.join(map(str, del_movie_l))
    del_movie.watched_movies = result

    movie = MoviesList.objects.get(rank = rank)
    
    movie_genre = movie.genre

    if 'Action' in movie_genre:
    	del_movie.action = del_movie.action - 1

    if 'Adventure' in movie_genre:
    	del_movie.adventure = del_movie.adventure - 1

    if 'Sci-Fi' in movie_genre:
    	del_movie.scifi = del_movie.scifi - 1

    if 'Mystery' in movie_genre:
    	del_movie.mystery = del_movie.mystery - 1

    if 'Horror' in movie_genre:
    	del_movie.horror = del_movie.horror - 1

    if 'Thriller' in movie_genre:
    	del_movie.thriller = del_movie.thriller - 1

    if 'Animation' in movie_genre:
    	del_movie.animation = del_movie.animation - 1

    if 'Comedy' in movie_genre:
    	del_movie.comedy = del_movie.comedy - 1

    if 'Family' in movie_genre:
    	del_movie.family = del_movie.family - 1

    if 'Fantasy' in movie_genre:
    	del_movie.fantasy = del_movie.fantasy - 1

    if 'Drama' in movie_genre:
    	del_movie.drama = del_movie.drama - 1

    if 'Music' in movie_genre:
    	del_movie.music = del_movie.music - 1

    if 'Biography' in movie_genre:
    	del_movie.biography = del_movie.biography - 1

    if 'Romance' in movie_genre:
    	del_movie.romance = del_movie.romance - 1

    if 'History' in movie_genre:
    	del_movie.history = del_movie.history - 1

    if 'Crime' in movie_genre:
    	del_movie.crime = del_movie.crime - 1

    if 'Western' in movie_genre:
    	del_movie.western = del_movie.western - 1

    if 'War' in movie_genre:
    	del_movie.war = del_movie.war - 1

    if 'Musical' in movie_genre:
    	del_movie.musical = del_movie.musical - 1

    if 'Sport' in movie_genre:
    	del_movie.sport = del_movie.sport - 1
    
    del_movie.save()

    if int(var) == 0:
        return redirect('home')
    else:
        return redirect('watched_movies')

'''def movies(request):
	return render(request, 'front/upload_movies.html')

def upload_movies(request):
	if request.method == 'POST':
		mlist = request.FILES['mlist']
		data = mlist.read().decode("utf-8")
		lines = data.split("\n")
		for x in lines:
			movie = x.split(",")
			try:
				print(movie)
				rank = movie[0]
				title = movie[1]
				genre = movie[2].replace("/",", ")
				description = movie[3].replace("/",",")
				director = movie[4].replace("/",",")
				actors = movie[5].replace("/",",")
				year = movie[6]
				rating = movie[7]
				#print(rank, title, genre, description, director, actors, year, rating)
				lis = MoviesList(rank = rank, title = title, genre = genre, description = description, director = director, 
				actors = actors, year = year, rating = rating)
				#lis.save()
			except:
				print("haha")

		return redirect('movies')'''