# Health and Fitness Club Management System (Final Project for COMP3005A)
# By: Badr Ahmed (#101226464) & Faris Ahmed (#101142716)

import database as db
from datetime import date

def manage_rooms():
    # Room booking and management
    print("\n------------- Room Management -------------")
    print("1. View all rooms")
    print("2. Check room bookings")
    print("3. Add new room")
    choice = input("Choose option (1-3): ")
    
    if choice == "1":
        view_rooms()
    elif choice == "2":
        check_room_bookings()
    elif choice == "3":
        add_room()
    else:
        print("invalid choice")

def view_rooms():
    # View all available rooms
    conn = db.get_connection()
    if not conn:
        return
    
    try:
        cur = conn.cursor()
        cur.execute("SELECT room_id, room_name, capacity, equipment_available FROM ROOM")
        rooms = cur.fetchall()
        
        print("\n------------- Viewing All Rooms -------------")
        for room in rooms:
            print(f"\nID: {room[0]}")
            print(f"Name: {room[1]}")
            print(f"Capacity: {room[2]}")
            print(f"Equipment: {room[3]}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cur.close()
        db.close_connection(conn)

def check_room_bookings():
    # Check what's booked in each room
    room_id = input("\nEnter room ID to check: ")
    check_date = input("Enter date (YYYY-MM-DD): ")
    
    conn = db.get_connection()
    if not conn:
        return
    
    try:
        cur = conn.cursor()
        
        # Check Personal Training Session sessions in this room
        print("\n------------- Personal Training Sessions -------------")
        cur.execute("""
            SELECT start_time, end_time, t.name as trainer, m.name as member
            FROM PERSONAL_TRAINING_SESSION pts
            JOIN TRAINER t ON pts.trainer_id = t.trainer_id
            JOIN MEMBER m ON pts.member_id = m.member_id
            WHERE pts.room_id = %s AND pts.session_date = %s
            ORDER BY start_time
        """, (room_id, check_date))
        
        sessions = cur.fetchall()
        if sessions:
            for session in sessions:
                print(f"{session[0]}-{session[1]}: Trainer {session[2]} with Member {session[3]}")
        else:
            print("No Personal Training Sessions booked")
        
        # Check group classes in this room
        print("\n--- Group Classes ---")
        cur.execute("""
            SELECT start_time, end_time, class_name, t.name as trainer
            FROM GROUP_CLASS gc
            JOIN TRAINER t ON gc.trainer_id = t.trainer_id
            WHERE gc.room_id = %s AND gc.class_date = %s
            ORDER BY start_time
        """, (room_id, check_date))
        
        classes = cur.fetchall()
        if classes:
            for cls in classes:
                print(f"{cls[0]}-{cls[1]}: {cls[2]} with Trainer {cls[3]}")
        else:
            print("no group classes scheduled")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cur.close()
        db.close_connection(conn)

def add_room():
    # Add a new room to the system
    print("\n------------- Adding New Room -------------")
    
    room_name = input("Enter Room name: ")
    capacity = input("Enter Capacity: ")
    equipment = input("Enter Equipment available: ")
    
    conn = db.get_connection()
    if not conn:
        return
    
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO ROOM (room_name, capacity, equipment_available)
            VALUES (%s, %s, %s)
            RETURNING room_id
        """, (room_name, capacity, equipment))
        
        room_id = cur.fetchone()[0]
        conn.commit()
        print(f"\nRoom added successfully! Room ID: {room_id}")
        
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cur.close()
        db.close_connection(conn)

def manage_classes():
    # Class schedule management
    print("\n------------- Class Management -------------")
    print("1. View all classes")
    print("2. Create new class")
    print("3. Update class")
    print("4. Cancel class")
    choice = input("Choose option (1-4): ")
    
    if choice == "1":
        view_all_classes()
    elif choice == "2":
        create_class()
    elif choice == "3":
        update_class()
    elif choice == "4":
        cancel_class()
    else:
        print("invalid choice")

def view_all_classes():
    # View all group classes
    conn = db.get_connection()
    if not conn:
        return
    
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT gc.class_id, gc.class_name, gc.class_date, gc.start_time, 
                   t.name as trainer, r.room_name, gc.capacity, gc.current_enrollment
            FROM GROUP_CLASS gc
            LEFT JOIN TRAINER t ON gc.trainer_id = t.trainer_id
            LEFT JOIN ROOM r ON gc.room_id = r.room_id
            ORDER BY gc.class_date, gc.start_time
        """)
        
        classes = cur.fetchall()
        if not classes:
            print("No classes scheduled")
            return
        
        print("\n------------- All Classes -------------")
        for cls in classes:
            print(f"\nID: {cls[0]}, Class: {cls[1]}")
            print(f"Date: {cls[2]}, Time: {cls[3]}")
            print(f"Trainer: {cls[4]}, Room: {cls[5]}")
            print(f"Enrollment: {cls[7]}/{cls[6]}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cur.close()
        db.close_connection(conn)

def create_class():
    # Create a new group class
    print("\n------------- Create New Class -------------")
    
    conn = db.get_connection()
    if not conn:
        return
    
    try:
        cur = conn.cursor()
        
        # Show available trainers
        cur.execute("SELECT trainer_id, name, specialization FROM TRAINER")
        trainers = cur.fetchall()
        print("\nAvailable Trainers:")
        for trainer in trainers:
            print(f"ID: {trainer[0]}, Name: {trainer[1]}, Specialization: {trainer[2]}")
        
        trainer_id = input("\nTrainer ID: ")
        
        # Show available rooms
        cur.execute("SELECT room_id, room_name, capacity FROM ROOM")
        rooms = cur.fetchall()
        print("\nAvailable Rooms:")
        for room in rooms:
            print(f"ID: {room[0]}, Name: {room[1]}, Capacity: {room[2]}")
        
        room_id = input("\nRoom ID: ")
        
        # Obtain class details
        class_name = input("Class name: ")
        class_date = input("Date (YYYY-MM-DD): ")
        start_time = input("Start time (HH:MM): ")
        end_time = input("End time (HH:MM): ")
        capacity = input("Capacity: ")
        
        # Create the class
        cur.execute("""
            INSERT INTO GROUP_CLASS 
            (trainer_id, room_id, class_name, class_date, start_time, end_time, capacity, current_enrollment)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 0)
            RETURNING class_id
        """, (trainer_id, room_id, class_name, class_date, start_time, end_time, capacity))
        
        class_id = cur.fetchone()[0]
        conn.commit()
        print(f"\nClass created successfully! Class ID: {class_id}")
        
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cur.close()
        db.close_connection(conn)

def update_class():
    # Update an existing class
    print("\n------------- Update Existing Class -----------")
    
    class_id = input("enter class ID to update: ")
    
    print("\nWhat would you like to update?")
    print("1. Date/Time")
    print("2. Capacity")
    choice = input("Choose (1-2): ")
    
    conn = db.get_connection()
    if not conn:
        return
    
    try:
        cur = conn.cursor()
        
        if choice == "1":
            new_date = input("New date (YYYY-MM-DD): ")
            new_start = input("New start time (HH:MM): ")
            new_end = input("New end time (HH:MM): ")
            
            cur.execute("""
                UPDATE GROUP_CLASS 
                SET class_date = %s, start_time = %s, end_time = %s
                WHERE class_id = %s
            """, (new_date, new_start, new_end, class_id))
            
        elif choice == "2":
            new_capacity = input("New capacity: ")
            cur.execute("""
                UPDATE GROUP_CLASS 
                SET capacity = %s
                WHERE class_id = %s
            """, (new_capacity, class_id))
        
        conn.commit()
        print("Class updated successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cur.close()
        db.close_connection(conn)

def cancel_class():
    # Cancel/delete a class
    print("\n------------- Cancel Class -------------")
    
    class_id = input("Enter class ID to cancel: ")
    confirm = input("Are you sure? this will remove all registrations! (yes/no): ")
    
    if confirm.lower() != "yes":
        print("Cancellation aborted")
        return
    
    conn = db.get_connection()
    if not conn:
        return
    
    try:
        cur = conn.cursor()
        
        # Delete the class
        cur.execute("DELETE FROM GROUP_CLASS WHERE class_id = %s", (class_id,))
        
        conn.commit()
        print("Class cancelled successfully")
        
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cur.close()
        db.close_connection(conn)

def equipment_maintenance():
    # Track equipment maintenance

    print("\n------------- Equipment Maintenance -------------")
    print("\nNote: This is a simplified demo")
    print("In a full implementation, we would have:")
    print("- An equipment table with equipment details")
    print("- a maintenance table tracking all issues")
    print("- Status tracking (operational, under repair, etc.)")
    print("\nFor this demo, we're showing the concept only.")
    
    input("\npress Enter to continue...")

def billing_payment():
    # Billing and payment processing (simulated)
    
    print("\n------------- Billing & Payment -------------")
    print("\nNote: This is a simplified demo")
    print("In a full implementation, we would have:")
    print("- Invoice table with bill details")
    print("- Payment table with payment records")
    print("- Integration with payment gateway")
    
    print("\n1. Generate sample bill")
    print("2. Record sample payment")
    choice = input("Choose option (1-2): ")
    
    if choice == "1":
        print("\n------------- Sample Bill Generated -------------")
        print("Invoice #: 001")
        print("Member: John Smith")
        print("Items:")
        print("Monthly Membership: $50.00")
        print("Personal Training Session: $75.00")
        print("Total: $125.00")
        print("Status: Pending")
        
    elif choice == "2":
        print("\n------------- Sample Payment Recorded -------------")
        print("Invoice #: 001")
        print("Amount: $125.00")
        print("Payment Method: Credit Card")
        print("Status: Paid")
        print("Payment Date: " + str(date.today()))
    
    input("\nPress Enter to continue...")