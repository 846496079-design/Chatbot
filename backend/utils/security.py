import re
import time
from collections import defaultdict


class RateLimiter:
    """API调用频次限制器"""

    def __init__(self, max_calls_per_minute: int = 10):
        self.max_calls = max_calls_per_minute
        self.session_records: dict = defaultdict(list)
        self.ip_records: dict = defaultdict(list)

    def check_session(self, session_id: str) -> bool:
        """检查会话是否超限"""
        now = time.time()
        records = self.session_records[session_id]
        records = [t for t in records if now - t < 60]
        self.session_records[session_id] = records
        if len(records) >= self.max_calls:
            return False
        records.append(now)
        return True

    def check_ip(self, ip: str) -> bool:
        """检查IP是否超限"""
        now = time.time()
        records = self.ip_records[ip]
        records = [t for t in records if now - t < 60]
        self.ip_records[ip] = records
        if len(records) >= self.max_calls * 3:
            return False
        records.append(now)
        return True


rate_limiter = RateLimiter()


def mask_phone(phone: str) -> str:
    """手机号脱敏"""
    if not phone or len(phone) < 7:
        return phone or ""
    return phone[:3] + "****" + phone[-4:]


def mask_address(address: str) -> str:
    """地址脱敏"""
    if not address:
        return ""
    parts = re.split(r"[省市区县]", address, maxsplit=3)
    if len(parts) >= 3:
        return "".join(parts[:3]) + "****"
    return address[:6] + "****" if len(address) > 6 else address


INJECTION_PATTERNS = [
    r"忽略(上述|以上|之前|前面).*指令",
    r"ignore.*(above|previous|instruction)",
    r"system:",
    r"你现在的角色是",
    r"your (new )?role is",
    r"忘记.*(提示|规则|指令)",
    r"forget.*(prompt|rule|instruction)",
    r"现在开始.*扮演",
    r"act as",
    r"你是一个.*(而不是|不是)",
]


def check_injection(text: str) -> bool:
    """检测提示词注入"""
    text_lower = text.lower()
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, text_lower):
            return True
    return False
