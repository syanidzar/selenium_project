from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
from pynput import keyboard

# Configuration
SUBMIT_FUNCTION = 'SUBMIT'  # submit or else reset

USER_INFO_FILE_LOCATION = 'files\generated.pengguna.csv'
EDGE_DRIVER_PATH = '.browser_driver\msedgedriver.exe'
LOGIN_URL = 'http://localhost/mlatih/index.php/login/check_login_web'
FORM_URL = 'http://localhost/mlatih/index.php/admin/register'
USERNAME = 'superadmin@test.com'
PASSWORD = '123456'

# Initialize the WebDriver
def init_driver():
    driver_service = webdriver.EdgeService(executable_path=EDGE_DRIVER_PATH)
    return webdriver.Edge(service=driver_service)

# Login function
def login(driver):
    driver.get(LOGIN_URL)
    wait = WebDriverWait(driver, 10)

    username_input = wait.until(EC.presence_of_element_located((By.NAME, 'username')))
    password_input = wait.until(EC.presence_of_element_located((By.NAME, 'password')))
    
    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)
    
    login_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-primary')))
    login_button.click()
    
    print('Login Successful')

# Fill in dropdown fields - The Problematic select2
def select2_form_filler(wait_t, driver_t, user_data_obj, field_name, obj_object):
    try:
        # Find and click on the Select2 dropdown container
        dropdown_container = wait_t.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"select[name='{field_name}'] + .select2-container")))
        dropdown_container.click()

        # Type into the search box within Select2 dropdown
        search_box = wait_t.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".select2-search__field")))
        search_box.clear()
        search_box.send_keys(user_data_obj)

        # Wait for and select the matching option from the dropdown
        options = wait_t.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".select2-results__option")))

        # Loop through options to find a match and click
        for option in options:
            print(f"Available option: {option.text}")  # Debug to list available options
            if user_data_obj.strip().lower() == option.text.strip().lower():  # Match exact text
                option.click()
                print(f"Selected {obj_object}: {user_data_obj}")
                return

        # If no match is found, report an error
        print(f'Error: No matching option found for {obj_object}: "{user_data_obj}"')

    except Exception as e:
        print(f'Error selecting {obj_object}: "{user_data_obj}" - {e}')


# Fill form function
def fill_form(driver, user_data):
    wait = WebDriverWait(driver, 10)

    try:
        # Look and wait for  fields
        fill_ic = wait.until(EC.presence_of_element_located((By.NAME, 'user_username')))
        fill_password = wait.until(EC.presence_of_element_located((By.NAME, 'user_password')))
        fill_repassword = wait.until(EC.presence_of_element_located((By.NAME, 'user_repassword')))
        fill_nama = wait.until(EC.presence_of_element_located((By.NAME, 'user_profile_name')))
        fill_email = wait.until(EC.presence_of_element_located((By.NAME, 'user_profile_email')))
        fill_jawatan = wait.until(EC.presence_of_element_located((By.NAME, 'user_profile_jawatan')))
        fill_role = wait.until(EC.presence_of_element_located((By.NAME, 'user_cizacl_role_id')))
        # Fill in fields
        fill_ic.send_keys(user_data[0])
        fill_password.send_keys(user_data[1])
        fill_repassword.send_keys(user_data[1])
        fill_role.send_keys(user_data[2])  #
        fill_nama.send_keys(user_data[4])
        fill_email.send_keys(user_data[6])
        fill_jawatan.send_keys(user_data[7])

        # select2_form_filler(wait, driver, user_data[2], 'user_cizacl_role_id', 'Role')
        select2_form_filler(wait, driver, user_data[5], 'user_profile_agency', 'Agency')
        select2_form_filler(wait, driver, user_data[8], 'user_profile_scheme', 'Scheme')
        select2_form_filler(wait, driver, user_data[9], 'user_profile_grade', 'Grade')

        print(f"Form filled for: \n{user_data[4]}\n{user_data[5]}\n{user_data[8]}\n{user_data[9]}\n")
    except Exception as e:
        print(f"Error filling form for {user_data[4]}: {e}")

# Function to wait for key combination
def wait_for_f1_key():
    print("Press 'F2' to fill the next form...")
    
    # Function to detect F1 key press
    def on_press(key):
        try:
            if key == keyboard.Key.f2:  # Check if the pressed key is F1
                print("F1 key pressed!")  # Confirm key press
                return False  # Stop listener
        except AttributeError:
            pass

    # Collect events until F1 is pressed
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

    print("F1 key detected, proceeding...")

def submit_form(driver, option):
    print('Action = submit_form()')
    time.sleep(0.5)  # Optional delay for demonstration

    # Submit the form
    if option == 'SUBMIT':
        wait = WebDriverWait(driver, 10)
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn bg-blue') and contains(text(), 'Daftar')]")))
        submit_button.click()

    # reset the form for testing purposes
    else:
        wait = WebDriverWait(driver, 10)
        reset_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn bg-light') and contains(text(), 'Reset')]")))
        reset_button.click()

    time.sleep(0.5)  # Optional delay for demonstration

# Main execution flow
def main():
    driver = init_driver()
    login(driver)

    with open(USER_INFO_FILE_LOCATION, 'r') as file:
        rows = csv.reader(file)
        next(rows)  # Skip header

        for user_data in rows:
            try:
                driver.get(FORM_URL)

                print(f"Waiting for key combination for user: {user_data[4]}")
                wait_for_f1_key()  # Wait for the specific key combination
                
                print("Filling the form...")
                fill_form(driver, user_data)

                submit_form(driver, SUBMIT_FUNCTION.upper())

            except Exception as e:
                print(f'An error occurred while filling the form for {user_data[4]}: {e}')

    driver.quit()

if __name__ == "__main__":
    main()
