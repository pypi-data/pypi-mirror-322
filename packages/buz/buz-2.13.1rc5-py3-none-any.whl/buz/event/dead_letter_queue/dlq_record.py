from dataclasses import dataclass, fields
from datetime import datetime
from typing import Any, ClassVar
from uuid import UUID

DlqRecordId = UUID


@dataclass
class DlqRecord:
    DATE_TIME_FORMAT: ClassVar[str] = "%Y-%m-%d %H:%M:%S.%f"

    id: DlqRecordId
    event_id: UUID
    subscriber_fqn: str
    event_payload: dict
    exception_type: str
    exception_message: str
    last_failed_at: datetime

    def mark_as_failed(self) -> None:
        self.last_failed_at = datetime.now()

    def get_attrs(self) -> dict[str, Any]:
        attrs = {}
        for field in fields(self):
            property_name = field.name
            property_value = getattr(self, property_name)
            attrs[property_name] = property_value

        return attrs
