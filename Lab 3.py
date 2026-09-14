####################################
#Gabriel Murguia / gmurguia@usf.edu#
#Using encryption code for patient #
#data base                         #
####################################

from datetime import date
from os import name

from anonymate.anonymizer import Anonymizer

profiles = [
    {
        "name": "Oscar Newman",
        "birthdate": date(1927, 1, 19),
        "sex": "Male",
        "blood_group": "B+"
    },
    {
        "name": "Jermey Wilson",
        "birthdate": date(1996, 10, 12),
        "sex": "Male",
        "blood_group": "A-"
    },
    {
        "name": "Kenneth Rhodes",
        "birthdate": date(2003, 6, 15),
        "sex": "Male",
        "blood_group": "A-"
    },
    {
        "name": "Nicole Richardson",
        "birthdate": date(2003, 9, 7),
        "sex": "Female",
        "blood_group": "AB+"
    },
    {
        "name": "Gary Gambler",
        "birthdate": date(1968, 8, 19),
        "sex": "Male",
        "blood_group": "A+"
    }
]
anonymizer = Anonymizer()

encrypt = input("Should The Data Be Anonymized? (Y/N): ")
encrypted_profiles = []
if encrypt.lower() == "Y":
    for profile in profiles:
        encrypted_profile = {}
        encrypted_profile["name"] = anonymizer.encrypt_text(profile["name"])
        encrypted_profile["birthdate"] = anonymizer.encrypt_text(str(profile["birthdate"]))
        encrypted_profile["sex"] = anonymizer.encrypt_text(profile["sex"])
        encyrpted_profile["blood_group"] = anonymizer.encrypt_text(profile["blood_group"])

        encrypted_profiles.append(encrypted_profile)
if encrypt.lower() == "Y":
    data = encrypted_profiles
else:
    data = profiles

print("\n Search by:")
print("1. Name")
print("2. Birthdate")
print("3. Sex")
print("4. Blood Group")

choice = input("Enter your choice: ")
if choice == "1":
    field = "name"
    search = input("Enter Name: ")
elif choice == "2":
    field = "birthdate"
    search = input("Enter Birthdate (YYYY-MM-DD): ")
elif choice == "3":
    field = "sex"
    search = input("Enter Sex (Male/Female): ")
elif choice == "4":
    field = "blood_group"
    search = input("Enter Blood Type: ")
else:
    print("Invalid Choice")
    exit()

found = False

for i in range(len(data)):
    profile = data[i]
    if encrypt.lower() == "Y":
        value = anonymizer.decrypt_text(profile[field])
    else:
        value = str(profile[field])
    if value.lower() == search.lower():
        original = profiles[i]

        print("\nProfile Found")
        print("Name:", original["name"])
        print("Birthdate:", original["birthdate"])
        print("Sex:", original["sex"])
        print("Blood Group:", original["blood_group"])
        found = True
if found == False:
    print("Invalid Choice")
    exit()




