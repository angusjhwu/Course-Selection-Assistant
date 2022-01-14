from bs4 import BeautifulSoup
from selenium import webdriver
import scraper_methods as sm

from selenium.webdriver.chrome.options import Options
options = Options()
options.headless = True

driver = webdriver.Chrome(executable_path='C:\\path\\to\\chromedriver.exe',
                          options=options)

# This script scrape the University of Toronto Engineering Calendar "Programs" page
driver.get('https://engineering.calendar.utoronto.ca/programs')
soup = BeautifulSoup(driver.page_source, 'lxml')

# Collect all the link extensions to UofT engineering program pages
extensions = []
div = soup.find('div', attrs={'property': 'schema:text'})
for element in div.findAll('a'):
    if element.has_attr('href'):
        extensions.append(element['href'])

# Collects all the course codes from the engineering program pages
course_codes = []
for ext in extensions:
    course_codes.extend(sm.get_courses_on_page(ext))

course_codes_sorted = sorted(set(course_codes))
print(len(course_codes_sorted) + "courses found")  # Sanity check

# Scrapes course pages then write course information into text file
file = open('all_courses.txt', 'w')
for c in course_codes_sorted:
    sm.write_course_info(c, file)
file.close()
