## quotes/views.py
## description: write view functions to handle URL requests fro the quotes app

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import random
import time

QUOTES = [
    "If I am a child, you know what that makes you?",
    "It insists upon itself. [Referencing the Godfather]",
    "I Have An Idea So Smart That My Head Would Explode If I Even Began To Know What I Was Talking About.",
    "Bird Is The Word.",
    "I May Be An Idiot, But There's One Thing I'm Not Sir, And That Is An Idiot.",
    "Whoa, Whoa... Lois, This Is Not My Batman Glass.",
    "I Swear To God I Thought Dogs Could Breathe Underwater.",
    "I Don't Know What I'm Doin' Here. I Was Just Lookin' For The Can.",
    "I find this meat loaf…shallow and pedantic.",
    "Kerosene is fuel Brian, Red Bull is fuel, kerosene is Red Bull, and won't you leave me alone when I'm doing my important work."
]

IMAGES = [
    "https://static1.srcdn.com/wordpress/wp-content/uploads/peter-griffin-family-guy.jpg",
    "https://m.media-amazon.com/images/M/MV5BZmY5N2ZhNWMtMzEzZC00NmRlLTg5YWEtZmQwMGNiZWIxMzA5XkEyXkFqcGdeQXVyMjYwNDA2MDE@._V1_.jpg",
    "https://i.ytimg.com/vi/n9eHtXAHInA/maxresdefault.jpg",
    "https://imgix.ranker.com/list_img_v2/9086/2469086/original/2469086-u1?fit=crop&fm=pjpg&q=80&dpr=2&w=1200&h=720",
    "https://img.buzzfeed.com/buzzfeed-static/static/2015-09/25/16/campaign_images/webdr10/buttscratchaaaaaaa-2-18467-1443213056-7_dblbig.jpg?resize=1200:*",
    "https://cdn.shopify.com/s/files/1/1140/8354/files/Photo_of_Peter_Griffin_480x480.jpg?v=1682610602"

]

# Create your views here.
# def main(request):
#     '''Handle the main URL for the quotes app'''

#     response_text = '''
#     '''

#     HttpResponse(response_text)

def quote(request):
    '''
    Function to handle the URL request for /quote (main page).
    Delegate rendering to the template hw/quote.html.
    '''
    # Render the response
    template_name = 'quotes/quote.html'

    quote = random.choice(QUOTES)
    image = random.choice(IMAGES)

    context = {
        'current_time' : time.ctime(),
        'quote': quote,
        'image': image
    }

    # Delegate rendering work to the template
    return render(request, template_name, context)

def show_all(request):
    '''
    Function to handle the URL request for /show_all (main page).
    Delegate rendering to the template hw/show_all.html.
    '''
    # Render the response
    template_name = 'quotes/show_all.html'

    context = {
        "current_time" : time.ctime(),
        'quotes': QUOTES,
        'images': IMAGES
    }

    # Delegate rendering work to the template
    return render(request, template_name, context)

def about(request):
    '''
    Function to handle the URL request for /about (main page).
    Delegate rendering to the template hw/about.html.
    '''
    # Render the response
    template_name = 'quotes/about.html'

    context = {
        "current_time" : time.ctime()
    }

    # Delegate rendering work to the template
    return render(request, template_name, context)