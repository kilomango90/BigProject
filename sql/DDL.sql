-- Health and Fitness Club Management System (Final Project for COMP3005A)
-- By: Badr Ahmed (#101226464) & Faris Ahmed (#101142716)

-- Drop existing tables if they exist
DROP TABLE IF EXISTS CLASS_REGISTRATION CASCADE;
DROP TABLE IF EXISTS PERSONAL_TRAINING_SESSION CASCADE;
DROP TABLE IF EXISTS GROUP_CLASS CASCADE;
DROP TABLE IF EXISTS HEALTH_METRIC CASCADE;
DROP TABLE IF EXISTS FITNESS_GOAL CASCADE;
DROP TABLE IF EXISTS ROOM CASCADE;
DROP TABLE IF EXISTS ADMINISTRATIVE_STAFF CASCADE;
DROP TABLE IF EXISTS TRAINER CASCADE;
DROP TABLE IF EXISTS MEMBER CASCADE;

-- Initialize MEMBER table
-- address has been separated into street, city, and postal code fields to satisfy 1NF requirements
CREATE TABLE MEMBER (
    member_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    date_of_birth DATE,
    gender VARCHAR(10),
    street VARCHAR(100),
    city VARCHAR(50),
    postal_code VARCHAR(10)
);

-- Create TRAINER table
CREATE TABLE TRAINER (
    trainer_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    specialization VARCHAR(100)
);

-- Initialize ADMINSTRATIVE_STAFF table
CREATE TABLE ADMINISTRATIVE_STAFF (
    admin_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20)
);

-- Initialize FITNESS_GOAL table
-- Each goal belongs to one member (that's why member_id is there)
CREATE TABLE FITNESS_GOAL (
    goal_id SERIAL PRIMARY KEY,
    member_id INTEGER NOT NULL,
    goal_type VARCHAR(50),
    target_value DECIMAL(10,2),
    current_value DECIMAL(10,2),
    start_date DATE,
    target_date DATE,
    FOREIGN KEY (member_id) REFERENCES MEMBER(member_id) ON DELETE CASCADE
);

-- Make HEALTH_METRIC table
-- Health metrics track member health data over time so progress can be seen
CREATE TABLE HEALTH_METRIC (
    metric_id SERIAL PRIMARY KEY,
    member_id INTEGER NOT NULL,
    date_recorded DATE NOT NULL,
    weight DECIMAL(5,2),
    height DECIMAL(5,2),
    heart_rate INTEGER,
    body_fat_percentage DECIMAL(5,2),
    FOREIGN KEY (member_id) REFERENCES MEMBER(member_id) ON DELETE CASCADE
);

-- Initialize ROOM table
CREATE TABLE ROOM (
    room_id SERIAL PRIMARY KEY,
    room_name VARCHAR(50) NOT NULL,
    capacity INTEGER,
    equipment_available TEXT
);

-- Initialize PERSONAL_TRAINING_SESSION table
-- Connects members with trainers for 1 on 1 sessions (that's why there's a member id and a trainer id')
CREATE TABLE PERSONAL_TRAINING_SESSION (
    session_id SERIAL PRIMARY KEY,
    member_id INTEGER NOT NULL,
    trainer_id INTEGER,
    room_id INTEGER,
    session_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    status VARCHAR(20),
    FOREIGN KEY (member_id) REFERENCES MEMBER(member_id) ON DELETE CASCADE,
    FOREIGN KEY (trainer_id) REFERENCES TRAINER(trainer_id) ON DELETE SET NULL,
    FOREIGN KEY (room_id) REFERENCES ROOM(room_id) ON DELETE SET NULL
);

-- Create GROUP_CLASS table
-- These are classes that multiple members can attend
CREATE TABLE GROUP_CLASS (
    class_id SERIAL PRIMARY KEY,
    trainer_id INTEGER,  
    room_id INTEGER,
    class_name VARCHAR(100) NOT NULL,
    class_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    capacity INTEGER NOT NULL,
    current_enrollment INTEGER DEFAULT 0,
    FOREIGN KEY (trainer_id) REFERENCES TRAINER(trainer_id) ON DELETE SET NULL,
    FOREIGN KEY (room_id) REFERENCES ROOM(room_id) ON DELETE SET NULL
);

-- Initialize CLASS_REGISTRATION table
-- A member can register for many classes, and classes can have many members
CREATE TABLE CLASS_REGISTRATION (
    member_id INTEGER NOT NULL,
    class_id INTEGER NOT NULL,
    registration_date DATE NOT NULL DEFAULT CURRENT_DATE,
    PRIMARY KEY (member_id, class_id),
    FOREIGN KEY (member_id) REFERENCES MEMBER(member_id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES GROUP_CLASS(class_id) ON DELETE CASCADE
);

-- Shows useful summary info for each member
-- This lists a nice summary of each member's activity
CREATE VIEW member_dashboard AS
SELECT 
    m.member_id,
    m.name,
    m.email,
    COUNT(DISTINCT pts.session_id) as total_pt_sessions,
    COUNT(DISTINCT cr.class_id) as total_classes_registered,
    COUNT(DISTINCT hm.metric_id) as total_health_records
FROM MEMBER m
LEFT JOIN PERSONAL_TRAINING_SESSION pts ON m.member_id = pts.member_id
LEFT JOIN CLASS_REGISTRATION cr ON m.member_id = cr.member_id
LEFT JOIN HEALTH_METRIC hm ON m.member_id = hm.member_id
GROUP BY m.member_id, m.name, m.email;

-- Whenever someone registers or unregisters, update current_enrollment
CREATE OR REPLACE FUNCTION update_class_enrollment()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        -- Increase count if someone registers
        UPDATE GROUP_CLASS 
        SET current_enrollment = current_enrollment + 1
        WHERE class_id = NEW.class_id;
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN

        -- Decrease count if someone unregisters
        UPDATE GROUP_CLASS 
        SET current_enrollment = current_enrollment - 1
        WHERE class_id = OLD.class_id;
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER enrollment_trigger
AFTER INSERT OR DELETE ON CLASS_REGISTRATION
FOR EACH ROW
EXECUTE FUNCTION update_class_enrollment();

-- Indexes for better query performance
CREATE INDEX idx_member_email ON MEMBER(email);
CREATE INDEX idx_trainer_email ON TRAINER(email);
CREATE INDEX idx_session_date ON PERSONAL_TRAINING_SESSION(session_date);
CREATE INDEX idx_class_date ON GROUP_CLASS(class_date);
CREATE INDEX idx_health_metric_date ON HEALTH_METRIC(date_recorded);