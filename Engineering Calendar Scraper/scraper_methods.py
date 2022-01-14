from bs4 import BeautifulSoup
from selenium import webdriver
import re

from selenium.webdriver.chrome.options import Options
options = Options()
options.headless = True

driver = webdriver.Chrome(executable_path='C:\\path\\to\\chromedriver.exe',
                          options=options)


def get_course_url(code):
    """
    Returns the engineering calendar url for a course by course code.

    :param code: course code
    :return: engineering calendar url
    """
    return 'https://engineering.calendar.utoronto.ca/course/' + code


def write_course_info(code, file):
    """
    Scrapes the engineering calendar webpage of a course by course code,
    then writes the course information (course code, course name, course prerequisites)
    to text file.

    :param code: course code
    :param file: text file to write into
    """
    driver.get(get_course_url(code))
    soup = BeautifulSoup(driver.page_source, 'lxml')

    name = soup.find(attrs={'class': 'title page-title'})

    # Return when course is no longer offered
    if name.text.strip() == 'Sorry, this course is not in the current Calendar.':
        return

    # Course Code + Name
    file.write(name.text.strip() + '\n')

    prereq = soup.find(attrs={
        'class': 'clearfix text-formatted field field--name-field-prerequisite field--type-text-long '
                 'field--label-inline'})
    file.write('Prerequisites:\n')
    if prereq:
        prereq_list = prereq.div.next_element.next_element.next_element
        file.write(''.join(prereq_list.findAll(text=True))
                   .replace(u'\u200b', '*')              # Deprecated character
                   .replace(' and ', ', ')               # Formatting
                   .replace(' or ', '/ ')                # Formatting
                   .replace('/; ', ',\n')                # Formatting
                   .replace('; \n', ',\n')               # Formatting
                   .replace('; ', '\n').strip() + '\n')  # Formatting
    else:
        file.write('None\n')

    file.write('\n')


def get_courses_on_page(link):
    """
    Scrapes a webpage then returns all the course codes listed.

    :param link: link of webpage to scrape
    :return: list of all course codes found on page
    """
    driver.get('https://engineering.calendar.utoronto.ca' + link)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    all_names = ''.join(map(str, soup.findAll(attrs={'class': 'js-views-accordion-group-header'})))
    words = all_names.split()

    course_codes = [re.sub(r'\W+', '', word).upper()[:8] for word in words if 'H1' in word]
    return course_codes
