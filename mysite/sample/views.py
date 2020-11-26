from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from sample.control import QcControl
import traceback
from django.views.decorators.clickjacking import xframe_options_exempt
from django.template import RequestContext, loader
import json

user_control = {}


# allow post from other site
@csrf_exempt
# allow embedded into iframe
@xframe_options_exempt
def index(request):
    try:
        qc = get_qc(request)
        if not qc:
            return HttpResponse("not autherized")
        user = qc.get_user_info()
        if not user:
            return HttpResponse("not autherized")
        user_control[user["user_id"]] = qc
        template = loader.get_template('index.html')
        context = RequestContext(
            request,
            {
                'username': user['user_name'],
                'user_id': user['user_id'],
                'notify_email': user['email'],
            }
        )
        return HttpResponse(template.render(context))
    except Exception as e:
        print(e.message)
        exstr = traceback.format_exc()
        print(exstr)
        return HttpResponse(exstr)


# allow post from other site
@csrf_exempt
def service(request):
    try:
        user_id = request.POST["user_id"]
        action = request.POST["action"]
        params = request.POST
        qc = user_control[user_id]
        if action in qc.handle_map:
            response = qc.handle_map[action](**params)
            return HttpResponse(json.dumps(response))
        else:
            return HttpResponse("not supported action %s" % action)

    except Exception:
        exstr = traceback.format_exc()
        print exstr
        return HttpResponse(exstr)


def get_qc(request):
    if "code" not in request.GET:
        print("not authorized")
        return None
    token = request.GET["code"]
    return QcControl(token)
