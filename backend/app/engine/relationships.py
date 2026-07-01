from app.schemas.types import MBTIType


def relationship_score(a: MBTIType, b: MBTIType) -> float:
    """Friction/affinity between two types in [-1, 1]. Negative = friction, positive = affinity.

    Not yet implemented: MVP plan is to derive this from dichotomy overlap
    (shared letters -> affinity, opposing letters -> friction) per docs/PRD.md,
    swappable later for a hand-tuned table without changing this signature.
    """
    raise NotImplementedError
