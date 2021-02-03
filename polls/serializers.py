from rest_framework import serializers

class PollsSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    start = serializers.IntegerField()
    end = serializers.IntegerField()