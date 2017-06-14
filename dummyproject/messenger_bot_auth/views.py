import logging
import json

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

logger = logging.getLogger('messenger_auth_bot')


def index(request):
    return JsonResponse({'success': True})


@csrf_exempt
def webhook(request):

    mode = request.GET.get('hub.mode')
    challenge = request.GET.get('hub.challenge')
    verify_token = request.GET.get('hub.verify_token')

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    logger.debug(body_unicode)
    print(body_unicode)

    if mode == 'subscribe' and verify_token != settings.MESSENGER_BOT_VERIFY_TOKEN:
        raise HttpResponseForbidden('wrong verify token')

    return HttpResponse()
