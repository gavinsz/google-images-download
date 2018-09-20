# coding=utf-8
from google_images_download import google_images_download   #importing the library
from parse_html import get_star_list
import argparse
import codecs
import os

star_list = get_star_list('uc-star.html')
response = google_images_download.googleimagesdownload()   #class instantiation
arguments = {"keywords": "李湘",
             "limit": 50, "print_urls": True,
             "format": "jpg", "proxy": "127.0.0.1:12759",
             "output_directory": "cpc_images",
             "chromedriver": "chromedriver.exe"
             }

'''
for it in star_list:
    arguments["keywords"] = it
    #passing the arguments to the function
    paths = response.download(arguments)
    #printing absolute paths of the downloaded images
    print(paths)
'''

# args_list = ["keywords", "keywords_from_file", "prefix_keywords", "suffix_keywords",
#              "limit", "format", "color", "color_type", "usage_rights", "size",
#              "exact_size", "aspect_ratio", "type", "time", "time_range", "delay", "url", "single_image",
#              "output_directory", "image_directory", "no_directory", "proxy", "similar_images", "specific_site",
#              "print_urls", "print_size", "print_paths", "metadata", "extract_metadata", "socket_timeout",
#              "thumbnail", "language", "prefix", "chromedriver", "related_images", "safe_search", "no_numbering"]

def read_extern_file(file, star_list):
    f = codecs.open(file, 'r', 'utf-8')
    line = f.readline()
    while line != '':
        line = line.strip('\n')
        line = line.strip('\r')
        star_list.insert(1, line)
        line = f.readline()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--progress_id', action="store", help="1....n", default=1, type=int)
    args = parser.parse_args()
    start = args.progress_id
    
    #read_extern_file('diff.txt', star_list)
    #read_extern_file('iqiyi-top-stars.txt', star_list)
    star_list.clear()
    read_extern_file('persons.txt', star_list)
    #for i in range(start, len(star_list), 10):
    for i in range(start, len(star_list)):
        arguments["keywords"] = star_list[i]
        dir_name = arguments['output_directory'] + "/" + arguments["keywords"]
        '''
        if os.path.exists(dir_name):
            print('%s is exists, donot download'%(arguments["keywords"]))
        else:
            paths = response.download(arguments)
        '''
        paths = response.download(arguments)