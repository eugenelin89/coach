from django import forms


class RecommendationForm(forms.Form):
    HALF_INNING_CHOICES = (
        ('top', 'Top'),
        ('bottom', 'Bottom'),
    )

    offense_team = forms.CharField(label='Offense Team', max_length=100)
    defense_team = forms.CharField(label='Defense Team', max_length=100)
    inning = forms.IntegerField(min_value=1, label='Inning')
    half_inning = forms.ChoiceField(choices=HALF_INNING_CHOICES, label='Half Inning')
    outs = forms.IntegerField(min_value=0, max_value=2, label='Outs')
    balls = forms.IntegerField(min_value=0, max_value=3, label='Balls')
    strikes = forms.IntegerField(min_value=0, max_value=2, label='Strikes')
    runners_on_first = forms.BooleanField(required=False, label='Runner on First')
    runners_on_second = forms.BooleanField(required=False, label='Runner on Second')
    runners_on_third = forms.BooleanField(required=False, label='Runner on Third')
    score_difference = forms.IntegerField(
        label='Score Difference',
        help_text='Offense score minus defense score.',
    )
    context_notes = forms.CharField(
        required=False,
        label='Context Notes',
        widget=forms.Textarea(attrs={'rows': 3}),
    )
    save_to_history = forms.BooleanField(
        required=False,
        label='Save this recommendation to the play history',
    )
