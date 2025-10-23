import argparse
from pathlib import Path
from .parser import parse_mcmd
from .emitter import emit_commands
from .utils import normalize_newlines

def main():
    ap = argparse.ArgumentParser(description="MCMD compiler (MVP): .mcmd → setblock 스크립트 .txt")
    ap.add_argument("--facing", required=True, choices=["north","south","west","east"],
                    help="설치될 커맨드 블록 라인의 기본 바라보는 방향")
    ap.add_argument("--src", required=True, help=".mcmd 파일 경로")
    args = ap.parse_args()

    src_path = Path(args.src)
    if not src_path.exists():
        raise SystemExit(f"파일을 찾을 수 없습니다: {src_path}")

    text = normalize_newlines(src_path.read_text(encoding="utf-8"))
    program = parse_mcmd(text)
    cmds = emit_commands(program, args.facing)

    out_path = src_path.parent / f"out_{src_path.stem}.mcfunction"
    out_path.write_text("\n".join(cmds) + "\n", encoding="utf-8")
    print(f"[OK] {out_path.name} 생성 완료 ({len(cmds)} lines)")

if __name__ == "__main__":
    main()
