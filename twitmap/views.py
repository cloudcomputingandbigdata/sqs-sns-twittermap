from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import requests
from data_process import *

# Create your views here.
def index(request):
    return render(request, 'twittermap/index.html')

def getkeywords(request):
    ss = SearchServices()
    keywords = ss.keywords
    list = []
    for k in keywords:
        pair = {
            "name": k,
            "value": k
        }
        list.append(pair)

    output = {
        "success": True,
        "results": list
    }
    return JsonResponse(output)
    
def search_by_keyword(request, keyword = ''):
    if keyword == '':
        return HttpResponse("Please specify the keyword!")
    services = SearchServices()
    from_time = request.GET.get("from")
    to_time = request.GET.get("to")
    lat = request.GET.get("lat")
    lon = request.GET.get("lon")
    distance = request.GET.get("distance") # the format for "distance" should be in human-readable form, such as "2km"
    output = services.search_scroll(keyword, from_time, to_time, lat, lon, distance)
    return JsonResponse(output)

def scroll_results(request, sid):
    #scroll_id = request.GET.get('scroll_id', '')
    if sid == '':
        return HttpResponse("Please specify the scroll_id!")
    services = SearchServices()
    output = services.scroll_results(sid)
    return JsonResponse(output)

def test_search(request, keyword = ''):
    if keyword == '':
        return HttpResponse("Please specify the keyword!")
    services = SearchServices()
    from_time = request.GET.get("from")
    to_time = request.GET.get("to")
    output = services.get_results_by_keyword(keyword, from_time, to_time)
    return JsonResponse(output)

@csrf_exempt
def process_tweet(request):
    type = request.META.get('HTTP_X_AMZ_SNS_MESSAGE_TYPE')
    if type == 'SubscriptionConfirmation':
        received_json_data = json.loads(request.body)
        url = received_json_data['SubscribeURL']

        response = requests.get(url)
        return HttpResponse(response)
    elif type == 'Notification':
        received_json_data = json.loads(request.body)
        id = received_json_data['MessageId']
        message = received_json_data['Message']

        data_process = DataProcess()
        data_process.process(message)

        return HttpResponse(message)
    else:
        return HttpResponse('haha')

