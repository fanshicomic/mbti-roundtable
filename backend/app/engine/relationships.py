from app.schemas.types import MBTIType


def relationship_score(a: MBTIType, b: MBTIType) -> float:
    """Friction/affinity between two types in [-1, 1]. Negative = friction, positive = affinity.

    MVP derivation (per docs/PRD.md): dichotomy overlap. Each of the 4 letter positions
    either matches or opposes (there are only two options per axis), so matches and
    mismatches always sum to 4 — score = (matches - 2) / 2, giving -1.0 for fully
    opposite types (e.g. ESTJ vs INFP) up to 1.0 for identical types.
    """
    matches = sum(1 for x, y in zip(a.value, b.value) if x == y)
    return (matches - 2) / 2
