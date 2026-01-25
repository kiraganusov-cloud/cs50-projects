// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];
int table_size = 0;
bool free_node(node *node);
void convert_toupper(char *word);

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    char upper_word[LENGTH + 1];
    strcpy(upper_word, word);
    convert_toupper(upper_word);
    // printf("looking for %s\n", word);
    // find index in table array (bucket)
    unsigned int index = hash(word);

    // check linked list in position[index] and iterate until word is found
    node *word_node = table[index];
    while (word_node != NULL)
    {
        // printf("word here is %s\n", word_node->word);
        if (strcmp(word_node->word, upper_word) == 0)
        {
            // printf("found it\n");
            return true;
        }
        word_node = word_node->next;
        // printf("got next\n");
    }
    // printf("didnt find it\n");
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    return toupper(word[0]) - 'A';
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }

    // open the dictionary file and read line by line because each line is one word
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }
    char buffer[LENGTH + 1];
    while (fscanf(file, "%s\n", buffer) != EOF)
    {
        convert_toupper(buffer);
        // printf("buffer: %s\n", buffer);
        node *node = malloc(sizeof(struct node));
        strcpy(node->word, buffer);
        node->next = NULL;
        // for each word, get index from hash function
        int index = hash(buffer);
        // add the word to the linked list in that index
        node->next = table[index];
        table[index] = node;
        table_size++;
    }
    fclose(file);
    // printf("table size is %i\n", table_size);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return table_size;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // printf("got to unload\n");
    // go through every index of the table
    for (int i = 0; i < N; i++)
    {
        node *node = table[i];
        // go through every item in the linked list and free it
        if (table[i] != NULL)
        {
            free_node(node);
        }
    }
    return true;
}

bool free_node(node *node)
{
    if (node->next != NULL)
    {
        free_node(node->next);
    }
    free(node);
    return true;
}

void convert_toupper(char *word)
{
    for (int i = 0; i < strlen(word); i++)
    {
        word[i] = toupper(word[i]);
    }
}
