# Health and Fitness Club Management System (Final Project for COMP3005A)
# By: Badr Ahmed (#101226464) & Faris Ahmed (#101142716)

import database as db
from datetime import date

def register_member():
    # Register a new member
    print("\n------------- Member Registration -------------")
    
    # Get member info from user
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    phone = input("Enter your phone number: ")
    dob = input("Enter your date of birth (YYYY-MM-DD): ")
    gender = input("Enter your gender: ")
    street = input("Enter street address: ")
    city = input("Enter city: ")
    postal_code = input("Enter postal code: ")
    
    conn = db.get_connection()
    if not conn:
        print("failed to connect to database")
        return
    
    try:
        cur = conn.cursor()
        
        # Check if email already exists
        cur.execute("SELECT email FROM MEMBER WHERE email = %s", (email,))
        if cur.fetchone():
            print("This email is already registered.")
            return
        
        # Insert new member
        cur.execute("""
            INSERT INTO MEMBER (name, email, phone, date_of_birth, gender, street, city, postal_code)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING member_id
        """, (name, email, phone, dob, gender, street, city, postal_code))
        
        member_id = cur.fetchone()[0]
        conn.commit()
        
        print(f"\nRegistration successful! your member ID is: {member_id}")
        print("Welcome to the club!")
        
    except Exception as e:
        print(f"Error during registration: {e}")
        conn.rollback()
    finally:
        cur.close()
        db.close_connection(conn)

def update_profile(member_id):
    # Update member profile information
    
    print("\n------------- Update Profile -------------")
    print("1. Update personal info")
    print("2. Set fitness goal")
    print("3. Add health metric")
    choice = input("Choose option (1-3): ")
    
    if choice == "1":
        update_personal_info(member_id)
    elif choice == "2":
        set_fitness_goal(member_id)
    elif choice == "3":
        add_health_metric(member_id)
    else:
        print("invalid choice")

def update_personal_info(member_id):
    # Update personal details
    
    print("\nWhat would you like to update?")
    print("1. Phone")
    print("2. Address")
    choice = input("Choose (1-2): ")
    
    conn = db.get_connection()
    if not conn:
        return
    
    try:
        cur = conn.cursor()
        
        if choice == "1":
            new_phone = input("Enter new phone number: ")
            cur.execute("UPDATE MEMBER SET phone = %s WHERE member_id = %s", (new_phone, member_id))
            print("Phone number updated!")
            
        elif choice == "2":
            street = input("Enter new street: ")
            city = input("Enter new city: ")
            postal = input("Enter new postal code: ")
            cur.execute("""
                UPDATE MEMBER 
                SET street = %s, city = %s, postal_code = %s 
                WHERE member_id = %s
            """, (street, city, postal, member_id))
            print("Address updated!")
        
        conn.commit()
        
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cur.close()
        db.close_connection(conn)

def set_fitness_goal(member_id):
    # Set a new fitness goal
    
    print("\n------------- Set Fitness Goal -------------")
    
    goal_type = input("Goal type (e.g., Weight Loss, Muscle Gain): ")
    target = float(input("Target value: "))
    current = float(input("Current value: "))
    start_date = input("Start date (YYYY-MM-DD) or press Enter for today: ")
    if not start_date:
        start_date = str(date.today())
    target_date = input("Target date (YYYY-MM-DD): ")
    
    conn = db.get_connection()
    if not conn:
        return
    
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO FITNESS_GOAL (member_id, goal_type, target_value, current_value, start_date, target_date)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (member_id, goal_type, target, current, start_date, target_date))
        
        conn.commit()
        print("fitness goal set successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cur.close()
        db.close_connection(conn)

def add_health_metric(member_id):
    # Add a new health metric entry
    # This doesn't overwrite. it adds a new record
    print("\n------------- Add Health Metric -------------")
    
    weight = input("Weight (kg): ")
    height = input("Height (cm): ")
    heart_rate = input("Heart rate (BPM): ")
    body_fat = input("Body fat percentage: ")
    
    # Use today's date
    today = str(date.today())
    
    conn = db.get_connection()
    if not conn:
        return
    
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO HEALTH_METRIC (member_id, date_recorded, weight, height, heart_rate, body_fat_percentage)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (member_id, today, weight, height, heart_rate, body_fat))
        
        conn.commit()
        print("Health metric recorded!")
        
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cur.close()
        db.close_connection(conn)

def view_dashboard(member_id):
    # Show member dashboard with health stats, goals, and sessions
    
    print("------------- Member Dashboard -------------")
    
    conn = db.get_connection()
    if not conn:
        return
    
    try:
        cur = conn.cursor()
        
        # Get member info
        cur.execute("SELECT name, email FROM MEMBER WHERE member_id = %s", (member_id,))
        result = cur.fetchone()
        if not result:
            print("Member not found!")
            return
            
        name, email = result
        print(f"\nWelcome, {name}!")
        print(f"Email: {email}")
        
        # Get latest health metrics
        print("\n------------- Latest Health Metrics -------------")
        cur.execute("""
            SELECT date_recorded, weight, height, heart_rate, body_fat_percentage
            FROM HEALTH_METRIC
            WHERE member_id = %s
            ORDER BY date_recorded DESC
            LIMIT 1
        """, (member_id,))
        
        metric = cur.fetchone()
        if metric:
            print(f"Date: {metric[0]}")
            print(f"Weight: {metric[1]} kg")
            print(f"Height: {metric[2]} cm")
            print(f"Heart Rate: {metric[3]} BPM")
            print(f"Body Fat: {metric[4]}%")
        else:
            print("No health metrics recorded yet")
        
        # Get active fitness goals
        print("\n------------- Active Fitness Goals -------------")
        cur.execute("""
            SELECT goal_type, current_value, target_value, target_date
            FROM FITNESS_GOAL
            WHERE member_id = %s
            ORDER BY start_date DESC
        """, (member_id,))
        
        goals = cur.fetchall()
        if goals:
            for goal in goals:
                print(f"Goal: {goal[0]}")
                print(f"  Current: {goal[1]} -> Target: {goal[2]}")
                print(f"  Target Date: {goal[3]}")
        else:
            print("No fitness goals set yet")
        
        # Get class registration count
        print("\n------------- Class Participation -------------")
        cur.execute("""
            SELECT COUNT(*) FROM CLASS_REGISTRATION WHERE member_id = %s
        """, (member_id,))
        class_count = cur.fetchone()[0]
        print(f"total classes registered: {class_count}")
        
        # Get upcoming Personal Training Session sessions
        print("\n------------- Upcoming Training Sessions -------------")
        cur.execute("""
            SELECT pts.session_date, pts.start_time, pts.end_time, t.name as trainer_name
            FROM PERSONAL_TRAINING_SESSION pts
            JOIN TRAINER t ON pts.trainer_id = t.trainer_id
            WHERE pts.member_id = %s AND pts.status = 'Scheduled'
            ORDER BY pts.session_date, pts.start_time
        """, (member_id,))
        
        sessions = cur.fetchall()
        if sessions:
            for session in sessions:
                print(f"Date: {session[0]}, Time: {session[1]}-{session[2]}, Trainer: {session[3]}")
        else:
            print("No upcoming sessions")
        
        print("\n" + "="*50)
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cur.close()
        db.close_connection(conn)

def schedule_training_session(member_id):
   
    # Book a personal training session with a trainer
    
    print("\n------------- Schedule Personal Training Session -------------")
    
    conn = db.get_connection()
    if not conn:
        return
    
    try:
        cur = conn.cursor()
        
        # Show available trainers
        print("\nAvailable Trainers:")
        cur.execute("SELECT trainer_id, name, specialization FROM TRAINER")
        trainers = cur.fetchall()
        for trainer in trainers:
            print(f"ID: {trainer[0]}, Name: {trainer[1]}, Specialization: {trainer[2]}")
        
        trainer_id = input("\nEnter trainer ID: ")
        session_date = input("Enter session date (YYYY-MM-DD): ")
        start_time = input("Enter start time (HH:MM): ")
        end_time = input("Enter end time (HH:MM): ")
        
        # Show available rooms
        print("\nAvailable Rooms:")
        cur.execute("SELECT room_id, room_name, capacity FROM ROOM")
        rooms = cur.fetchall()
        for room in rooms:
            print(f"ID: {room[0]}, Name: {room[1]}, Capacity: {room[2]}")
        
        room_id = input("\nEnter room ID: ")
        
        # Check for conflicts
        cur.execute("""
            SELECT session_id FROM PERSONAL_TRAINING_SESSION
            WHERE trainer_id = %s 
            AND session_date = %s 
            AND start_time = %s
            AND status = 'Scheduled'
        """, (trainer_id, session_date, start_time))
        
        if cur.fetchone():
            print("Error: Trainer is not available at that time!")
            return
        
        # Book the session
        cur.execute("""
            INSERT INTO PERSONAL_TRAINING_SESSION 
            (member_id, trainer_id, room_id, session_date, start_time, end_time, status)
            VALUES (%s, %s, %s, %s, %s, %s, 'Scheduled')
        """, (member_id, trainer_id, room_id, session_date, start_time, end_time))
        
        conn.commit()
        print("\nsession booked successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cur.close()
        db.close_connection(conn)

def register_for_class(member_id):
    """
    Register for a group fitness class
    """
    print("\n------------- Register for Group Class -------------")
    
    conn = db.get_connection()
    if not conn:
        return
    
    try:
        cur = conn.cursor()
        
        # Show available classes
        print("\nUpcoming Classes:")
        cur.execute("""
            SELECT gc.class_id, gc.class_name, gc.class_date, gc.start_time, 
                   gc.capacity, gc.current_enrollment, t.name as trainer_name
            FROM GROUP_CLASS gc
            JOIN TRAINER t ON gc.trainer_id = t.trainer_id
            WHERE gc.class_date >= CURRENT_DATE
            ORDER BY gc.class_date, gc.start_time
        """)
        
        classes = cur.fetchall()
        if not classes:
            print("no upcoming classes available")
            return
        
        for cls in classes:
            spots_left = cls[4] - cls[5]
            print(f"\nID: {cls[0]}")
            print(f"Class: {cls[1]}")
            print(f"Date: {cls[2]}, Time: {cls[3]}")
            print(f"Trainer: {cls[6]}")
            print(f"Spots available: {spots_left}/{cls[4]}")
        
        class_id = input("\nEnter class ID to register: ")
        
        # Check if already registered
        cur.execute("""
            SELECT * FROM CLASS_REGISTRATION 
            WHERE member_id = %s AND class_id = %s
        """, (member_id, class_id))
        
        if cur.fetchone():
            print("You're already registered for this class!")
            return
        
        # Check capacity
        cur.execute("""
            SELECT capacity, current_enrollment 
            FROM GROUP_CLASS WHERE class_id = %s
        """, (class_id,))
        
        result = cur.fetchone()
        if not result:
            print("Class not found!")
            return
            
        capacity, enrolled = result
        if enrolled >= capacity:
            print("Sorry, this class is full.")
            return
        
        # Register for class
        cur.execute("""
            INSERT INTO CLASS_REGISTRATION (member_id, class_id, registration_date)
            VALUES (%s, %s, CURRENT_DATE)
        """, (member_id, class_id))
        
        conn.commit()
        print("\nSuccessfully registered for class!")
        print("The enrollment count will be automatically updated by the trigger.")
        
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cur.close()
        db.close_connection(conn)