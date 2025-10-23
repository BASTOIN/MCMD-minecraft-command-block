import re
from dataclasses import dataclass, field
from typing import List, Optional
from .utils import normalize_newlines, split_comment_trailing

# '>' 또는 'R>' 로 시작 (라인 선두 공백 허용)
CMD_START_RE = re.compile(r'^\s*(R?>)\s+(.*)$')

@dataclass
class BlockSpec:
    needs_redstone: bool
    kind: str                 # I | R | C
    conditional: bool         # True == 조건적(\=\), False == 무조건적(\\)
    mount_up: Optional[int]   # -M=<int>
    command: str              # 멀티라인 포함
    comment: Optional[str]    # 마지막 줄 꼬리 '###' 주석

@dataclass
class Group:
    tag: Optional[str] = None
    blocks: List[BlockSpec] = field(default_factory=list)

@dataclass
class Program:
    groups: List[Group] = field(default_factory=list)

def _parse_flag_chunk(flag_chunk: str):
    """
    예: '-I -M=2 \\' , '-C \\=\\'
    반환: kind, mount(int|None), conditional(True/False)
    """
    tokens = flag_chunk.strip().split()
    kind = None
    mount = None
    conditional = None

    for t in tokens:
        if t in ("-I", "--impulse"):
            kind = "I"
        elif t in ("-R", "--repeat"):
            kind = "R"
        elif t in ("-C", "--chain"):
            kind = "C"
        elif t.startswith("-M=") or t.startswith("--mount="):
            val = t.split("=", 1)[1]
            try:
                mount = int(val)
            except:
                raise ValueError(f"-M 값은 정수여야 합니다: {t}")
        elif t == "\\\\":
            conditional = False
        elif t == "\\=\\":
            conditional = True
        else:
            # 확장 여지: 기타 토큰은 무시
            pass

    if kind is None:
        raise ValueError("블록 종류(-I|-R|-C)가 필요합니다.")
    if conditional is None:
        raise ValueError("조건 구분(\\\\ 또는 \\=\\)이 필요합니다.")
    return kind, mount, conditional

def parse_mcmd(text: str) -> Program:
    """
    .mcmd → Program
    변경점:
      ✔ 블록 본문 멀티라인 지원.
        - 블록 시작 라인 이후, 다음 블록/태그/3연속 공백이 나오기 전까지 전부 포함.
      ✔ 주석은 '마지막 줄의 꼬리 ###'만 인식.
    그룹 구분:
      - '@tag' 단독 라인 → 새 그룹 시작 + 태그
      - 3줄 이상 연속 공백 → 그룹 분리
    """
    text = normalize_newlines(text)
    lines = text.split("\n")

    program = Program()
    cur_group = Group()

    def flush_group():
        nonlocal cur_group
        if cur_group.blocks or cur_group.tag:
            program.groups.append(cur_group)
        cur_group = Group()

    i = 0
    # 그룹 분리를 위한 공백 카운터는 "블록 수집 중"일 땐 로컬로 처리
    global_blank_run = 0

    while i < len(lines):
        line = lines[i]

        # '@tag' : 새 그룹
        if line.strip().startswith("@"):
            flush_group()
            cur_group.tag = line.strip()[1:].strip()
            i += 1
            global_blank_run = 0
            continue

        # 3연속 공백 → 그룹 분리
        if line.strip() == "":
            global_blank_run += 1
            if global_blank_run >= 3:
                flush_group()
                global_blank_run = 0
            i += 1
            continue
        else:
            global_blank_run = 0

        # 블록 시작?
        m = CMD_START_RE.match(line)
        if not m:
            # 규격 외 라인은 무시
            i += 1
            continue

        starter = m.group(1)   # '>' or 'R>'
        rest = m.group(2)

        # 조건 토큰 위치 탐색
        idx_cond1 = rest.find("\\\\")
        idx_cond2 = rest.find("\\=\\")
        if idx_cond1 == -1 and idx_cond2 == -1:
            raise ValueError("조건 구분자(\\\\ 또는 \\=\\)가 필요합니다.")
        if idx_cond1 != -1 and idx_cond2 != -1:
            idx_cond = min(idx_cond1, idx_cond2)
            cond_token = "\\=\\" if idx_cond == idx_cond2 else "\\\\"
        else:
            idx_cond = idx_cond1 if idx_cond1 != -1 else idx_cond2
            cond_token = "\\=\\" if idx_cond == idx_cond2 else "\\\\"
        idx_after_cond = idx_cond + len(cond_token)

        flag_chunk = (rest[:idx_after_cond]).strip()
        first_body = rest[idx_after_cond:].lstrip()

        kind, mount, is_cond = _parse_flag_chunk(flag_chunk)

        # 🔽 멀티라인 본문 수집
        body_lines = [first_body] if first_body != "" else []
        j = i + 1
        local_blank_run = 0
        ended_by_group_split = False

        while j < len(lines):
            ln = lines[j]

            # 다음 블록 시작이 보이면 중단
            if CMD_START_RE.match(ln):
                break
            # 다음 태그가 보이면 중단
            if ln.strip().startswith("@"):
                break

            # 공백 3연속 → 이 블록 끝 + 그룹 분리
            if ln.strip() == "":
                local_blank_run += 1
                if local_blank_run >= 3:
                    ended_by_group_split = True
                    break
                else:
                    body_lines.append("")  # 본문 내의 빈 줄은 유지
                    j += 1
                    continue
            else:
                local_blank_run = 0

            body_lines.append(ln)
            j += 1

        body = "\n".join(body_lines).rstrip()

        # 마지막 줄 꼬리 '###' 만 주석으로 인식
        code, cmt = split_comment_trailing(body)

        bs = BlockSpec(
            needs_redstone=(starter == "R>"),
            kind=kind,
            conditional=is_cond,
            mount_up=mount,
            command=code,
            comment=cmt
        )
        cur_group.blocks.append(bs)

        # 인덱스 이동
        i = j

        # 만약 공백 3연속으로 블록이 끝났다면 여기서 그룹도 끊는다
        if ended_by_group_split:
            flush_group()
            global_blank_run = 0  # 이미 끊었으므로 초기화

    # 마지막 그룹 flush
    if cur_group.blocks or cur_group.tag:
        program.groups.append(cur_group)

    return program
