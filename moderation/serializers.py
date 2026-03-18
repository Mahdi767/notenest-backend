
from rest_framework import serializers
from moderation.models import ModerationAction,ResourceReport



class ModerationActionSerializer(serializers.ModelSerializer):
    moderator = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = ModerationAction
        fields = "__all__"

class ResourceReportSerializer (serializers.ModelSerializer):
    reported_by = serializers.PrimaryKeyRelatedField(read_only=True)
    status = serializers.CharField(read_only=True)
    class Meta:
        model = ResourceReport
        fields = "__all__"
