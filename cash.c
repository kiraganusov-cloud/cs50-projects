#include <cs50.h>
#include <stdio.h>
int main(void)
{
    // ask for change owed in cents
    // repeat asking if it is less than 0
    int cents;
    do
    {
        cents = get_int("Change owed: ");
    }
    while (cents < 0);
    // declaring the variables to counts amount of each coin per type of coin
    int qnumber = 0;
    int dnumber = 0;
    int nnumber = 0;
    int pnumber = 0;
    // calculate amount of quarters needed
    while (cents >= 25)
    {
        qnumber++;
        cents -= 25;
    }

    // calculate the amount of dimes you can give
    while (cents >= 10)
    {
        dnumber++;
        cents -= 10;
    }

    // calculate the amount of nickels you can give
    while (cents >= 5)
    {
        nnumber++;
        cents -= 5;
    }

    // calculate the amount of pennies you should give
    while (cents >= 1)
    {
        pnumber++;
        cents -= 1;
    }
    // add up the numbers of each kind of coin and then print that number

    int coins = qnumber + dnumber + nnumber + pnumber;
    printf("%i\n", coins);
}
