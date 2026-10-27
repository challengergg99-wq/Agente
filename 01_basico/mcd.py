def mcd(str1, str2):
    while str1 != 0 and str2 != 0:
        if str1 > str2:
            str1 = str1 % str2
        else:
            str2 = str2 % str1
    return str1 + str2

print(mcd(48, 18))  # Output: 6


def mdc(str1, str2):
    if str1 + str2 != str2 + str1:
        return ""

    def gcd(len1, len2):
        while len2:
            len1, len2 = len2, len1 % len2
        return len1

    return str1[:gcd(len(str1), len(str2))]

print(mdc("ABCABC", "ABC"))  # Output: "ABC"