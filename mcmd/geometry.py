from .utils import FacingBasis

FACING_TABLE = {
    "north": FacingBasis(fwd=(0, 0, -1), right=(1, 0, 0)),
    "south": FacingBasis(fwd=(0, 0, 1), right=(-1, 0, 0)),
    "west":  FacingBasis(fwd=(-1, 0, 0), right=(0, 0, -1)),
    "east":  FacingBasis(fwd=(1, 0, 0), right=(0, 0, 1)),
}

def add(a, b):
    return (a[0]+b[0], a[1]+b[1], a[2]+b[2])

def mul(v, k):
    return (v[0]*k, v[1]*k, v[2]*k)

def to_rel(pos):
    x, y, z = pos
    # ~, ~ ~ 로 출력 (상대좌표)
    return f"~{x if x!=0 else ''} ~{y if y!=0 else ''} ~{z if z!=0 else ''}"

def block_facing_prop(global_facing: str, force_up: bool):
    if force_up:
        return "up"
    return {
        "north": "north",
        "south": "south",
        "west":  "west",
        "east":  "east",
    }[global_facing]
