# MCMD 마크 커맨드 

이 프로젝트는 마인크래프트 커맨드 블록의 작성을 쉽고 한 눈에 볼 수 있게 도와주는 변환기를 만든다.

---

### 작성법
#### 기초
##### 파일 이름 작성법
- 파일명은 `{파일이름}.mcmd` 로 작성한다.<br

##### CLI 사용법
- CLI 는 다음과 같이 사용한다. `python -m mcmd --facing="<north | south | west | east>" --src="{filename}.mcmd"`
#### .mcmd 작성법
mcmd 작성 규칙은 다음과 같다.
1. 한 커맨드에 들어갈 코드의 시작마다 `>` 혹은 `R>` 를 작성한다. <br> `>` 는 항상 활성화를 말한다. `R>` 은 레드스톤 필요를 말한다.

2. 한 커맨드에 들어갈 코드의 시작에있는 `>` 혹은 `R>` 뒤에 커맨드 블록의 종류(반복,반응,체인)을 명시한다.<br>
`-I` 혹은 `--impulse` 는 반응형 커맨드 블록이다.<br>
`-R` 혹은 `--repeat` 는 반복형 커맨드 블록이다. <br>
`-C` 혹은 `--chain` 는 체인 커맨드블록이다.

3. (선택사항) 종류 명시이후 커맨드블록을 위로 올릴것인지 명시한다.<br> `-M=<int>` 혹은 `--mount=<int>` 식으로 쓴다. 이 코드가 들어간 블록은 위쪽 코드로 작성된 커맨드 블록의 y좌표의 `<int>`만큼 위에 무조건 위쪽 방향으로 바라보고 설치된다

4. 종류 혹은 마운트 명시 이후 커맨드 블록의 타입(조건적, 무조건적)을 명시한다.<br>`\\` 는 무조건적 커맨드블록이다.<br>
`\=\` 는 조건적 커맨드 블록이다.

5. 이후 코드는 커맨드 블록 내부에 그대로 작성된다. 코드는 엔터 없이 다음 `>` 혹은 `R>` 을 만날때 까지 개행 없이 작성된다. 단, 코드내부에 작성된 엔터가 아닌 개행`\n` 은 그대로 작성된다.

6. 주석 코드 가장 끄트머리에만 작성한다. `###` 을 쓰며, 이 주석은 command 블록의 y좌표 한블록 위에 textdisplay 소환하고, 그 내부에 작성된다.<br> 엔티티의 태그는 `mcmd` 이다.  

8. 커맨드블록 뭉치를 때고 싶으면 세번 이상 개행하여 구분한다

예시:<br>

`CLI >> py -m mcmd --facing="north" --src="./asdf.mcmd"`

```
R> -I \\ execute @a at @s run tellraw @s {"text":"hello"} ### 모두에게 헬로 출력

R> -R \\ execute as @a at @s if block ~ ~ ~ minectaft:stone run damage @s 10 ### 발아래 돌블록 감지
> -C \=\ execute as @a at @s run 
tellraw @a [
    {text:"hello",color:"red"},
    {text:"you dead",color:"blue"}
]
> -C \=\ execute as @p at @s run kill @s 



R> -I \\ execute @a at @s run tellraw @s {"text":"hello22"} ### 모두에게 헬로22 출력



R> -I \\ execute @a at @s run tellraw @s {"text":"hello333"} ### 모두에게 헬로333 출력
```

설명:
위족 커맨드들은 cli에서 제시한듯이 모두 북쪽을 바라본다.<br>
위쪽 임펄스, 반복, 체인*3 은 한줄로 연결이 되어있다.

아래쪽 세번 개행된 반응 커맨드는 오른쪽으로 한칸띄워 북쪽을 바라보고 설치되어있다.

그 아럐쪽 세번 개행된 반응 커맨드는 그 오른쪽으로 한칸 띄워 설치되어있다.

#### 심화 코드 작성법
(필수는 아니다.)<br>
처음 작성하거나 세번 개행구분하여 작성할때, `@` 를 사용하여 그 아래 작성될 커맨드가 바라보는 방향의 뒷쪽 에 마커를 소환, `@` 뒤에 문자열이 그 마커의 태그가 된다. <br>
`@` 는 3번 개행을 안했어도 3번 개행한것으로 간주한다.<br>
예:
```
@init    <--- init 태그를 가진 마커 생성
R> -I \\ execute as @a at @s run scoreboard players set coin coin 0 ### 돈 리셋
> -C \=\ execute as @a at @s run scoreboard players set atk stat 20 ### 공격력 리셋



@kill   <--- kill 태그를 가진 마커 생성
R> -R \\ execute as @a at @s if block ~ ~-1 ~ minecraft:stone run kill @s
```
`□⟨□⟨□` 이렇게 설치될때, `□⟨□⟨□■` 채워진 네모쪽에 마커를 소환

### 출력
mcmd 실행파일이 있는 폴더에 `out_{.mcmd 파일명}.txt` 파일을 만들고, 그 파일 내부에는 .mcmd를 작성한 코드를 원커맨드 형식으로 만들어 작성한다.