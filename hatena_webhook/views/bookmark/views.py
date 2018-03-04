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
            if not request.data.has_key(required_key):
                return Response(HTTP_400_BAD_REQUEST, "request parameter not found. {}".format(required_key))

        key = request.data["key"].value
        if key != os.environ['HATENA_KEY']:
            return Response(HTTP_400_BAD_REQUEST, "hatena key bad.")

        username = request.data["username"].value
        title = request.data["title"].value
        timestamp = request.data["timestamp"].value
        status = request.data["status"].value

        if status == "add":
            logger.info("[%s] %sさんが %s をブックマークしました".format(timestamp, username, title))
        elif status == "update":
            logger.info("[%s] %sさんが %s をブックマークを更新しました".format(timestamp, username, title))
        elif status == "delete":
            logger.info("[%s] %sさんが %s をブックマークを削除しました".format(timestamp, username, title))
        else:
            return Response(HTTP_400_BAD_REQUEST, "status parameter bad. {}".format(status))

        return Response(HTTP_200_OK)
