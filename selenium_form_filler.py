from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
from pynput import keyboard  # Import pynput for keyboard input

# Configuration
USER_INFO_FILE_LOCATION = 'files/generated.pengguna.csv'
GECKODRIVER_PATH = '/snap/bin/geckodriver'
LOGIN_URL = 'http://localhost/mlatih/index.php/login/check_login_web'
FORM_URL = 'http://localhost/mlatih/index.php/admin/register'
USERNAME = 'superadmin@test.com'
PASSWORD = '123456'

# Initialize the WebDriver
def init_driver():
    driver_service = webdriver.FirefoxService(executable_path=GECKODRIVER_PATH)
    return webdriver.Firefox(service=driver_service)

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

# Fill form function
def fill_form(driver, user_data):
    wait = WebDriverWait(driver, 10)

    try:
        # Fill in text fields
        fill_ic = wait.until(EC.presence_of_element_located((By.NAME, 'user_username')))
        fill_password = wait.until(EC.presence_of_element_located((By.NAME, 'user_password')))
        fill_repassword = wait.until(EC.presence_of_element_located((By.NAME, 'user_repassword')))
        fill_nama = wait.until(EC.presence_of_element_located((By.NAME, 'user_profile_name')))
        fill_email = wait.until(EC.presence_of_element_located((By.NAME, 'user_profile_email')))
        fill_jawatan = wait.until(EC.presence_of_element_located((By.NAME, 'user_profile_jawatan')))

        # Fill in dropdown fields
        fill_role = wait.until(EC.presence_of_element_located((By.NAME, 'user_cizacl_role_id')))
        select_role = Select(fill_role)
        select_role.select_by_visible_text(f'{user_data[2]}')

        # Fill in remaining fields
        fill_ic.send_keys(user_data[0])
        fill_password.send_keys(user_data[1])
        fill_repassword.send_keys(user_data[1])
        fill_nama.send_keys(user_data[4])
        fill_email.send_keys(user_data[6])
        fill_jawatan.send_keys(user_data[7])


        # Submit or reset the form
        # reset_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-light')))
        # reset_button.click()

        print(f"Form filled for: \n{user_data[4]}\n{user_data[5]}\n{user_data[8]}\n{user_data[9]}\n")
    except Exception as e:
        print(f"Error filling form for {user_data[4]}: {e}")

# Function to wait for key combination
def wait_for_f1_key():
    print("Press 'F1' to fill the next form...")
    
    # Function to detect F1 key press
    def on_press(key):
        try:
            if key == keyboard.Key.f1:  # Check if the pressed key is F1
                print("F1 key pressed!")  # Confirm key press
                return False  # Stop listener
        except AttributeError:
            pass

    # Collect events until F1 is pressed
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

    print("F1 key detected, proceeding...")

# Main execution flow
def main():
    driver = init_driver()
    login(driver)

    with open(USER_INFO_FILE_LOCATION, 'r') as file:
        rows = csv.reader(file)
        next(rows)  # Skip header

        driver.get(FORM_URL)

        for user_data in rows:
            try:
                print(f"Waiting for key combination for user: {user_data[4]}")
                wait_for_f1_key()  # Wait for the specific key combination
                
                print("Filling the form...")
                fill_form(driver, user_data)
                time.sleep(0.5)  # Optional delay for demonstration
            except Exception as e:
                print(f'An error occurred while filling the form for {user_data[4]}: {e}')

    driver.quit()

if __name__ == "__main__":
    main()
