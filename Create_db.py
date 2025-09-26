import sqlite3  # Import the SQLite library to interact with the database

def create_database():
    # Connect to SQLite database 
    conn = sqlite3.connect('gym_database.db')
    cursor = conn.cursor()

    try:
        # Create 'staff' table to store staff details
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS staff (
                forname TEXT,
                surname TEXT,
                username TEXT PRIMARY KEY,
                email TEXT,
                password TEXT,
                staff_id TEXT,
                role TEXT
            )
        ''')

        # Create 'members' table to store member details and their membership plans
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS members (
                username TEXT PRIMARY KEY,
                email TEXT,
                password TEXT,
                member_id TEXT,
                role TEXT,
                membership_plan TEXT,
                price REAL
            )
        ''')

        # Create 'classes' table to store class schedule and details
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS classes (
                class_id TEXT PRIMARY KEY,
                class_name TEXT,
                date TEXT,
                time TEXT,
                duration TEXT,
                capacity INTEGER,
                difficulty_level TEXT
            )
        ''')

        # Create 'trainers' table to store trainer details 
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trainers (
                forname TEXT,
                surname TEXT,
                staff_id TEXT PRIMARY KEY
            )
        ''')

        # Create 'member_class' table to record which members sign up for which classes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS member_class (
                member_id TEXT,
                class_id TEXT,
                signup_date TEXT,
                PRIMARY KEY (member_id, class_id),
                FOREIGN KEY (member_id) REFERENCES members(member_id),
                FOREIGN KEY (class_id) REFERENCES classes(class_id)
            )
        ''')

        # Create 'assignments' table to assign trainers to classes and record assignment details
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS assignments (
                assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                class_id TEXT,
                class_name TEXT,
                trainer_id TEXT,
                trainer_name TEXT,
                date TEXT,
                duration_minutes INTEGER,
                assignment_date TEXT,
                FOREIGN KEY (class_id) REFERENCES classes(class_id),
                FOREIGN KEY (trainer_id) REFERENCES trainers(staff_id)
            )
        ''')

        # Create 'trainer_hours' table to track hours worked by each trainer
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trainer_hours (
                record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                trainer_id TEXT,
                trainer_name TEXT,
                date TEXT,
                minutes_worked INTEGER,
                FOREIGN KEY (trainer_id) REFERENCES trainers(staff_id)
            )
        ''')

        # Adding data into 'staff' table
        staff_data = [
            ('Jake', 'Smith', 'j.smith1', 'j.smith1@flexigym.com', 'nuhuyty123!!', 'JS897', 'admin/trainer'),
            ('Paul', 'Wright', 'P.wright12', 'P.wright12@flexigym.com', 'nhhhyy67512!', 'PW876556', 'trainer'),
            ('Ian', 'Gayle', 'I.Gayle', 'i.gayle@flexigym.com', 'bghiujjy767', 'IG764', 'manager'),
            ('Hasan', 'Shah', 'H.Shah', 'H.Shah@flexigym.com', 'qwerty55412', 'HS1265', 'trainer'),
            ('Jason', 'Smith', 'j.smith2', 'j.smith2@flexigym.com', 'csaqwert56', 'JS89767', 'trainer'),
            ('Kelly', 'Cates', 'k.cates23', 'k.cates23@flexigym.com', 'tyvggyt543', 'KC54321', 'trainer'),
            ('Aaron', 'James', 'a.james2', 'a.james2@flexigym.com', 'jhtygvbui23', 'AJYTBT1', 'trainer'),
            ('Ian', 'Ward', 'i.ward', 'i.ward@flexigym.com', 'ygt63466871!', 'IW454321', 'trainer'),
            ('Yousuf', 'Raza', 'y.raza', 'y.raza@flexigym.com', 'bhyt234511', 'YR2346876', 'trainer'),
            ('Hayley', 'Wright', 'H.Wright', 'h.wright@flexigym.com', 'gtyybtytqwe', 'HW3224567', 'trainer')
        ]
        cursor.executemany('''
            INSERT OR REPLACE INTO staff 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', staff_data)

        # Adding  data into 'members' table
        members_data = [
            ('TJ234', 'Javis11@gmail.com', 'wer1234!!', 'TomJ236', 'member', 'Basic', 10.00),
            ('BeingSalmanKhan21', 'beinghuman23@gmail.com', 'nbhbytb123!', 'KHA1234', 'member', 'Silver', 15.00),
            ('shera01', 'beingshera@live.com', 'nhgbuytb', 'Gur23458', 'member', 'Gold', 20.00),
            ('Kevin-_1', 'k.hil123@gmail.com', 'nbnhon123!', 'KEV233', 'member', 'Inclusive', 25.00),
            ('Mstarc223', 'starc22@gmail.com', 'bvyvhy123!', 'Matt765', 'member', 'Student', 30.00),
            ('qasimero234', 'qasimero13@outlook.com', 'jhijbv12335', 'QAS3246', 'member', 'VIP Elite', 35.00),
            ('Stuart08', 'broaddy@gmail.com', 'bvyyt123!!', 'STU1289', 'member', 'Premium', 40.00),
            ('Jimmy09', 'JA99@outlook.com', 'hghnqwe34!', 'JAM2347', 'member', 'Personal Training', 55.00),
            ('JS234', 'JS21@outlook.com', 'bhybtynb1!', 'JOH768943', 'member', 'Platinum', 60.00),
            ('Smith01', 'e.smith23@gmail.com', 'bhygbf67g!!1', 'EMM234', 'member', 'Diamond', 65.00),
            ('Louise23', 'l.tate234@gmail.com', 'bbhhyytfqw', 'LOU123!!', 'member', 'Family', 70.00)
        ]
        cursor.executemany('''
            INSERT OR REPLACE INTO members 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', members_data)

        # Adding data into 'classes' table
        classes_data = [
            ('Y0001', 'Morning Yoga', '03/06/2025', '7:30am', '60min', 10, 'Beginner'),
            ('HI002', 'Hip Pop Dance', '07/06/2025', '10:00am', '45min', 20, 'Advanced'),
            ('SC003', 'Spin Cycling', '13/06/2025', '11:30am', '30min', 15, 'Intermediate'),
            ('PI004', 'Pilates Core', '16/06/2025', '3:00pm', '30min', 8, 'Beginner'),
            ('B0005', 'Boxing Fitness', '17/06/2025', '3:30pm', '45min', 10, 'Intermediate'),
            ('ZU006', 'Zumba Dance', '21/06/2025', '8:00am', '30min', 20, 'Beginner'),
            ('PL007', 'Powerlifting', '01/07/2025', '5:00pm', '15min', 9, 'Advanced'),
            ('SR008', 'Stretch & Relax', '05/07/2025', '9:30am', '20min', 25, 'Beginner'),
            ('CF009', 'CrossFit', '20/07/2025', '4:15pm', '45min', 10, 'Advanced'),
            ('KB010', 'Kickboxing', '30/07/2025', '9:45pm', '35min', 5, 'Intermediate')
        ]
        cursor.executemany('''
            INSERT OR REPLACE INTO classes 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', classes_data)

        # Adding data into 'trainers' table
        trainers_data = [
            ('Jake', 'Smith', 'JS897'),
            ('Paul', 'Wright', 'PW876556'),
            ('Hasan', 'Shah', 'HS1265'),
            ('Jason', 'Smith', 'JS89767'),
            ('Kelly', 'Cates', 'KC54321'),
            ('Aaron', 'James', 'AJYTBT1'),
            ('Ian', 'Ward', 'IW454321'),
            ('Yousuf', 'Raza', 'YR2346876'),
            ('Hayley', 'Wright', 'HW3224567')
        ]
        cursor.executemany('''
            INSERT OR REPLACE INTO trainers 
            VALUES (?, ?, ?)
        ''', trainers_data)

        # Commit to database
        conn.commit()
        print("Database created successfully!")

        # Optional: print record count from each table for verification
        print("\nVerifying data counts:")
        tables = ['staff', 'members', 'classes', 'trainers', 'member_class', 'assignments', 'trainer_hours']
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"{table}: {count} records")

    except sqlite3.Error as e:
        # Handle database errors and rollback if needed
        print(f"Database error: {e}")
        conn.rollback()
    finally:
        # Close database connection
        conn.close()

# Run the function to create the database when the script is executed
if __name__ == "__main__":
    create_database()
