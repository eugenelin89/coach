from django.contrib import admin

from .models import GamePlay


@admin.register(GamePlay)
class GamePlayAdmin(admin.ModelAdmin):
    list_display = (
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
        'generated_from_engine',
        'created_at',
    )
    list_filter = (
        'half_inning',
        'outs',
        'runners_on_first',
        'runners_on_second',
        'runners_on_third',
        'generated_from_engine',
        'created_at',
    )
    search_fields = (
        'offense_team',
        'defense_team',
        'context_notes',
        'catcher_instructions',
        'offensive_sign',
        'runner_instructions',
    )
