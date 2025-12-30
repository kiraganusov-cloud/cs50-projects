#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

string code_array;
int check_key(string key);
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
    if (check_key(argv[1]) != 0)
    {
        printf("Invalid key\n");
    }
    code_array = argv[1];

    string plaintext = get_string("plaintext: ");
    printf("ciphertext: %s\n", convert(plaintext));
    return 0;
}

int check_key(string key)
{
    for (int i = 0; i < strlen(key); i++)
    {
        if (!isalpha(key[i]))
        {
            return 1;
        }
    }
    for (int i = 0; i < strlen(key); i++)
    {
        for (int j = i + 1; j < strlen(key); j++)
        {
            if (tolower(key[j]) == tolower(key[i]))
            {
                return 1;
            }
        }
    }
    return 0;
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
            cipher = toupper(code_array[index]);
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
