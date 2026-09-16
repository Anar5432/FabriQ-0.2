import sqlite3
conn = sqlite3.connect('factory.db')
c = conn.cursor()
try:
    c.execute("ALTER TABLE orders ADD COLUMN difficulty VARCHAR")
except:
    pass
try:
    c.execute("ALTER TABLE orders ADD COLUMN workers_assigned INTEGER")
except:
    pass
try:
    c.execute("ALTER TABLE orders ADD COLUMN planned_days INTEGER")
except:
    pass
conn.commit()
conn.close()
