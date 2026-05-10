MOCK_TICKETS = []


def create_ticket(order_id, issue_type, description, expectation=None):
    """创建售后工单"""
    import uuid
    ticket_id = f"TK-{uuid.uuid4().hex[:8].upper()}"
    ticket = {
        "ticket_id": ticket_id,
        "order_id": order_id,
        "issue_type": issue_type,
        "description": description,
        "expectation": expectation,
        "status": "处理中",
        "created_at": "2026-05-07 10:00",
        "estimated_time": "24小时内"
    }
    MOCK_TICKETS.append(ticket)
    return ticket


def get_ticket(ticket_id):
    """获取工单详情"""
    for t in MOCK_TICKETS:
        if t["ticket_id"] == ticket_id:
            return t
    return None
