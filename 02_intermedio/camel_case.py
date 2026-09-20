def to_camel_case(text):
    if not text:
        return ""
    words = text.replace("_","-").split("-")
    camel_case = words[0] + "".join(word.capitalize() for word in words[1:])
    return camel_case