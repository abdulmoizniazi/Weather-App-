from django.shortcuts import render
from django.http import HttpResponse
import requests
import datetime

def index(request):
    # Check if the form was submitted via POST
    if request.method == 'POST':
        city = request.POST.get('city', 'Buenos Aires')
    else:
        # For GET requests or first load
        city = request.GET.get('city', 'Buenos Aires')

    # Default image in case the search fails
    image_url = "https://images.pexels.com/photos/3008509/pexels-photo-3008509.jpeg"
    exception_occurred = False
    
    # First get weather data
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=6b9ef98eade20278e6a44dad6cf0b703'
    PARAMS = {'units': 'metric'}
    
    try:
        response = requests.get(url, params=PARAMS)
        weather_data = response.json()

        if response.status_code == 200:
            description = weather_data['weather'][0]['description']
            icon = weather_data['weather'][0]['icon']
            temp = weather_data['main']['temp']
        else:
            description, icon, temp = "N/A", "N/A", "N/A"
            exception_occurred = True
    except:
        description, icon, temp = "N/A", "N/A", "N/A"
        exception_occurred = True

    # Then try to get the background image
    try:
        API_KEY = "AIzaSyB18c9PvA-lVZzGPnYzWggE5qZHX_0azTU"
        SEARCH_ENGINE_ID = "e61994b897c20431a"
        query = city + " 1920x1080"  # Fixed spacing in the query
        page = 1
        start = (page - 1) * 10 + 1
        searchType = 'image'
        city_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"
        
        image_response = requests.get(city_url)
        image_data = image_response.json()
        
        if "items" in image_data and len(image_data["items"]) > 1:
            image_url = image_data["items"][1]['link']
    except Exception as e:
        # Keep the default image URL if there's an error
        print(f"Error fetching image: {e}")
        # No need to change image_url as we already set a default

    day = datetime.date.today()

    return render(request, 'weather_app/index.html', {
        'description': description,
        'icon': icon,
        'temp': temp,
        'day': day, 
        'city': city,
        'exception_occurred': exception_occurred,
        'image_url': image_url,
    })