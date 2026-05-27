# Database Initialization Function with Cloud Safety Fallback
def init_db():
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS evaluation_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                cgpa REAL,
                iq INTEGER,
                status_result TEXT
            )
        ''')
        conn.commit()
        conn.close()
    except sqlite3.OperationalError:
        # If running on Streamlit Cloud's read-only system, skip database initialization gracefully
        pass

def log_prediction(cgpa_val, iq_val, result_text):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO evaluation_logs (cgpa, iq, status_result)
            VALUES (?, ?, ?)
        ''', (cgpa_val, iq_val, result_text))
        conn.commit()
        conn.close()
    except sqlite3.OperationalError:
        pass

def get_prediction_logs():
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query("SELECT timestamp, cgpa, iq, status_result FROM evaluation_logs ORDER BY id DESC", conn)
        conn.close()
        return df
    except Exception:
        # Return an empty dataframe placeholder if database logging is restricted online
        return pd.DataFrame(columns=["timestamp", "cgpa", "iq", "status_result"])
