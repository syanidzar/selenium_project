# Importing necessary libraries
import random  # For generating random data
from datetime import datetime, timedelta  # For generating random dates
from pathlib import Path  # For managing file paths and directories
import csv  # For working with CSV files
import time  # For measuring execution time

# Define file paths for required files
csv_file_lists_of_pengguna = 'files/generated.pengguna.temp.csv'  # The path to the CSV file for storing user data
csv_file_lists_of_pengguna_append = 'files/generated.pengguna.csv'  # Appending user data in this file
malay_names_male_file = 'files/names/malay.male'  # Path to file containing male Malay first names
malay_names_female_file = 'files/names/malay.female'  # Path to file containing female Malay first names
chinese_names_male_file = 'files/names/chinese.male'  # Path to file containing male Chinese first names
chinese_names_female_file = 'files/names/chinese.female'  # Path to file containing female Chinese first names
chinese_surnames_file = 'files/names/chinese.surname'  # Path to file containing Chinese surnames
indian_names_male_file = 'files/names/indian.male'  # Path to file containing male Indian first names
indian_names_female_file = 'files/names/indian.female'  # Path to file containing female Indian first names
indian_surnames_file = 'files/names/indian.surname'  # Path to file containing Indian surnames
lists_of_agencies = 'files/options/agencies'  # Path to file containing list of agencies
lists_of_positions = 'files/options/positions'  # Path to file containing list of job positions
lists_of_grades = 'files/options/grades'  # Path to file containing list of grades
lists_of_schemes = 'files/options/schemes'  # Path to file containing list of schemes

# Function to read a random entry from a file
def set_read_list(which_lists):
    with open(which_lists, 'r') as file:
        pick_from_list = file.readlines()  # Read all lines from the file
        return random.choice(pick_from_list).strip()  # Randomly choose one line and strip any extra spaces

# Function to generate a random date of birth between 21 and 31 years ago
def generate_random_dob():
    start_date = datetime.now() - timedelta(days=31*365)  # 31 years ago
    end_date = datetime.now() - timedelta(days=21*365)  # 21 years ago
    random_dob = start_date + (end_date - start_date) * random.random()  # Generate a random date in the range
    return random_dob

# Function to generate a unique Malaysian Identity Card number (Kad Pengenalan)
def generate_kad_pengenalan():
    dob = generate_random_dob()  # Generate random DOB
    dob_str = dob.strftime('%y%m%d')  # Format the date of birth as YYMMDD
    state_num = random.randint(1, 14)  # Random state number between 01 and 14
    kad_pengenalan = f"{dob_str}{state_num:02d}{random.randint(0, 9999):04d}"  # Combine to create IC number
    return kad_pengenalan

# Function to randomly choose gender (male or female)
def set_gender():
    return random.choice(['male', 'female'])  # Randomly return 'male' or 'female'

# Function to randomly choose an ethnicity based on weight distribution
def set_ethnicity():
    ethnicities = ['malay', 'chinese', 'indian']  # List of possible ethnicities
    weights = [0.5, 0.3, 0.2]  # The weight distribution (more likely to choose 'malay')
    return random.choices(ethnicities, weights)[0]  # Randomly pick an ethnicity based on weights

# Function to read a random name from a file and return it
def read_name_from_file(which_file):
    try:
        with open(which_file, 'r') as file:
            lines = file.readlines()  # Read all lines in the file
            if not lines:  # If the file is empty, raise an exception
                raise ValueError(f'The file {which_file} is empty')
            return random.choice(lines).strip()  # Randomly pick one name and strip extra spaces
    except FileNotFoundError:  # Handle file not found error
        raise FileNotFoundError(f'The file {which_file} was not found')
    except Exception as e:  # Catch any other exceptions
        raise Exception(f'Error reading {which_file}: {e}')

# Function to generate a full name based on ethnicity and gender
def generate_name(ethnicity, gender):
    match ethnicity:
        case 'malay':  # Malay names (bin/binti)
            if gender == 'male':
                first_name = read_name_from_file(malay_names_male_file)
                onoma = 'bin'
            else:
                first_name = read_name_from_file(malay_names_female_file)
                onoma = 'binti'
            surname = f'{onoma} {read_name_from_file(malay_names_male_file)}'  # Male surname for both genders
        case 'chinese':  # Chinese names (no bin/binti)
            if gender == 'male':
                first_name = read_name_from_file(chinese_names_male_file)
            else:
                first_name = read_name_from_file(chinese_names_female_file)
            surname = read_name_from_file(chinese_surnames_file)  # Chinese surname
        case 'indian':  # Indian names (no bin/binti)
            if gender == 'male':
                first_name = read_name_from_file(indian_names_male_file)
            else:
                first_name = read_name_from_file(indian_names_female_file)
            surname = read_name_from_file(indian_surnames_file)  # Indian surname
    return f'{first_name} {surname}', ethnicity, gender  # Return full name, ethnicity, and gender

# Function to set roles for the users based on a given total number of users
def set_roles(total_users):
    roles = {
        'Pentadbir System': 1,
        'Penyelia': 1,
        'Ketua Jabatan': 1,
        'Setiausaha Tetap': 1,
        'Penyelaras Kursus/Pe': 1,
        'Ketua Bahagian': 1,
        'Staf': total_users - 6  # Remaining users will be assigned 'Staf' role
    }
    assigned_roles = []
    # Assign fixed roles first
    for role, count in roles.items():
        assigned_roles.extend([role] * count)  # Add the role to the list the specified number of times
    return assigned_roles  # Return the list of assigned roles

# Function to set the user status to 'enabled'
def set_status():
    return 'enabled'  # All users are set to 'enabled'

# Function to ensure that the file and necessary directories exist, and create them if not
def check_and_create_file(file_path):
    directory = Path(file_path).parent  # Get the parent directory of the file path
    directory.mkdir(parents=True, exist_ok=True)  # Create the directory if it doesn't exist
    file_path_check = Path(file_path)  # Create a Path object for the file
    file_path_check.touch(exist_ok=True)  # Create the file if it doesn't exist
    return file_path_check  # Return the Path object

# Function to read and return a set of existing IC numbers from the CSV file
def list_of_ic():
    file_path_check = check_and_create_file(csv_file_lists_of_pengguna)  # Ensure the file exists
    list_of_ic = set()  # Create an empty set to store IC numbers
    if file_path_check.is_file():  # Check if the file exists
        with open(csv_file_lists_of_pengguna, 'r') as file:
            csv_row = csv.reader(file)  # Read the CSV file
            next(csv_row, None)  # Skip the header row if it exists
            for col in csv_row:  # Iterate through the rows
                list_of_ic.add(col[0])  # Add the IC number (first column) to the set
    return list_of_ic  # Return the set of IC numbers

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
                get_name = generate_name(get_ethnicity, get_gender)[0]  # Generate full name
                get_agency = set_read_list(lists_of_agencies)  # Get a random agency
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
                    get_name, get_agency, get_email,
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
    main()  # Call the main function to start the user generation process    
    end_time = time.time()  # End time for performance tracking
    execution_time = end_time - start_time  # Calculate execution time
    print(f"Script executed in {execution_time:.2f} seconds")  # Print execution time
