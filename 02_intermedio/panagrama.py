def is_panagram(sentence):
    cleaned_sentence = ''.join(filter(str.isalpha, sentence.lower()))

    unique_letters = set(cleaned_sentence)

    return len(unique_letters) == 26