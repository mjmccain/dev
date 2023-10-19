#This program will take data from an excel file and create a corresponding ansible variables file
#for use in playbooks. It requires pandas and openpyxl to be installed. 

import pandas as pd
import os
pd.set_option('display.max_columns', None)  #Shows all columns in the imported file. 


# Read the Excel file and create dataframe
print("Enter the path of the Excel file to read.")
excel_file_path = input()  
df = pd.read_excel(excel_file_path, engine='openpyxl', header=0)

print(df.columns)

def main():
    menu = {'1.': 'Rename columns.', '2.': 'Edit Data in Columns','3.': 'Assign Data To Vars File.',
             '4.': 'Build Ansible Vars file.', '5.': 'Special functions.', '6.': 'Write data to new excel file.', '7.': 'Quit the program.' }
    
    for key,value in menu.items():
        print(key,value)
    user_choice = input("Select an option from the menu\n")
    if user_choice == '1':
        rename_columns()
    if user_choice == '2':
        edit_row_data()
    elif user_choice == '3':
        data_to_vars()
    elif user_choice == '4':
        build_file()
    elif user_choice == '5':
        add_gateway()
    elif user_choice == '6':
        create_file()
    elif user_choice == '7' or user_choice.lower() == 'q':
        exit(0)
    else:
        print("Not a valid choice")
        main()

#Allows the user to rename a column
def rename_columns():
    modify_column = ''
    while modify_column != 'Q':
        os.system('cls')
        print(df.head())
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
    exit(0)

def add_gateway():
    print("To add a column for IP gateway, specify the IP address column or Q to quit to main menu.")
    ip_column=input()
    print("Enter a name for the gateway column ie. ops_gateway, oobm_gateway")
    gateway_column = input()
    df[gateway_column] = ''
                                          
    main()

def create_file():
    new_file = input("Input new file name. The .xlsx extension will be added automatically.")
    df.to_excel(f"{new_file}.xlsx")
    main()


main()
