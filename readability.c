#include <cs50.h>
#include <stdio.h>
#include <math.h>
#include <string.h>
#include <ctype.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);
int calculate_readability(string text);

int main(void)
{
    // prompt for sentence
    string text = get_string("Text: ");

    // calculate readability
    int readability = calculate_readability(text);
    
    // print readability
    if (readability < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (readability < 16)
    {
        printf("Grade %i\n", readability);
    }
    else
    {
        printf("Grade 16+\n");
    }
}

int count_letters(string text)
{
    int letters = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (isalpha(text[i]))
        {
            letters++;
        }
    }
    return letters;
}

int count_words(string text)
{
    int words = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (isblank(text[i]))
        {
            words++;
        }
    }
    return words + 1;
}

int count_sentences(string text)
{
    int sentences = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        char letter = text[i];
        if (letter == '.' || letter == '!' || letter == '?')
        {
            sentences++;
        }
    }
    return sentences;
}

int calculate_readability(string text)
{
    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);

    float L = (float)letters/words * 100;
    float S = (float)sentences/words * 100;

    return round(0.0588 * L - 0.296 * S - 15.8);
}
