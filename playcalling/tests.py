from django.test import SimpleTestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import GamePlay
from .recommendations import generate_recommendation


class RecommendationEngineTests(SimpleTestCase):
    def test_first_and_third_two_out_tie_game(self):
        context = {
            'offense_team': 'Visitors',
            'defense_team': 'Home',
            'inning': 7,
            'half_inning': 'top',
            'outs': 2,
            'balls': 1,
            'strikes': 1,
            'runners_on_first': True,
            'runners_on_second': False,
            'runners_on_third': True,
            'score_difference': 0,
            'context_notes': '',
        }

        recommendation = generate_recommendation(context)

        self.assertIn('four-seam fastball up', recommendation['pitch_call'].lower())
        self.assertIn('throw through to second', recommendation['catcher_plan'].lower())
        self.assertIn('first-and-third offense', ' '.join(recommendation['key_points']).lower())

    def test_full_count_free_pass_prevention(self):
        context = {
            'offense_team': 'Visitors',
            'defense_team': 'Home',
            'inning': 5,
            'half_inning': 'bottom',
            'outs': 1,
            'balls': 3,
            'strikes': 2,
            'runners_on_first': False,
            'runners_on_second': False,
            'runners_on_third': False,
            'score_difference': -1,
            'context_notes': '',
        }

        recommendation = generate_recommendation(context)

        self.assertIn('challenge four-seam fastball', recommendation['pitch_call'].lower())
        self.assertEqual(
            'take all the way until a strike is thrown.',
            recommendation['offensive_signs']['hitter'].lower(),
        )


class RecommendationApiTests(APITestCase):
    def setUp(self):
        self.payload = {
            'offense_team': 'Visitors',
            'defense_team': 'Home',
            'inning': 3,
            'half_inning': 'top',
            'outs': 1,
            'balls': 2,
            'strikes': 1,
            'runners_on_first': True,
            'runners_on_second': False,
            'runners_on_third': False,
            'score_difference': 1,
            'context_notes': 'Early game situation.',
        }

    def test_recommendation_endpoint_returns_plan(self):
        url = reverse('recommendation')
        response = self.client.post(url, data=self.payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key in ['pitch_call', 'catcher_plan', 'defensive_alignment', 'offensive_signs', 'key_points']:
            self.assertIn(key, response.data)

    def test_recommendation_can_persist_history(self):
        url = reverse('recommendation')
        payload = {**self.payload, 'save_to_history': True}

        response = self.client.post(url, data=payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(GamePlay.objects.count(), 1)
        play = GamePlay.objects.first()
        self.assertTrue(play.generated_from_engine)
        self.assertTrue(play.offensive_sign)
        self.assertTrue(play.runner_instructions)


class GamePlayViewSetTests(APITestCase):
    def test_list_endpoint_returns_saved_history(self):
        GamePlay.objects.create(
            offense_team='Visitors',
            defense_team='Home',
            inning=4,
            half_inning='bottom',
            outs=2,
            balls=0,
            strikes=2,
            runners_on_first=False,
            runners_on_second=True,
            runners_on_third=False,
            score_difference=-1,
            offensive_sign='Aggressive approach.',
        )

        url = reverse('plays-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
