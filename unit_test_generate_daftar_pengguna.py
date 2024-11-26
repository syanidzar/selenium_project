import unittest
from unittest.mock import patch, mock_open, MagicMock
from datetime import datetime, timedelta
import random
import generate_daftar_pengguna

class TestUserGenerator(unittest.TestCase):
    
    # Test for the generate_random_dob function
    @patch('generate_daftar_pengguna.datetime')
    def test_generate_random_dob(self, mock_datetime):
        # Mock the datetime to control the "current" date (January 1, 2024)
        mock_datetime.now.return_value = datetime(2024, 1, 1)
        
        # Call the function to generate a random date of birth
        dob = generate_daftar_pengguna.generate_random_dob()
        
        # Check if the generated DOB is within the expected range (1993 to 2003)
        self.assertTrue(datetime(1993, 1, 1) <= dob <= datetime(2003, 1, 1))
    
    # Test for the generate_kad_pengenalan function (Identity Card generation)
    @patch('generate_daftar_pengguna.generate_random_dob', return_value=datetime(1990, 5, 15))  # Mock the DOB to be May 15, 1990
    @patch('random.randint', side_effect=[10, 1234])  # Mock the randint function to return specific values
    def test_generate_kad_pengenalan(self, mock_randint, mock_dob):
        # Call the function to generate the Identity Card number
        ic = generate_daftar_pengguna.generate_kad_pengenalan()
        
        # Check if the generated IC is in the expected format: "900515101234"
        self.assertEqual(ic, "900515101234")
    
    # Test for the set_gender function, ensuring it returns either 'male' or 'female'
    def test_set_gender(self):
        # Generate 100 random gender values and check that both 'male' and 'female' are possible
        genders = set(generate_daftar_pengguna.set_gender() for _ in range(100))
        self.assertEqual(genders, {"male", "female"})
    
    # Test for the set_ethnicity function, mocking the random choices to return a specific ethnicity
    @patch('random.choices', return_value=['malay'])  # Mock to always return 'malay'
    def test_set_ethnicity(self, mock_choices):
        # Call the function to generate ethnicity
        ethnicity = generate_daftar_pengguna.set_ethnicity()
        
        # Check if the ethnicity returned is 'malay'
        self.assertEqual(ethnicity, "malay")
    
    # Test for the read_name_from_file function, mocking the file read
    @patch('builtins.open', new_callable=mock_open, read_data='Name1\nName2\nName3')  # Mock file contents
    def test_read_name_from_file(self, mock_file):
        # Call the function to read a name from the file
        name = generate_daftar_pengguna.read_name_from_file('dummy_file')
        
        # Check if the name is one of the names present in the mocked file
        self.assertIn(name, ['Name1', 'Name2', 'Name3'])
    
    # Test for the generate_name function, mocking the name reading and ethnicity/gender
    @patch('generate_daftar_pengguna.read_name_from_file', side_effect=['Ali', 'Hassan'])  # Mock name reading
    def test_generate_name_malay_male(self, mock_read_name):
        # Call the function to generate a name, ethnicity, and gender
        name, ethnicity, gender = generate_daftar_pengguna.generate_name('malay', 'male')
        
        # Check that the generated name is in the expected format ('Ali bin Hassan')
        self.assertEqual(name, 'Ali bin Hassan')
        # Ensure the ethnicity and gender are correctly returned
        self.assertEqual(ethnicity, 'malay')
        self.assertEqual(gender, 'male')

    # Test for the set_roles function, ensuring roles are shuffled and correctly assigned
    @patch('random.shuffle')  # Mock shuffle to avoid random behavior
    def test_set_roles(self, mock_shuffle):
        # Call the function to generate a list of 10 roles
        roles = generate_daftar_pengguna.set_roles(10)
        
        # Ensure the list of roles contains 10 roles
        self.assertEqual(len(roles), 10)
        # Check that 'Pentadbir System' and 'Staf' are present in the roles
        self.assertIn('Pentadbir System', roles)
        self.assertIn('Staf', roles)

    # Test for the check_and_create_file function, ensuring the file is created correctly
    @patch('generate_daftar_pengguna.Path.touch')  # Mock the Path.touch method to simulate file creation
    def test_check_and_create_file(self, mock_touch):
        # Call the function to check and create the file
        file_path = generate_daftar_pengguna.check_and_create_file('dummy_file.csv')
        
        # Verify that the file creation method was called with exist_ok=True
        mock_touch.assert_called_once_with(exist_ok=True)
        # Ensure the returned file path matches the expected file
        self.assertEqual(str(file_path), 'dummy_file.csv')

    # Test for the list_of_ic function, checking if IC numbers are correctly extracted from CSV
    @patch('builtins.open', new_callable=mock_open, read_data="No. Kad Pengenalan\n123456789012\n")  # Mock file contents
    @patch('generate_daftar_pengguna.csv.reader', return_value=[["No. Kad Pengenalan"], ["123456789012"]])  # Mock CSV reader
    def test_list_of_ic(self, mock_csv_reader, mock_file):
        # Call the function to extract the list of ICs from the file
        ics = generate_daftar_pengguna.list_of_ic()
        
        # Ensure that the IC '123456789012' is correctly included in the set
        self.assertEqual(ics, {"123456789012"})  # Checking that the set contains the correct IC number
    
if __name__ == "__main__":
    # Run all the tests
    unittest.main()
