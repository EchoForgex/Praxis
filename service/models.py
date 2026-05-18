import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Rule(Base):
    __tablename__ = "rules"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)

    trigger_type: Mapped[str] = mapped_column(String, nullable=False)
    trigger_config: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

    conditions: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    action_template: Mapped[dict] = mapped_column(JSONB, nullable=False)

    autonomy_level: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    state: Mapped[str] = mapped_column(String, nullable=False, default="active")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )


class RuleExecution(Base):
    __tablename__ = "rule_executions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rule_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("rules.id"), nullable=False, index=True
    )
    tenant_id: Mapped[str] = mapped_column(String, nullable=False, index=True)

    goal_id: Mapped[str | None] = mapped_column(String, nullable=True)
    triggered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    event_snapshot: Mapped[dict] = mapped_column(JSONB, nullable=False)
    outcome: Mapped[str | None] = mapped_column(String, nullable=True)
    outcome_detail: Mapped[str | None] = mapped_column(String, nullable=True)
