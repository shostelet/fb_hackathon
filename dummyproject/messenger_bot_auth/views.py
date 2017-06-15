import logging
import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

# from messenger_bot_auth.models import Profile
from messenger_bot_auth.models import CrowdtanglePreference

from requests import Request, Session

logger = logging.getLogger('messenger_auth_bot')


def index(request):
    context = {}
    return render(request, 'homepage/index.html', context)


@csrf_exempt
def webhook(request):

    mode = request.GET.get('hub.mode')
    challenge = request.GET.get('hub.challenge')
    verify_token = request.GET.get('hub.verify_token')

    if challenge and mode == 'subscribe' and verify_token == settings.MESSENGER_BOT_VERIFY_TOKEN:
        return HttpResponse(challenge)

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    # print("MODE: ")
    # print(mode)

    # logger.debug(body_unicode)
    # print(body_unicode)

    fb_user_id = extract_user_id(body)
    # logger.debug(fb_user_id)
    # print(fb_user_id)

    if fb_user_id:
        # profile, is_created = Profile.objects.get_or_create(
        #     messenger_app_user_id=fb_user_id
        # )

        # save text as Profile preference
        text = extract_text(body)
        if text:

            text = text.lower()
            if text == 'help':
                message = "Commands available: " \
                          "\nhelp" \
                          "\nlist" \
                          "\ndelete <keyword>"
                send_message_to_user(fb_user_id, message)
            elif text == 'list':
                prefs = CrowdtanglePreference.objects.filter(
                    user_bot_id=fb_user_id
                ).values_list('search_preference', flat=True)

                if prefs:
                    message = 'Your keywords: {}'.format(', '.join(prefs))
                else:
                    message = 'You have no keywords yet!'
                send_message_to_user(fb_user_id, message)

            elif text == "get user_id":
                send_message_to_user(fb_user_id, str(fb_user_id))
            elif text.startswith("delete"):
                # Delete command
                text = text.replace("delete ", "")

                query = CrowdtanglePreference.objects.filter(
                    search_preference__iexact=text,
                    user_bot_id=fb_user_id
                )

                if query.count():
                    query.delete()
                    send_message_to_user(fb_user_id, 'Keyword deleted!')
                else:
                    send_message_to_user(fb_user_id, 'Keyword not found!')
            else:
                pref, is_created = CrowdtanglePreference.objects.get_or_create(
                    search_preference=text,
                    user_bot_id=fb_user_id
                )

                send_message_to_user(fb_user_id, 'Keyword added!')

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


def send_message_to_user(user_id, message):
    payload = {
        "recipient": {"id": user_id},
        "message": {
            "text": message
        }
    }
    payload = json.dumps(payload)
    headers = {'Content-type': 'application/json'}
    request = Request('POST', settings.FACEBOOK_MESSENGER_API_URL, data=payload, headers=headers)
    prepped_request = request.prepare()

    s = Session()
    s.send(prepped_request)
