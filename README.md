# Final_Project-4320

## Project: Trip Reservation System
Project Objectives
To further gain experience and develop skill working with Docker and Flask, or another language/platform chosen by the scrum team.
To further develop team chemistry and communication skill.
To further develop skill using agile project management and Jira



## Scenario
You and a number of IT students are going to a ski trip/hackathon over winter break in Colorado. To manage sign ups, the program has asked your team to create a simple web based reservation system so that students can reserve their seats on the bus. Students will be charged different amounts based on the seat they pick. You will be provided with a pricing chart for the seating.


## Requirements
Create a menu-driven reservation system using Flask Python, or another language with the ability to load and save reservations data to/from the reservations database. The application should also allow an administrator to login to the admin portal where they can view the bus seating chart and see the total sales. The bus can seat up to 48 people, 12 rows of 4 seats each. You can use your project 3a as a template for this project.

### Your application will need to have the following functionality:

* Create a seating chart and load the initial reservations
*  Display the main menu that asks the user whether they want to reserve a seat or log in as an administrator
*  If the user selects the admin login option they are taken to a page with a form to login. Information the user provides:
admin username
admin password
* If the user successfully logs in a seating chart is displayed along with the total sales collected.
* If the user selects the the reservation option they are taken to a page with a form to reserve a seat. Information the user provides
first name
last name
seat row
seat column
* Display a flight chart
* Calculate and get the total sales for the flight when the user successfully logs in as an admin
* Create and print a reservation code for the user when the user successfully makes a reservation
* Insert the reservation into the reservations table in the reservations SQLite database
* Each page should have a link to the main option page.
