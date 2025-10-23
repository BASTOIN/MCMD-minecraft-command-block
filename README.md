# README.md
## MCMD

### 설치

- Python 3.8+

- 프로젝트 구조:

```
MCMD/
 ├─ mcmd/
 │   ├─ __init__.py
 │   ├─ __main__.py
 │   ├─ parser.py
 │   ├─ emitter.py
 │   ├─ geometry.py
 │   └─ utils.py
 └─ example.mcmd   # (예시 파일)
```

### 실행
```
# 폴더: MCMD/
python -m mcmd --facing="north" --src="example.mcmd"
# 결과: out_example.mcfunction 생성
```

out_*.mcfunction 안의 명령들을 마인크래프트에서 실행하면 커맨드 블록이 자동 설치됩니다.

### 개요

#### 목적:
이 프로젝트는 마인크래프트 커맨드 블록을 더 편하고 가독성 있게 제작하기 위해 만들어진 프로젝트 이다.
#### 출력 방식:
작성한 `.mcmd` 파일을 읽어 .mcfunction 에서 사용해 커맨드를 설치 할 수 있는 `(out_{filename}.mcfunction)`로 저장함.<br>
실행은 `/execute as @s at @s run function ...`<br>
혹은 `/execute positioned ~ ~ ~ run function ...` 을 이용할것

### 주요 작성 규칙

1. 시작 구분자

    - `>` : 항상 활성화된 커맨드 블록

    - `R>` : 레드스톤 신호 필요

2. 커맨드 블록 종류

    - `-I` / `--impulse` : 반응형

    - `-R` / `--repeat` : 반복형

    - `-C` / `--chain` : 체인형

3. 이동수직 마운트 (선택)

    - `-M=<int>` / `--mount=<int>`
해당 블록을 이전 블록의 y 기준으로 `<int>` 만큼 위에 배치합니다.
이때 블록의 facing은 up 으로 강제됩니다.

4. 조건 구분

    - `\\` : 무조건적

    - `\=\` : 조건적

5. 명령어 입력

    - 커맨드 블록 내부 코드에 다음 `>` or `R>` 이전까지 개행 없이 작성됨

6. 주석

    - `###` 로 작성, 커맨드블록 한 칸 위에 text_display 엔티티로 표시
`(태그: mcmd)`

7. 세 단락 이상 개행

    - 블록 덩어리 구분용 (새 라인 설치)

### 심화 문법

- `@{tag}` : 커맨드 블록 덩어리 시작 시 마커 생성 (태그명 지정)

    - 자동으로 “3줄 개행 구분”으로 인식

    - 마커는 해당 방향의 뒷쪽에 소환됨

### 배치 규칙 (Emitter)
- 전역 방향: `--facing=<north | south | west | east>`

- 각 그룹은 기준점에서 오른쪽으로 g칸(g=그룹 인덱스) 떨어져 시작

- 그룹 내부 블록은 앞으로 한 칸씩 이어서 배치

- `-M`이 있으면 해당 블록은 수직으로 누적 상승(y += M), `facing=up`

- 조건/무조건 상태는 블록 스테이트 `conditional=true/false` 반영

- `>` → `auto:1b`, `R>` → `auto:0b` 로 설정

- `@`태그가 있으면 그룹 시작점 뒤쪽(전역 facing 반대)에 armor_stand 마커 소환

### 예시
**입력(test.mcmd)**
```
@init
R> -I \\ scoreboard objectives add coin dummy ### 코인 오브젝트 추가
> -C \\ scoreboard players set @a coin 0 ### 모든 플레이어 코인 초기화
> -C \=\ tellraw @a {"text":"게임 시작!","color":"gold"}


R> -R \\ execute as @a at @s if block ~ ~-1 ~ minecraft:gold_block run scoreboard players add @s coin 1 ### 금블록 위면 코인+1
> -C \=\ execute as @a run title @s actionbar {"text":"코인 획득!","color":"yellow"}
> -C \=\ execute as @a run playsound minecraft:entity.experience_orb.pickup master @s


@shop
R> -I \\ execute as @a at @s if entity @s[nbt={SelectedItem:{id:"minecraft:emerald"}}] run scoreboard players remove @s coin 5 ### 에메랄드로 구매
> -C \=\ execute as @a if score @s coin matches ..-1 run tellraw @s {
    "text":"코인이 부족합니다!",
    "color":"red"
}
> -C \\ execute as @a if score @s coin matches 0.. run give @s minecraft:golden_apple 1
> -C \=\ execute as @a run tellraw @s {"text":"구매 완료!","color":"green"}



R> -I \\ execute as @a run say 모든 블록 배치 완료
```

### 출력(발췌)
```
summon minecraft:armor_stand ~ ~ ~-1 {Invisible:1b,NoGravity:1b,Marker:1b,Tags:["mcmd","init"]}
setblock ~ ~ ~ minecraft:command_block[facing=north,conditional=false] replace {Command:"scoreboard objectives add coin dummy",auto:0b,TrackOutput:0b}
summon minecraft:text_display ~ ~1 ~ {text:'{"text":"코인 오브젝트 추가"}',Tags:["mcmd"]}
setblock ~ ~ ~-1 minecraft:chain_command_block[facing=north,conditional=false] replace {Command:"scoreboard players set @a coin 0",auto:1b,TrackOutput:0b}
...
summon minecraft:armor_stand ~1 ~ ~-1 {Invisible:1b,NoGravity:1b,Marker:1b,Tags:["mcmd","shop"]}
setblock ~1 ~ ~ minecraft:command_block[facing=north,conditional=false] replace {Command:"execute as @a at @s if entity @s[nbt={SelectedItem:{id:\"minecraft:emerald\"}}] run scoreboard players remove @s coin 5",auto:0b,TrackOutput:0b}
setblock ~1 ~ ~-1 minecraft:chain_command_block[facing=north,conditional=true] replace {Command:"execute as @a if score @s coin matches ..-1 run tellraw @s {\"text\":\"코인이 부족합니다!\",\"color\":\"red\"}",auto:1b,TrackOutput:0b}
...
```

### CLI
`python -m mcmd --facing <north|south|west|east> --src <path/to/file.mcmd>
`
- `--facing` : 전역 방향 설정 (필수)
- `--src` : 입력 `.ㅡmcmd` 경로 (필수)