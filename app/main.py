# Health and Fitness Club Management System (Final Project for COMP3005A)
# By: Badr Ahmed (#101226464) & Faris Ahmed (#101142716)

import member_functions as member
import trainer_functions as trainer
import admin_functions as admin
import database as db

def main_menu():
    print("\n------------- Health And Fitness Club Management System -------------\n")
    print("1. Member")
    print("2. Trainer")
    print("3. Adminstrative Staff")
    print("4. Exit")
    
    choice = input("\nselect user type (1-3) or 4 to exit: ")
    return choice

def member_menu():
    # Member menu and operations
    print("\n------------- Member Login ------------- ")
    print("1. Register as new member")
    print("2. Login as existing member")
    print("3. Back to main menu")
    
    choice = input("\nChoose an option (1-3): ")
    
    if choice == "1":
        member.register_member()
        input("\nPress Enter to continue...")
        
    elif choice == "2":
        member_id = input("Enter your member ID: ")
        member_operations(member_id)
        
    elif choice == "3":
        return
    else:
        print("Invalid choice")

def member_operations(member_id):
    # Operations available to logged-in members
    while True:
        print("\n------------- Member Menu -------------")
        print("1. View Dashboard")
        print("2. Update Profile")
        print("3. Schedule Training Session")
        print("4. Register for Group Class")
        print("5. Logout")
        
        choice = input("\nChoose option (1-5): ")
        
        if choice == "1":
            member.view_dashboard(member_id)
            input("\nPress Enter to continue...")
            
        elif choice == "2":
            member.update_profile(member_id)
            
        elif choice == "3":
            member.schedule_training_session(member_id)
            
        elif choice == "4":
            member.register_for_class(member_id)
            
        elif choice == "5":
            print("Logging out...")
            break
            
        else:
            print("invalid choice")

def trainer_menu():
    # Trainer menu and operations
    print("\n------------- Trainer Login -------------")
    
    trainer_id = input("Enter your trainer ID: ")
    
    # Verify trainer exists
    conn = db.get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT name FROM TRAINER WHERE trainer_id = %s", (trainer_id,))
            result = cur.fetchone()
            
            if not result:
                print("Trainer ID not found")
                cur.close()
                db.close_connection(conn)
                return
            
            trainer_name = result[0]
            print(f"\nWelcome, {trainer_name}!")
            cur.close()
            db.close_connection(conn)
            
        except Exception as e:
            print(f"Error: {e}")
            db.close_connection(conn)
            return
    
    # Trainer operations loop
    while True:
        print("\n------------- Trainer Menu -------------")
        print("1. View My Schedule")
        print("2. Search Member")
        print("3. Set Availability")
        print("4. Logout")
        
        choice = input("\nChoose option (1-4): ")
        
        if choice == "1":
            trainer.view_schedule(trainer_id)
            input("\nPress Enter to continue...")
            
        elif choice == "2":
            trainer.search_member()
            
        elif choice == "3":
            trainer.set_availability(trainer_id)
            
        elif choice == "4":
            print("Logging out...")
            break
            
        else:
            print("invalid choice")

def admin_menu():
    # Admin menu and operations
    print("\n------------- Adminstrative Staff Login -------------")
    
    admin_id = input("Enter your admin ID: ")
    
    conn = db.get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT name FROM ADMINISTRATIVE_STAFF WHERE admin_id = %s", (admin_id,))
            result = cur.fetchone()
            
            if not result:
                print("Admin ID not found!")
                cur.close()
                db.close_connection(conn)
                return
            
            admin_name = result[0]
            print(f"\nWelcome, {admin_name}!")
            cur.close()
            db.close_connection(conn)
            
        except Exception as e:
            print(f"Error: {e}")
            db.close_connection(conn)
            return
    
    # Admin operations loop
    while True:
        print("\n------------- Adminstrative Staff Menu -------------")
        print("1. Manage Rooms")
        print("2. Manage Classes")
        print("3. Equipment Maintenance")
        print("4. Billing & Payment")
        print("5. Logout")
        
        choice = input("\nChoose option (1-5): ")
        
        if choice == "1":
            admin.manage_rooms()
            
        elif choice == "2":
            admin.manage_classes()
            
        elif choice == "3":
            admin.equipment_maintenance()
            
        elif choice == "4":
            admin.billing_payment()
            
        elif choice == "5":
            print("Logging out...")
            break
            
        else:
            print("Invalid choice")

def main():
    # Main program
    print("\nStarting Health and Fitness Club Management System...")
    
    # Test database connection
    conn = db.get_connection()
    if not conn:
        print("\nERROR: Could not connect to database.")
        print("please check your database.py file")
        return
    else:
        print("Database connection successful!")
        db.close_connection(conn)
    
    # Main program loop
    while True:
        choice = main_menu()
        
        if choice == "1":
            member_menu()
            
        elif choice == "2":
            trainer_menu()
            
        elif choice == "3":
            admin_menu()
            
        elif choice == "4":
            print("\nThank you for using Health And Fitness Club Management System!")
            break
            
        else:
            print("\nInvalid choice! Please try again.")

# Run the program
if __name__ == "__main__":
    main()