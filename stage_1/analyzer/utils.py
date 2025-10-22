import hashlib

#Calculates the length of the text
def get_length(text):
    counted = 0
    for i in text:
        counted += 1
    return counted

#Boolean indicating if the string reads the same forwards and backwards (case-insensitive)
def is_palindrome(text):
    new_text = text.lower()
    cleaned_text = ""
    for char in new_text:
        if char.isalnum():
            cleaned_text += char
    reversed_text = ""
    for i in cleaned_text:
        reversed_text = i + reversed_text
    return cleaned_text == reversed_text


#Count of distinct characters in the string
def unique_characters(text):
    new_list = []
    for i in text:
        if i != " " and i not in new_list:
            new_list.append(i)
    return len(new_list)


#Number of words separated by whitespace
def word_count(text):
    trimmed_text = text.strip()
    counted = 0
    in_word = False
    for i in trimmed_text:
        if i != " " and not in_word:
            counted += 1
            in_word = True
        elif i == " ":
            in_word = False

    return counted

#SHA-256 hash of the string for unique identification
def sha256_hash(text):
    hash_object = hashlib.sha256(text.encode()) #converts the text into bytes 
    return hash_object.hexdigest() #returns a readable hexadecimal string version of the hash

#Object/dictionary mapping each character to its occurrence count
def character_frequency_map(text):
    empty_dict = {}
    for i in text:
        if i in empty_dict:
            empty_dict[i] += 1
        else:
            empty_dict[i] = 1

    return empty_dict
