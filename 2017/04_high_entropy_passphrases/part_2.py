"""
For added security, yet another system policy has been put in place.
Now, a valid passphrase must contain no two words that are anagrams of each other -
that is, a passphrase is invalid if any word's letters can be rearranged
to form any other word in the passphrase.

For example:

-   abcde fghij is a valid passphrase.
-   abcde xyz ecdab is not valid - the letters from the third word
    can be rearranged to form the first word.
-   a ab abc abd abf abj is a valid passphrase,
    because all letters need to be used when forming another word.
-   iiii oiii ooii oooi oooo is valid.
-   oiii ioii iioi iiio is not valid - any of these words
    can be rearranged to form any other word.

Under this new system policy, how many passphrases are valid?
"""


def is_valid(passphrase: str) -> bool:
    words = set()

    for word in passphrase.split(" "):
        hashed_word = "".join(sorted(word))
        if hashed_word in words:
            return False
        words.add(hashed_word)

    return True


assert is_valid("abcde fghij") is True
assert is_valid("abcde xyz ecdab") is False
assert is_valid("a ab abc abd abf abj") is True
assert is_valid("iiii oiii ooii oooi oooo") is True
assert is_valid("oiii ioii iioi iiio") is False


with open("2017/04_high_entropy_passphrases/input.txt") as f:
    passphrases = [line.strip() for line in f]
    print(sum(map(is_valid, passphrases)))
