read_file_location = 'files/unclean'
write_file_location = 'files/cleaned'

try:
    # Read the unclean lines from the file
    with open(read_file_location, 'r', encoding='utf-8') as file:
        unclean_lines = file.readlines()

    # Clean the lines to extract option values

    cleaned = [line.split('>')[1].split('<')[0] for line in unclean_lines if '<option' in line and '>' in line]

    # cleaned = [line.strip() for line in unclean_lines]


    # Print cleaned data (optional)
    print(cleaned)

    # Write the cleaned data to a new file
    with open(write_file_location, 'w', encoding='utf-8') as cleaned_file:
        for item in cleaned:
            cleaned_file.write(f"{item}\n")  # Write each cleaned item on a new line

except FileNotFoundError:
    print(f"The file at {read_file_location} was not found.")
except IndexError:
    print("Error: A line did not contain the expected format.")
except Exception as e:
    print(f"An error occurred: {e}") 
