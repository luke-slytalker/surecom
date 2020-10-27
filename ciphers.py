
# obfuscate text to add an additional degree of "eh.. it's probably just garbage"
def lukefuscate(text):
    obfs = str.maketrans('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890=-+/',
                         't]Uv[0Wxy}1;:2{>,9.?Z5!zA@#<$C%^&*bDQrSe8)PFo`N(37gm~4H|i-L6kJ+_O/')
    return text.translate(obfs)


# turn obfuscated text back into something meaningful
def unlukefuscate(text):
    obfs = str.maketrans('t]Uv[0Wxy}1;:2{>,9.?Z5!zA@#<$C%^&*bDQrSe8)PFo`N(37gm~4H|i-L6kJ+_O/',
                         'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890=-+/')
    return text.translate(obfs)

