s = "钟山风雨起苍黄，百万雄师过大江。\
虎踞龙盘今胜昔，天翻地覆慨而慷。\
宜将剩勇追穷寇，不可沽名学霸王。\
天若有情天亦老，人间正道是沧桑。"
lines = ""
#**********Program**********

sh = 0
po_line = []
for i in range(len(s)):
    if s[i] == '，' or s[i] == '。':
        po_line.append(s[sh: i])
        sh = i+1
for i in po_line:
    lens = len(i)
    lines += (" " * int((30 - lens) / 2))
    lines += (i)
    lines += (" " * int((30 - lens) / 2))
    lines += ("\n")

#**********  End  **********

fo = open("七律.txt", "w")
fo.write(lines)
fo.close()