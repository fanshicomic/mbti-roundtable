from enum import Enum


class MBTIType(str, Enum):
    ISTJ = "ISTJ"
    ISFJ = "ISFJ"
    INFJ = "INFJ"
    INTJ = "INTJ"
    ISTP = "ISTP"
    ISFP = "ISFP"
    INFP = "INFP"
    INTP = "INTP"
    ESTP = "ESTP"
    ESFP = "ESFP"
    ENFP = "ENFP"
    ENTP = "ENTP"
    ESTJ = "ESTJ"
    ESFJ = "ESFJ"
    ENFJ = "ENFJ"
    ENTJ = "ENTJ"


class EmotionState(str, Enum):
    NEUTRAL = "neutral"
    ROASTED = "roasted"
    FIRED_UP = "fired_up"
    SMUG = "smug"
    WORN_DOWN = "worn_down"
