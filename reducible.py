"""
This program finds the longest reducible words from a given word list.
A word is reducible if removing one letter at a time eventually reduces it to
a single-letter word ('a', 'i', or 'o').

It uses a hash table with double hashing for efficient lookup and memoization
to speed up reducibility checks.
"""
import sys
STEP_SIZE_CONSTANT = 3


def is_prime(n):
    """Returns True if n is prime, otherwise False.
    Parameters:
    int n
    Returns:
    int n"""
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    for div in range(3, int(n ** 0.5) + 1, 2):
        if n % div == 0:
            return False
    return True


def next_prime(n):
    """Finds the next prime number greater than or equal to n."""
    while not is_prime(n):
        n += 1
    return n


def hash_word(s, size):
    """Hashes a lowercase string to an index in a hash table."""
    hash_idx = 0
    for c in s:
        letter = ord(c) - 96  # Convert 'a' to 1, 'b' to 2, ..., 'z' to 26
        hash_idx = (hash_idx * 26 + letter) % size
    return hash_idx


def step_size(s):
    """Calculates step size for double hashing to avoid infinite loops."""
    step = STEP_SIZE_CONSTANT - (hash_word(s, STEP_SIZE_CONSTANT) % STEP_SIZE_CONSTANT)
    return max(step, 1)  # Ensure step size is never 0


def insert_word(s, hash_table):
    """Inserts a string into the hash table using double hashing for collision resolution."""
    table_size = len(hash_table)
    index = hash_word(s, table_size)

    if hash_table[index] == "":
        hash_table[index] = s
        return

    step = step_size(s)
    original = index

    while hash_table[index] != "":
        if hash_table[index] == s:  # Avoid inserting duplicates
            return
        index = (index + step) % table_size
        if index == original:  # Prevent infinite loop
            return
    hash_table[index] = s


def find_word(s, hash_table):
    """Searches for a string in the hash table."""
    table_size = len(hash_table)
    index = hash_word(s, table_size)
    step = step_size(s)

    while hash_table[index] != "":
        if hash_table[index] == s:
            return True
        index = (index + step) % table_size
    return False


def is_reducible(s, hash_table, hash_memo):
    """Checks if a word is reducible by recursively reducing it."""
    if s in ["a", "i", "o"]:  # Base case: single-letter words
        return True
    if find_word(s, hash_memo):  # If memoized, return True
        return True

    for i in range(len(s)):
        sub_word = s[:i] + s[i + 1:]  # Remove one character
        if find_word(sub_word, hash_table) and is_reducible(sub_word, hash_table, hash_memo):
            insert_word(s, hash_memo)  # Memoize reducible words
            return True

    return False


def get_longest_words(string_list):
    """Finds the longest words from a list. 
    
    Returns a list of the longest words in `string_list`. 
    If the input list is empty, returns an empty list.

    Parameters:
    string_list (list[str]): A list of words.

    Returns:
    list[str]: A list containing the longest words.
    """
    if not string_list: 
        return []
    max_length = max(len(word) for word in string_list)
    return [word for word in string_list if len(word) == max_length]


def main():
    """The main function that calculates the longest reducible words."""
    word_list = []
    try:
        for line in sys.stdin:
            word = line.strip()
            if word:
                word_list.append(word)
    except EOFError:
        pass

    word_list_length = len(word_list)
    if word_list_length == 0:
        return

    # Determine prime numbers for hash tables
    n_ = next_prime(2 * word_list_length)
    m_= next_prime(int(0.2 * word_list_length) + 1)

    # Create hash tables
    hash_list = [""] * n_
    hash_memo = [""] * m_

    # Insert words into hash table
    for word in word_list:
        insert_word(word, hash_list)

    # Find reducible words
    reducible_words = [word for word in word_list if is_reducible(word, hash_list, hash_memo)]

    # Get longest reducible words
    longest_reducible_words = get_longest_words(reducible_words)

    # Print longest reducible words in alphabetical order
    for word in sorted(longest_reducible_words):
        print(word)


if __name__ == "__main__":
    main()
