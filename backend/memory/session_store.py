from typing import Dict, Any, List
from config import DEFAULT_USER_PROFILE


class SessionStore:
    """会话级别的内存存储，管理短期记忆和用户画像"""

    def __init__(self):
        self._sessions: Dict[str, Dict[str, Any]] = {}

    def create_session(self, session_id: str) -> dict:
        """创建新会话"""
        session = {
            "session_id": session_id,
            "created_at": "",
            "messages": [],
            "current_intent": None,
            "current_emotion": None,
            "current_flow": None,
            "current_step": None,
            "business_slots": {},
            "user_profile": dict(DEFAULT_USER_PROFILE),
            "token_usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
            "fallback_count": 0,
            "negative_emotion_count": 0,
            "snapshot_stack": [],
            "need_escalation": False,
            "need_comfort": False,
            "quick_actions": [],
            "recommended_products": [],
            "user_interested_in_product": False,
            "pending_action": None,
        }
        self._sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> dict:
        """获取会话"""
        if session_id not in self._sessions:
            return self.create_session(session_id)
        return self._sessions[session_id]

    def update_session(self, session_id: str, updates: dict):
        """更新会话状态"""
        session = self.get_session(session_id)
        session.update(updates)

    def add_message(self, session_id: str, role: str, content: str):
        """添加消息到对话历史"""
        session = self.get_session(session_id)
        session["messages"].append({"role": role, "content": content})

    def get_conversation_history(self, session_id: str, max_rounds: int = 10) -> str:
        """获取格式化的对话历史"""
        session = self.get_session(session_id)
        messages = session["messages"]
        recent = messages[-(max_rounds * 2):]
        lines = []
        for msg in recent:
            role_label = "U" if msg["role"] == "user" else "A"
            lines.append(f"{role_label}: {msg['content']}")
        return "\n".join(lines)

    def add_token_usage(self, session_id: str, usage: dict):
        """累加Token消耗"""
        session = self.get_session(session_id)
        for key in ["prompt_tokens", "completion_tokens", "total_tokens"]:
            session["token_usage"][key] = session["token_usage"].get(key, 0) + usage.get(key, 0)

    def update_user_profile(self, session_id: str, profile_updates: dict):
        """更新用户画像"""
        session = self.get_session(session_id)
        for key, value in profile_updates.items():
            if value is not None and value != "" and value != []:
                if key in session["user_profile"]:
                    if isinstance(session["user_profile"][key], list) and isinstance(value, list):
                        existing = set(session["user_profile"][key])
                        existing.update(value)
                        session["user_profile"][key] = list(existing)
                    else:
                        session["user_profile"][key] = value

    def push_snapshot(self, session_id: str):
        """保存当前流程快照到栈中"""
        session = self.get_session(session_id)
        snapshot = {
            "flow": session.get("current_flow"),
            "step": session.get("current_step"),
            "business_slots": dict(session.get("business_slots", {})),
            "intent": session.get("current_intent"),
        }
        session["snapshot_stack"].append(snapshot)

    def pop_snapshot(self, session_id: str) -> dict:
        """从栈中恢复上一个流程快照"""
        session = self.get_session(session_id)
        if session["snapshot_stack"]:
            snapshot = session["snapshot_stack"].pop()
            session["current_flow"] = snapshot["flow"]
            session["current_step"] = snapshot["step"]
            session["business_slots"] = snapshot["business_slots"]
            session["current_intent"] = snapshot["intent"]
            return snapshot
        return None

    def has_snapshot(self, session_id: str) -> bool:
        """检查是否有可恢复的快照"""
        session = self.get_session(session_id)
        return len(session["snapshot_stack"]) > 0

    def delete_session(self, session_id: str):
        """删除会话"""
        if session_id in self._sessions:
            del self._sessions[session_id]


session_store = SessionStore()
