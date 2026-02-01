from cs50 import get_int

while True:
    height = get_int("Height : ")
    if (type(height) == int and int(height) >= 1 and int(height) <= 8):
        break

for i in range(1, height + 1):
    print(" " * (height - i) + "#" * i)
