from enum import Enum


class RegulationType(Enum):
    CONTENT_REGULATION = "内容监管"
    BEHAVIOR_REGULATION = "行为监管"
    QUALITY_REGULATION = "质量监管"
    PROCESS_REGULATION = "流程监管"


class ClauseType(Enum):
    COMPLEX_CLAUSE = 0
    ATOMIC_CLAUSE = 1


class AutoSupervision(Enum):
    NOT_AUTO_SUPERVISED = 0
    AUTO_SUPERVISED = 1
