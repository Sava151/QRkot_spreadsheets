from datetime import datetime, timezone

from app.models.base import QrkotBase


def invest_funds(
    target: QrkotBase,
    sources: list[QrkotBase]
) -> list[QrkotBase]:
    changed_sources = []
    for source in sources:
        changed_sources.append(source)
        transfer_amount = min(
            target.full_amount - target.invested_amount,
            source.full_amount - source.invested_amount
        )
        for obj in (target, source):
            obj.invested_amount += transfer_amount
            if obj.invested_amount >= obj.full_amount:
                obj.fully_invested = True
                obj.close_date = datetime.now(timezone.utc)
        if target.fully_invested:
            break
    return changed_sources
