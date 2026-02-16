from cs50 import get_string


text = get_string("Text: ")

letters = 0
words = 0
sentences = 0

for char in text:
    # count words
    if (char == " "):
        words += 1

    # count sentences
    elif (char == "." or char == "?" or char == "!"):
        sentences += 1

    # count letters
    elif (char.isalpha()):
        letters += 1

words += 1

# print(f"Words: {words}, Letters: {letters}, Sentences: {sentences}")


L = (letters / words) * 100
S = (sentences / words) * 100

index = 0.0588 * L - 0.296 * S - 15.8
grade = round(index)

if index < 1:
    print("Before Grade 1")
elif index >= 16:
    print("Grade 16+")
else:
    print(f"Grade: {grade}")
