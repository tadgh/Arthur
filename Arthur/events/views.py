import logging

from django.db.models import Count
from django.shortcuts import render

# Create your views here.
from rest_framework import status, generics
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from django.conf import settings
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from events.filters import LeaderboardFilter
from events.messagehandler import handle_event, parse_define_command, handle_explain, handle_define
from events.models import Team, HotWord, Utterance, SlackMessage
from events.serializers import TeamSerializer, HotWordSerializer, UtteranceSerializer, LeaderboardSerializer


SLACK_SIGNING_SECRET = getattr(settings, 'SLACK_SIGNING_SECRET', None)

logger = logging.getLogger(__name__)

class Teams(generics.ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class HotWords(ReadOnlyModelViewSet):
    queryset = HotWord.objects.all()
    serializer_class = HotWordSerializer

    @action(methods=['post'], detail=False)
    def explain(self, request, *args, **kwargs):
        slash_payload = request.data
        return handle_explain(slash_payload)

    @action(methods=['post'], detail=False)
    def define(self, request, *args, **kwargs):
        slash_payload = request.data
        print(request.data)
        return handle_define(slash_payload)

class Utterances(generics.ListAPIView):
    queryset = Utterance.objects.all()
    serializer_class = UtteranceSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

class Leaderboard(ModelViewSet):
    queryset = Utterance.objects.all().values('utterer').annotate(total=Count('utterer')).order_by('total')
    filterset_class = LeaderboardFilter
    serializer_class = LeaderboardSerializer

    @action(detail=False, methods=['post'])
    def slash(self, request, *args, **kwargs):
        leaderboard_message = self._respond_with_leaderboard(request)
        return Response(data={"response_type":"ephemeral", "text": leaderboard_message}, status=status.HTTP_200_OK)

    def _respond_with_leaderboard(self, request):
        for q in self.get_queryset():
            print(q)
        return "\n".join(f"<@{buzztotal['utterer']}> : {buzztotal['total']}" for buzztotal in self.get_queryset())


class Events(APIView):
    def post(self, request, *args, **kwargs):
        slack_message = request.data
        if slack_message.get("token") != SLACK_SIGNING_SECRET:
            return Response(status=status.HTTP_403_FORBIDDEN)

        if slack_message.get("type") == "url_verification":
            return Response(data=slack_message, status=status.HTTP_200_OK)

        if "event" in slack_message:
            handle_event(slack_message.get("event"))

        return Response(status=status.HTTP_200_OK)






