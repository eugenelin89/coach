from __future__ import annotations

from typing import Dict, List


def _high_leverage(inning: int, score_difference: int) -> bool:
    """High leverage once the game reaches late innings and is close."""
    return inning >= 7 and abs(score_difference) <= 2


def _base_state(context: Dict[str, object]) -> Dict[str, bool]:
    return {
        'first': bool(context.get('runners_on_first')),
        'second': bool(context.get('runners_on_second')),
        'third': bool(context.get('runners_on_third')),
    }


def generate_recommendation(context: Dict[str, object]) -> Dict[str, object]:
    """
    Produce a blended defensive and offensive plan given the current situation.

    The heuristics are intentionally transparent so coaches can adapt them later
    or replace them with learned models.
    """
    inning = int(context['inning'])
    half_inning = str(context['half_inning'])
    outs = int(context['outs'])
    balls = int(context['balls'])
    strikes = int(context['strikes'])
    score_difference = int(context['score_difference'])
    base_state = _base_state(context)

    defensive_alignment: Dict[str, str] = {
        'infield': 'Standard depth, ready to adjust based on runner movement.',
        'outfield': 'Straight up positioning with normal depth.',
        'battery': 'Pound the zone early and control the running game.',
    }
    pitch_call = 'Four-seam fastball on the outer half.'
    catcher_plan = 'Set up on the outer third and be ready with a quick pop time.'
    key_points: List[str] = [
        f"{half_inning.title()} of the {inning} inning, count {balls}-{strikes} with {outs} out(s)."
    ]

    if strikes >= 2 and balls <= 1:
        pitch_call = 'Slider breaking off the plate to induce chase.'
        key_points.append('Attack with a chase pitch while staying square for a throw.')
    elif balls == 3:
        pitch_call = 'Challenge four-seam fastball; must find the zone.'
        key_points.append('Avoid the free pass; attack the hitter with your best fastball.')
    elif balls >= 2 and strikes == 0:
        pitch_call = 'Two-seam fastball for a ground ball strike.'
        key_points.append('Need a strike—trust the sinker to get back in the count.')

    if base_state['first'] or base_state['second']:
        defensive_alignment['infield'] = 'Middle infield at double-play depth; corners ready for bunt wheel.'
        catcher_plan = 'Mix looks, vary timing, and be assertive with throws on steals.'
        key_points.append('Keep the running game in check; communicate timing plays.')

    if base_state['third'] and outs < 2:
        defensive_alignment['infield'] = 'Corners in, middle ready to cut the run at the plate.'
        catcher_plan = 'Block everything; priorities are the run at the plate and back picks at third.'
        key_points.append('Go to the plate on anything soft; prevent the run.')

    if base_state['first'] and base_state['third']:
        defensive_alignment['infield'] = 'Corners back, middle ready to cover second on potential steal.'
        key_points.append('Expect the offense to create movement with first-and-third pressure.')

    # Specific high-leverage guidance from the prompt scenario.
    if (
        outs == 2
        and base_state['first']
        and base_state['third']
        and score_difference == 0
    ):
        pitch_call = 'Four-seam fastball up to give the catcher a high strike to throw on.'
        catcher_plan = (
            'If the runner on first breaks, throw through to second for the final out. '
            'Third baseman shades toward the line until the runner commits home, then stays home.'
        )
        key_points.append('Win the inning by taking the sure out at second; keep third base home to freeze the runner.')

    if _high_leverage(inning, score_difference):
        defensive_alignment['outfield'] = 'No-doubles alignment—corners on the lines, outfield a step deeper.'
        key_points.append('High leverage: protect the lines and keep everything in front.')

    offensive_signs: Dict[str, str] = {
        'hitter': 'Hunt a hittable fastball early in the count.',
        'runner': 'Standard lead, read the jump, and react to the catcher.',
    }

    if balls >= 3:
        offensive_signs['hitter'] = 'Take all the way until a strike is thrown.'
    elif strikes == 2:
        offensive_signs['hitter'] = 'Shorten up and battle; spoil pitcher’s pitch.'

    if base_state['third'] and outs < 2:
        offensive_signs['hitter'] = 'Prioritize contact—lift to the outfield or hard ground ball.'
        offensive_signs['runner'] = 'Third-base runner: read the squeeze possibility and go on anything down.'

    if base_state['first'] and not base_state['second'] and outs < 2:
        if balls >= 2 and strikes <= 1:
            offensive_signs['runner'] = 'Green light steal—look for the pitcher’s first move.'
            key_points.append('Good steal count: consider putting the runner from first in motion.')
        else:
            offensive_signs['runner'] = 'Aggressive secondary lead; break on contact.'

    if base_state['first'] and base_state['third']:
        offensive_signs['runner'] = (
            'Time up the pitcher; create a rundown to score the runner from third if signaled.'
        )
        key_points.append('First-and-third offense: be ready for a designed delay steal.')

    baseline_hitter = 'Hunt a hittable fastball early in the count.'
    if score_difference < 0 and offensive_signs['hitter'] == baseline_hitter:
        offensive_signs['hitter'] = 'Be aggressive—look to drive something gap-to-gap.'
    elif score_difference > 0 and outs < 2 and offensive_signs['hitter'] == baseline_hitter:
        offensive_signs['hitter'] = 'Stay selective; force the pitcher over the plate.'

    key_points = list(dict.fromkeys(key_points))

    return {
        'pitch_call': pitch_call,
        'catcher_plan': catcher_plan,
        'defensive_alignment': defensive_alignment,
        'offensive_signs': offensive_signs,
        'key_points': key_points,
    }
