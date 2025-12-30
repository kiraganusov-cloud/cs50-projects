#include <cs50.h>
#include <ctype.h>
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
    char cipher;
    for (int i = 0; i < strlen(plaintext); i++)
    {
        if (isupper(plaintext[i]))
        {
            index = plaintext[i] - 'A';
            cipher = code_array[index];
        }
        else if (islower(plaintext[i]))
        {
            index = plaintext[i] - 'a';
            cipher = tolower(code_array[index]);
        }
        else
        {
            cipher = plaintext[i];
        }
        ciphertext[i] = cipher;
    }
    return ciphertext;
}
