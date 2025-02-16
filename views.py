from django.shortcuts import render

from django.http import JsonResponse
from django.utils.timezone import now


def whoami(request):
    client_ip = get_client_ip(request)

    client_browser = request.META.get('HTTP_USER_AGENT', 'Unknown')

    current_time = now()

    return JsonResponse({
        'browser': client_browser,
        'ip': client_ip,
        'server_time': current_time.strftime('%Y-%m-%d %H:%M:%S'),
    })


def get_client_ip(request):

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip