"""
Semiotic Comparison: Challenge ON vs OFF

Compares sign patterns across experimental conditions per the
Empirical Social Semiotics methodology.
"""

import json
import sys
sys.path.insert(0, '.')
from social_rl.semiotic_coder import (
    SemioticCoder, JustificationType, VoiceMarker, RelationalStance
)

def load_experiment(path):
    """Load all rounds from an experiment."""
    rounds = {}
    for round_num in [1, 2, 3]:
        try:
            with open(f'{path}/round{round_num}_social_rl.json') as f:
                rounds[round_num] = json.load(f)
        except FileNotFoundError:
            pass
    return rounds


def analyze_experiment(path, name, coder):
    """Analyze an experiment and return metrics by agent x round."""
    rounds = load_experiment(path)
    results = {}

    for round_num, data in rounds.items():
        results[round_num] = {}

        # Group messages by agent_id
        messages = data.get('messages', [])
        agent_messages = {}
        for msg in messages:
            aid = msg.get('agent_id', '')
            if aid not in agent_messages:
                agent_messages[aid] = []
            agent_messages[aid].append(msg)

        for agent_id, turns in agent_messages.items():
            if not turns:
                continue

            codings = []
            for t in turns:
                content = t.get('content', '')
                if not content:
                    continue
                turn_num = t.get('turn_number', 1)
                coding = coder.code_utterance(content, agent_id, turn_num, round_num)
                codings.append(coding)

            if not codings:
                continue

            # Aggregate - compute valences from enum values
            total = len(codings)
            just_count = sum(1 for c in codings if c.justification == JustificationType.JUSTIFICATORY)
            alien_count = sum(1 for c in codings if c.voice == VoiceMarker.ALIENATED)
            empower_count = sum(1 for c in codings if c.voice == VoiceMarker.EMPOWERED)
            bridge_count = sum(1 for c in codings if c.stance == RelationalStance.BRIDGING)
            dismiss_count = sum(1 for c in codings if c.stance == RelationalStance.DISMISSIVE)

            voice_val = (empower_count - alien_count) / total if total > 0 else 0
            stance_val = (bridge_count - dismiss_count) / total if total > 0 else 0

            # Get engagement from feedback
            feedback = data.get('feedback', {})
            agent_feedback = feedback.get(agent_id, {})
            eng = agent_feedback.get('engagement', 0)

            results[round_num][agent_id] = {
                'engagement': eng,
                'voice_valence': voice_val,
                'stance_valence': stance_val,
                'justificatory_pct': just_count / total if total > 0 else 0,
                'n_utterances': total
            }

    return results


def print_comparison_table(off_results, on_results):
    """Print the comparison table from generalizing_on_ces."""

    print("\n" + "=" * 80)
    print("EMPIRICAL SOCIAL SEMIOTICS: Challenge ON vs OFF Comparison")
    print("=" * 80)

    # Header
    print(f"\n{'Agent':<20} {'Round':<6} {'Cond':<6} {'Eng':>6} {'Voice':>7} {'Stance':>7} {'Just%':>7}")
    print("-" * 80)

    # Get all agents across both conditions
    all_agents = set()
    for r in off_results.values():
        all_agents.update(r.keys())
    for r in on_results.values():
        all_agents.update(r.keys())

    for agent in sorted(all_agents):
        for round_num in [1, 2, 3]:
            off_data = off_results.get(round_num, {}).get(agent)
            on_data = on_results.get(round_num, {}).get(agent)

            if off_data:
                print(f"{agent:<20} R{round_num:<5} {'OFF':<6} "
                      f"{off_data['engagement']:>6.2f} "
                      f"{off_data['voice_valence']:>7.2f} "
                      f"{off_data['stance_valence']:>7.2f} "
                      f"{off_data['justificatory_pct']*100:>6.0f}%")

            if on_data:
                print(f"{'':<20} {'':<6} {'ON':<6} "
                      f"{on_data['engagement']:>6.2f} "
                      f"{on_data['voice_valence']:>7.2f} "
                      f"{on_data['stance_valence']:>7.2f} "
                      f"{on_data['justificatory_pct']*100:>6.0f}%")
        print()

    # Summary statistics
    print("\n" + "=" * 80)
    print("SUMMARY: Mean differences (Challenge ON - Challenge OFF)")
    print("=" * 80)

    for round_num in [1, 2, 3]:
        off_round = off_results.get(round_num, {})
        on_round = on_results.get(round_num, {})

        if not off_round or not on_round:
            continue

        # Compute means for each condition
        off_eng = sum(d['engagement'] for d in off_round.values()) / len(off_round)
        off_voice = sum(d['voice_valence'] for d in off_round.values()) / len(off_round)
        off_stance = sum(d['stance_valence'] for d in off_round.values()) / len(off_round)
        off_just = sum(d['justificatory_pct'] for d in off_round.values()) / len(off_round)

        on_eng = sum(d['engagement'] for d in on_round.values()) / len(on_round)
        on_voice = sum(d['voice_valence'] for d in on_round.values()) / len(on_round)
        on_stance = sum(d['stance_valence'] for d in on_round.values()) / len(on_round)
        on_just = sum(d['justificatory_pct'] for d in on_round.values()) / len(on_round)

        print(f"\nRound {round_num}:")
        print(f"  Engagement:   OFF={off_eng:.2f}  ON={on_eng:.2f}  Δ={on_eng-off_eng:+.2f}")
        print(f"  Voice:        OFF={off_voice:.2f}  ON={on_voice:.2f}  Δ={on_voice-off_voice:+.2f}")
        print(f"  Stance:       OFF={off_stance:.2f}  ON={on_stance:.2f}  Δ={on_stance-off_stance:+.2f}")
        print(f"  Justificatory: OFF={off_just*100:.0f}%   ON={on_just*100:.0f}%   Δ={((on_just-off_just)*100):+.0f}pp")


if __name__ == "__main__":
    coder = SemioticCoder()

    off_path = "outputs/ces_14B_performer_7B_coach"
    on_path = "outputs/ces_14B_7B_challenge_ON_v2"

    print(f"Challenge OFF: {off_path}")
    print(f"Challenge ON:  {on_path}")

    off_results = analyze_experiment(off_path, "Challenge OFF", coder)
    on_results = analyze_experiment(on_path, "Challenge ON", coder)

    print_comparison_table(off_results, on_results)
