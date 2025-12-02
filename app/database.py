# Health and Fitness Club Management System (Final Project for COMP3005A)
# By: Badr Ahmed (#101226464) & Faris Ahmed (#101142716)

import psycopg2
from psycopg2 import Error

# Database connection settings
# Update this with your own pgAdmin4 credentionals
Database_Configuration = {
    'dbname': 'Health_Fitness_Club_System',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': '5432'
}

def get_connection():
    # Creates and returns a connection to the database
    try:
        conn = psycopg2.connect(**Database_Configuration)
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

def close_connection(conn):
    # Closes the database connection
    
    if conn:
        conn.close()