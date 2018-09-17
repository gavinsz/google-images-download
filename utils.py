# coding=utf-8
import codecs
from urllib.request import urlretrieve
import os

def write_list_to_file(s, file_name):
    f = codecs.open(file_name, 'w', 'utf-8')
    for it in s:
        #print(it)
        f.write(it + '\n')
    
    f.close()

def get_files_num(src_dir):
    num_files = 0
    for fn in os.listdir(src_dir):
            num_files += 1

    return num_files
    
def download_img(out_dir, person_name, img_url):
    dst_dir = os.path.join(out_dir, person_name)
    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)

    num = get_files_num(dst_dir)
    file_name = str(num+1) + '.jpg'
    full_path = os.path.join(dst_dir, file_name)
    #print('full_path=', full_path)
    #print('img_url=', img_url)
    urlretrieve(img_url, full_path)