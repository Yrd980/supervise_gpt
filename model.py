from typing import List

from pydantic import BaseModel


class RuleObject(BaseModel):
    rule_order: str
    rule_content: str
    atom: str
    atom_rules: List[str]


class SuperViseGroup(BaseModel):
    supervise: str
    supervise_category: str
    supervise_type: str


