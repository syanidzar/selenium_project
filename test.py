import random
from datetime import datetime, timedelta
import csv
import time

# Define file paths
csv_file_location = 'files/generated.pengguna.Bahagian_Istiadat_dan_Protokol.csv'
csv_file_lists_of_pengguna = 'files/generated.pengguna.csv'
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
    return random.choice(['malay', 'chinese', 'indian'])

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
        case 'chinese':
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

def set_roles(total_users):
    roles = {
        'Pentadbir Agensi': 1,
        'Penyelia': 1,
        'Ketua Jabatan': 1,
        'Setiausaha Tetap': 1,
        'Penyelaras Kursus/Pe': 1,
        'Ketua Bahagian': 1,
        'Staf': total_users - 6  # Remaining users will be Staf
    }
    assigned_roles = []
    # Assign fixed roles first
    for role, count in roles.items():
        assigned_roles.extend([role] * count)
    return assigned_roles

def set_status():
    return 'enabled'

if __name__ == '__main__':
    start_time = time.time()  # Start time
    total_users = 10  # Total number of users to generate
    n = 1
    set_of_ic = set()
    
    with open(csv_file_location, 'w', newline='', encoding='utf-8') as file_write, \
         open(csv_file_lists_of_pengguna, 'a', newline='', encoding='utf-8') as file_append:  # Open for appending
        data_pengguna_write = csv.writer(file_write, lineterminator='\n')  # Ensures no extra blank line
        data_pengguna_append = csv.writer(file_append, lineterminator='\n')  # Ensures no extra blank line
        
        header = ['No. Kad Pengenalan', 'Kata Laluan', 'Peranan', 'Status',
                  'Nama Penuh', 'Agensi', 'Email', 'Jawatan', 'Skim', 'Gred']
        
        # Write header to the writing file if it's empty or newly created
        if file_write.tell() == 0:
            data_pengguna_write.writerow(header)
        
        # Write header to the appending file if it's empty or newly created
        if file_append.tell() == 0:
            data_pengguna_append.writerow(header)
        
        roles = set_roles(total_users)
        random.shuffle(roles)  # Shuffle roles to assign randomly
        
        for i in range(total_users):
            try:
                get_ethnicity = set_ethnicity()
                get_gender = set_gender()
                get_ic = generate_kad_pengenalan()
                get_role = roles[i]  # Assign role from shuffled list
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
                
                row = [
                    get_ic, '12345', get_role, get_status,
                    get_name, get_agency, get_email,
                    get_position, get_scheme, get_grade
                ]
                
                data_pengguna_write.writerow(row)
                data_pengguna_append.writerow(row)
                
            except Exception as e:
                print(f'Error occurred during iteration {i+1}: {e}')
                continue
    
    end_time = time.time()  # End time
    execution_time = end_time - start_time
    print(f"Script executed in {execution_time:.2f} seconds")
