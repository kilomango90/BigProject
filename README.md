\# Health and Fitness Club Management System (Final Project for COMP3005A)

\*\*By: Badr Ahmed (#101226464) \& Faris Ahmed (#101142716)\*\*



Video Link: https://youtu.be/blhx2chIatY



\## Project Description:

This is a database management system for a health and fitness club. It lets members register, track their fitness goals and health metrics (like weight, heart rate, body fat %), book personal training sessions, and sign up for group classes. Trainers can view and modify their schedules and availabilities and search for member information. Administrative staff can manage rooms, create and update classes, and handle equipment maintenance and billing.



\## Sample Data:

The SQL files are populated with the following sample data:

\- \*\*Members:\*\* 1 (John Smith), 2 (Sarah Johnson), 3 (Mike Brown), 4 (Emily Davis), 5 (David Wilson)

\- \*\*Trainers:\*\* 1 (Jane Cooper - Yoga), 2 (Tom Harris - Weight Training), 3 (Lisa Martinez - Cardio), 4 (Chris Lee - CrossFit)

\- \*\*Admins:\*\* 1 (Admin User), 2 (Manager Smith), 3 (Front Desk)



\## To run the application:

\- Run pgAdmin4

\- Create a new database called exactly "Health\_Fitness\_Club\_System"

\- Click the folder icon that says "Open File" when hovered, and import the file DDL.sql

\- Click the arrow icon that says "Execute Script" when hovered. Confirm it ran successfully by finding the message log that states "Query returned successfully"

\- Click the folder icon that says "Open File" when hovered, and import the file DML.sql

\- Click the arrow icon that says "Execute Script" when hovered.

\- Confirm tables have added successfully by navigating the menu on the left by clicking Health\_Fitness\_Club\_System ---> Schemas ---> Tables. There should be nine tables.

\- Download and install python to your computer

\- Run a console terminal

\- Run the command "py -m pip install psycopg2-binary". This installs the PostgreSQL database adapter

\- Run the command cd \[Where you placed your files]. As per the assignment, this should be a path that ends with /app which is where the source code is

\- Run the command "python main.py"

\- If you are faced with an error related to the password authentication, run database.py in an IDE and change the value of the key 'password' to whatever your PostgreSQL is.

