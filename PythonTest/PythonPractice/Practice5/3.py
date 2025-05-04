def string_num(ch):
    letters = 0
    digits = 0
    spaces = 0
    others = 0
    for char in ch:
        if char.isalpha():
            letters += 1
        elif char.isdigit():
            digits += 1
        elif char.isspace():
            spaces += 1
        else:
            others += 1
    return letters, digits, spaces, others

ch = input()
letters, digits, spaces, others = string_num(ch)
print(f"统计结果：字母有{letters}个，数字有{digits}个，空格有{spaces}个，其他字符有{others}个。")