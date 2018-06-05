__author__ = 'shiyu'


from num2words import num2words


def spellnumbers(num):
    a = []
    for i in str(num):
        a.append(num2words(int(i)))
    return ' '.join(a)

print spellnumbers(1234)