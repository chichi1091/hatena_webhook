#-*- coding:utf-8 -*-
import os
import logging

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

logger = logging.getLogger(__name__)

class BookmarkView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        required_keys = ["key", "username", "title", "status", "timestamp"]
        for required_key in required_keys:
            if not request.data.get(required_key) or request.data.get(required_key) is None:
                return Response(HTTP_400_BAD_REQUEST, "request parameter not found. {}".format(required_key))

        key = request.data.get("key")
        if key != os.environ['HATENA_KEY']:
            return Response(HTTP_400_BAD_REQUEST, "hatena key bad.")

        username = request.data.get("username")
        title = request.data.get("title")
        timestamp = request.data.get("timestamp")
        status = request.data.get("status")

        if status == "add":
            logger.info("{0} {1}さんが {2} をブックマークしました".format(timestamp, username, title))
        elif status == "update":
            logger.info("[{0}] {1}さんが {2} をブックマークを更新しました".format(timestamp, username, title))
        elif status == "delete":
            logger.info("[{0}] {1}さんが {2} をブックマークを削除しました".format(timestamp, username, title))
        else:
            return Response(HTTP_400_BAD_REQUEST, "status parameter bad. {}".format(status))

        return Response(HTTP_200_OK)
