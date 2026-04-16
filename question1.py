# Function to shift a character inside its own group
# This function keeps characters within a specific range (e.g., a-m or n-z)
# and applies circular shifting using modulo arithmetic.
def shift_within_group(char, group_start, group_size, shift, forward=True):
    # find the position of the character inside the group
    offset = ord(char) - ord(group_start)

    # move forward or backward inside the group using modulo for wrap-around
    if forward:
        new_offset = (offset + shift) % group_size
    else:
        new_offset = (offset - shift) % group_size

    # convert back to a character
    return chr(ord(group_start) + new_offset)


# Function to encrypt one character based on assignment rules
# Each group (a-m, n-z, A-M, N-Z) uses a different transformation rule
def encrypt_char(char, shift1, shift2):

    # lowercase a-m → shift forward by shift1 * shift2
    if 'a' <= char <= 'm':
        return shift_within_group(char, 'a', 13, shift1 * shift2, forward=True)

    # lowercase n-z → shift backward by shift1 + shift2
    elif 'n' <= char <= 'z':
        return shift_within_group(char, 'n', 13, shift1 + shift2, forward=False)

    # uppercase A-M → shift backward by shift1
    elif 'A' <= char <= 'M':
        return shift_within_group(char, 'A', 13, shift1, forward=False)

    # uppercase N-Z → shift forward by shift2 squared
    elif 'N' <= char <= 'Z':
        return shift_within_group(char, 'N', 13, shift2 * shift2, forward=True)

    # non-alphabet characters remain unchanged
    return char


# Function to decrypt one character
# Decryption reverses the exact transformation applied during encryption
def decrypt_char(char, shift1, shift2):

    # lowercase a-m → reverse of forward shift → shift backward
    if 'a' <= char <= 'm':
        return shift_within_group(char, 'a', 13, shift1 * shift2, forward=False)

    # lowercase n-z → reverse of backward shift → shift forward
    elif 'n' <= char <= 'z':
        return shift_within_group(char, 'n', 13, shift1 + shift2, forward=True)

    # uppercase A-M → reverse of backward shift → shift forward
    elif 'A' <= char <= 'M':
        return shift_within_group(char, 'A', 13, shift1, forward=True)

    # uppercase N-Z → reverse of forward shift → shift backward
    elif 'N' <= char <= 'Z':
        return shift_within_group(char, 'N', 13, shift2 * shift2, forward=False)

    # non-alphabet characters remain unchanged
    return char


# Function to process the whole text
# Applies encryption or decryption character by character
def transform_text(text, shift1, shift2, encrypt=True):
    result = ""

    # iterate through each character in the text
    for char in text:
        if encrypt:
            result += encrypt_char(char, shift1, shift2)
        else:
            result += decrypt_char(char, shift1, shift2)

    return result


# Function to encrypt the file
# Reads raw_text.txt and writes encrypted result to encrypted_text.txt
def encrypt_file(shift1, shift2):
    with open("raw_text.txt", "r", encoding="utf-8") as file:
        original_text = file.read()

    encrypted_text = transform_text(original_text, shift1, shift2, encrypt=True)

    with open("encrypted_text.txt", "w", encoding="utf-8") as file:
        file.write(encrypted_text)


# Function to decrypt the file
# Reads encrypted_text.txt and writes decrypted result to decrypted_text.txt
def decrypt_file(shift1, shift2):
    with open("encrypted_text.txt", "r", encoding="utf-8") as file:
        encrypted_text = file.read()

    decrypted_text = transform_text(encrypted_text, shift1, shift2, encrypt=False)

    with open("decrypted_text.txt", "w", encoding="utf-8") as file:
        file.write(decrypted_text)


# Function to verify the result
# Compares original and decrypted text to ensure correctness
def verify_decryption():
    with open("raw_text.txt", "r", encoding="utf-8") as file:
        original_text = file.read()

    with open("decrypted_text.txt", "r", encoding="utf-8") as file:
        decrypted_text = file.read()

    if original_text == decrypted_text:
        print("Verification successful: decrypted text matches original text.")
    else:
        print("Verification failed: decrypted text does not match original text.")


# Main function
# Takes user input for shift values and runs the full process
def main():
    shift1 = int(input("Enter shift1: "))
    shift2 = int(input("Enter shift2: "))

    encrypt_file(shift1, shift2)
    decrypt_file(shift1, shift2)
    verify_decryption()


# Program entry point
if __name__ == "__main__":
    main()
