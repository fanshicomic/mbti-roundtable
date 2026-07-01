def check_content(text: str) -> bool:
    """True if `text` is allowed (blunt roasting is fine; slurs/protected-class attacks/harassment are not).

    Not yet implemented — layered on top of the LLM provider's own safety layer, see docs/PRD.md.
    """
    raise NotImplementedError


def enforce_output_contract(text: str, max_words: int) -> str:
    """Truncate/strip to satisfy the one-short-sentence output contract. No retry call to the LLM."""
    raise NotImplementedError
