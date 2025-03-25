import chardet

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    result = chardet.detect(raw_data)
    return result['encoding']

def filter_words(input_file, output_file):
    file_encoding = detect_encoding(input_file)
    print(f"Detected file encoding: {file_encoding}")

    with open(input_file, 'r', encoding=file_encoding, errors='ignore') as infile:
        words = infile.readlines()

    filtered_words = [word.strip() for word in words if len(word.strip()) >= 8]

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for word in filtered_words:
            outfile.write(word + '\n')

    print(f"Done! Filtered words saved to {output_file}")

if __name__ == "__main__":
    input_file = input('Enter the name of the wordlist: ')
    output_file = input('Enter the name of the output file: ')
    filter_words(input_file, output_file)
