#This program will take data from excel/csv files and allows the user to perform a number of data operations. You can
# even turn the data into an Ansible variables file for use in playbooks.  It requires pandas and openpyxl to be installed. 

import pandas as pd
import os
import math
pd.set_option('display.max_columns', None)  #Shows all columns in the imported file. 

#TODO Add gateway, Add OS, MATH
rhel9_iso =  "[VxRail-Virtual-SAN-Datastore-c50e3e2a-15a2-4e1d-8a9a-238a6046d346] 16fa1a65-18af-dede-f2df-00620b310ed0/rhel-9.2-x86_64-dvd.iso"
rhel8_iso =  "[VxRail-Virtual-SAN-Datastore-c50e3e2a-15a2-4e1d-8a9a-238a6046d346] 16fa1a65-18af-dede-f2df-00620b310ed0/rhel-8.8-x86_64-dvd.iso"


def main():
    menu = {'1.': 'Import Excel or CSV file', '2.': 'Rename columns.', '3.': 'Edit Data in Columns','4.': 'Assign Data To Vars File.',
             '5.': 'Build Ansible Vars file.', '6.': 'Toolbox.', '7.': 'Save changes to a new file.', '8.': 'Quit the program (unsaved changes will be lost).' }
    
    for key,value in menu.items():
        print(key,value)
    user_choice = input("Select an option from the menu\n")
    if user_choice == '1':
        import_files()
    elif user_choice == '2':
        rename_columns()
    elif user_choice == '3':
        edit_row_data()
    elif user_choice == '4':
        data_to_vars()
    elif user_choice == '5':
        build_file()
    elif user_choice == '6':
        toolbox()
    elif user_choice == '7':
        create_file()
    elif user_choice == '8' or user_choice.lower() == 'q':
        exit(0)
    else:
        print("Not a valid choice")
        main()

#Imports csv or xlsx files and converts them to pandas dataframe
def import_files():
    counter = 0
    files_list = []
    dataframes = []
    print("Enter the path of the files to read. Press Enter when done.")
    excel_file_path = None
    while excel_file_path != '':
        excel_file_path = input() 
        files_list.append(excel_file_path) 
    
    for filename in files_list:
        if filename.endswith('.csv'):
            df_to_add = pd.read_csv(filename, header=0)
            dataframes.append(df_to_add)
        elif filename.endswith('.xlsx'):
            df_to_add = pd.read_excel(filename, engine='openpyxl', header=0)
            dataframes.append(df_to_add)
    global df
    df = pd.concat(dataframes, ignore_index=False, axis=1)
    main()

#Allows the user to rename a column
def rename_columns():
    modify_column = ''
    while modify_column != 'Q':
        os.system('cls')
        print(df.head(5))
        modify_column = input("\n\n\nSelect a column to modify or 'Q' to quit to main menu.\n")
        if modify_column.lower() == 'q':
            main()
        else:
            new_name = input("Enter new column name or enter nothing to remove the column entirely.\n")
            if new_name == '':
                df.drop([modify_column], axis=1, inplace=True)
            else:    
                df.rename(columns={modify_column : new_name.lower()}, inplace=True)
                os.system('cls')
                print(df.head())

#Allows the user to remove and replace patterns of text in a column
def edit_row_data():
    os.system('cls')
    column=''
    while column != 'Q':
        print(df.head())
        column = input("\n\n\nSelect a column to modify or 'Q' to quit to main menu.\n")
        if column.lower() == 'q':
            main()
        else:
            remove_pattern = input("Enter the pattern to remove from the columns.\n")
            replace_pattern = input("Enter the pattern that will replace the removed pattern.\n")
            df[column] = df[column].str.replace(remove_pattern, replace_pattern)

#user chooses which columns to include in the final dataset. All others are automatically removed
def data_to_vars():
    var_keys = []
    os.system('cls')
    print(df.head())
    print("Enter columns to add to Ansible variables file. When you are ready to build the vars file type 'Build'. Enter 'Q' to quit to main menu.")
    column_choice=input()
    while column_choice.lower() != 'build':
            if column_choice.lower == 'q':
                main()
            else:
                var_keys.append(column_choice.lower())
                column_choice = input()
    build_file(var_keys)

#Turns the dataset into ansible vars file. Columns are the keys and rows are the values.     
def build_file(var_keys):
    os.system('cls')
    for i in df.columns:
        if i.lower() not in var_keys:
            df.drop([i], axis=1, inplace=True)
    print("Will build ansible vars file with these values.")
    print(df.head(5))

    ansible_file_name = input("Enter the name of the file. The .yml extension will be added automatically.\n")
    ansible_file_name += '.yml'
    header = input("Enter a name for the list of variables.")
    content = '---\n'+ str(header) + ':\n'

    with open(ansible_file_name, 'w') as file:
        file.write(content)
        for i, row in df.iterrows():
            for column in df.columns:
                if column == var_keys[0]:
                    file.write(f"- {column}: {row[column]}\n")
                else:
                    file.write(f"  {column}: {row[column]}\n")

    print(f"Ansible variables file '{ansible_file_name}' has been created.")
    main()


def create_file():
    new_file = input("Input new file name with .xlsx or .csv extension or 'Q' to go to main menu.")
    if new_file.endswith('.xlsx'):
        df.to_excel(new_file, index=False)
        main()
    elif new_file.endswith(".csv"):
        df.to_csv(new_file, index=False)
        main()
    elif new_file.lower() == "q":
        main()
    else:
        print("New file must have either .xlsx or .csv extension")
        create_file()

def toolbox():
    os.system('cls')
    functions = { "1." : "Add an IP Gateway", "2.": "Add Operating System", "3.": "Do Math", "4": "Add a custom column"}
    for key,values in functions.items():
        print(key, values)
    function_choice = input("Selection a function or enter 'Q' to return to the main menu.")
    if function_choice == '1':
        ip_row = input("Input the ip row to modify\n")
        gateway_row = input("Enter a name for the gateway row.\n")
        df[gateway_row] = df[ip_row].apply(add_gateway)
        main()
    elif function_choice == '2':
        add_os()
    elif function_choice == '3':
        row = input("Select a column to apply math to.\n")
        operation = input("Enter the mathematical expression to apply to the data. (e.g. *2, /5, +4, -3)\n")
        df[row] = df[row].apply(math, operation=operation)
        main()
    elif function_choice == '4':
        custom_column()



def add_gateway(ip_add):
    octets = str(ip_add).split('.')
    if len(octets) == 4:
        octets[-1] = '254'
        return '.'.join(octets)
    else:
        return ip_add        

def add_os():
    os.system('cls')
    os_exceptions = []
    os_options = {"RHEL 9" : [rhel9_iso, 'Rhel9_64Guest', 'lmfs.com'], "RHEL 8" : [rhel8_iso, 'rhel8_64Guest', 'lmfs.com'], 
                  "Windows Server 2022": ['','', 'win.lmfs.com'],  "Windows Server 2019": ['','windows2019srv_64Guest', 'win.lmfs.com'], 
                  "Windows 11 Workstation": ['','','win.lmfs.com'], "Windows 10 Workstation": ['','', 'win.lmfs']  }
    #Have user select an OS for RHEL and Windows servers/workstations. Allow them to specify hostname exceptions and which OS the host should use
    #Also give them option of specifying GUI or CLI.
    hostname_column = input("Enter the name of the hostname column.\n\n")
    print("OS Options")
    for op_sys in os_options.keys():
       print(op_sys)
    default_linux_os = input("Enter the default OS for Linux servers.\n")
    default_windows_os = input("Enter the default OS for Windows servers.\n")
    exception = None
    print("If any hosts need a different OS enter them now in the form of 'hostname:OS'. Press Enter when finished.\n")
    if exception != '':
        exception = input()
        os_exceptions.append(os_exceptions)
    df['Operating System'] = df[hostname_column].str.extract(r'(lsrv|lwks|wsrv|wwks)')
    os_mapping = {'lsrv': default_linux_os, 'wsrv': default_windows_os}
    df['Operating System'] = df['Operating System'].map(os_mapping)
    main()

def math(x, operation):
    if pd.isna(x):
        return None
    else: 
        result=eval(str(x) + operation)
        return result
    
def custom_function():
    column_name = input("Enter the name for the new column.")

main()
