summon minecraft:armor_stand ~-1 ~ ~ {Invisible:1b,NoGravity:1b,Marker:1b,Tags:["mcmd","init"]}
setblock ~ ~ ~ minecraft:command_block[facing=east,conditional=false] replace {Command:"scoreboard objectives add coin dummy",auto:0b,TrackOutput:0b}
summon minecraft:text_display ~ ~1 ~ {text:'{"text":"코인 오브젝트 추가"}',Tags:["mcmd"]}
setblock ~1 ~ ~ minecraft:chain_command_block[facing=east,conditional=false] replace {Command:"scoreboard players set @a coin 0",auto:1b,TrackOutput:0b}
summon minecraft:text_display ~1 ~1 ~ {text:'{"text":"모든 플레이어 코인 초기화"}',Tags:["mcmd"]}
setblock ~2 ~ ~ minecraft:chain_command_block[facing=east,conditional=true] replace {Command:"tellraw @a {\"text\":\"게임 시작!\", \"color\":\"gold\"}",auto:1b,TrackOutput:0b}
setblock ~ ~ ~1 minecraft:repeating_command_block[facing=east,conditional=false] replace {Command:"execute as @a at @s if block ~ ~-1 ~ minecraft:gold_block run scoreboard players add @s coin 1",auto:0b,TrackOutput:0b}
summon minecraft:text_display ~ ~1 ~1 {text:'{"text":"금블록 위면 코인+1"}',Tags:["mcmd"]}
setblock ~1 ~ ~1 minecraft:chain_command_block[facing=east,conditional=true] replace {Command:"execute as @a run title @s actionbar {\"text\":\"코인 획득!\", \"color\":\"yellow\"}",auto:1b,TrackOutput:0b}
setblock ~2 ~ ~1 minecraft:chain_command_block[facing=east,conditional=true] replace {Command:"execute as @a run playsound minecraft:entity.experience_orb.pickup master @s",auto:1b,TrackOutput:0b}
summon minecraft:armor_stand ~-1 ~ ~2 {Invisible:1b,NoGravity:1b,Marker:1b,Tags:["mcmd","shop"]}
setblock ~ ~ ~2 minecraft:command_block[facing=east,conditional=false] replace {Command:"execute as @a at @s if entity @s[nbt={SelectedItem:{id:\"minecraft:emerald\"}}] run scoreboard players remove @s coin 5",auto:0b,TrackOutput:0b}
summon minecraft:text_display ~ ~1 ~2 {text:'{"text":"에메랄드로 아이템 구매"}',Tags:["mcmd"]}
setblock ~1 ~ ~2 minecraft:chain_command_block[facing=east,conditional=true] replace {Command:"execute as @a if score @s coin matches ..-1 run tellraw @s { \"text\":\"코인이 부족합니다!\", \"color\":\"red\" }",auto:1b,TrackOutput:0b}
summon minecraft:text_display ~1 ~1 ~2 {text:'{"text":"ㅁㄴㅇㄻㄴㅇㄹ"}',Tags:["mcmd"]}
setblock ~2 ~ ~2 minecraft:chain_command_block[facing=east,conditional=false] replace {Command:"execute as @a if score @s coin matches 0.. run give @s minecraft:golden_apple 1",auto:1b,TrackOutput:0b}
summon minecraft:text_display ~2 ~1 ~2 {text:'{"text":"코인이 충분하면 황금사과 지급"}',Tags:["mcmd"]}
setblock ~3 ~ ~2 minecraft:chain_command_block[facing=east,conditional=true] replace {Command:"execute as @a run tellraw @s {\"text\":\"구매 완료!\",\"color\":\"green\"}",auto:1b,TrackOutput:0b}
setblock ~ ~ ~3 minecraft:command_block[facing=east,conditional=false] replace {Command:"execute as @a run say 모든 블록 배치 완료",auto:0b,TrackOutput:0b}
summon minecraft:text_display ~ ~1 ~3 {text:'{"text":"마지막 확인용 메시지"}',Tags:["mcmd"]}
