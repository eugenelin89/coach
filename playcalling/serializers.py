from rest_framework import serializers

from .models import GamePlay


class GamePlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = GamePlay
        fields = [
            'id',
            'offense_team',
            'defense_team',
            'inning',
            'half_inning',
            'outs',
            'balls',
            'strikes',
            'runners_on_first',
            'runners_on_second',
            'runners_on_third',
            'score_difference',
            'context_notes',
            'recommended_pitch',
            'defensive_alignment',
            'catcher_instructions',
            'offensive_sign',
            'runner_instructions',
            'actual_outcome',
            'generated_from_engine',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'generated_from_engine',
            'created_at',
            'updated_at',
        ]


class RecommendationRequestSerializer(serializers.Serializer):
    offense_team = serializers.CharField(max_length=128)
    defense_team = serializers.CharField(max_length=128)
    inning = serializers.IntegerField(min_value=1)
    half_inning = serializers.ChoiceField(choices=[('top', 'top'), ('bottom', 'bottom')])
    outs = serializers.IntegerField(min_value=0, max_value=2)
    balls = serializers.IntegerField(min_value=0, max_value=3)
    strikes = serializers.IntegerField(min_value=0, max_value=2)
    runners_on_first = serializers.BooleanField(default=False)
    runners_on_second = serializers.BooleanField(default=False)
    runners_on_third = serializers.BooleanField(default=False)
    score_difference = serializers.IntegerField()
    context_notes = serializers.CharField(required=False, allow_blank=True)
    save_to_history = serializers.BooleanField(default=False)


class RecommendationResponseSerializer(serializers.Serializer):
    pitch_call = serializers.CharField()
    catcher_plan = serializers.CharField()
    defensive_alignment = serializers.DictField(child=serializers.CharField())
    offensive_signs = serializers.DictField(child=serializers.CharField())
    key_points = serializers.ListField(child=serializers.CharField())
