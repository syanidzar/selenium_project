# Input multiline string
data = """

insert data here

"""

# Split the input string into lines and extract the first word
first_words = [line.split()[0] for line in data.strip().split('\n') if line]

# Write the first words to a file line by line
file_location = './script.python/files/names/file_name'
with open(file_location, 'w', encoding='utf-8') as file:
    for word in first_words:
        file.write(f"{word}\n")

