import sqlite3
from datetime import datetime
import bcrypt  # إضافة المكتبة

class FinanceManager:
    def __init__(self, user_id=None):
        self.conn = sqlite3.connect('finance.db', check_same_thread=False)
        self.user_id = user_id
        self.create_tables()
        self._initialize_sample_data()

    def _initialize_sample_data(self):
        # Check if sample data already exists
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users WHERE username='mohamed'")
        if cursor.fetchone()[0] > 0:
            return
            
        # Create sample user
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                      ('mohamed', '123'))
        
        # Create sample accounts
        accounts = [
            ('البنك الأهلي', 5000.0),
            ('محفظة النقود', 2000.0),
            ('بطاقة الائتمان', -1000.0)
        ]
        for name, balance in accounts:
            cursor.execute("INSERT INTO accounts (user_id, name, balance) VALUES (?, ?, ?)",
                         (1, name, balance))
        
        # Create sample categories
        categories = [
            (1, 'IN', 'مرتب'),
            (1, 'IN', 'مكافأة'),
            (1, 'OUT', 'طعام'),
            (1, 'OUT', 'مواصلات'),
            (1, 'OUT', 'تسوق')
        ]
        for acc_id, trans_type, name in categories:
            cursor.execute("INSERT INTO categories (account_id, transaction_type, name) VALUES (?, ?, ?)",
                         (acc_id, trans_type, name))
        
        # Create sample transactions
        transactions = [
            (1, 100.0, 'IN', 'مرتب شهر يناير', 'تحويل بنكي', 'مرتب', '2023-01-01'),
            (1, 50.0, 'OUT', 'سوبر ماركت', 'بطاقة ائتمان', 'طعام', '2023-01-05'),
            (2, 20.0, 'OUT', 'تاكسي', 'كاش', 'مواصلات', '2023-01-10'),
            (3, 200.0, 'OUT', 'ملابس', 'بطاقة ائتمان', 'تسوق', '2023-01-15'),
            (1, 500.0, 'IN', 'مكافأة أداء', 'تحويل بنكي', 'مكافأة', '2023-01-20')
        ]
        for acc_id, amount, trans_type, desc, method, category, date in transactions:
            cursor.execute("""
                INSERT INTO transactions 
                (account_id, amount, type, description, payment_method, category, date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (acc_id, amount, trans_type, desc, method, category, date))
        
        self.conn.commit()

    def create_tables(self):
        with self.conn:
            # جدول المستخدمين
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password TEXT NOT NULL
                )
            ''')
            # جدول الحسابات
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS accounts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    name TEXT,
                    balance REAL,
                    min_balance REAL,
                    created_at TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(username)
                )
            ''')
            # جدول المعاملات
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    date TEXT,
                    type TEXT,
                    amount REAL,
                    account_id INTEGER,
                    description TEXT,
                    payment_method TEXT,
                    category TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(username),
                    FOREIGN KEY (account_id) REFERENCES accounts(id)
                )
            ''')

    def add_user(self, username, password):
        """إضافة مستخدم جديد مع تشفير كلمة المرور"""
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        with self.conn:
            try:
                self.conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
                self.conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False  # المستخدم موجود بالفعل

    def verify_user(self, username, password):
        """التحقق من بيانات المستخدم مع فك تشفير كلمة المرور"""
        with self.conn:
            cursor = self.conn.execute('SELECT password FROM users WHERE username = ?', (username,))
            result = cursor.fetchone()
            return result and bcrypt.checkpw(password.encode('utf-8'), result[0])

    def add_account(self, name, opening_balance, min_balance):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO accounts (user_id, name, balance, min_balance, created_at) VALUES (?, ?, ?, ?, ?)",
                (self.user_id, name, opening_balance, min_balance, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            self.conn.commit()

    def get_all_accounts(self):
        with self.conn:
            cursor = self.conn.execute("SELECT * FROM accounts WHERE user_id = ?", (self.user_id,))
            return cursor.fetchall()

    def add_transaction(self, account_id, amount, trans_type, description, payment_method, category):
        with self.conn:
            cursor = self.conn.cursor()
            date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                "INSERT INTO transactions (user_id, date, type, amount, account_id, description, payment_method, category) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (self.user_id, date_now, trans_type, amount, account_id, description, payment_method, category)
            )
            if trans_type == "IN":
                cursor.execute("UPDATE accounts SET balance = balance + ? WHERE user_id = ? AND id = ?", (amount, self.user_id, account_id))
            else:
                cursor.execute("UPDATE accounts SET balance = balance - ? WHERE user_id = ? AND id = ?", (amount, self.user_id, account_id))
            self.conn.commit()
            return self.check_alerts()

    def get_all_transactions(self):
        with self.conn:
            cursor = self.conn.execute("SELECT * FROM transactions WHERE user_id = ?", (self.user_id,))
            return cursor.fetchall()

    def filter_transactions(self, account_id=None, start_date=None, end_date=None, trans_type=None, category=None):
        query = "SELECT * FROM transactions WHERE user_id = ?"
        params = [self.user_id]
        if account_id:
            query += " AND account_id = ?"
            params.append(account_id)
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        if trans_type:
            query += " AND type = ?"
            params.append(trans_type)
        if category:
            query += " AND category = ?"
            params.append(category)
        with self.conn:
            cursor = self.conn.execute(query, params)
            return cursor.fetchall()

    def edit_transaction(self, trans_id, account_id, amount, trans_type, description, payment_method, category):
        with self.conn:
            cursor = self.conn.cursor()
            old_trans = cursor.execute("SELECT type, amount, account_id FROM transactions WHERE user_id = ? AND id = ?", (self.user_id, trans_id)).fetchone()
            if old_trans:
                old_type, old_amount, old_account_id = old_trans
                cursor.execute("UPDATE transactions SET account_id = ?, type = ?, amount = ?, description = ?, payment_method = ?, category = ? WHERE user_id = ? AND id = ?",
                               (account_id, trans_type, amount, description, payment_method, category, self.user_id, trans_id))
                if old_account_id == account_id:
                    if old_type == "IN" and trans_type == "IN":
                        diff = amount - old_amount
                        cursor.execute("UPDATE accounts SET balance = balance + ? WHERE user_id = ? AND id = ?", (diff, self.user_id, account_id))
                    elif old_type == "OUT" and trans_type == "OUT":
                        diff = old_amount - amount
                        cursor.execute("UPDATE accounts SET balance = balance + ? WHERE user_id = ? AND id = ?", (diff, self.user_id, account_id))
                    elif old_type == "IN" and trans_type == "OUT":
                        cursor.execute("UPDATE accounts SET balance = balance - ? - ? WHERE user_id = ? AND id = ?", (old_amount, amount, self.user_id, account_id))
                    elif old_type == "OUT" and trans_type == "IN":
                        cursor.execute("UPDATE accounts SET balance = balance + ? + ? WHERE user_id = ? AND id = ?", (old_amount, amount, self.user_id, account_id))
                else:
                    if old_type == "IN":
                        cursor.execute("UPDATE accounts SET balance = balance - ? WHERE user_id = ? AND id = ?", (old_amount, self.user_id, old_account_id))
                    else:
                        cursor.execute("UPDATE accounts SET balance = balance + ? WHERE user_id = ? AND id = ?", (old_amount, self.user_id, old_account_id))
                    if trans_type == "IN":
                        cursor.execute("UPDATE accounts SET balance = balance + ? WHERE user_id = ? AND id = ?", (amount, self.user_id, account_id))
                    else:
                        cursor.execute("UPDATE accounts SET balance = balance - ? WHERE user_id = ? AND id = ?", (amount, self.user_id, account_id))
                self.conn.commit()
                return self.check_alerts()

    def check_alerts(self):
        with self.conn:
            cursor = self.conn.execute("SELECT id, name, balance, min_balance FROM accounts WHERE user_id = ?", (self.user_id,))
            alerts = [f"الحساب {row[1]} تحت الحد الأدنى: {row[2]:,.2f} (الحد: {row[3]:,.2f})" for row in cursor.fetchall() if row[2] < row[3]]
            return "تنبيه: " + ", ".join(alerts) if alerts else None

    def get_custom_categories(self, account_id, trans_type):
        with self.conn:
            cursor = self.conn.execute("SELECT DISTINCT category FROM transactions WHERE user_id = ? AND account_id = ? AND type = ? AND category IS NOT NULL", 
                                       (self.user_id, account_id, trans_type))
            return cursor.fetchall()

    def add_custom_category(self, account_id, trans_type, category_name):
        existing = self.get_custom_categories(account_id, trans_type)
        if category_name not in [cat[0] for cat in existing]:
            self.add_transaction(account_id, 0, trans_type, f"إضافة فئة: {category_name}", "كاش", category_name)

    def delete_custom_category_by_name(self, account_id, trans_type, category_name):
        with self.conn:
            self.conn.execute("UPDATE transactions SET category = NULL WHERE user_id = ? AND account_id = ? AND type = ? AND category = ?", 
                              (self.user_id, account_id, trans_type, category_name))
            self.conn.commit()