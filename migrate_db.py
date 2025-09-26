import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('instance/app.db')
cursor = conn.cursor()

# Check if the columns exist before trying to alter
cursor.execute("PRAGMA table_info(geolocation_searches)")
columns = cursor.fetchall()
column_names = [column[1] for column in columns]

# Create a new table with the updated schema
cursor.execute('''
CREATE TABLE IF NOT EXISTS geolocation_searches_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ip_address VARCHAR(45) NOT NULL,
    location VARCHAR(100) NOT NULL,
    isp VARCHAR(100) NOT NULL,
    timestamp DATETIME NOT NULL,
    user_id INTEGER NOT NULL
)
''')

# Copy data from the old table to the new table
if 'phone_number' in column_names and 'provider' in column_names:
    cursor.execute('''
    INSERT INTO geolocation_searches_new (id, ip_address, location, isp, timestamp, user_id)
    SELECT id, phone_number, location, provider, timestamp, user_id FROM geolocation_searches
    ''')
    
    # Drop the old table
    cursor.execute('DROP TABLE geolocation_searches')
    
    # Rename the new table to the original name
    cursor.execute('ALTER TABLE geolocation_searches_new RENAME TO geolocation_searches')
    
    print("Database migration completed successfully!")
else:
    cursor.execute('DROP TABLE geolocation_searches_new')
    print("Migration not needed or columns already updated.")

# Commit the changes and close the connection
conn.commit()
conn.close()