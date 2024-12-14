import argparse
import os
from collections import Counter
import re

def read_file(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        exit(1)

def clean_text(text):
    return re.findall(r'[а-яА-Я0-9-]+', text)

def count_words(text_list):
    return dict(Counter(text_list))

def save_word_counts(file_name, word_counts):
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    try:
        with open(file_name, 'w', encoding='utf-8') as file:
            for word, count in sorted_words:
                file.write(f"{word}: {count}\n")
    except IOError:
        print(f"Error: Unable to write to file '{file_name}'.")

def calculate_statistics(text, word_counts):
    punctuation = ['.', ',', ';', '?', '!', '"', '...']
    stats = {punct: text.count(punct) for punct in punctuation}

    for length in range(1, 21):
        stats[length] = sum(count for word, count in word_counts.items() if len(word) == length)

    stats['unique_words'] = len(word_counts)
    return stats

def save_statistics(file_name, stats):
    try:
        with open(file_name, 'w', encoding='utf-8') as file:
            for key, value in stats.items():
                file.write(f"{key}: {value}\n")
    except IOError:
        print(f"Error: Unable to write to file '{file_name}'.")

def main():
    parser = argparse.ArgumentParser(description="Text statistics generator")
    parser.add_argument('input_file', help="Path to the input text file")
    parser.add_argument('--output_dir', default='result', help="Directory to save output files")
    args = parser.parse_args()

    input_file = args.input_file
    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)

    text = read_file(input_file).lower()
    words = clean_text(text)

    word_counts = count_words(words)
    words_output_file = os.path.join(output_dir, os.path.basename(input_file).replace('.txt', '_words.txt'))
    save_word_counts(words_output_file, word_counts)

    stats = calculate_statistics(text, word_counts)
    stats_output_file = os.path.join(output_dir, os.path.basename(input_file).replace('.txt', '_stat.txt'))
    save_statistics(stats_output_file, stats)

    print(f"Processing complete! Results saved in '{output_dir}'.")
    print(f"Total words: {sum(word_counts.values())}")
    print(f"Unique words: {len(word_counts)}")
    print("Top 5 words:")
    for word, count in list(word_counts.items())[:5]:
        print(f"{word}: {count}")

if __name__ == "__main__":
    main()
