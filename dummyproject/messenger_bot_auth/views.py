import logging
import json

from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from messenger_bot_auth.models import Profile, CrowdtanglePreference
from requests import Request, Session

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

    print("MODE: ")
    print(mode)

    logger.debug(body_unicode)
    print(body_unicode)

    fb_user_id = extract_user_id(body)
    logger.debug(fb_user_id)
    print(fb_user_id)

    if fb_user_id:
        profile, is_created = Profile.objects.get_or_create(
            messenger_app_user_id=fb_user_id
        )

        # save text as Profile preference
        text = extract_text(body)
        if text:
            pref, is_created = CrowdtanglePreference.objects.get_or_create(
                search_preference=text,
                profile_id=profile.id
            )

            send_ack_to_user(fb_user_id)

    if mode == 'subscribe' and verify_token != settings.MESSENGER_BOT_VERIFY_TOKEN:
        raise HttpResponseForbidden('wrong verify token')

    return HttpResponse()


def extract_user_id(body):
    try:
        return body['entry'][0]['messaging'][0]['sender']['id']
    except KeyError:
        return None


def extract_text(body):
    try:
        return body['entry'][0]['messaging'][0]['message']['text']
    except KeyError:
        return None


def send_ack_to_user(user_id):
    payload = {
        "recipient": {"id": user_id},
        "message": {
            "text": "Got it!"
        }
    }
    payload = json.dumps(payload)
    headers = {'Content-type': 'application/json'}
    request = Request('POST', settings.FACEBOOK_MESSENGER_API_URL, data=payload, headers=headers)
    prepped_request = request.prepare()

    s = Session()
    s.send(prepped_request)
