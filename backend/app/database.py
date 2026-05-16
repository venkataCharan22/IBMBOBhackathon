"""
Database initialization and models
SQLite database with projects and risks tables
"""

import sqlite3
from pathlib import Path
from typing import Optional
import json
from datetime import datetime


class Database:
    """SQLite database manager for Bug2PR"""
    
    def __init__(self, db_path: str = "./bug2pr.db"):
        self.db_path = db_path
        self.init_db()
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection with row factory"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        """Initialize database with required tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Projects table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                repo_url TEXT,
                github_owner TEXT,
                github_repo TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'active',
                metadata TEXT
            )
        """)
        
        # Risks/Issues table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS risks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                title TEXT NOT NULL,
                description TEXT,
                severity TEXT DEFAULT 'medium',
                category TEXT,
                error_log TEXT,
                stack_trace TEXT,
                file_path TEXT,
                line_number INTEGER,
                status TEXT DEFAULT 'open',
                pr_url TEXT,
                pr_number INTEGER,
                fix_description TEXT,
                test_added BOOLEAN DEFAULT 0,
                security_audit_passed BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                resolved_at TIMESTAMP,
                metadata TEXT,
                FOREIGN KEY (project_id) REFERENCES projects (id)
            )
        """)
        
        # Analysis results table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                risk_id INTEGER,
                agent_name TEXT NOT NULL,
                analysis_type TEXT,
                result TEXT,
                confidence_score REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT,
                FOREIGN KEY (risk_id) REFERENCES risks (id)
            )
        """)
        
        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_risks_project ON risks(project_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_risks_status ON risks(status)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_analysis_risk ON analysis_results(risk_id)")
        
        conn.commit()
        conn.close()
    
    def create_project(self, name: str, description: Optional[str] = None, 
                      repo_url: Optional[str] = None, **kwargs) -> int:
        """Create a new project"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        metadata = json.dumps(kwargs) if kwargs else None
        
        cursor.execute("""
            INSERT INTO projects (name, description, repo_url, metadata)
            VALUES (?, ?, ?, ?)
        """, (name, description, repo_url, metadata))
        
        project_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return project_id
    
    def create_risk(self, project_id: int, title: str, description: Optional[str] = None,
                   severity: str = "medium", **kwargs) -> int:
        """Create a new risk/issue"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        metadata = json.dumps({k: v for k, v in kwargs.items() 
                              if k not in ['error_log', 'stack_trace', 'file_path', 'line_number']})
        
        cursor.execute("""
            INSERT INTO risks (
                project_id, title, description, severity, 
                error_log, stack_trace, file_path, line_number, metadata
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            project_id, title, description, severity,
            kwargs.get('error_log'), kwargs.get('stack_trace'),
            kwargs.get('file_path'), kwargs.get('line_number'),
            metadata
        ))
        
        risk_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return risk_id
    
    def update_risk(self, risk_id: int, **kwargs):
        """Update risk fields"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Build dynamic update query
        fields = []
        values = []
        for key, value in kwargs.items():
            if key != 'id':
                fields.append(f"{key} = ?")
                values.append(value)
        
        if fields:
            fields.append("updated_at = CURRENT_TIMESTAMP")
            query = f"UPDATE risks SET {', '.join(fields)} WHERE id = ?"
            values.append(risk_id)
            cursor.execute(query, values)
            conn.commit()
        
        conn.close()
    
    def get_project(self, project_id: int) -> Optional[dict]:
        """Get project by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    def get_risk(self, risk_id: int) -> Optional[dict]:
        """Get risk by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM risks WHERE id = ?", (risk_id,))
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    def list_projects(self, status: Optional[str] = None) -> list[dict]:
        """List all projects"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if status:
            cursor.execute("SELECT * FROM projects WHERE status = ? ORDER BY created_at DESC", (status,))
        else:
            cursor.execute("SELECT * FROM projects ORDER BY created_at DESC")
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def list_risks(self, project_id: Optional[int] = None, 
                   status: Optional[str] = None) -> list[dict]:
        """List risks with optional filters"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM risks WHERE 1=1"
        params = []
        
        if project_id:
            query += " AND project_id = ?"
            params.append(project_id)
        
        if status:
            query += " AND status = ?"
            params.append(status)
        
        query += " ORDER BY created_at DESC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]


# Global database instance
db = Database()

# Made with Bob
