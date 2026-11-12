"""A stand-in for a real email provider. It records emails instead of sending them."""

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


@dataclass
class SentEmail:
    to: str
    kind: str
    subject: str
    sent_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class FakeEmailSender:
    def __init__(self):
        self.sent: list[SentEmail] = []

    def send(self, to: str, kind: str, subject: str) -> None:
        email = SentEmail(to=to, kind=kind, subject=subject)
        self.sent.append(email)
        logger.info("Sent %s email to %s", kind, to)

    def count(self, to: str, kind: str) -> int:
        return sum(1 for e in self.sent if e.to == to and e.kind == kind)
