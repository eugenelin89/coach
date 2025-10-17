from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import GamePlay
from .recommendations import generate_recommendation
from .serializers import (
    GamePlaySerializer,
    RecommendationRequestSerializer,
    RecommendationResponseSerializer,
)


class GamePlayViewSet(viewsets.ModelViewSet):
    """CRUD interface for stored play history."""

    queryset = GamePlay.objects.all().order_by('-created_at')
    serializer_class = GamePlaySerializer


class RecommendationView(APIView):
    """Generate the next play recommendation based on the current game state."""

    def post(self, request, *args, **kwargs):
        request_serializer = RecommendationRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        validated = request_serializer.validated_data

        recommendation = generate_recommendation(validated)
        response_serializer = RecommendationResponseSerializer(recommendation)

        if validated.get('save_to_history', False):
            history_fields = {
                field: validated[field]
                for field in [
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
                ]
            }
            history_fields.update(
                {
                    'recommended_pitch': recommendation['pitch_call'],
                    'defensive_alignment': recommendation['defensive_alignment'],
                    'catcher_instructions': recommendation['catcher_plan'],
                    'offensive_sign': recommendation['offensive_signs'].get('hitter', ''),
                    'runner_instructions': recommendation['offensive_signs'].get('runner', ''),
                    'generated_from_engine': True,
                }
            )
            GamePlay.objects.create(**history_fields)

        return Response(response_serializer.data, status=status.HTTP_200_OK)
