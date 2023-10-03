import pandas as pd

# Read the Excel file and create dataframe
print("Enter the path of the Excel file to read.")
excel_file_path = input()  # Replace with the path to your Excel file
df = pd.read_excel(excel_file_path, engine='openpyxl')

#input the excel column headers
print("Enter the Excel hostname column text.")
hostname_column = input()
print('Enter the Excel Ip Address column text.')
ip_column = input()


# Create an empty list to store the DNS records
dns_records = []

# Loop through the rows of the dataframe and create dns records
for index, row in df.iterrows():
    hostname = row[hostname_column]
    ipaddress = row[ip_column]
    dns_record = {'host': hostname, 'ipadd': ipaddress}
    dns_records.append(dns_record)

# Create the Ansible variables file
header = '---\ndns:\n'
for dns_record in dns_records:
    header += f'  - host: {dns_record["host"]}\n\tipadd: {dns_record["ipadd"]}\n'

# Write the Ansible variables file to a file
ansible_vars_file = 'dns_vars.yml'
with open(ansible_vars_file, 'w') as file:
    file.write(header)

print(f"Ansible variables file '{ansible_vars_file}' has been created.")
