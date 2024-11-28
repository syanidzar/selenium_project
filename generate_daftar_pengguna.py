import csv
import random
import time
from datetime import datetime, timedelta
from pathlib import Path

# Define file paths for required files
csv_file_lists_of_pengguna = 'files/generated.pengguna.temp.csv'
csv_file_lists_of_pengguna_append = 'files/generated.pengguna.csv'
malay_names_male_file = 'files/names/malay.male'
malay_names_female_file = 'files/names/malay.female'
chinese_names_male_file = 'files/names/chinese.male'
chinese_names_female_file = 'files/names/chinese.female'
chinese_surnames_file = 'files/names/chinese.surname'
indian_names_male_file = 'files/names/indian.male'
indian_names_female_file = 'files/names/indian.female'
indian_surnames_file = 'files/names/indian.surname'
lists_of_agencies = 'files/options/agencies'
lists_of_positions = 'files/options/positions'
lists_of_grades = 'files/options/grades'
lists_of_schemes = 'files/options/schemes'

# Function to read a random entry from a file
def set_read_list(which_lists):
    with open(which_lists, 'r') as file:
        return random.choice(file.readlines()).strip()

# Function to generate a random date of birth between 21 and 31 years ago
def generate_random_dob():
    start_date = datetime.now() - timedelta(days=31*365)
    end_date = datetime.now() - timedelta(days=21*365)
    random_dob = start_date + (end_date - start_date) * random.random()
    return random_dob

# Function to generate a unique Malaysian Identity Card number (Kad Pengenalan)
def generate_kad_pengenalan():
    dob = generate_random_dob()
    dob_str = dob.strftime('%y%m%d')
    state_num = random.randint(1, 14)
    kad_pengenalan = f"{dob_str}{state_num:02d}{random.randint(0, 9999):04d}"
    return kad_pengenalan

# Function to randomly choose gender (male or female)
def set_gender():
    return random.choice(['male', 'female'])

# Function to randomly choose an ethnicity based on weight distribution
def set_ethnicity():
    ethnicities = ['malay', 'chinese', 'indian']
    weights = [0.5, 0.3, 0.2]
    return random.choices(ethnicities, weights)[0]

# Function to read a random name from a file and return it
def read_name_from_file(which_file):
    try:
        with open(which_file, 'r') as file:
            names = file.readlines()
            return random.choice(names).strip()
    except FileNotFoundError:
        print(f"File not found: {which_file}")
        return ""
    except Exception as e:
        print(f"Error reading file {which_file}: {e}")
        return ""

# Function to generate a full name based on ethnicity and gender
def generate_name(ethnicity, gender):
    match ethnicity:
        case 'malay':
            if gender == 'male':
                first_name = read_name_from_file(malay_names_male_file)
            else:
                first_name = read_name_from_file(malay_names_female_file)
            surname = f'{first_name} bin {read_name_from_file(malay_names_male_file)}' if gender == 'male' else f'{first_name} binti {read_name_from_file(malay_names_male_file)}'
        case 'chinese':
            if gender == 'male':
                first_name = read_name_from_file(chinese_names_male_file)
            else:
                first_name = read_name_from_file(chinese_names_female_file)
            surname = f'{read_name_from_file(chinese_surnames_file)} {first_name}'
        case 'indian':
            if gender == 'male':
                first_name = read_name_from_file(indian_names_male_file)
            else:
                first_name = read_name_from_file(indian_names_female_file)
            surname = f'{read_name_from_file(indian_surnames_file)} {first_name}'
    return surname

# Function to set roles for the users based on a given total number of users
def set_roles(total_users):
    roles = {
        'Pentadbir System': 1,
        'Penyelia': 1,
        'Ketua Jabatan': 1,
        'Setiausaha Tetap': 1,
        'Penyelaras Kursus/Pe': 1,
        'Ketua Bahagian': 1,
        'Staf': total_users - 6
    }
    assigned_roles = []
    for role, count in roles.items():
        assigned_roles.extend([role] * count)
    return assigned_roles

# Function to set the user status to 'enabled'
def set_status():
    return 'enabled'

# Function to ensure that the file and necessary directories exist, and create them if not
def check_and_create_file(file_path):
    path = Path(file_path)
    if not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.touch()

# Function to read and return a set of existing IC numbers from the CSV file
def list_of_ic():
    ic_set = set()
    if Path(csv_file_lists_of_pengguna_append).is_file():
        with open(csv_file_lists_of_pengguna_append, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                ic_set.add(row[0])
    return ic_set

# Main function that generates the user data and writes it to the CSV file
def main():
    n = 1  # Initialize a counter for the email suffix
    
    # Check if the append file already exists and has content
    append_file_exists = Path(csv_file_lists_of_pengguna_append).is_file() and Path(csv_file_lists_of_pengguna_append).stat().st_size > 0
    
    # Open the CSV files for writing and appending user data
    with open(csv_file_lists_of_pengguna, 'w', newline='', encoding='utf-8') as file_write, \
         open(csv_file_lists_of_pengguna_append, 'a', newline='', encoding='utf-8') as file_append:
        
        data_pengguna_write = csv.writer(file_write, lineterminator='\n')  # Prepare to write to CSV
        data_pengguna_append = csv.writer(file_append, lineterminator='\n')  # Prepare to append to CSV
        
        header = ['No. Kad Pengenalan', 'Kata Laluan', 'Peranan', 'Status',  # Define the CSV header
                  'Nama Penuh', 'Agensi', 'Email', 'Jawatan', 'Skim', 'Gred']
        
        # Write header to the main file
        data_pengguna_write.writerow(header)
        
        # Write header to the append file if it's empty or newly created
        if not append_file_exists:
            data_pengguna_append.writerow(header)
        
        roles = set_roles(total_users)  # Generate a list of roles for the users
        random.shuffle(roles)  # Shuffle the roles to assign them randomly
        
        set_of_ic = set(list_of_ic())  # Read existing IC numbers to avoid duplicates
        for i in range(total_users):
            try:
                # Generate random user attributes
                get_ethnicity = set_ethnicity()
                get_gender = set_gender()
                get_ic = generate_kad_pengenalan()
                get_role = roles[i]  # Get the role from the shuffled list
                get_status = set_status()  # Set the user status
                get_name = generate_name(get_ethnicity, get_gender)  # Generate full name
                get_email = f'{get_name.lower().replace(" ", "_")}{n}@dummyemail.test'  # Generate email address
                n += 1
                get_position = set_read_list(lists_of_positions)  # Get a random job position
                get_scheme = set_read_list(lists_of_schemes)  # Get a random scheme
                get_grade = set_read_list(lists_of_grades)  # Get a random grade
                
                # Check if IC number already exists and regenerate if necessary
                while get_ic in set_of_ic:
                    print(f'IC found in row {i+1} ... regenerating IC number')
                    get_ic = generate_kad_pengenalan()
                set_of_ic.add(get_ic)  # Add IC number to the set of used ICs
                
                # Prepare the row for CSV file
                row = [
                    get_ic, '123456', get_role, get_status,
                    get_name, chosen_agency, get_email,
                    get_position, get_scheme, get_grade
                ]
                
                data_pengguna_write.writerow(row)  # Write the row to the main CSV
                data_pengguna_append.writerow(row)  # Append the row to the append CSV
                
            except Exception as e:
                print(f'Error occurred during iteration {i+1}: {e}')  # Handle errors during user generation
                continue

# Entry point for the script
if __name__ == '__main__':
    start_time = time.time()  # Start time for performance tracking
    total_users = int(input('How many users to generate: '))  # Ask user for the total number of users to generate
    
    # Ask user to choose an agency
    with open(lists_of_agencies, 'r') as file:
        agencies = file.readlines()
        for idx, agency in enumerate(agencies, start=1):
            print(f"{idx}. {agency.strip()}")
        agency_choice = int(input('Choose an agency by number: '))
        chosen_agency = agencies[agency_choice - 1].strip()
    
    main()  # Call the main function to start the user generation process    
    end_time = time.time()  # End time for performance tracking
    execution_time = end_time - start_time  # Calculate execution time
    print(f"Script executed in {execution_time:.2f} seconds")  # Print execution time
