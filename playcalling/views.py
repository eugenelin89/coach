from django.views.generic import TemplateView
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import RecommendationForm
from .models import GamePlay
from .recommendations import generate_recommendation
from .serializers import (
    GamePlaySerializer,
    RecommendationRequestSerializer,
    RecommendationResponseSerializer,
)


def _persist_history(validated_request, recommendation):
    history_fields = {
        'offense_team': validated_request['offense_team'],
        'defense_team': validated_request['defense_team'],
        'inning': validated_request['inning'],
        'half_inning': validated_request['half_inning'],
        'outs': validated_request['outs'],
        'balls': validated_request['balls'],
        'strikes': validated_request['strikes'],
        'runners_on_first': validated_request['runners_on_first'],
        'runners_on_second': validated_request['runners_on_second'],
        'runners_on_third': validated_request['runners_on_third'],
        'score_difference': validated_request['score_difference'],
        'context_notes': validated_request.get('context_notes', ''),
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
            _persist_history(validated, recommendation)

        return Response(response_serializer.data, status=status.HTTP_200_OK)


class RecommendationDashboardView(TemplateView):
    template_name = 'playcalling/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault('form', RecommendationForm())
        context.setdefault('recommendation', None)
        context.setdefault('history_created', False)
        return context

    def post(self, request, *args, **kwargs):
        form = RecommendationForm(request.POST)
        recommendation_data = None
        history_created = False

        if form.is_valid():
            serializer = RecommendationRequestSerializer(data=form.cleaned_data)
            if serializer.is_valid():
                validated = serializer.validated_data
                recommendation = generate_recommendation(validated)
                recommendation_data = RecommendationResponseSerializer(recommendation).data

                if validated.get('save_to_history'):
                    _persist_history(validated, recommendation)
                    history_created = True
            else:
                for field, errors in serializer.errors.items():
                    for error in errors:
                        if field in form.fields:
                            form.add_error(field, error)
                        else:
                            form.add_error(None, error)

        context = self.get_context_data(
            form=form,
            recommendation=recommendation_data,
            history_created=history_created,
        )
        return self.render_to_response(context)
