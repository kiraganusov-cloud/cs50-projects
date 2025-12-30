#include <stdio.h>
#include <cs50.h>
#include <string.h>

int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
int letter_points(int letter);
int word_points(string word);

int main(void)
{
    //ask for users word
    string answer1 = get_string("Player 1: ");
    int points1 = word_points(answer1);
    // find the points for each letter and add together

    string answer2 = get_string("Player 2: ");
    int points2 = word_points(answer2);

    if (points1 > points2)
    {
        printf("Player 1 wins!\n");
    }
    else if (points2 > points1)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
}

int word_points(string word)
{
    int sum = 0;
    for(int i = 0; i < strlen(word); i++)
    {
        sum += letter_points(word[i]);
    }
    return sum;
}

int letter_points(int letter)
{
    if (65 <= letter && letter <= 90)
    {
        return POINTS[letter - 'A'];
    }
    else if (97 <= letter && letter <= 122)
    {
        return POINTS[letter - 'a'];
    }
    else
    {
        return 0;
    }
}
