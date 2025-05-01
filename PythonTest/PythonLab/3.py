ks = input()

for i in ks:
    print(chr((ord(i) - ord('a') - 3) % 26 + ord('a')), end='')
