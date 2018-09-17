import urllib
import codecs
from bs4 import BeautifulSoup


def get_star_list(html_file):
    star_list = []
    html_doc = codecs.open(html_file, 'r', 'utf-8')
    #html_doc = urllib.request.urlopen(html_file).read()
    soup = BeautifulSoup(html_doc, features='html5lib')
    #print(soup.title)
    all_star = soup.find_all(attrs={"class": "star-name"})
    for it in all_star:
        if it.get_text() != '':
            #print(it.get_text())
            star_list.append(it.get_text())
    
    
    all_h2 = soup.find_all('h2')
    for it in all_h2:
        #print('type=', type(it), it)
        #print(it.get_text())
        star_list.append(it.get_text())
        if len(star_list) == 1400:
            break
    
    return star_list

if __name__ == '__main__':
    get_star_list('./uc-star.html')