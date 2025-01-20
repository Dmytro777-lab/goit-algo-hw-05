import pandas as pd
import timeit
from charset_normalizer import detect


def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps


def kmp_search(main_string, pattern):
    M = len(pattern)
    N = len(main_string)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1


def build_shift_table(pattern):
    table = {}
    length = len(pattern)

    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1

    table.setdefault(pattern[-1], length)
    return table


def boyer_moore_search(text, pattern):
    shift_table = build_shift_table(pattern)
    i = 0

    while i <= len(text) - len(pattern):
        j = len(pattern) - 1

        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1

        if j < 0:
            return i

        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    return -1


def polynomial_hash(s, base=256, modulus=101):
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value


def rabin_karp_search(main_string, substring):
    substring_length = len(substring)
    main_string_length = len(main_string)

    base = 256
    modulus = 101

    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(
        main_string[:substring_length], base, modulus)

    h_multiplier = pow(base, substring_length - 1) % modulus

    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i:i + substring_length] == substring:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash -
                                  ord(main_string[i]) * h_multiplier) % modulus
            current_slice_hash = (
                current_slice_hash * base + ord(main_string[i + substring_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1


def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = detect(f.read())
        return result['encoding']


encoding1 = detect_encoding('text1.txt')
encoding2 = detect_encoding('text2.txt')


with open('text1.txt', 'r', encoding=encoding1) as f1, open('text2.txt', 'r', encoding=encoding2) as f2:
    text1 = f1.read()
    text2 = f2.read()

substring_exist = "example"
substring_non_exist = "not_in_text"


def measure_time(search_function, text, pattern):
    return timeit.timeit(lambda: search_function(text, pattern), number=1)


results = []

for text, text_name in [(text1, "text1"), (text2, "text2")]:
    for pattern, pattern_type in [(substring_exist, "Existing"), (substring_non_exist, "Non-Existing")]:
        results.append({
            "Text": text_name,
            "Pattern Type": pattern_type,
            "Algorithm": "Boyer-Moore",
            "Time": measure_time(boyer_moore_search, text, pattern)
        })
        results.append({
            "Text": text_name,
            "Pattern Type": pattern_type,
            "Algorithm": "Knuth-Morris-Pratt",
            "Time": measure_time(kmp_search, text, pattern)
        })
        results.append({
            "Text": text_name,
            "Pattern Type": pattern_type,
            "Algorithm": "Rabin-Karp",
            "Time": measure_time(rabin_karp_search, text, pattern)
        })

df = pd.DataFrame(results)
df.sort_values(by=["Text", "Pattern Type", "Time"], inplace=True)

# Сохранение результатов в файл
df.to_csv('algorithm_performance.csv', index=False)
print("Результаты сохранены в файл algorithm_performance.csv")
