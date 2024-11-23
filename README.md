# User Data Generator and Form Filler

## Overview

This project consists of two main components:
1. **User Data Generator**: A script to generate randomized user data and store it in a CSV file.
2. **Form Filler**: A script to automate the process of filling out a web form using the generated user data.

## User Data Generator

### Description

The user data generator script (`generate_daftar_pengguna.py`) creates a list of users with randomized information including IC number, name, gender, ethnicity, and other relevant details. The generated data is saved to a CSV file.

### Usage

1. Place the necessary name and options files in the `files` directory.
2. Run the script:
    ```sh
    python generate_daftar_pengguna.py
    ```

### Configuration

- The script reads from several files to generate names and other attributes:
    - `files/names/malay.male`
    - `files/names/malay.female`
    - `files/names/chinese.male`
    - `files/names/chinese.female`
    - `files/names/chinese.surname`
    - `files/names/indian.male`
    - `files/names/indian.female`
    - `files/names/indian.surname`
    - `files/options/agencies`
    - `files/options/positions`
    - `files/options/grades`
    - `files/options/schemes`

## Form Filler

### Description

The form filler script (`form_filler.py`) uses Selenium WebDriver to log into a web application and fill out a registration form with the generated user data.

### Prerequisites

- Ensure you have the Edge WebDriver (`msedgedriver.exe`) that matches your Edge browser version.
- Install the required Python packages:
    ```sh
    pip install selenium pynput
    ```

### Usage

1. Update the following constants in the script as needed:
    - `USER_INFO_FILE_LOCATION`: Path to the generated user data CSV file.
    - `EDGE_DRIVER_PATH`: Path to the Edge WebDriver.
    - `LOGIN_URL`: URL of the login page.
    - `FORM_URL`: URL of the registration form page.
    - `USERNAME`: Login username.
    - `PASSWORD`: Login password.

2. Run the script:
    ```sh
    python form_filler.py
    ```

### Instructions

- The script will open the web application, log in, navigate to the registration form, and wait for user input (press 'F2') to fill and submit each form.
- It will read user data from the CSV file and fill out the form fields accordingly.

## Running Unit Tests

Unit tests for the user data generator are provided in `test_generate_daftar_pengguna.py`.

### Running the Tests

1. Ensure the `unittest` framework is installed.
2. Run the tests:
    ```sh
    python -m unittest test_generate_daftar_pengguna.py
    ```

## Contributions

Contributions are welcome! Please open an issue or submit a pull request.
