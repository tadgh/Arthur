from rest_framework import serializers

from events.models import Team, Utterance


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = "__all__"


class HotWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = "__all__"

class UtteranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utterance
        read_only_fields = "__all__"

class LeaderboardSerializer(serializers.Serializer):
    utterer = serializers.CharField()
    total = serializers.IntegerField()

