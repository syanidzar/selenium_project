# Specify the filename
filename = './files/generated_program_gred.sql'

# Open the file for writing
with open(filename, 'w') as file:
    # Write the SQL commands to the file
    sql = (
        "CREATE TABLE IF NOT EXISTS `program_gred` (\n"
        "    `id_gred` VARCHAR(2) NOT NULL,\n"
        "    `jenis_gred` VARCHAR(2) NOT NULL,\n"
        "    `status_aktif` TINYINT NOT NULL,\n"
        "    `create_by` VARCHAR(50) DEFAULT '',\n"
        "    `create_date` DATETIME DEFAULT CURRENT_TIMESTAMP,\n"
        "    `modify_by` VARCHAR(50) DEFAULT '',\n"
        "    `modify_date` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\n"
        "    PRIMARY KEY (`id_gred`)\n"
        ");\n\n"
    )

    # Prepare the insert statement
    sql += "INSERT INTO `program_gred` (`id_gred`, `jenis_gred`, `status_aktif`, `create_by`, `modify_by`) VALUES \n"
    
    values = []
    for i in range(1, 100):
        id_gred = str(i).zfill(2)  # Pads the number with leading zeros
        values.append(f"('{id_gred}', '{id_gred}', '1', '', '')")
    
    sql += ",\n".join(values) + ";\n"

    # Write the SQL commands to the file
    file.write(sql)

print(f"SQL file '{filename}' created successfully.")
