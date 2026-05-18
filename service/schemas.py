import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel


class RuleSchema(BaseModel):
    id: uuid.UUID
    tenant_id: str
    name: str
    description: str | None
    trigger_type: str
    trigger_config: dict[str, Any]
    conditions: list[Any]
    action_template: dict[str, Any]
    autonomy_level: int
    state: str
    created_at: datetime
    updated_at: datetime | None

    model_config = {"from_attributes": True}


class CreateRuleRequest(BaseModel):
    tenant_id: str
    name: str
    description: str | None = None
    trigger_type: str
    trigger_config: dict[str, Any] = {}
    conditions: list[Any] = []
    action_template: dict[str, Any]
    autonomy_level: int = 3
    state: str = "active"


class UpdateRuleRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    conditions: list[Any] | None = None
    action_template: dict[str, Any] | None = None
    autonomy_level: int | None = None
    state: str | None = None


class RuleExecutionSchema(BaseModel):
    id: uuid.UUID
    rule_id: uuid.UUID
    tenant_id: str
    goal_id: str | None
    triggered_at: datetime
    event_snapshot: dict[str, Any]
    outcome: str | None
    outcome_detail: str | None

    model_config = {"from_attributes": True}


class CreateExecutionRequest(BaseModel):
    goal_id: str | None = None
    event_snapshot: dict[str, Any]
    outcome: str | None = None
    outcome_detail: str | None = None
