import re
from dataclasses import dataclass

def split_comment_trailing(body: str):
    """
    멀티라인 본문에서 '###' 주석을 '마지막 줄의 꼬리'에서만 인식한다.
    - 마지막 비어있지 않은 줄의 '###' 이후를 주석으로 간주.
    - 본문 중간의 '###' (예: JSON 문자열 내부)는 무시.
    반환: (code_without_trailing_comment, comment_or_None)
    """
    # 오른쪽 공백 제거만 (본문 내부 개행은 유지)
    rstripped = body.rstrip()
    if not rstripped:
        return body, None

    lines = rstripped.split("\n")
    last_line = lines[-1]
    if "###" not in last_line:
        return body, None

    # 마지막 줄의 마지막 '###'만 인식
    idx = last_line.rfind("###")
    code_last = last_line[:idx].rstrip()
    comment = last_line[idx+3:].strip()

    lines[-1] = code_last
    code = "\n".join(lines)
    return code, (comment if comment != "" else None)

def flatten_for_command(s: str) -> str:
    """
    멀티라인 본문을 Command용 '한 줄'로 평탄화.
    - CR 제거
    - 각 줄바꿈(\n) 앞뒤 공백 포함하여 ' ' 하나로 치환
    - 공백 2개 이상은 1개로 축소
    """
    s = s.replace("\r", "")
    s = re.sub(r"[ \t]*\n[ \t]*", " ", s)   # 줄 사이 공백 정리
    s = re.sub(r"[ \t]{2,}", " ", s)        # 다중 공백 축소
    return s.strip()

def esc_nbt_string(s: str) -> str:
    """
    NBT 문자열 이스케이프:
    - 역슬래시 -> \\\\
    - 큰따옴표 -> \\"
    (줄바꿈은 flatten_for_command에서 이미 공백으로 바뀜)
    """
    s = s.replace("\\", "\\\\")
    s = s.replace('"', '\\"')
    return s

def normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")

def strip_trailing_blank_lines(lines):
    while lines and lines[-1].strip() == "":
        lines.pop()
    return lines

@dataclass
class FacingBasis:
    fwd: tuple   # (dx, dy, dz)
    right: tuple # (dx, dy, dz)
