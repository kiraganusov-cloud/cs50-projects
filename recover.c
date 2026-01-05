#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // accept a single command-line argument
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }

    // open the memory card
    FILE *card = fopen(argv[1], "r");
    if (card == NULL)
    {
        printf("File could not be opened\n");
        return 2;
    }
    // buffer
    uint8_t buffer[512];

    int jpeg_counter = 0;
    char file_name[9];
    FILE *file;

    // while there's still data left to read from the memory card
    while (fread(buffer, 1, 512, card) == 512)
    {
        // if the first 4 bytes are the jpeg header (0xff 0xd8 0xff 0xe?)
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            // if its the first file make a new file
            if (jpeg_counter == 0)
            {
                sprintf(file_name, "%03i.jpg", jpeg_counter);
                file = fopen(file_name, "w");
                jpeg_counter++;
            }
            // else if its not the first file close the previous file and open a new one
            else
            {
                fclose(file);
                sprintf(file_name, "%03i.jpg", jpeg_counter);
                file = fopen(file_name, "w");
                jpeg_counter++;
            }
            fwrite(buffer, 1, 512, file);
        }
        // else : write into the currently opened file
        else
        {
            if (jpeg_counter != 0)
            {
                fwrite(buffer, 1, 512, file);
            }
        }
    }
    if (jpeg_counter != 0)
    {
        fclose(file);
    }
}
