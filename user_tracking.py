import sqlite3
import json
from datetime import datetime
import os

class UserTracker:
    def __init__(self):
        self.db_path = 'user_data.db'
        self.init_db()
    
    def init_db(self):
        """Create tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Simple interactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT DEFAULT 'anonymous',
                article_title TEXT,
                article_url TEXT,
                category TEXT,
                action TEXT,
                reading_time INTEGER DEFAULT 0,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # User preferences (calculated from interactions)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                user_id TEXT PRIMARY KEY,
                category_scores TEXT,
                last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def track_interaction(self, article_title, article_url, category, action, reading_time=0, user_id='anonymous'):
        """Track user interaction with article"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO user_interactions 
            (user_id, article_title, article_url, category, action, reading_time)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, article_title, article_url, category, action, reading_time))
        
        conn.commit()
        conn.close()
        
        # Update user preferences after each interaction
        self.update_user_preferences(user_id)
    
    def update_user_preferences(self, user_id='anonymous'):
        """Calculate user preferences based on interactions"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get category interactions for this user
        cursor.execute('''
            SELECT category, COUNT(*) as clicks, AVG(reading_time) as avg_time
            FROM user_interactions 
            WHERE user_id = ? AND action = 'click'
            GROUP BY category
        ''', (user_id,))
        
        results = cursor.fetchall()
        
        # Simple scoring: clicks * 1 + avg_reading_time * 0.1
        category_scores = {}
        for category, clicks, avg_time in results:
            if avg_time is None:
                avg_time = 0
            score = clicks * 1.0 + (avg_time * 0.1)
            category_scores[category] = round(score, 2)
        
        # Save preferences
        cursor.execute('''
            INSERT OR REPLACE INTO user_preferences (user_id, category_scores, last_updated)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        ''', (user_id, json.dumps(category_scores)))
        
        conn.commit()
        conn.close()
        
        return category_scores
    
    def get_user_preferences(self, user_id='anonymous'):
        """Get user's category preferences"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT category_scores FROM user_preferences WHERE user_id = ?
        ''', (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return json.loads(result[0])
        return {}
    
    def get_recommended_categories(self, user_id='anonymous', limit=3):
        """Get top categories for user"""
        preferences = self.get_user_preferences(user_id)
        
        if not preferences:
            # Default categories for new users
            return ['india', 'trending', 'technology']
        
        # Sort by score and return top categories
        sorted_cats = sorted(preferences.items(), key=lambda x: x[1], reverse=True)
        return [cat for cat, score in sorted_cats[:limit]]
