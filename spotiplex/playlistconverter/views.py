from django.shortcuts import render
from . import splex
# Create your views here.


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # This exempts the view from CSRF protection for demonstration purposes. In production, handle CSRF properly.



def convert(request):
    # For demonstration, fetching data. You'd replace this with your Python code.
    plexApiKey = request.POST.get('plexApiKey', '') 
    plexServerUrl = request.POST.get('plexServerUrl', '')
    spotifyApiKey = request.POST.get('spotifyApiKey', '')
    spotifyApiId = request.POST.get('spotifyApiId', '')
    lidarrUrl = request.POST.get('lidarrUrl', '')
    lidarrKey = request.POST.get('lidarrKey', '')
    plexipy = splex.connect_plex(plexServerUrl,plexApiKey)
    spotip = splex.connect_spotify(spotifyApiId,spotifyApiKey)
    #lidapy = splex.make_lidarr_api_call(lidarrUrl,lidarrKey)

    plextracks, dataList2 = splex.get_spotify_playlist_tracks(spotip,plexipy,"37i9dQZF1E39IiYmV2BQyD")
    
    dataList1 = splex.serializeplextracks(plextracks)
    
    return JsonResponse({"dataList1": dataList1, "dataList2": dataList2})


def homepage(request):
    return render(request, 'playlistconverter/index.html')
