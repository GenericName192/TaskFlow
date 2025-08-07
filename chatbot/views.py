from django.contrib.auth.decorators import login_required
from utility.constants import LOGIN_URL_NAME
import json
from django.http import HttpResponseNotAllowed, JsonResponse
from .chatbot_tools import chatbot_controller


@login_required(login_url=LOGIN_URL_NAME)
def chat_bot_view(request):
    reply = {}
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_id = data["user"]
            conversation = data["conversation"]
            reply["response"] = chatbot_controller(user_id, conversation)
        except json.JSONDecodeError as e:
            reply["response"] = "something has gone wrong: " + str(e)
        except KeyError as e:
            reply["response"] = "something has gone wrong: " + str(e)
        except Exception as e:
            reply["response"] = "something has gone wrong: " + str(e)
        return JsonResponse(reply)
    else:
        return HttpResponseNotAllowed(['POST'])
