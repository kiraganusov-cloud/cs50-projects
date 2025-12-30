#include <cs50.h>
#include <stdio.h>
#include <string.h>

string code_array;
string convert(string plaintext);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    else if (argc == 2)
    {
        if (strlen(argv[1]) != 26)
        {
            printf("Key must contain 26 characters.\n");
            return 1;
        }
    }
    code_array = argv[1];

    string plaintext = get_string("plaintext: ");
    printf("ciphertext: %s\n", convert(plaintext));
}

string convert(string plaintext)
{
    string ciphertext = plaintext;
    int index = 0;
    for (int i = 0; i < strlen(plaintext); i++)
    {
        if ('A' <= plaintext[i] && plaintext[i] <= 'Z')
        {
            index = plaintext[i] - 'A';
        }
        else if ('a' <= plaintext[i] && plaintext[i] <= 'z')
        {
            index = plaintext[i] - 'a';
        }
        ciphertext[i] = code_array[index];
    }
    return ciphertext;
}
