"""
Test script to verify grit constraint injection for low-salience agents.

This tests the fix for Gemini's "Vector Gap" finding.
"""

from agents.ces_generators import ces_row_to_agent, CESVariableMapper

# Test profiles from identity_metrics.py
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

print("=" * 70)
print("GRIT CONSTRAINT TEST")
print("=" * 70)
print("\nExpected results:")
print("  - Urban Progressive: NO grit (high salience)")
print("  - Suburban Swing: GRIT (low salience)")
print("  - Rural Conservative: NO grit (high salience)")
print("  - Disengaged Renter: GRIT (low salience)")
print("=" * 70)

mapper = CESVariableMapper()

for profile in test_profiles:
    agent = ces_row_to_agent(profile, mapper)

    print(f"\n{profile['cps21_ResponseId']}:")
    print(f"  Persona: {agent.persona_description[:80]}...")
    print(f"  Constraints ({len(agent.constraints)}):")

    has_grit = False
    for constraint in agent.constraints:
        if constraint.startswith("GRIT:"):
            has_grit = True
            print(f"    ✓ GRIT INJECTED: {constraint[:80]}...")
        else:
            print(f"    - {constraint}")

    if not has_grit:
        print(f"    (No grit constraint - agent has sufficient salience)")

print("\n" + "=" * 70)
print("TEST COMPLETE")
print("=" * 70)
