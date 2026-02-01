height = 0
while (height < 1 or height > 8):
    height = int(input("Height : "))

for i in range(1, height + 1):
    print(" " * (height - i) + "*" * i)
