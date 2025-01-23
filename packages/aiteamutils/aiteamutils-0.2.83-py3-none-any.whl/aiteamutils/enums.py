"""시스템 전체에서 사용되는 열거형 정의."""
from enum import Enum

def hyphen_to_camel_case(text: str) -> str:
    """하이픈을 카멜케이스로 변환하는 함수"""
    words = text.split('-')
    return words[0].capitalize() + ''.join(word.capitalize() for word in words[1:])

class UserStatus(str, Enum):
    """사용자 상태."""
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    BLOCKED = "BLOCKED"

class ActivityType(str, Enum):
    """시스템 활동 유형."""
    # 인증 관련
    ACCESS_TOKEN_ISSUED = "ACCESS_TOKEN_ISSUED"
    REFRESH_TOKEN_ISSUED = "REFRESH_TOKEN_ISSUED"
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    
    # 사용자 관련
    USER_CREATED = "USER_CREATED"
    USER_UPDATED = "USER_UPDATED"
    USER_DELETED = "USER_DELETED"
    PASSWORD_CHANGE = "PASSWORD_CHANGE"