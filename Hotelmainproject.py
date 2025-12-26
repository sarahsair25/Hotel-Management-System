import json
import os
import hashlib


class User:
    def __init__(self, id, name, email, contact, city, password_hash):
        self.id = id
        self.name = name
        self.email = email
        self.contact = contact
        self.city = city
        self.password_hash = password_hash

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "contact": self.contact,
            "city": self.city,
            "password_hash": self.password_hash
        }


class Hotel:
    FILE_NAME = "users.json"
    userlist = []
    count = 1

    def __init__(self):
        self.load_users()

    # 🔐 Password hashing
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def load_users(self):
        if not os.path.exists(self.FILE_NAME):
            return

        with open(self.FILE_NAME, "r") as file:
            data = json.load(file)
            for item in data:
                user = User(
                    item["id"],
                    item["name"],
                    item["email"],
                    item["contact"],
                    item["city"],
                    item["password_hash"]
                )
                Hotel.userlist.append(user)

        if Hotel.userlist:
            Hotel.count = Hotel.userlist[-1].id + 1

    def save_users(self):
        with open(self.FILE_NAME, "w") as file:
            json.dump([u.to_dict() for u in Hotel.userlist], file, indent=4)

    def register(self):
        print("\n----- Registration -----")
        name = input("Enter Name: ")
        email = input("Enter Email: ")
        contact = input("Enter Contact: ")
        city = input("Enter City: ")
        password = input("Enter Password: ")

        password_hash = self.hash_password(password)

        user = User(
            Hotel.count,
            name,
            email,
            contact,
            city,
            password_hash
        )

        Hotel.userlist.append(user)
        Hotel.count += 1
        self.save_users()

        print("\n✅ User registered securely and saved to JSON.")

    def login(self):
        print("\n----- Login -----")
        email = input("Enter Email: ")
        password = input("Enter Password: ")

        password_hash = self.hash_password(password)

        for user in Hotel.userlist:
            if user.email == email and user.password_hash == password_hash:
                print(f"\n✅ Login successful. Welcome, {user.name}!")
                return

        print("\n❌ Invalid email or password.")

    def display_users(self):
        if not Hotel.userlist:
            print("\nNo users found.")
            return

        print("\nID\tName\tEmail\tContact\tCity")
        for user in Hotel.userlist:
            print(f"{user.id}\t{user.name}\t{user.email}\t{user.contact}\t{user.city}")

    def call(self):
        while True:
            print("\n--- Hotel Management System ---")
            print("1. Register User")
            print("2. Login User")
            print("3. View All Users")
            print("4. Exit")

            choice = input("Enter your choice: ")

            if not choice.isdigit():
                print("Please enter a valid number.")
                continue

            choice = int(choice)

            if choice == 1:
                self.register()
            elif choice == 2:
                self.login()
            elif choice == 3:
                self.display_users()
            elif choice == 4:
                print("Exiting program...")
                break
            else:
                print("Invalid choice.")


h = Hotel()
h.call()
