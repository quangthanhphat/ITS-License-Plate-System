import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from Database.violation_repository import (
    add_violation,
    get_all_violations
)

success = add_violation(
    1,
    "Lan lan",
    "Output/test.jpg"
)

print("Them vi pham:", success)

violations = get_all_violations()

for violation in violations:
    print(violation)