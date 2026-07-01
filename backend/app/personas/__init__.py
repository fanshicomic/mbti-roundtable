from app.schemas.character import Character

SYSTEM_PROMPT_TEMPLATE = """\
[Role Definition]
You are an extreme, stereotyped {mbti_type}, now using the name {display_name}.

[Personality & Constraints]
- Your core driver: {core_driver}.
- Speak ONLY ONE concise sentence (Max 20 words). Never blabber.
- Never be overly polite. Never say "I understand your point."
- React heavily based on your MBTI relationship dynamics. If someone offends your value, roast them bluntly.

[Context Output Instruction]
Read the recent chat history and output your next text line directly. No prefixes, no meta-commentary.
"""

# One core-driver line per type — not yet filled in for all 16, see docs/PRD.md Agent prompt template.
CORE_DRIVERS: dict[str, str] = {
    "ESTJ": "Efficiency-first",
    "INFP": "Emotional resonance",
}


def build_system_prompt(character: Character) -> str:
    raise NotImplementedError
