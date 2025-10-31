from typing import List
from .geometry import FACING_TABLE, add, mul, to_rel, block_facing_prop
from .utils import esc_nbt_string, flatten_for_command

def _block_id(kind: str) -> str:
    return {
        "I": "minecraft:command_block",
        "R": "minecraft:repeating_command_block",
        "C": "minecraft:chain_command_block",
    }[kind]

def _auto_value(needs_redstone: bool) -> int:
    # Always Active: auto:1b / Redstone 필요: auto:0b
    return 0 if needs_redstone else 1

def emit_commands(program, facing: str) -> List[str]:
    """
    Program → setblock/data/summon 명령들의 리스트(여러 줄).
    배치 규칙(MVP):
      - 전체 기본 방향은 --facing
      - 그룹 g는 시작 기준점에서 '오른쪽'으로 g칸 벌려 배치
      - 각 그룹 내부는 '앞으로' 한 칸씩 이어 붙임
      - -M=n 이 있으면, 그 블록은 '이전 블록의 y'에서 n 만큼 위로, 그리고 'facing=up'으로 설치
      - 조건 여부는 blockstate conditional=true/false 로 반영
      - R>(레드스톤 필요)은 auto:0b, >(항상활성)은 auto:1b
      - 주석(###)은 text_display를 블록 위(y+1)에 소환하여 표시
      - '@tag'가 있으면, 그룹 첫 블록 시작점 뒤쪽(= global facing의 반대) 한 칸에 marker(armor_stand, 태그부여)를 소환
    """
    if facing not in FACING_TABLE:
        raise ValueError(f"--facing 값이 올바르지 않습니다: {facing}")

    basis = FACING_TABLE[facing]
    out = []

    # 월드 상대 기준점: ~ ~ ~
    origin = (0, 0, 0)

    for g_idx, group in enumerate(program.groups):
        group_origin = add(origin, mul(basis.right, g_idx * 2))  # 오른쪽으로 g_idx 만큼
        # '@tag' 마커 소환
        if group.tag:
            # 뒤쪽 = forward의 반대
            back = mul(basis.fwd, -1)
            marker_pos = add(group_origin, back)
            out.append(
                f"summon minecraft:armor_stand {to_rel(marker_pos)} {{Invisible:1b,NoGravity:1b,Marker:1b,Tags:[\"mcmd\",\"{esc_nbt_string(group.tag)}\"]}}"
            )

        cur_pos = group_origin
        cur_y = 0  # 그룹 내부 상대 y

        for b_idx, blk in enumerate(group.blocks):
            # 위치 결정
            if b_idx == 0:
                # 첫 블록: group_origin
                pass
            else:
                # 기본은 앞으로 한 칸 진전
                cur_pos = add(cur_pos, basis.fwd)

            # mount 처리
            force_up = False
            if blk.mount_up is not None:
                cur_y += blk.mount_up
                force_up = True

            place_pos = (cur_pos[0], cur_y, cur_pos[2])

            block_id = _block_id(blk.kind)
            facing_prop = block_facing_prop(facing, force_up)
            cond_state = "true" if blk.conditional else "false"
            auto = _auto_value(blk.needs_redstone)
            cmd_flat = flatten_for_command(blk.command)
            cmd_nbt = esc_nbt_string(cmd_flat)

            out.append(
                f"setblock {to_rel(place_pos)} {block_id}[facing={facing_prop},conditional={cond_state}]{{Command:\"{cmd_nbt}\",auto:{auto}b,TrackOutput:0b}}"
            )

            # 주석 → text_display 소환
            if blk.comment:
                comment_text = esc_nbt_string(blk.comment)
                comment_pos = (place_pos[0], place_pos[1]+1, place_pos[2])
                # 간단한 text_display
                out.append(
                    "summon minecraft:text_display "
                    f"{to_rel(comment_pos)} "
                    #"{text:'{\"text\":\"" + comment_text + "\"}',Tags:[\"mcmd\"]}"
                    "{text:\"" + comment_text + "\",Tags:[\"mcmd\"],billboard:\"center\"}"
                )

    return out
