from django import template
from portal.resources import CENSOR_LIST
register = template.Library()


@register.filter()
def censor(value):
    if not isinstance(value, str):
        raise TypeError('Ожидается строка.')
    else:
        words = value.split()
        censored_words = []
        for word in words:
            if word in CENSOR_LIST:
                censored_word = f'{word[0]}***'
                censored_words.append(censored_word)
            else:
                censored_words.append(word)
    return ' '.join(censored_words)