import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        print("Incorrect command line arguement")
        return 1

    # TODO: Read database file into a variable
    database = open(sys.argv[1])
    reader = csv.DictReader(database)

    people = []

    for row in reader:
        people.append(row)

    strs = reader.fieldnames[1:]

    # TODO: Read DNA sequence file into a variable
    sequence = open(sys.argv[2])
    dna_sequence = sequence.read()


    # TODO: Find longest match of each STR in DNA sequence
    sequence_results = []

    for i in strs:
        sequence_results.append(longest_match(dna_sequence, i))


    # TODO: Check database for matching profiles
    for person in people:

        case = True

        for i in range(len(strs)):
            if int(person[strs[i]]) != sequence_results[i]:
                case = False
                break

        if case:
            print(person["name"])
            return

    print("No match")
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in sequence, return longest run found
    return longest_run


main()
