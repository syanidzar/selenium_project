import unittest
from unittest.mock import patch, mock_open, MagicMock
from datetime import datetime, timedelta
import random
import generate_daftar_pengguna

class TestUserGenerator(unittest.TestCase):
    
    @patch('generate_daftar_pengguna.datetime')
    def test_generate_random_dob(self, mock_datetime):
        # Mock datetime to control the range of DOB
        mock_datetime.now.return_value = datetime(2024, 1, 1)
        dob = generate_daftar_pengguna.generate_random_dob()
        self.assertTrue(datetime(1993, 1, 1) <= dob <= datetime(2003, 1, 1))
    
    @patch('generate_daftar_pengguna.generate_random_dob', return_value=datetime(1990, 5, 15))
    @patch('random.randint', side_effect=[10, 1234])
    def test_generate_kad_pengenalan(self, mock_randint, mock_dob):
        ic = generate_daftar_pengguna.generate_kad_pengenalan()
        self.assertEqual(ic, "900515101234")
    
    def test_set_gender(self):
        genders = set(generate_daftar_pengguna.set_gender() for _ in range(100))
        self.assertEqual(genders, {"male", "female"})
    
    @patch('random.choices', return_value=['malay'])
    def test_set_ethnicity(self, mock_choices):
        ethnicity = generate_daftar_pengguna.set_ethnicity()
        self.assertEqual(ethnicity, "malay")
    
    @patch('builtins.open', new_callable=mock_open, read_data='Name1\nName2\nName3')
    def test_read_name_from_file(self, mock_file):
        name = generate_daftar_pengguna.read_name_from_file('dummy_file')
        self.assertIn(name, ['Name1', 'Name2', 'Name3'])
    
    @patch('generate_daftar_pengguna.read_name_from_file', side_effect=['Ali', 'Hassan'])
    def test_generate_name_malay_male(self, mock_read_name):
        name, ethnicity, gender = generate_daftar_pengguna.generate_name('malay', 'male')
        self.assertEqual(name, 'Ali bin Hassan')
        self.assertEqual(ethnicity, 'malay')
        self.assertEqual(gender, 'male')

    @patch('random.shuffle')
    def test_set_roles(self, mock_shuffle):
        roles = generate_daftar_pengguna.set_roles(10)
        self.assertEqual(len(roles), 10)
        self.assertIn('Pentadbir Agensi', roles)
        self.assertIn('Staf', roles)

    @patch('generate_daftar_pengguna.Path.touch')
    def test_check_and_create_file(self, mock_touch):
        file_path = generate_daftar_pengguna.check_and_create_file('dummy_file.csv')
        mock_touch.assert_called_once_with(exist_ok=True)
        self.assertEqual(str(file_path), 'dummy_file.csv')

    @patch('builtins.open', new_callable=mock_open, read_data="No. Kad Pengenalan\n123456789012\n")
    @patch('generate_daftar_pengguna.csv.reader', return_value=[["No. Kad Pengenalan"], ["123456789012"]])
    def test_list_of_ic(self, mock_csv_reader, mock_file):
        ics = generate_daftar_pengguna.list_of_ic()
        self.assertEqual(ics, {"123456789012"})  # Checking that the set contains the correct IC number
    
if __name__ == "__main__":
    unittest.main()
