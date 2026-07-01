from app.schemas.session import SessionState


class SessionStore:
    """Persists finished session transcripts under a shareable session ID (no user auth).

    Not yet implemented — SQLite is enough for MVP, see docs/PRD.md "Persistence & sharing".
    """

    def save(self, state: SessionState) -> None:
        raise NotImplementedError

    def load(self, session_id: str) -> SessionState | None:
        raise NotImplementedError
