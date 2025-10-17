from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class GamePlay(models.Model):
    """Represents a recorded play context and associated strategic calls."""

    HALF_INNING_CHOICES = [
        ('top', 'Top'),
        ('bottom', 'Bottom'),
    ]

    offense_team = models.CharField(max_length=128)
    defense_team = models.CharField(max_length=128)
    inning = models.PositiveSmallIntegerField(default=1)
    half_inning = models.CharField(max_length=6, choices=HALF_INNING_CHOICES, default='top')
    outs = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(2)],
        help_text='Number of outs before the play.',
    )
    balls = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)],
        help_text='Ball count before the play.',
    )
    strikes = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(2)],
        help_text='Strike count before the play.',
    )
    runners_on_first = models.BooleanField(default=False)
    runners_on_second = models.BooleanField(default=False)
    runners_on_third = models.BooleanField(default=False)
    score_difference = models.IntegerField(
        default=0,
        help_text='Offense score minus defense score before the play.',
    )
    context_notes = models.TextField(blank=True)

    recommended_pitch = models.CharField(max_length=128, blank=True)
    defensive_alignment = models.JSONField(default=dict, blank=True)
    catcher_instructions = models.TextField(blank=True)
    offensive_sign = models.TextField(blank=True)
    runner_instructions = models.TextField(blank=True)
    actual_outcome = models.TextField(blank=True)

    generated_from_engine = models.BooleanField(
        default=False,
        help_text='True when this record was created from the recommendation engine.',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        base_state = ''.join([
            '1' if self.runners_on_first else '-',
            '2' if self.runners_on_second else '-',
            '3' if self.runners_on_third else '-',
        ]) or '---'
        return (
            f"{self.offense_team} vs {self.defense_team} | "
            f"{self.half_inning.title()} {self.inning} | Outs: {self.outs} | Bases: {base_state}"
        )
