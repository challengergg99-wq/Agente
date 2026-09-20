# Task
# You've definitely seen this formula in an algebra class in high school:
# Not too hard, right? Your task is to output an expression of the form sin(n * x) with an input of a value of n. Note, that n can be in range from [-3000, 3000] but don't worry, there will only be 5 tests for |n| > 1000 cases.
# Like in the original kata, you are supposed to output a string in the form sin({coefficient} * x)  ==  {expression}. Every term in an expression should be joined by a space character. The other rules are the same as in every math expression kata:
# The only difference is, in that kata, the powers of cos(x) ascend in an expression, while this kata, requires the powers of sin(x) go up with each term.

# Input
# An integer, representing the coefficient of sin(n * x).

# Output
# A string, representing the whole expansion.




import math

def sin_expression(n):
    if n == 0:
        return "sin(0 * x) == 0"
    
    original_n = n
    is_negative = n < 0
    n = abs(n)
    
    terms = []
    for k in range(1, n + 1, 2):
        coeff = math.comb(n, k)
        if ((k - 1) // 2) % 2 == 1:
            coeff = -coeff
            
        if is_negative:
            coeff = -coeff
            
        cos_pow = n - k
        sin_pow = k
        
        cos_str = ""
        if cos_pow > 0:
            cos_str = "cos(x)" if cos_pow == 1 else f"cos(x)^{cos_pow}"
            
        sin_str = "sin(x)" if sin_pow == 1 else f"sin(x)^{sin_pow}"
        trig_str = f"{cos_str} {sin_str}" if cos_str else sin_str
        
        terms.append((coeff, trig_str))
        
    result_parts = []
    for i, (coeff, trig) in enumerate(terms):
        if coeff == 0:
            continue
            
        abs_coeff = abs(coeff)
        coeff_str = "" if abs_coeff == 1 else f"{abs_coeff}"
        
        if i == 0:
            if coeff < 0:
                sign_and_coeff = f"-{coeff_str}" if coeff_str else "-"
            else:
                sign_and_coeff = coeff_str
        else:
            sign = "- " if coeff < 0 else "+ "
            sign_and_coeff = f"{sign}{coeff_str}" if coeff_str else sign.strip()
            
        if sign_and_coeff:
            if sign_and_coeff.endswith(" ") or not sign_and_coeff:
                result_parts.append(f"{sign_and_coeff}{trig}")
            else:
                if coeff_str:
                    result_parts.append(f"{sign_and_coeff} {trig}")
                else:
                    result_parts.append(f"{sign_and_coeff}{trig}")
        else:
            result_parts.append(trig)
            
    expression = " ".join(result_parts).replace("+  ", "+ ").replace("-  ", "- ")
    return f"sin({original_n} * x) == {expression}"



print(sin_expression(1))  
print(sin_expression(5))  
print(sin_expression(-3))  