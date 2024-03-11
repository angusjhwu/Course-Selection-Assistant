#################################
# Author: Angus Wu
# Usage:
# > python3 scrape_courses.py > dump.txt

import requests
from bs4 import BeautifulSoup
import sys

import settings
from data import data_utils


def get_all_links_with_substr(url: str, substr: str) -> tuple[list[str], list[str]]:
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all links in the page
    rel_links = []
    full_links = []
    links = soup.find_all('a')
    for link in links:
        href = link.get('href')  # Use .get() method to avoid KeyError
        if href:
            if href.startswith(substr):
                rel_links.append(href)
            elif substr in href:
                full_links.append(href)
    return rel_links, full_links


def get_course_links_from_url(url: str) -> tuple[list[str], list[str]]:
    eng_courses, non_eng_courses = get_all_links_with_substr(url, '/course/')
    base_url = 'https://engineering.calendar.utoronto.ca'
    eng_courses = [base_url + ec for ec in eng_courses]
    return eng_courses, non_eng_courses


if __name__ == "__main__":
    
    # Input handling
    if len(sys.argv) == 1:          # Default saving locations
        eng_dir = f'{settings.project_dir}/data/eng_courses_url.txt'
        noneng_dir = f'{settings.project_dir}/data/non_eng_courses_url.txt'
    else:
        if len(sys.argv) != 3:      # User's prefered locations
            print("Usage: python script.py <eng_course_store_dir> <non_eng_course_store_dir>")
            sys.exit(1)
        eng_dir = sys.argv[1]
        noneng_dir = sys.argv[2]
        
    # Scrape all Eng Calendar pages for courses
    url_list = []
    print('Pages to scrape:')
    # "all courses" pages
    for page_index in range(18):
        url = f"https://engineering.calendar.utoronto.ca/search-courses?page={page_index}"
        url_list.append(url)
        print(f'    {url}')
    # all program pages
    sections, _ = get_all_links_with_substr('https://engineering.calendar.utoronto.ca/programs', '/section/')
    for section in sorted(list(set(sections))):
        url = f"https://engineering.calendar.utoronto.ca{section}"
        url_list.append(url)
        print(f'    {url}')
    print()
    
    # Find all courses within those pages
    eng_courses, non_eng_courses = [], []
    for url in url_list:
        ec, nec = get_course_links_from_url(url)
        eng_courses += ec
        non_eng_courses += nec

    eng_courses = list(set(eng_courses))
    eng_courses = sorted(eng_courses)
    data_utils.save_list_to_file(eng_courses, eng_dir)
    print(f'All eng courses saved to {eng_dir}')

    non_eng_courses = list(set(non_eng_courses))
    non_eng_courses = sorted(non_eng_courses)
    data_utils.save_list_to_file(non_eng_courses, noneng_dir)
    print(f'All non-eng courses saved to {noneng_dir}')

    # sys.exit()

    # # Initializing all courses
    # all_courses: list[Course] = []
    # count = 0
    # for course_url in (eng_courses + non_eng_courses):
    #     course = Course.try_init(course_url)
    #     if course:
    #         all_courses.append(course)
    #         print(repr(course))
    #         count += 1
    #         if count == 9:
    #             raise RuntimeError('Early Stopping')

    # print('\nAll Courses Currently Offered:')
    # for c in all_courses:
    #     print(repr(c))
