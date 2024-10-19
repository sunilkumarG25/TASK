from registration_system import RegistrationSystem

# Create instance of registration system
reg_system = RegistrationSystem()

# Test 1: Create a new user
print("Test 1: Creating a new user")
new_user = {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "date_of_birth": "1990-01-01",
    "phone_number": "1234567890",
    "address": "123 Main St"
}

try:
    # Create user
    user_id = reg_system.create_registration(new_user)
    print(f"Created user with ID: {user_id}")

    # Read user
    user = reg_system.read_registration(user_id)
    print(f"User details: {user}")

    # Update user
    print("\nTest 2: Updating user")
    update_data = {
        "phone_number": "9876543210",
        "address": "456 New St"
    }
    success = reg_system.update_registration(user_id, update_data)
    print(f"Update successful: {success}")

    # Read updated user
    updated_user = reg_system.read_registration(user_id)
    print(f"Updated user details: {updated_user}")

    # Show all users
    print("\nTest 3: Showing all users")
    all_users = reg_system.read_all_registrations()
    for user in all_users:
        print(f"User: {user}")

    # Delete user
    print("\nTest 4: Deleting user")
    delete_success = reg_system.delete_registration(user_id)
    print(f"Delete successful: {delete_success}")

except ValueError as e:
    print(f"Error occurred: {e}")



