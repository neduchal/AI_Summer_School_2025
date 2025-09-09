import requests

ASR_ROOT = 'https://uwebasr.zcu.cz/api/v2/speechcloud/generic/en'      # en
#ASR_ROOT = 'https://uwebasr.zcu.cz/api/v2/speechcloud/generic/de'      # de


def recognize(fn, words_only=False):
    """Recognizes the file fn using the UWebASR service

    If words_only is True, then the function returns array of words,
    otherwise it returns array of dictionaries containing more detailed
    recognition results.

    Example:
    recognize("test.wav")

    UWebASR service is provided by Department of Cybernetics, University of
    West Bohemia
    """
    with open(fn, 'rb') as fr:
        r = requests.post(ASR_ROOT, data=fr, params={'format': 'json'})
        r.raise_for_status()
        ret = r.json()

    if words_only:
        return [i['word'] for i in ret]
    else:
        return ret

print(f'Recognized: {recognize("test.wav", words_only=True)}')
