from pydantic.dataclasses import dataclass


@dataclass
class ReferralDTO:
    ref_counts: int
    ref_income: int