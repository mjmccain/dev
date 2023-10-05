import pandas as pd

# Read the Excel file and create dataframe
print("Enter the path of the Excel file to read.")
excel_file_path = input()  # Replace with the path to your Excel file
df = pd.read_excel(excel_file_path, engine='openpyxl')
print(df)

#input the excel column headers
print("Enter the Excel hostname column text.")
hostname_column = input()
print('Enter the Excel Ip Address column text.')
ip_column = input()

# Create an empty list to store the DNS records
dns_records = []

print("Are you building management ip[y,n]?")
man_ip = input()
# Loop through the rows of the dataframe and create dns records
for index, row in df.iterrows():
    if man_ip == 'y':
        hostname = row[hostname_column] + 'm'
    else:
        hostname = row[hostname_column]
    if '.0' in str(row[ip_column]):
        ipaddress = row[ip_column].split('.0')
        ipaddress = ipaddress[0] + '.' + ipaddress[1]
    else:
        ipaddress = row[ip_column]
    if 'lsrv' in hostname or 'lwks' in hostname:
        domain = 'lmfs.com'
    elif 'wsrv' in hostname or 'wwks' in hostname:
        domain = 'win.lmfs.com'
    else:
        domain = 'lmfs.com'
    dns_record = {'host': hostname, 'ipadd': ipaddress, 'domain': domain}
    dns_records.append(dns_record)

# Create the Ansible variables file
header = '---\ndns:\n'
for dns_record in dns_records:
    header += f'  - host: {dns_record["host"]}\n    ipadd: {dns_record["ipadd"]}\n    domain: {dns_record["domain"]}\n'

# Write the Ansible variables file to a file
if man_ip == 'y':
    ansible_vars_file = 'dns_vars_oobm.yml'
else:
    ansible_vars_file = 'dns_vars_ops.yml'

with open(ansible_vars_file, 'w') as file:
    file.write(header)

print(f"Ansible variables file '{ansible_vars_file}' has been created.")
