#include <cs50.h>
#include <stdio.h>

void print_row(int bricks);

int main(void)
{
    //prompt for input
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1);

    //print pyramid
    for (int i = 0; i < height; i++)
    {
        for (int s = height - i; s > 0; s--)
        {
            printf(" ");
        }
        print_row(i+1);
    }
}
void print_row(int bricks)
{
    for (int i = 0; i < bricks; i++)
    {
        printf("#");
    }
    printf("\n");
}

