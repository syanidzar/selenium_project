import random
from datetime import datetime, timedelta
import csv
import time

# Define file paths
csv_file_location_old = './script.python/files/generated.pengguna.csv'
csv_file_location = './script.python/files/new_generated.pengguna.csv'
malay_names_male_file = './script.python/files/names/malay.male'
malay_names_female_file = './script.python/files/names/malay.female'
chinese_names_male_file = './script.python/files/names/chinese.male'
chinese_names_female_file = './script.python/files/names/chinese.female'
chinese_surnames_file = './script.python/files/names/chinese.surname'
indian_names_male_file = './script.python/files/names/indian.male'
indian_names_female_file = './script.python/files/names/indian.female'
indian_surnames_file = './script.python/files/names/indian.surname'
lists_of_agencies = './script.python/files/options/agencies'
lists_of_positions = './script.python/files/options/positions'
lists_of_grades = './script.python/files/options/grades'
lists_of_schemes = './script.python/files/options/schemes'

def set_read_list(which_lists):
    with open(which_lists, 'r') as file:
        pick_from_list = file.readlines()
        return random.choice(pick_from_list).strip()

def generate_random_dob():
    start_date = datetime.now() - timedelta(days=31*365)
    end_date = datetime.now() - timedelta(days=21*365)
    random_dob = start_date + (end_date - start_date) * random.random()
    return random_dob

def generate_kad_pengenalan():
    dob = generate_random_dob()
    dob_str = dob.strftime('%y%m%d')
    state_num = random.randint(1, 14)
    kad_pengenalan = f"{dob_str}{state_num:02d}{random.randint(0, 9999):04d}"
    return kad_pengenalan

def set_gender():
    return random.choice(['male', 'female'])

def set_ethnicity():
    return random.choice(['malay', 'chineese', 'indian'])

def read_name_from_file(which_file):
    with open(which_file, 'r') as file:
        lines = file.readlines()
        return random.choice(lines).strip()

def generate_name(ethnicity, gender):
    match ethnicity:
        case 'malay':
            if gender == 'male':
                first_name = read_name_from_file(malay_names_male_file)
                onoma = 'bin'
            else:
                first_name = read_name_from_file(malay_names_female_file)
                onoma = 'binti'
            surname = f'{onoma} {read_name_from_file(malay_names_male_file)}'
        case 'chineese':
            if gender == 'male':
                first_name = read_name_from_file(chinese_names_male_file)
            else:
                first_name = read_name_from_file(chinese_names_female_file)
            surname = read_name_from_file(chinese_surnames_file)
        case 'indian':
            if gender == 'male':
                first_name = read_name_from_file(indian_names_male_file)
            else:
                first_name = read_name_from_file(indian_names_female_file)
            surname = read_name_from_file(indian_surnames_file)
    return f'{first_name} {surname}', ethnicity, gender

def set_role():
    roles = ['Pentadbir Agensi', 'Penyelia', 'Super Administrator', 'Staf', 'Ketua Jabatan', 'Setiausaha Tetap', 'Penyelaras Kursus/Pe', 'Ketua Bahagian']
    weights = {
    'Pentadbir Agensi': 2,  # 2 per agency
    'Penyelia': 5,          # 5 per agency
    'Super Administrator': 0, # Super Administrator, with great power comes great responsibility.
    'Staf': 20,             # The rest of the staff
    'Ketua Jabatan': 1,     # 1 per agency
    'Setiausaha Tetap': 1,  # 1 per agency
    'Penyelaras Kursus/Pe': 2, # 2 per agency
    'Ketua Bahagian': 1     # 1 per agency
    }
    
    weighted_roles = []
    for role, count in weights.items():
        weighted_roles.extend([role] * count)

    return random.choice(weighted_roles)

def set_status():
    return 'enabled'

if __name__ == '__main__':
    start_time = time.time()  # Start time

    n_times = 50
    n = 1
    set_of_ic = set()

    with open(csv_file_location, 'w', newline='', encoding='utf-8') as file:
        data_pengguna = csv.writer(file, lineterminator='\n')  #  lineterminator Ensures no extra blank line
        data_pengguna.writerow([
            'No. Kad Pengenalan', 'Kata Laluan', 'Peranan', 'Status', 
            'Nama Penuh', 'Agensi', 'Email', 'Jawatan', 'Skim', 'Gred'
        ])

        for i in range(n_times):
            try:
                get_ethnicity = set_ethnicity()
                get_gender = set_gender()
                get_ic = generate_kad_pengenalan()
                get_role = set_role()
                get_status = set_status()
                get_name = generate_name(get_ethnicity, get_gender)[0]
                get_agency = set_read_list(lists_of_agencies)
                get_email = f'BIP_{get_name.lower().replace(" ", "_")}{n}@dummyemail.test'
                n += 1
                get_position = set_read_list(lists_of_positions)
                get_scheme = set_read_list(lists_of_schemes)
                get_grade = set_read_list(lists_of_grades)

                while get_ic in set_of_ic:
                    print(f'IC found in row {i+1} ... regenerating IC number')
                    get_ic = generate_kad_pengenalan()

                set_of_ic.add(get_ic)

                data_pengguna.writerow([
                    get_ic, '12345', get_role, get_status, 
                    get_name, get_agency, get_email, 
                    get_position, get_scheme, get_grade
                ])

            except Exception as e:
                print(f'Error occurred during iteration {i+1}: {e}')
                continue

    end_time = time.time()  # End time
    execution_time = end_time - start_time
    print(f"Script executed in {execution_time:.2f} seconds")