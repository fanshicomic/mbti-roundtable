from app.engine.relationships import relationship_score
from app.schemas.types import MBTIType


def test_identical_types_score_max_affinity() -> None:
    assert relationship_score(MBTIType.ESTJ, MBTIType.ESTJ) == 1.0


def test_fully_opposite_types_score_max_friction() -> None:
    assert relationship_score(MBTIType.ESTJ, MBTIType.INFP) == -1.0


def test_partial_overlap_is_between_extremes() -> None:
    # ESTJ vs ESTP differ only on the last axis (J/P)
    assert relationship_score(MBTIType.ESTJ, MBTIType.ESTP) == 0.5


def test_symmetric() -> None:
    assert relationship_score(MBTIType.INFJ, MBTIType.ENTP) == relationship_score(MBTIType.ENTP, MBTIType.INFJ)
