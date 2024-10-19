import sqlite3
from datetime import datetime
from typing import Dict, List, Optional

class RegistrationSystem:
    def __init__(self, db_name: str = "registration.db"):
        """Initialize the registration system with a SQLite database."""
        self.db_name = db_name
        self.create_table()
    
    def create_table(self) -> None:
        """Create the Registration table if it doesn't exist."""
        query = '''
        CREATE TABLE IF NOT EXISTS Registration (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            date_of_birth DATE NOT NULL,
            phone_number VARCHAR(20),
            address TEXT,
            registration_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            status VARCHAR(20) DEFAULT 'active' CHECK(status IN ('active', 'inactive', 'pending')),
            CONSTRAINT valid_email CHECK(email LIKE '%_@__%.__%'),
            CONSTRAINT valid_name CHECK(length(name) >= 2)
        )
        '''
        with sqlite3.connect(self.db_name) as conn:
            conn.execute(query)
    
    def create_registration(self, user_data: Dict) -> int:
        """
        Create a new registration record.
        
        Args:
            user_data: Dictionary containing user information
            
        Returns:
            The ID of the newly created registration
        """
        query = '''
        INSERT INTO Registration (name, email, date_of_birth, phone_number, address)
        VALUES (?, ?, ?, ?, ?)
        '''
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(query, (
                    user_data['name'],
                    user_data['email'],
                    user_data['date_of_birth'],
                    user_data.get('phone_number'),
                    user_data.get('address')
                ))
                return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            if "email" in str(e):
                raise ValueError("Email already exists")
            raise ValueError(str(e))
    
    def read_registration(self, registration_id: int) -> Optional[Dict]:
        """
        Read a registration record by ID.
        
        Args:
            registration_id: The ID of the registration to retrieve
            
        Returns:
            Dictionary containing registration data or None if not found
        """
        query = "SELECT * FROM Registration WHERE id = ?"
        with sqlite3.connect(self.db_name) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, (registration_id,))
            result = cursor.fetchone()
            return dict(result) if result else None
    
    def read_all_registrations(self) -> List[Dict]:
        """
        Read all registration records.
        
        Returns:
            List of dictionaries containing registration data
        """
        query = "SELECT * FROM Registration"
        with sqlite3.connect(self.db_name) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]
    
    def update_registration(self, registration_id: int, update_data: Dict) -> bool:
        """
        Update a registration record.
        
        Args:
            registration_id: The ID of the registration to update
            update_data: Dictionary containing fields to update
            
        Returns:
            True if update was successful, False if record not found
        """
        allowed_fields = {'name', 'email', 'date_of_birth', 'phone_number', 'address', 'status'}
        update_fields = {k: v for k, v in update_data.items() if k in allowed_fields}
        
        if not update_fields:
            raise ValueError("No valid fields to update")
        
        query = f'''
        UPDATE Registration 
        SET {', '.join(f'{field} = ?' for field in update_fields)}
        WHERE id = ?
        '''
        
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(query, (*update_fields.values(), registration_id))
                return cursor.rowcount > 0
        except sqlite3.IntegrityError as e:
            raise ValueError(str(e))
    
    def delete_registration(self, registration_id: int) -> bool:
        """
        Delete a registration record.
        
        Args:
            registration_id: The ID of the registration to delete
            
        Returns:
            True if deletion was successful, False if record not found
        """
        query = "DELETE FROM Registration WHERE id = ?"
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (registration_id,))
            return cursor.rowcount > 0

# Example usage
def main():
    # Initialize the registration system
    reg_system = RegistrationSystem()
    
    # Create a new registration
    new_user = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "date_of_birth": "1990-01-01",
        "phone_number": "1234567890",
        "address": "123 Main St"
    }
    
    try:
        # Create
        user_id = reg_system.create_registration(new_user)
        print(f"Created new registration with ID: {user_id}")
        
        # Read
        user = reg_system.read_registration(user_id)
        print(f"Retrieved user: {user}")
        
        # Update
        update_successful = reg_system.update_registration(user_id, {
            "phone_number": "9876543210"
        })
        print(f"Update successful: {update_successful}")
        
        # Delete
        delete_successful = reg_system.delete_registration(user_id)
        print(f"Delete successful: {delete_successful}")
        
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()