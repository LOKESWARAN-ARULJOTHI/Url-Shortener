def url_shortener(longurl,id):
    id_val=id+1000000000000 # adding 1 trillion to get 7 chars short link
    characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    base = 62
    result=[]
    while id_val>0:
        value = id_val%base
        # print(value)
        result.append(characters[value])
        id_val=id_val//base
    return 'https://shrtyurl.herokuapp.com/'+''.join(result[::-1])

# print(url_shortener('https://github.com/minsuk-heo/coding_interview/blob/master/shorten_url.ipynb',1))