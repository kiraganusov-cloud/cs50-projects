from cs50 import get_float

dollars = get_float("Change: ")

cents = dollars * 100
coins = 0
#check quarters
while (cents >= 25):
    cents -= 25
    coins += 1

#check dines
while (cents >= 10):
    cents -= 10
    coins += 1

#check nickels
while (cents >= 5):
    cents -= 5
    coins += 1

#check pennies
while (cents >= 1):
    cents -= 1
    coins += 1

#print min coins
print(coins)
