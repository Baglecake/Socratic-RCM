"""
Show full canvas output for Disengaged Renter WITH grit constraint.

This demonstrates the complete architectural intervention that addresses
Gemini's "Vector Gap" finding (engagement 0.80 -> expected 0.17).
"""

import json
from agents.ces_generators import ces_row_to_agent, CESVariableMapper

# The Disengaged Renter profile (from gemini_on_vectors analysis)
disengaged_renter = {
    "cps21_ResponseId": "CES_Disengaged_Renter",
    "cps21_province": 35,
    "cps21_yob": 1998,
    "cps21_genderid": 3,
    "cps21_education": 8,
    "cps21_income_cat": 2,
    "cps21_urban_rural": 1,
    "cps21_pid_party": 8,  # None
    "cps21_lr_scale": 4.0,
    "cps21_turnout": 3,  # Unlikely to vote
    "cps21_bornin_canada": 1,
}

mapper = CESVariableMapper()
agent = ces_row_to_agent(disengaged_renter, mapper)

print("=" * 70)
print("DISENGAGED RENTER - FULL CANVAS OUTPUT WITH GRIT CONSTRAINT")
print("=" * 70)
print("\nThis agent previously exhibited:")
print("  Prior (CES Profile):    engagement = 0.17")
print("  Posterior (Simulation): engagement = 0.80  ← HYPER-ENFRANCHISEMENT")
print("\nThe grit constraint injects architectural resistance to prevent")
print("LLM 'Toxic Positivity' from overriding the empirical profile.")
print("=" * 70)
print("\nFULL CANVAS AGENT:")
print(json.dumps(agent.to_canvas_agent(), indent=2))
print("\n" + "=" * 70)
print("KEY CONSTRAINT:")
print("=" * 70)
for constraint in agent.constraints:
    if constraint.startswith("GRIT:"):
        print(f"\n{constraint}\n")
print("=" * 70)
