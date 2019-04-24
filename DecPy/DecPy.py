import time
import sys
import json

from twisted.web.static import File
from klein import run, route
from Modules.APIModule import Api
from Models.ResponseModels import ErrorResponseModel


global api

# Api Route
@route('/', methods=['POST'])
def apiRoute(request):
    global api

    try:
        rawData = request.content.read()
        data = json.loads(rawData)
    except:
        return ErrorResponseModel("json error").toJSON()

    try:
        response = api.requestHandler(data, rawData)
    except Exception as e:
        print e
        return ErrorResponseModel("internal error").toJSON()

    return response

# Startup
if __name__ == '__main__':
    # Get IP and PORT from command line parameters
    if len(sys.argv) == 3:
        if sys.argv[1] != "" and sys.argv[2] != "":
            ip = sys.argv[1]
            port = int(sys.argv[2])

    # If not set use Default
    else:
        ip = "192.168.0.57"
        port = 6967

    #api = Api()
    #run(ip, port)                 # Init Api
