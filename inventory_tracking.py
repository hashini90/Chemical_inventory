#!/usr/bin/env python
# coding: utf-8

# !pip install pandas openpyxl
# !pip install openpyxl
# 

# In[4]:


import pandas as pd
from tkinter import *
from tkinter import messagebox, simpledialog

# Function to load the CSV file automatically
def load_csv():
    global df
    try:
        # Load the CSV file
        df = pd.read_csv("CHEM INVENTORY.csv")
        
        # Check if required columns are present
        required_columns = {'Name', 'Amount', 'Code', 'Found'}
        if not required_columns.issubset(df.columns):
            raise ValueError("CSV file must contain columns: 'Name', 'Amount', 'Code', and 'Found'")
        
        messagebox.showinfo("File Loaded", "CHEM INVENTORY.csv has been loaded successfully.")
    except FileNotFoundError:
        messagebox.showerror("File Not Found", "The file CHEM INVENTORY.csv was not found.")
    except ValueError as e:
        messagebox.showerror("Invalid File Structure", str(e))

# Function to prompt for barcode, check or add entry, and allow continuous checking
def start_continuous_check():
    global checking_active
    if df.empty:
        messagebox.showwarning("No Data", "The data file is not loaded or is empty.")
        return
    
    # Disable the Start button and enable the Done button
    start_button.config(state=DISABLED)
    done_button.config(state=NORMAL)
    
    # Set the flag for continuous checking
    checking_active = True
    continuous_check()

# Recursive function to continuously prompt for barcode
def continuous_check():
    # If the Done button was clicked, exit the loop
    if not checking_active:
        return
    
    # Prompt for barcode
    barcode = simpledialog.askstring("Input", "Please enter a barcode (or click Done to stop):")
    if not barcode:
        # Stop if the user clicks cancel or enters nothing
        done_checking()
        return

    # Extract last 4 digits of the barcode
    last_4_digits = barcode[-4:]

    # Check if the last 4 digits match any code in the DataFrame
    if any(df['Code'].astype(str).str[-4:] == last_4_digits):
        # Update 'Found' column to 'Y' for matching entries
        df.loc[df['Code'].astype(str).str[-4:] == last_4_digits, 'Found'] = 1
        messagebox.showinfo("Match Found", "Yes, the barcode matches.")
    else:
        messagebox.showinfo("Not Found", "This entry does not exist in the CSV file.")
        add_new_entry(last_4_digits)

    # Continue the loop after a delay to avoid recursion issues
    if checking_active:
        root.after(100, continuous_check)

# Function to add a new entry if no match is found
def add_new_entry(last_4_digits):
    name = simpledialog.askstring("Input", "Enter name:")
    amount = simpledialog.askstring("Input", "Enter amount:")
    code = simpledialog.askstring("Input", "Enter code:")

    if name and amount and code:
        # Add new row with 'Found' set to 'N'
        new_row = pd.DataFrame([[name, amount, code, 0]], columns=['Name', 'Amount', 'Code', 'Found'])
        global df
        df = pd.concat([df, new_row], ignore_index=True)
        messagebox.showinfo("Entry Added", f"New entry added with code ending in {last_4_digits}.")
    else:
        messagebox.showwarning("Incomplete Data", "Please enter all fields to add a new entry.")

# Function to stop the continuous checking loop
def done_checking():
    global checking_active
    checking_active = False
    start_button.config(state=NORMAL)
    done_button.config(state=DISABLED)

# Function to save the DataFrame back to CSV
def save_csv():
    try:
        df.to_csv("CHEM INVENTORY.csv", index=False)  # Save to the same CSV file
        messagebox.showinfo("File Saved", "Data has been saved to CHEM INVENTORY.csv.")
    except Exception as e:
        messagebox.showerror("Save Error", f"Failed to save file: {e}")

# Setting up the GUI
root = Tk()
root.title("Barcode Checker")

df = pd.DataFrame()  # Placeholder DataFrame
load_csv()  # Load file on startup

checking_active = False  # Flag to control the continuous checking loop

start_button = Button(root, text="Start Continuous Check", command=start_continuous_check)
start_button.pack(pady=10)

done_button = Button(root, text="Done", command=done_checking, state=DISABLED)
done_button.pack(pady=10)

save_button = Button(root, text="Save CSV File", command=save_csv)
save_button.pack(pady=10)

root.geometry("300x200")
root.mainloop()


# In[6]:





# In[ ]:





# In[ ]:




