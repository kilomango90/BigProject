# Health and Fitness Club Management System (Final Project for COMP3005A)
# By: Badr Ahmed (#101226464) & Faris Ahmed (#101142716)

import database as db

def view_schedule(trainer_id):
    # View trainer's schedule
    print("\n------------- Trainer Schedule -------------")
    
    conn = db.get_connection()
    if not conn:
        return
    
    try:
        cur = conn.cursor()
        
        # Get personal training sessions
        print("\n------------- Personal Training Sessions -------------")
        cur.execute("""
            SELECT pts.session_date, pts.start_time, pts.end_time, 
                   m.name as member_name, r.room_name, pts.status
            FROM PERSONAL_TRAINING_SESSION pts
            JOIN MEMBER m ON pts.member_id = m.member_id
            LEFT JOIN ROOM r ON pts.room_id = r.room_id
            WHERE pts.trainer_id = %s
            ORDER BY pts.session_date, pts.start_time
        """, (trainer_id,))
        
        sessions = cur.fetchall()
        if sessions:
            for session in sessions:
                print(f"Date: {session[0]}, Time: {session[1]}-{session[2]}")
                print(f"  Member: {session[3]}, Room: {session[4]}, Status: {session[5]}")
        else:
            print("no training sessions scheduled")
        
        # Get group classes
        print("\n------------- Group Classes -------------")
        cur.execute("""
            SELECT class_name, class_date, start_time, end_time, 
                   capacity, current_enrollment, room_name
            FROM GROUP_CLASS gc
            LEFT JOIN ROOM r ON gc.room_id = r.room_id
            WHERE gc.trainer_id = %s
            ORDER BY gc.class_date, gc.start_time
        """, (trainer_id,))
        
        classes = cur.fetchall()
        if classes:
            for cls in classes:
                print(f"\nClass: {cls[0]}")
                print(f"Date: {cls[1]}, Time: {cls[2]}-{cls[3]}")
                print(f"Room: {cls[6]}, Enrollment: {cls[5]}/{cls[4]}")
        else:
            print("no group classes scheduled")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cur.close()
        db.close_connection(conn)

def search_member():
    # Search for a member by name and view their info (but not edit since they are not admins)
    print("\n------------- Search Member -------------")
    
    search_name = input("Enter member name (or part of name): ")
    
    conn = db.get_connection()
    if not conn:
        return
    
    try:
        cur = conn.cursor()
        
        # Search members
        cur.execute("""
            SELECT member_id, name, email, phone
            FROM MEMBER
            WHERE LOWER(name) LIKE LOWER(%s)
        """, (f'%{search_name}%',))
        
        members = cur.fetchall()
        
        if not members:
            print("No members found with that name")
            return
        
        # Show search results
        print("\nsearch Results:")
        for member in members:
            print(f"ID: {member[0]}, Name: {member[1]}, Email: {member[2]}, Phone: {member[3]}")
        
        # Let trainer select a member to view details
        member_id = input("\nEnter member ID to view details (or 0 to cancel): ")
        
        if member_id == "0":
            return
        
        # Get member's current goal
        print("\n------------- Member's Current Goals -------------")
        cur.execute("""
            SELECT goal_type, current_value, target_value, start_date, target_date
            FROM FITNESS_GOAL
            WHERE member_id = %s
            ORDER BY start_date DESC
            LIMIT 3
        """, (member_id,))
        
        goals = cur.fetchall()
        if goals:
            for goal in goals:
                print(f"Goal: {goal[0]}")
                print(f"  Progress: {goal[1]} -> {goal[2]}")
                print(f"  Started: {goal[3]}, Target: {goal[4]}")
        else:
            print("No fitness goals set")
        
        # Get member's latest health metric
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
            print(f"Recorded: {metric[0]}")
            print(f"Weight: {metric[1]} kg, Height: {metric[2]} cm")
            print(f"Heart Rate: {metric[3]} BPM, Body Fat: {metric[4]}%")
        else:
            print("no health metrics recorded")
        
    except Exception as e:
        print(f"error: {e}")
    finally:
        cur.close()
        db.close_connection(conn)

def set_availability(trainer_id):

    # Set trainer availability
    # For simplicity, we're just showing the concept. In a real system this would be more complex

    print("\n=== Set Availability ===")
    print("Note: This is a simplified version")
    print("In a real system, you would have a separate AVAILABILITY table")
    
    print("\nYour availability would be set here.")
    print("For this demo, trainers are considered available unless they have")
    print("a session or class already scheduled at that time.")
    
    input("\nPress Enter to continue...")