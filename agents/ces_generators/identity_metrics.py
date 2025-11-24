"""
Identity Salience and Tie-to-Place Metrics

Derives Weber-inspired identity metrics from CES 2021 profiles.
These metrics capture:
- identity_salience: strength of political identity and engagement
- tie_to_place: rootedness in geographic and social context

Based on theory from Social Aesthetics paper and ChatGPT feedback (notes/Next).
"""

from typing import Dict, Any, Tuple


def compute_identity_salience(profile: Dict[str, Any]) -> float:
    """
    Compute identity salience (0-1) from CES profile.

    High salience indicators:
    - Strong party identification (not None/Independent)
    - High turnout (voted in last election)
    - Clear ideological position (not centrist)

    Args:
        profile: CES profile dict with keys like cps21_pid_party, cps21_turnout, etc.

    Returns:
        Float 0-1 representing identity salience
    """
    score = 0.0
    max_score = 3.0

    # Party identification strength (0-1)
    party = profile.get('cps21_pid_party', 8)
    if party in [2, 3]:  # Conservative or NDP (strong partisan identity)
        score += 1.0
    elif party in [1, 4, 5, 6]:  # Other parties (moderate identity)
        score += 0.6
    elif party in [7, 8]:  # Other/None (weak identity)
        score += 0.2

    # Turnout (0-1)
    turnout = profile.get('cps21_turnout', 3)
    if turnout == 1:  # Voted
        score += 1.0
    elif turnout == 2:  # Didn't vote but could have
        score += 0.3
    else:  # Not eligible or didn't answer
        score += 0.1

    # Ideological clarity (distance from center on L-R scale)
    lr_scale = profile.get('cps21_lr_scale', 5.0)
    # Scale is 0-10, center is 5
    ideological_distance = abs(lr_scale - 5.0) / 5.0  # 0-1
    score += ideological_distance

    return score / max_score


def compute_tie_to_place(profile: Dict[str, Any]) -> float:
    """
    Compute tie to place (0-1) from CES profile.

    High tie indicators:
    - Rural residence (stronger community ties)
    - Born in Canada (longer settlement)
    - Older age (more established)
    - Homeownership proxy (higher income in non-urban areas)

    Args:
        profile: CES profile dict

    Returns:
        Float 0-1 representing tie to place
    """
    score = 0.0
    max_score = 4.0

    # Urban-rural (rural = higher tie to specific place)
    urban_rural = profile.get('cps21_urban_rural', 1)
    if urban_rural == 3:  # Rural
        score += 1.0
    elif urban_rural == 2:  # Suburban
        score += 0.6
    else:  # Urban
        score += 0.4  # Urban can still have strong neighborhood ties

    # Born in Canada (longer settlement = stronger ties)
    born_canada = profile.get('cps21_bornin_canada', 1)
    if born_canada == 1:
        score += 1.0
    else:
        score += 0.4

    # Age proxy (older = more established)
    yob = profile.get('cps21_yob', 1980)
    age = 2021 - yob
    if age >= 55:
        score += 1.0
    elif age >= 40:
        score += 0.7
    elif age >= 30:
        score += 0.4
    else:
        score += 0.2

    # Income as stability proxy (middle-high income = more settled)
    income = profile.get('cps21_income_cat', 5)
    if income >= 6:  # Higher income
        score += 0.8
    elif income >= 4:  # Middle income
        score += 0.6
    else:  # Lower income
        score += 0.3

    return score / max_score


def compute_identity_metrics(profile: Dict[str, Any]) -> Dict[str, float]:
    """
    Compute all identity metrics for a CES profile.

    Returns dict with:
    - identity_salience: 0-1
    - tie_to_place: 0-1
    - combined_identity: geometric mean of both (for G-identity condition)
    """
    salience = compute_identity_salience(profile)
    tie = compute_tie_to_place(profile)

    # Combined metric for identifying "strongly rooted" agents
    combined = (salience * tie) ** 0.5  # Geometric mean

    return {
        'identity_salience': round(salience, 3),
        'tie_to_place': round(tie, 3),
        'combined_identity': round(combined, 3)
    }


def get_identity_category(metrics: Dict[str, float]) -> str:
    """
    Categorize agent based on identity metrics.

    Categories:
    - "rooted_partisan": high salience + high tie (Rural Conservative archetype)
    - "urban_engaged": high salience + moderate tie (Urban Progressive archetype)
    - "settled_swing": low salience + moderate/high tie (Suburban Swing archetype)
    - "unanchored": low salience + low tie (Disengaged Renter archetype)
    """
    salience = metrics['identity_salience']
    tie = metrics['tie_to_place']

    if salience >= 0.6 and tie >= 0.6:
        return "rooted_partisan"
    elif salience >= 0.6 and tie < 0.6:
        return "urban_engaged"
    elif salience < 0.6 and tie >= 0.5:
        return "settled_swing"
    else:
        return "unanchored"


# Example usage and test
if __name__ == "__main__":
    # Test with the 4 standard CES agents
    test_profiles = [
        {
            "cps21_ResponseId": "CES_Urban_Progressive",
            "cps21_province": 35,
            "cps21_yob": 1995,
            "cps21_genderid": 2,
            "cps21_education": 9,
            "cps21_income_cat": 4,
            "cps21_urban_rural": 1,
            "cps21_pid_party": 3,  # NDP
            "cps21_lr_scale": 2.5,
            "cps21_turnout": 1,
            "cps21_bornin_canada": 1,
        },
        {
            "cps21_ResponseId": "CES_Suburban_Swing",
            "cps21_province": 35,
            "cps21_yob": 1975,
            "cps21_genderid": 1,
            "cps21_education": 7,
            "cps21_income_cat": 7,
            "cps21_urban_rural": 2,
            "cps21_pid_party": 8,  # None
            "cps21_lr_scale": 5.5,
            "cps21_turnout": 2,
            "cps21_bornin_canada": 1,
        },
        {
            "cps21_ResponseId": "CES_Rural_Conservative",
            "cps21_province": 35,
            "cps21_yob": 1960,
            "cps21_genderid": 1,
            "cps21_education": 5,
            "cps21_income_cat": 5,
            "cps21_urban_rural": 3,
            "cps21_pid_party": 2,  # Conservative
            "cps21_lr_scale": 7.5,
            "cps21_turnout": 1,
            "cps21_bornin_canada": 1,
        },
        {
            "cps21_ResponseId": "CES_Disengaged_Renter",
            "cps21_province": 35,
            "cps21_yob": 1998,
            "cps21_genderid": 3,
            "cps21_education": 8,
            "cps21_income_cat": 2,
            "cps21_urban_rural": 1,
            "cps21_pid_party": 8,  # None
            "cps21_lr_scale": 4.0,
            "cps21_turnout": 3,
            "cps21_bornin_canada": 1,
        }
    ]

    print("Identity Metrics for CES Agents")
    print("=" * 60)
    for profile in test_profiles:
        metrics = compute_identity_metrics(profile)
        category = get_identity_category(metrics)
        print(f"\n{profile['cps21_ResponseId']}:")
        print(f"  identity_salience: {metrics['identity_salience']:.3f}")
        print(f"  tie_to_place:      {metrics['tie_to_place']:.3f}")
        print(f"  combined_identity: {metrics['combined_identity']:.3f}")
        print(f"  category:          {category}")
