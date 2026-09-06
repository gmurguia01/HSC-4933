######################################
# Gabriel Murguia # gmurguia@usf.edu #
# Lab 2: Uses functions with heart   #
# rate samples                       #
######################################

heart_rate_samples = {
"J. Alvarez": [72, 75, 78],
"M. Chen": [80, 82],
"R. Okafor": [65, 68, 70, 66],
"S. Patel": [90, 95, 92, 88, 91],
"T. Nguyen": [77, 79],
"L. Kowalski": [68, 70, 69],
"D. Osei": [98, 101, 95, 99],
"A. Whitfield": [74, 76, 75, 73],
}

def patient_stats(heart_rates):
    average = sum(heart_rates) / len(heart_rates)
    minimum = min(heart_rates)
    maximum = max(heart_rates)
    count = len(heart_rates)
    return average, minimum, maximum, count,

def display_stats(average, minimum, maximum, count, choice):

    if choice == "all":
        print("Average", average)
        print("Minimum", minimum)
        print("Maximum", maximum)
        print("samples", count)

    elif choice == "average":
        print("Average", average)

    elif choice == "minimum":
        print("Minimum", minimum)

    elif choice == "maximum":
        print("Maximum", maximum)

    elif choice == "count":
        print("Count", count)

    else:
        print("Invalid choice")

print("Heart Rate Search")
patients = list(heart_rate_samples.keys())

for i, patient in enumerate(patients, start=1):
    print (i, patient)

patient_number = int(input("Enter patient number: "))
patient_name = patients[patient_number - 1]

print("\nPatient:", patient_name)

heart_rates = heart_rate_samples[patient_name]
print("heart rate samples:", heart_rates)

average, minimum, maximum, count = patient_stats(heart_rates)

print("\nSelect number to retrieve information:")
print("1. All Statistics")
print("2. Average")
print("3. Minimum")
print("4. Maximum")
print("5. Samples")

choice = input("\nEnter your choice: ")

if choice == "1":
    display_stats(average, minimum, maximum, count, "all")
elif choice == "2":
    display_stats(average, minimum, maximum, count, "average")
elif choice == "3":
    display_stats(average, minimum, maximum, count, "minimum")
elif choice == "4":
    display_stats(average, minimum, maximum, count, "maximum")
elif choice == "5":
    display_stats(average, minimum, maximum, count, "count")

else:
    print("Invalid choice")

