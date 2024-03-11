# Course Selection Assistant

Course selection is a cumbersome process, having to monitor the prerequisite courses and the courses' term availability. This tool aims to improve organization during course selection planning and to automatically schedule the desired courses such that all the prerequisite requirements are filled, as well as accounting for the users' planning restrictions like preferred course sequence or time.

## Part 1: Webscraper

- Scrape the University of Toronto Engineering Calendar website to collect all the available courses and their prerequisites
- User can find the course information for all of UofT's engineering and related courses

## Part 2: Database (to-do)

- Create a graph datastructure that stores and connects all the courses with their corequisites and prerequisites
- User can find a course with its information as well as all its prerequisites and future courses where the selected course is a prerequisite

## Part 3: Automated Planner (to-do)

- Create a GUI/web app where the user can select all the courses they desire to take, then all the courses are to be displayed in a connected fashion for groups of prerequisite-related courses
- Courses are put into the correct year and term such that it satisfies university requirements and course prerequisites
- Users can input their perferred course sequence, which the program will then take into account while optimizing the planner

## Quality of Life Features (to-do)

- Share course time table through link or file
- Suggestions for Certificates and Minors based on existing courses