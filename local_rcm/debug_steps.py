
import os
from runtime_parser import Runtime

base_path = os.path.join(os.path.dirname(__file__), "runtime-files")
runtime = Runtime(
    f"{base_path}/B42_Runtime_Phase1_Conceptualization.txt",
    f"{base_path}/B42_Runtime_Phase2_Drafting.txt",
    f"{base_path}/B42_Runtime_Phase3_Review.txt"
)

print("Loaded steps:")
for step_id in sorted(runtime.steps.keys()):
    print(f"'{step_id}'")
