-- Health and Fitness Club Management System (Final Project for COMP3005A)
-- By: Badr Ahmed (#101226464) & Faris Ahmed (#101142716)

-- Adding MEMBER data
INSERT INTO MEMBER (name, email, phone, date_of_birth, gender, street, city, postal_code)
VALUES 
    ('John Smith', 'john.smith@email.com', '613-555-0001', '1990-05-15', 'Male', '123 Main St', 'Ottawa', 'K1A 0B1'),
    ('Sarah Johnson', 'sarah.j@email.com', '613-555-0002', '1985-08-22', 'Female', '456 Oak Ave', 'Kanata', 'K2K 1X4'),
    ('Mike Brown', 'mbrown@email.com', '613-555-0003', '1992-03-10', 'Male', '789 Pine Rd', 'Nepean', 'K2G 3J2'),
    ('Emily Davis', 'emily.davis@email.com', '613-555-0004', '1988-11-30', 'Female', '321 Elm St', 'Ottawa', 'K1P 5N2'),
    ('David Wilson', 'dwilson@email.com', '613-555-0005', '1995-07-18', 'Male', '654 Maple Dr', 'Barrhaven', 'K2J 4B4');

 -- Adding TRAINER data
INSERT INTO TRAINER (name, email, phone, specialization)
VALUES 
    ('Jane Cooper', 'jane.cooper@fitness.com', '613-555-1001', 'Yoga'),
    ('Tom Harris', 'tom.harris@fitness.com', '613-555-1002', 'Weight Training'),
    ('Lisa Martinez', 'lisa.m@fitness.com', '613-555-1003', 'Cardio'),
    ('Chris Lee', 'chris.lee@fitness.com', '613-555-1004', 'CrossFit');

 -- Adding ADMINSTRATIVE_STAFF data
 INSERT INTO ADMINISTRATIVE_STAFF (name, email, phone)
VALUES 
    ('Admin User', 'admin@fitness.com', '613-555-9001'),
    ('Manager Smith', 'manager@fitness.com', '613-555-9002'),
    ('Front Desk', 'frontdesk@fitness.com', '613-555-9003');

-- Adding FITNESS_GOAL data
    -- John has 2 goals as stated by the member id
    -- Sarah has 1 goal as stated by the member id 
    -- Mike has 1 goal as stated by the member id 
    -- Emily has 1 goal as stated by the member id 
INSERT INTO FITNESS_GOAL (member_id, goal_type, target_value, current_value, start_date, target_date)
VALUES 
    (1, 'Weight Loss', 80.0, 90.0, '2024-11-01', '2025-03-01'),
    (1, 'Running Distance', 10.0, 3.0, '2024-11-01', '2025-02-01');
INSERT INTO FITNESS_GOAL (member_id, goal_type, target_value, current_value, start_date, target_date)
VALUES 
    (2, 'Muscle Gain', 60.0, 55.0, '2024-10-15', '2025-04-15');

INSERT INTO FITNESS_GOAL (member_id, goal_type, target_value, current_value, start_date, target_date)
VALUES 
    (3, 'Body Fat Reduction', 15.0, 22.0, '2024-11-10', '2025-05-10');
INSERT INTO FITNESS_GOAL (member_id, goal_type, target_value, current_value, start_date, target_date)
VALUES 
    (4, 'Cardio Endurance', 45.0, 30.0, '2024-11-15', '2025-03-15');

-- Adding HEALTH_METRIC data
    -- First are John's metrics over time as stated by the member id
    -- Second are Sarah's metrics over time as stated by the member id
    -- Third are Mike's metrics over time as stated by the member id
    -- Fourth are Emily's metrics over time as stated by the member id
INSERT INTO HEALTH_METRIC (member_id, date_recorded, weight, height, heart_rate, body_fat_percentage)
VALUES 
    (1, '2024-11-01', 90.0, 178.0, 80, 25.0),
    (1, '2024-11-15', 88.5, 178.0, 78, 24.0),
    (1, '2024-12-01', 87.0, 178.0, 75, 23.5);
INSERT INTO HEALTH_METRIC (member_id, date_recorded, weight, height, heart_rate, body_fat_percentage)
VALUES 
    (2, '2024-10-15', 55.0, 165.0, 70, 20.0),
    (2, '2024-11-15', 56.5, 165.0, 68, 19.5);
INSERT INTO HEALTH_METRIC (member_id, date_recorded, weight, height, heart_rate, body_fat_percentage)
VALUES 
    (3, '2024-11-10', 85.0, 180.0, 75, 22.0),
    (3, '2024-11-25', 84.0, 180.0, 73, 21.0);
INSERT INTO HEALTH_METRIC (member_id, date_recorded, weight, height, heart_rate, body_fat_percentage)
VALUES 
    (4, '2024-11-15', 62.0, 168.0, 72, 22.0);

-- Adding ROOM data
INSERT INTO ROOM (room_name, capacity, equipment_available)
VALUES 
    ('Studio A', 20, 'Yoga mats, mirrors, sound system'),
    ('Weight Room', 15, 'Free weights, bench press, squat rack, dumbbells'),
    ('Cardio Zone', 25, 'Treadmills, ellipticals, bikes, rowing machines'),
    ('Multipurpose Room', 30, 'Mats, resistance bands, kettlebells');

-- Adding GROUP_CLASS data
    -- First and second are Jane's Yoga as stated by the trainer id
    -- Third is Tom's strength training as stated by the trainer id
    -- Fourth is Lisa teaching cardio as stated by the trainer id
    -- Fifth is Chris teaching crossfit as stated by the trainer id
INSERT INTO GROUP_CLASS (trainer_id, room_id, class_name, class_date, start_time, end_time, capacity, current_enrollment)
VALUES
    (1, 1, 'Morning Yoga', '2024-12-02', '08:00', '09:00', 20, 0),
    (1, 1, 'Evening Yoga', '2024-12-02', '18:00', '19:00', 20, 0),
    (2, 2, 'Strength Training 101', '2024-12-03', '10:00', '11:00', 15, 0),
    (3, 3, 'Cardio Blast', '2024-12-03', '17:00', '18:00', 25, 0),
    (4, 4, 'CrossFit Fundamentals', '2024-12-04', '12:00', '13:00', 30, 0);

-- Adding CLASS_REGISTRATION data
    -- First John registers for morning yoga and weight room as stated by member id and class id
    -- Second Sarah registers for evening yoga and crossfit as stated by member id and class id
    -- Third Mike registers for cardio as stated by member id and class id
    -- Fourth Emily registers for morning yoga as stated by member id and class id
    -- Fifth David registers for weight room and cardio as stated by member id and class id
INSERT INTO CLASS_REGISTRATION (member_id, class_id, registration_date)
VALUES 
    (1, 1, '2024-11-20'),
    (1, 3, '2024-11-21');
INSERT INTO CLASS_REGISTRATION (member_id, class_id, registration_date)
VALUES 
    (2, 2, '2024-11-22'),
    (2, 5, '2024-11-22');
INSERT INTO CLASS_REGISTRATION (member_id, class_id, registration_date)
VALUES 
    (3, 4, '2024-11-23');
INSERT INTO CLASS_REGISTRATION (member_id, class_id, registration_date)
VALUES 
    (4, 1, '2024-11-24');
INSERT INTO CLASS_REGISTRATION (member_id, class_id, registration_date)
VALUES 
    (5, 3, '2024-11-25'),
    (5, 4, '2024-11-25');

-- Adding PERSONAL_TRAINING_SESSION data
    -- First John is scheduled a session with Tom
    -- Second Sarah is scheduled a session with Lisa
    -- Third Mike is scheduled a session with Chris
    -- Fourth Emily is scheduled a session with Jane
    -- Fifth David is scheduled a session with Tom

INSERT INTO PERSONAL_TRAINING_SESSION (member_id, trainer_id, room_id, session_date, start_time, end_time, status)
VALUES 
    (1, 2, 2, '2024-12-02', '14:00', '15:00', 'Scheduled');
INSERT INTO PERSONAL_TRAINING_SESSION (member_id, trainer_id, room_id, session_date, start_time, end_time, status)
VALUES 
    (2, 3, 3, '2024-12-03', '15:00', '16:00', 'Scheduled'),
    (2, 3, 3, '2024-11-28', '15:00', '16:00', 'Completed');
INSERT INTO PERSONAL_TRAINING_SESSION (member_id, trainer_id, room_id, session_date, start_time, end_time, status)
VALUES 
    (3, 4, 4, '2024-12-04', '16:00', '17:00', 'Scheduled');
INSERT INTO PERSONAL_TRAINING_SESSION (member_id, trainer_id, room_id, session_date, start_time, end_time, status)
VALUES 
    (4, 1, 1, '2024-12-05', '10:00', '11:00', 'Scheduled'),
    (4, 1, 1, '2024-11-29', '10:00', '11:00', 'Completed');
INSERT INTO PERSONAL_TRAINING_SESSION (member_id, trainer_id, room_id, session_date, start_time, end_time, status)
VALUES 
    (5, 2, 2, '2024-12-06', '11:00', '12:00', 'Scheduled');

-- Checking if insertions and enrollment were correct
SELECT 'Members:', COUNT(*) FROM MEMBER;
SELECT 'Trainers:', COUNT(*) FROM TRAINER;
SELECT 'Admins:', COUNT(*) FROM ADMINISTRATIVE_STAFF;
SELECT 'Fitness Goals:', COUNT(*) FROM FITNESS_GOAL;
SELECT 'Health Metrics:', COUNT(*) FROM HEALTH_METRIC;
SELECT 'Rooms:', COUNT(*) FROM ROOM;
SELECT 'Group Classes:', COUNT(*) FROM GROUP_CLASS;
SELECT 'Class Registrations:', COUNT(*) FROM CLASS_REGISTRATION;
SELECT 'Personal Training Sessions:', COUNT(*) FROM PERSONAL_TRAINING_SESSION;
SELECT class_name, capacity, current_enrollment 
FROM GROUP_CLASS 
ORDER BY class_id;