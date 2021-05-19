from django.conf import settings
import redis
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
# Connect to our Redis instance
# redis_instance = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True,  db=0)
redis_instance = redis.Redis(host="localhost", port="6379", decode_responses=True,  db=0)


@api_view(['GET'])
def get_all_bhav(request, *args, **kwargs):
    if request.method == 'GET':
        items = {}
        count = 0
        for key in redis_instance.keys("*"):
            items[count+1] = json.loads(redis_instance.get(key))
            count += 1
        response = {
            'count': count,
            'msg': f"Found {count} items.",
            'items': items
        }
        return Response(response, status=200)

@api_view(['GET'])
def get_single_bhav(request, *args, **kwargs):
    if request.method == 'GET':
        if kwargs['key']:
            items = {}
            count = 0
            for key in redis_instance.keys("*" + kwargs['key'] + "*" ):
                items[count+1] = json.loads(redis_instance.get(key))
                count += 1
            response = {
                'count': count,
                'msg': f"Found {count} items.",
                'items': items
            }
            return Response(response, status=200)
