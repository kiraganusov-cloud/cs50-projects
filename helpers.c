#include "helpers.h"
#include <math.h>
#include <stdio.h>

// Return the min of two bytes

BYTE cap_255(float value)
{
    if (value > 255)
    {
        return 255;
    }
    return value;
}


// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            BYTE average = round((image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.0);
            image[i][j].rgbtRed = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtBlue = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            BYTE originalRed = image[i][j].rgbtRed;
            BYTE originalGreen = image[i][j].rgbtGreen;
            BYTE originalBlue = image[i][j].rgbtBlue;

            BYTE sepiaRed = cap_255(round(.393 * originalRed + .769 * originalGreen + .189 * originalBlue));
            BYTE sepiaGreen = cap_255(round(.349 * originalRed + .686 * originalGreen + .168 * originalBlue));
            BYTE sepiaBlue = cap_255(round(.272 * originalRed + .534 * originalGreen + .131 * originalBlue));

            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE tmp;
    for (int i = 0; i < height; i++)
    {
        for(int j = 0; j < width / 2; j++)
        {
            tmp = image[i][j];
            image[i][j] = image[i][width - j - 1];
            image[i][width - j - 1] = tmp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Create a copy of image
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    // blur
    for (int i = 0; i < height; i++)
    {
        for(int j = 0; j < width; j++)
        {
            int accRed = 0, accGreen = 0, accBlue = 0;
            float count = 0;
            for (int row = fmax(i - 1, 0); row < fmin(i + 2, height); row++)
            {
                for (int col = fmax(j - 1, 0); col < fmin(j + 2, width); col++)
                {
                    count++;
                    accRed += copy[row][col].rgbtRed;
                    accGreen += copy[row][col].rgbtGreen;
                    accBlue += copy[row][col].rgbtBlue;
                }
            }
            image[i][j].rgbtRed = cap_255(accRed / count);
            image[i][j].rgbtGreen = cap_255(accGreen / count);
            image[i][j].rgbtBlue = cap_255(accBlue / count);

        }
    }

    return;
}
