import random
import string

def generate_random_words(prefix, min_length, max_length, count, custom_characters):
    words = []
    for _ in range(count):
        random_length = random.randint(min_length - len(prefix), max_length - len(prefix))
        random_part = ''.join(random.choice(custom_characters) for _ in range(random_length))
        word = prefix + random_part
        words.append(word)
    return words

def save_to_file(words, filename):
    with open(filename, 'w') as file:
        for word in words:
            file.write(word + '\n')

if __name__ == "__main__":
    prefix = input("Enter the fixed prefix (or leave blank for fully random passwords): ")
    min_length = int(input("Enter the minimum length of the password: "))
    max_length = int(input("Enter the maximum length of the password: "))
    count = int(input("Enter the number of passwords to generate: "))
    filename = input("Enter the filename to save the passwords: ")
    custom_characters = input("Enter the characters, numbers, or symbols you want to use (or leave blank for default): ")
    
    if not custom_characters:
        custom_characters = string.ascii_letters + string.digits + "!@#$%^&*"
    
    if min_length > max_length:
        print("Error: Minimum length cannot be greater than maximum length.")
    elif min_length < len(prefix):
        print("Error: Minimum length cannot be less than the length of the prefix.")
    else:
        words = generate_random_words(prefix, min_length, max_length, count, custom_characters)
        save_to_file(words, filename)
        print(f"{count} passwords have been generated and saved to the file {filename}.")
