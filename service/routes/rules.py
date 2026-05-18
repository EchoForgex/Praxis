import uuid

from fastapi import APIRouter, Depends, Header, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from database import get_db
from models import Rule, RuleExecution
from schemas import (
    CreateExecutionRequest,
    CreateRuleRequest,
    RuleExecutionSchema,
    RuleSchema,
    UpdateRuleRequest,
)

router = APIRouter(prefix="/rules", tags=["rules"])


def verify_token(x_service_token: str = Header(...)):
    if x_service_token != settings.praxis_service_secret:
        raise HTTPException(status_code=401, detail="Invalid service token")


@router.get("", response_model=list[RuleSchema])
async def list_rules(
    tenant_id: str = Query(...),
    event_type: str | None = Query(None),
    state: str = Query("active"),
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_token),
):
    stmt = select(Rule).where(Rule.tenant_id == tenant_id, Rule.state == state)
    if event_type:
        stmt = stmt.where(Rule.trigger_type == event_type)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.post("", response_model=RuleSchema, status_code=201)
async def create_rule(
    body: CreateRuleRequest,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_token),
):
    rule = Rule(**body.model_dump())
    db.add(rule)
    await db.commit()
    await db.refresh(rule)
    return rule


@router.patch("/{rule_id}", response_model=RuleSchema)
async def update_rule(
    rule_id: uuid.UUID,
    body: UpdateRuleRequest,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_token),
):
    result = await db.execute(select(Rule).where(Rule.id == rule_id))
    rule = result.scalar_one_or_none()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(rule, field, value)
    await db.commit()
    await db.refresh(rule)
    return rule


@router.get("/{rule_id}/executions", response_model=list[RuleExecutionSchema])
async def list_executions(
    rule_id: uuid.UUID,
    limit: int = Query(50),
    offset: int = Query(0),
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_token),
):
    stmt = (
        select(RuleExecution)
        .where(RuleExecution.rule_id == rule_id)
        .limit(limit)
        .offset(offset)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


@router.post("/{rule_id}/executions", response_model=RuleExecutionSchema, status_code=201)
async def create_execution(
    rule_id: uuid.UUID,
    body: CreateExecutionRequest,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_token),
):
    result = await db.execute(select(Rule).where(Rule.id == rule_id))
    rule = result.scalar_one_or_none()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    execution = RuleExecution(
        rule_id=rule_id,
        tenant_id=rule.tenant_id,
        **body.model_dump(),
    )
    db.add(execution)
    await db.commit()
    await db.refresh(execution)
    return execution
