def generate_hastag(text):
    text = text.strip()
    text = text.capitalize()  
    hashtag = text.replace(" ", "")  
    if hashtag == 0 or len(hashtag) > 140:
        return False
    if hashtag == "":
        return False
    else:
        True
    hashtag = "#" + hashtag
    
    return hashtag

print(generate_hastag("  hello world  "))  # Output: #HelloWorld