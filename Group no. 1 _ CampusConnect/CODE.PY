import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from PIL import Image, ImageTk
import pymysql
import uuid
import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string
import re

# Constants
DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '3005',
    'database': 'campusconnect'
}

# Function to connect to the MySQL database
def connect_to_database():
    try:
        connection = pymysql.connect(**DATABASE_CONFIG)
        return connection
    except pymysql.MySQLError as e:
        messagebox.showerror("Database Error", f"Error connecting to database: {e}")
        return None

# Function to clear the current frame
def clear_frame():
    for widget in root.winfo_children():
        widget.destroy()

# Function to update subjects based on the selected class
def update_subjects(*args):
    selected_class = class_option.get()
    subjects = {
        "FE_A": ["MATHS 1", "CHEM 1", "PHY 1", "MECH", "BEE", "C"],
        "FE_B": ["MATHS 1", "CHEM 1", "PHY 1", "MECH", "BEE", "C"],
        "FE_C": ["MATHS 1", "CHEM 1", "PHY 1", "MECH", "BEE", "C"],
        "SE_A": ["MATHS 2", "AOA", "DBMS", "DLCOA", "DSGT", "OS"],
        "SE_B": ["MATHS 2", "AOA", "DBMS", "DLCOA", "DSGT", "OS"],
        "TE_A": ["MATHS 3", "DS", "MP", "PYTHON", "CSS", "ML"],
        "TE_B": ["MATHS 3", "DS", "MP", "PYTHON", "CSS", "ML"],
        "BE": ["AIML", "BLOCKCHAIN", "HTML", "DA", "MATHS 4", "CYBERSECURITY"]
    }

    subjects = subjects.get(selected_class, [])
    subject_option.set(subjects[0] if subjects else "")

    menu = subject_menu['menu']
    menu.delete(0, 'end')

    for subject in subjects:
        menu.add_command(label=subject, command=tk._setit(subject_option, subject))

# Function to create the welcome page
def welcome_page():
    clear_frame()
    welcome_page_fm = tk.Frame(root, bg="#ffffff")
    welcome_page_fm.pack(pady=30, fill="both", expand=True)

    boundary_frame = tk.Frame(welcome_page_fm, bg="#ffffff", highlightbackground="#000000", highlightthickness=2)
    boundary_frame.pack(padx=1, pady=1, fill="both", expand=True)

    inner_frame = tk.Frame(boundary_frame, bg="#ffffff")
    inner_frame.pack(pady=30, fill="both", expand=True)

    logo_fm = tk.Frame(inner_frame, bg="#ffffff")
    logo_fm.place(relx=0.5, rely=0.5, anchor="center")

    logo_image = Image.open("C:\\Users\\Ashis\\OneDrive\\Desktop\\BG\\Campusconnect.png")  # Update with your logo path
    logo_image = logo_image.resize((800, 800))
    logo_image = ImageTk.PhotoImage(logo_image)

    logo_label = tk.Label(logo_fm, image=logo_image, bg="#ffffff")
    logo_label.image = logo_image
    logo_label.pack()

    heading_lb = tk.Label(inner_frame, text='WELCOME TO CampusConnect', bg="#ffffff", fg="#007bff", font=('Flatory Sans', 30, 'bold'))
    heading_lb.place(relx=0.5, rely=0.1, anchor="center")

    button_frame = tk.Frame(inner_frame, bg="#ffffff")
    button_frame.place(x=2, rely=0.5, anchor="w")

    login_hod_btn = tk.Button(button_frame, text='Login HOD', bg="#87CEEB", fg='white', font=('Bold', 28), command=login_hod_page)
    login_hod_btn.pack(pady=20, fill="x")

    login_staff_btn = tk.Button(button_frame, text='Login Staff', bg="#FFFF00", fg='black', font=('Bold', 28), command=login_staff_page)
    login_staff_btn.pack(pady=20, fill="x")

    login_student_btn = tk.Button(button_frame, text='Login Student', bg="#C6F4D6", fg='black', font=('Bold', 28), command=login_student_page)
    login_student_btn.pack(pady=20, fill="x")

    register_btn = tk.Button(button_frame, text='Register', bg="#FFC0CB", fg='black', font=('Bold', 28), command=registration_page)
    register_btn.pack(pady=20, fill="x")

# Function to create the registration page
def registration_page():
    clear_frame()
    registration_frame = tk.Frame(root, bg="#ADD8E6")
    registration_frame.pack(pady=30, fill="both", expand=True)

    logo_frame = tk.Frame(registration_frame, bg="#ADD8E6")
    logo_frame.place(relx=0.5, rely=0.5, anchor="center")

    logo_image = Image.open("C:\\Users\\Ashis\\OneDrive\\Desktop\\BG\\Campusconnect.png")  # Update with your logo path
    logo_image = logo_image.resize((800, 800))
    logo_image = ImageTk.PhotoImage(logo_image)
    logo_label = tk.Label(logo_frame, image=logo_image, bg="#ADD8E6")
    logo_label.image = logo_image
    logo_label.pack()

    heading_lb = tk.Label(logo_frame, text='REGISTRATION', bg="#ADD8E6", fg="#007bff", font=('Bold', 45))
    heading_lb.place(relx=0.5, rely=0.15, anchor="center")

    button_frame = tk.Frame(logo_frame, bg="#ADD8E6")
    button_frame.place(relx=0.5, rely=0.9, anchor="center")

    student_register_button = tk.Button(button_frame, text='Register as Student', bg="#ffffff", fg='black', font=('Bold', 24), command=student_registration)
    student_register_button.pack(side='left', padx=20)

    staff_register_button = tk.Button(button_frame, text='Register as Staff', bg="#ffffff", fg='black', font=('Bold', 24), command=staff_registration)
    staff_register_button.pack(side='left', padx=20)

    home_button = tk.Button(registration_frame, text='Home', bg="#ffffff", fg='black', font=('Bold', 14), command=welcome_page)
    home_button.place(relx=1, rely=1, anchor="se")

# Function to create the student registration page
def student_registration():
    clear_frame()
    student_registration_frame = tk.Frame(root, bg="#ADD8E6")
    student_registration_frame.pack(pady=30, fill="both", expand=True)

    student_registration_heading_lb = tk.Label(student_registration_frame, text='STUDENT REGISTRATION', bg="#ADD8E6", fg="#007bff", font=('Bold', 45))
    student_registration_heading_lb.pack(pady=20)

    student_form_frame = tk.Frame(student_registration_frame, bg="#ADD8E6")
    student_form_frame.pack(pady=10, fill='x')

    student_id_var = tk.StringVar()
    student_id_var.set(generate_student_id("FE"))

    student_id_lb = tk.Label(student_form_frame, text='Student ID Number:', bg="#ADD8E6", fg='black', font=('Bold', 14))
    student_id_lb.grid(row=0, column=0, padx=10, pady=10)

    student_id_display_lb = tk.Label(student_form_frame, textvariable=student_id_var, bg="#ADD8E6", fg='black', font=('Bold', 14))
    student_id_display_lb.grid(row=0, column=1, padx=10, pady=10)

    student_name_lb = tk.Label(student_form_frame, text='Enter Student Full Name:', bg="#ADD8E6", fg='black', font=('Bold', 14))
    student_name_lb.grid(row=1, column=0, padx=10, pady=10)

    student_name_entry = tk.Entry(student_form_frame, width=30, font=('Bold', 14))
    student_name_entry.grid(row=1, column=1, padx=10, pady=10)

    student_gender_lb = tk.Label(student_form_frame, text='Select Student Gender:', bg="#ADD8E6", fg='black', font=('Bold', 14))
    student_gender_lb.grid(row=2, column=0, padx=10, pady=10)

    student_gender_var = tk.StringVar(value="Male")
    student_gender_male_rb = tk.Radiobutton(student_form_frame, text="Male", variable=student_gender_var, value="Male")
    student_gender_male_rb.grid(row=2, column=1, padx=10, pady=10)

    student_gender_female_rb = tk.Radiobutton(student_form_frame, text="Female", variable=student_gender_var, value="Female")
    student_gender_female_rb.grid(row=2, column=2, padx=10, pady=10)

    student_age_lb = tk.Label(student_form_frame, text='Enter Student Age:', bg="#ADD8E6", fg='black', font=('Bold', 14))
    student_age_lb.grid(row=3, column=0, padx=10, pady=10)

    student_age_entry = tk.Entry(student_form_frame, width=30, font=('Bold', 14))
    student_age_entry.grid(row=3, column=1, padx=10, pady=10)

    student_phone_lb = tk.Label(student_form_frame, text='Enter Contact Phone Number:', bg="#ADD8E6", fg='black', font=('Bold', 14))
    student_phone_lb.grid(row=4, column=0, padx=10, pady=10)

    student_phone_entry = tk.Entry(student_form_frame, width=30, font=('Bold', 14))
    student_phone_entry.grid(row=4, column=1, padx=10, pady=10)

    student_class_lb = tk.Label(student_form_frame, text='Select Student Class:', bg="#ADD8E6", fg='black', font=('Bold', 14))
    student_class_lb.grid(row=5, column=0, padx=10, pady=10)

    student_class_var = tk.StringVar(value="FE_A")
    student_class_dropdown = tk.OptionMenu(student_form_frame, student_class_var, "FE_A", "FE_B", "FE_C", "SE_A", "SE_B")
    student_class_dropdown.grid(row=5, column=1, padx=10, pady=10)

    student_email_lb = tk.Label(student_form_frame, text='Enter Student Email Address:', bg="#ADD8E6", fg='black', font=('Bold', 14))
    student_email_lb.grid(row=6, column=0, padx=10, pady=10)

    student_email_entry = tk.Entry(student_form_frame, width=30, font=('Bold', 14))
    student_email_entry.grid(row=6, column=1, padx=10, pady=10)

    student_password_lb = tk.Label(student_form_frame, text='Create Account Password:', bg="#ADD8E6", fg='black', font=('Bold', 14))
    student_password_lb.grid(row=7, column=0, padx=10, pady=10)

    student_password_entry = tk.Entry(student_form_frame, show='*', width=30, font=('Bold', 14))
    student_password_entry.insert(0, f"{student_id_var.get()}@cc")
    student_password_entry.grid(row=7, column=1, padx=10, pady=10)

    button_frame = tk.Frame(student_registration_frame, bg="#ADD8E6")
    button_frame.pack(pady=20)

    def register_student():
        student_info = {
            "ID": student_id_var.get(),
            "Name": student_name_entry.get(),
            "Gender": student_gender_var.get(),
            "Age": student_age_entry.get(),
            "Phone": student_phone_entry.get(),
            "Class": student_class_var.get(),
            "Email": student_email_entry.get(),
            "Password": student_password_entry.get(),
        }

        if not validate_student_info(student_info):
            return

        save_student_to_database(student_info)
        login_student_page()

    register_button = tk.Button(button_frame, text='Register', bg="#ffffff", fg='black', font=('Bold', 14), command=register_student)
    register_button.pack(side='left', padx=5)

    home_button = tk.Button(student_registration_frame, text='Home', bg="#ffffff", fg='black', font=('Bold', 14), command=registration_page)
    home_button.pack(pady=10)

# Function to validate student information
def validate_student_info(student_info):
    if not student_info["Name"]:
        messagebox.showerror("Error", "Student Name is required.")
        return False
    if not student_info["Age"].isdigit() or int(student_info["Age"]) < 18 or int(student_info["Age"]) > 24:
        messagebox.showerror("Error", "Please enter a valid age between 18 and 24.")
        return False
    if not student_info["Phone"].isdigit() or len(student_info["Phone"]) != 10:
        messagebox.showerror("Error", "Please enter a valid 10-digit phone number.")
        return False
    if not re.match(r'^[^@]+@(?:gmail\.com|yahoo\.com|outlook\.com)$', student_info["Email"]):
        messagebox.showerror("Error", "Please enter a valid email address from gmail.com, yahoo.com, or outlook.com.")
        return False
    if not student_info["Password"]:
        messagebox.showerror("Error", "Password is required.")
        return False
    return True

# Function to save student information to the database
def save_student_to_database(student_info):
    connection = connect_to_database()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO students (student_id, name, gender, age, phone, class, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (student_info["ID"], student_info["Name"], student_info["Gender"], student_info["Age"], student_info["Phone"], student_info["Class"], student_info["Email"], student_info["Password"]))
                connection.commit()
            messagebox.showinfo("Information", "Registration Successful!")
        except pymysql.MySQLError as e:
            messagebox.showerror("Database Error", f"Error saving to database: {e}")
        finally:
            connection.close()

# Function to create the staff registration page
def staff_registration():
    clear_frame()
    staff_registration_frame = tk.Frame(root, bg="#ADD8E6")
    staff_registration_frame.pack(pady=30, fill="both", expand=True)

    staff_registration_heading_lb = tk.Label(staff_registration_frame, text='STAFF REGISTRATION', bg="#ADD8E6", fg="#007bff", font=('Bold', 45))
    staff_registration_heading_lb.pack(pady=20)

    staff_form_frame = tk.Frame(staff_registration_frame, bg="#ADD8E6")
    staff_form_frame.pack(pady=10, fill='x')

    staff_name_lb = tk.Label(staff_form_frame, text='Staff Name:', bg="#ADD8E6", fg='black', font=('Bold', 14))
    staff_name_lb.grid(row=0, column=0, padx=10, pady=10)

    staff_name_entry = tk.Entry(staff_form_frame, width=30, font=('Bold', 14))
    staff_name_entry.grid(row=0, column=1, padx=10, pady=10)

    staff_id = str(random.randint(1000, 9999))
    staff_id_label = tk.Label(staff_form_frame, text=staff_id, bg="#ADD8E6", fg='black', font=('Bold', 14))
    staff_id_label.grid(row=1, column=1, padx=10, pady=10)

    staff_id_lb = tk.Label(staff_form_frame, text='Staff ID Number:', bg="#ADD8E6", fg='black', font=('Bold', 14))
    staff_id_lb.grid(row=1, column=0, padx=10, pady=10)

    staff_password_lb = tk.Label(staff_form_frame, text='Staff Password:', bg="#ADD8E6", fg='black', font=('Bold', 14))
    staff_password_lb.grid(row=2, column=0, padx=10, pady=10)

    staff_password_entry = tk.Entry(staff_form_frame, show='*', width=30, font=('Bold', 14))
    staff_password_entry.insert(0, f"{staff_id}@cc")
    staff_password_entry.grid(row=2, column=1, padx=10, pady=10)

    staff_designation_lb = tk.Label(staff_form_frame, text='Designation:', bg="#ADD8E6", fg='black', font=('Bold', 14))
    staff_designation_lb.grid(row=3, column=0, padx=10, pady=10)

    staff_designation_var = tk.StringVar()
    staff_designation_dropdown = tk.OptionMenu(staff_form_frame, staff_designation_var, 'Prof', 'Assistant Prof', 'Associate Prof', 'Dr')
    staff_designation_dropdown.grid(row=3, column=1, padx=10, pady=10)

    staff_contact_no_lb = tk.Label(staff_form_frame, text='Contact Number:', bg="#ADD8E6", fg='black', font=('Bold', 14))
    staff_contact_no_lb.grid(row=4, column=0, padx=10, pady=10)

    staff_contact_no_entry = tk.Entry(staff_form_frame, width=30, font=('Bold', 14))
    staff_contact_no_entry.grid(row=4, column=1, padx=10, pady=10)

    staff_email_lb = tk.Label(staff_form_frame, text='Email Address:', bg="#ADD8E6", fg='black', font=('Bold', 14))
    staff_email_lb.grid(row=5, column=0, padx=10, pady=10)

    staff_email_entry = tk.Entry(staff_form_frame, width=30, font=('Bold', 14))
    staff_email_entry.grid(row=5, column=1, padx=10, pady=10)

    subjects = ['MATHS 1', 'CHEM 1', 'PHY 1', 'MECH', 'BEE', 'C', 'MATHS 2', 'AOA', 'DBMS', 'DLCOA', 'DSGT', 'OS', 'MATHS 3', 'DS', 'MP', 'PYTHON', 'CSS', 'ML', 'AIML', 'BLOCKCHAIN', 'HTML', 'DA', 'MATHS 4', 'CYBERSECURITY']

    staff_subject_lb = tk.Label(staff_form_frame, text='Subject:', bg="#ADD8E6", fg='black', font=('Bold', 14))
    staff_subject_lb.grid(row=6, column=0, padx=10, pady=10)

    staff_subject_var = tk.StringVar()
    staff_subject_dropdown = tk.OptionMenu(staff_form_frame, staff_subject_var, *subjects)
    staff_subject_dropdown.grid(row=6, column=1, padx=10, pady=10)

    button_frame = tk.Frame(staff_registration_frame, bg="#ADD8E6")
    button_frame.pack(pady=20)

    def register_staff():
        staff_info = {
            "ID": staff_id,
            "Name": staff_name_entry.get(),
            "Password": staff_password_entry.get(),
            "Designation": staff_designation_var.get(),
            "Contact": staff_contact_no_entry.get(),
            "Email": staff_email_entry.get(),
            "Subject": staff_subject_var.get(),
        }

        if not validate_staff_info(staff_info):
            return

        save_staff_to_database(staff_info)
        login_staff_page()

    register_button = tk.Button(button_frame, text='Register', bg="#ffffff", fg='black', font=('Bold', 14), command=register_staff)
    register_button.pack(side='left', padx=5)

    home_button = tk.Button(staff_registration_frame, text='Home', bg="#ffffff", fg='black', font=('Bold', 14), command=registration_page)
    home_button.pack(pady=10)

# Function to validate staff information
def validate_staff_info(staff_info):
    if not staff_info["Name"]:
        messagebox.showerror("Error", "Staff Name is required.")
        return False
    if not staff_info["Contact"].isdigit() or len(staff_info["Contact"]) != 10:
        messagebox.showerror("Error", "Please enter a valid 10-digit contact number.")
        return False
    if not re.match(r'^[^@]+@(?:gmail\.com|yahoo\.com|outlook\.com)$', staff_info["Email"]):
        messagebox.showerror("Error", "Please enter a valid email address from gmail.com, yahoo.com, or outlook.com.")
        return False
    if not staff_info["Password"]:
        messagebox.showerror("Error", "Password is required.")
        return False
    return True

# Function to save staff information to the database
def save_staff_to_database(staff_info):
    connection = connect_to_database()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO staff (staff_id, name, designation, contact, email, subject, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (staff_info["ID"], staff_info["Name"], staff_info["Designation"], staff_info["Contact"], staff_info["Email"], staff_info["Subject"], staff_info["Password"]))
                connection.commit()
            messagebox.showinfo("Information", "Registration Successful!")
        except pymysql.MySQLError as e:
            messagebox.showerror("Database Error", f"Error saving to database: {e}")
        finally:
            connection.close()

# Function to create the login HOD page
def login_hod_page():
    clear_frame()
    login_hod_frame = tk.Frame(root, bg="#ffffff")
    login_hod_frame.pack(pady=30, fill="both", expand=True)

    boundary_frame = tk.Frame(login_hod_frame, bg="#ffffff", highlightbackground="#000000", highlightthickness=2)
    boundary_frame.pack(padx=1, pady=1, fill="both", expand=True)

    inner_frame = tk.Frame(boundary_frame, bg="#ffffff")
    inner_frame.pack(padx=10, pady=10, fill="both", expand=True)

    login_hod_image = Image.open("C:\\Users\\Ashis\\OneDrive\\Desktop\\BG\\login.png")  # Update with your image path
    login_hod_image = login_hod_image.resize((400, 400))
    login_hod_image = ImageTk.PhotoImage(login_hod_image)

    login_hod_label = tk.Label(inner_frame, image=login_hod_image, bg="#ffffff")
    login_hod_label.image = login_hod_image
    login_hod_label.pack()

    login_hod_heading_lb = tk.Label(inner_frame, text='LOGIN HOD', bg="#ffffff", fg="#007bff", font=('Bold', 28))
    login_hod_heading_lb.pack(pady=10)

    hod_id_frame = tk.Frame(inner_frame, bg="#ffffff")
    hod_id_frame.pack(pady=5, fill='x')

    hod_id_lb = tk.Label(hod_id_frame, text='HOD ID Number:', bg="#ffffff", fg='black', font=('Bold', 20))
    hod_id_lb.pack(side='left')

    hod_id_entry = tk.Entry(hod_id_frame, width=20, font=('Bold', 20))
    hod_id_entry.pack(side='left', padx=5)

    hod_password_frame = tk.Frame(inner_frame, bg="#ffffff")
    hod_password_frame.pack(pady=5, fill='x')

    hod_password_lb = tk.Label(hod_password_frame, text='HOD Password:', bg="#ffffff", fg='black', font=('Bold', 20))
    hod_password_lb.pack(side='left')

    hod_password_entry = tk.Entry(hod_password_frame, show='*', width=20, font=('Bold', 20))
    hod_password_entry.pack(side='left', padx=5)

    button_frame = tk.Frame(inner_frame, bg="#ffffff")
    button_frame.pack(pady=10)

    def login():
        if hod_id_entry.get() == "AnaghaA_1" and hod_password_entry.get() == "hod123":
            login_hod_frame.destroy()
            hod_dashboard_page()
        else:
            messagebox.showerror("Error", "Invalid HOD ID or Password")

    def forgot_password():
        if messagebox.askyesno("Confirmation", "Do you want to proceed with forgot password?"):
            forgot_password_page()

    login_button = tk.Button(button_frame, text='Login', bg="#87CEEB", fg='white', font=('Bold', 20), command=login)
    login_button.pack(side='left', padx=5)

    forgot_password_button = tk.Button(button_frame, text='Forgot Password', bg="#87CEEB", fg='white', font=('Bold', 20), command=forgot_password)
    forgot_password_button.pack(side='left', padx=5)

    home_button_hod = tk.Button(inner_frame, text='Home', bg="#87CEEB", fg='white', font=('Bold', 20), command=welcome_page)
    home_button_hod.pack(pady=10)

# Function to create the forgot password page for HOD
def forgot_password_page():
    clear_frame()
    forgot_password_frame = tk.Frame(root, bg="#ffffff")
    forgot_password_frame.pack(pady=30, fill="both", expand=True)

    forgot_password_label = tk.Label(forgot_password_frame, text='Forgot Password', bg="#ffffff", fg="#007bff", font=('Bold', 28))
    forgot_password_label.pack(pady=20)

    hod_id_frame = tk.Frame(forgot_password_frame, bg="#ffffff")
    hod_id_frame.pack(pady=5, fill='x')

    hod_id_lb = tk.Label(hod_id_frame, text='HOD ID Number:', bg="#ffffff", fg='black', font=('Bold', 20))
    hod_id_lb.pack(side='left')

    hod_id_entry = tk.Entry(hod_id_frame, width=20, font=('Bold', 20))
    hod_id_entry.pack(side='left', padx=5)

    hod_email_frame = tk.Frame(forgot_password_frame, bg="#ffffff")
    hod_email_frame.pack(pady=5, fill='x')

    hod_email_lb = tk.Label(hod_email_frame, text='HOD Email:', bg="#ffffff", fg='black', font=('Bold', 20))
    hod_email_lb.pack(side='left')

    hod_email_entry = tk.Entry(hod_email_frame, width=20, font=('Bold', 20))
    hod_email_entry.pack(side='left', padx=5)

    button_frame = tk.Frame(forgot_password_frame, bg="#ffffff")
    button_frame.pack(pady=10)

    def reset_password():
        hod_id = hod_id_entry.get().strip()
        hod_email = hod_email_entry.get().strip()
        connection = connect_to_database()
        if connection:
            try:
                with connection.cursor() as cursor:
                    sql = "SELECT * FROM hod WHERE hod_id = %s AND email = %s"
                    cursor.execute(sql, (hod_id, hod_email))
                    result = cursor.fetchone()
                    if result:
                        new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
                        update_sql = "UPDATE hod SET password = %s WHERE hod_id = %s"
                        cursor.execute(update_sql, (new_password, hod_id))
                        connection.commit()

                        # Send email with the new password
                        msg = MIMEMultipart()
                        msg['From'] = 'campusconnect@example.com'
                        msg['To'] = hod_email
                        msg['Subject'] = 'Password Reset'
                        body = f'Your new password is: {new_password}'
                        msg.attach(MIMEText(body, 'plain'))

                        server = smtplib.SMTP('smtp.example.com', 587)
                        server.starttls()
                        server.login('campusconnect@example.com', 'your_password')
                        text = msg.as_string()
                        server.sendmail('campusconnect@example.com', hod_email, text)
                        server.quit()

                        messagebox.showinfo("Success", "A new password has been sent to your email.")
                    else:
                        messagebox.showerror("Error", "Invalid HOD ID or Email")
            except pymysql.MySQLError as e:
                messagebox.showerror("Database Error", f"Error resetting password: {e}")
            finally:
                connection.close()

    reset_password_button = tk.Button(button_frame, text='Reset Password', bg="#87CEEB", fg='white', font=('Bold', 14), command=reset_password)
    reset_password_button.pack(side='left', padx=5)

    back_button = tk.Button(button_frame, text='Back', bg="#87CEEB", fg='white', font=('Bold', 14), command=login_hod_page)
    back_button.pack(side='left', padx=5)

# Function to create the HOD dashboard page
def hod_dashboard_page():
    clear_frame()
    dashboard_frame = tk.Frame(root, bg="#ffffff")
    dashboard_frame.pack(pady=30, fill="both", expand=True)

    boundary_frame = tk.Frame(dashboard_frame, bg="#ffffff", highlightbackground="#000000", highlightthickness=2)
    boundary_frame.pack(padx=1, pady=1, fill="both", expand=True)

    inner_frame = tk.Frame(boundary_frame, bg="#ffffff")
    inner_frame.pack(padx=10, pady=10, fill="both", expand=True)

    logo_frame = tk.Frame(inner_frame, bg="#ffffff")
    logo_frame.place(relx=0.5, rely=0.5, anchor="center")

    logo_image = Image.open("C:\\Users\\Ashis\\OneDrive\\Desktop\\BG\\Campusconnect.png")  # Update with your logo path
    logo_image = logo_image.resize((800, 800))
    logo_image = ImageTk.PhotoImage(logo_image)

    logo_label = tk.Label(logo_frame, image=logo_image, bg="#ffffff")
    logo_label.image = logo_image
    logo_label.pack()

    heading_lb = tk.Label(logo_frame, text='HOD Dashboard', bg="#ffffff", fg="#007bff", font=('Bold', 32))
    heading_lb.place(relx=0.5, rely=0.15, anchor="center")

    left_button_frame = tk.Frame(inner_frame, bg="#ffffff")
    left_button_frame.place(x=10, rely=0.5, anchor="w")

    notify_students_button = tk.Button(left_button_frame, text='Notify Students', bg="#ADD8E6", fg='black', font=('Bold', 14), command=notify_students_page)
    notify_students_button.pack(pady=10, fill="x")

    view_student_details_button = tk.Button(left_button_frame, text='View Student Details', bg="#ADD8E6", fg='black', font=('Bold', 14), command=view_student_details_page)
    view_student_details_button.pack(pady=10, fill="x")

    view_staff_details_button = tk.Button(left_button_frame, text='View staff Details', bg="#ADD8E6", fg='black', font=('Bold', 14), command=view_staff_details_page)
    view_staff_details_button.pack(pady=10, fill="x")

    mark_attendance_button = tk.Button(left_button_frame, text='Mark Attendance', bg="#ADD8E6", fg='black', font=('Bold', 14), command=mark_attendance_page)
    mark_attendance_button.pack(pady=10, fill="x")

    upload_notes_button = tk.Button(left_button_frame, text='Upload Notes', bg="#ADD8E6", fg='black', font=('Bold', 14), command=lambda: upload_page("Notes"))
    upload_notes_button.pack(pady=10, fill="x")

    upload_results_button = tk.Button(left_button_frame, text='Upload Results', bg="#ADD8E6", fg='black', font=('Bold', 14), command=lambda: upload_page("Results"))
    upload_results_button.pack(pady=10, fill="x")

    generate_assignment_links_button = tk.Button(left_button_frame, text='Generate Assignment Links', bg="#ADD8E6", fg='black', font=('Bold', 14), command=generate_assignment_links_page)
    generate_assignment_links_button.pack(pady=10, fill="x")

    home_button_dashboard = tk.Button(inner_frame, text='Home', bg="#87CEEB", fg='white', font=('Bold', 10), command=welcome_page)
    home_button_dashboard.place(relx=0.95, rely=0.95, anchor="se")

    notification_frame = tk.Frame(inner_frame, bg="#ffffff", highlightbackground="#000000", highlightthickness=1)
    notification_frame.place(relx=0.95, rely=0.05, anchor="ne")

    notification_label = tk.Label(notification_frame, text='Notifications', bg="#ffffff", fg="#007bff", font=('Bold', 14))
    notification_label.pack()

    notification_text = tk.Text(notification_frame, width=30, height=5, font=('Bold', 12), state='disabled')
    notification_text.pack()

    def update_notifications(message):
        notification_text.config(state='normal')
        notification_text.insert(tk.END, message + '\n')
        notification_text.config(state='disabled')

    update_notifications("New announcement from HOD: Staff meeting at 3 PM.")

# Function to create the notify students page
def notify_students_page():
    clear_frame()
    notify_students_frame = tk.Frame(root, bg="#ffffff")
    notify_students_frame.pack(pady=30, fill="both", expand=True)

    boundary_frame = tk.Frame(notify_students_frame, bg="#ffffff", highlightbackground="#000000", highlightthickness=2)
    boundary_frame.pack(padx=1, pady=1, fill="both", expand=True)

    inner_frame = tk.Frame(boundary_frame, bg="#ffffff")
    inner_frame.pack(pady=10, fill="both", expand=True)

    heading_lb = tk.Label(inner_frame, text='Notify Students', bg="#ffffff", fg="#007bff", font=('Bold', 28))
    heading_lb.pack(pady=20)

    notify_frame = tk.Frame(inner_frame, bg="#ffffff")
    notify_frame.pack(pady=10, fill="x")

    student_id_lb = tk.Label(notify_frame, text='Student ID:', bg="#ffffff", fg='black', font=('Bold', 14))
    student_id_lb.pack(side='left')

    student_id_entry = tk.Entry(notify_frame, width=20, font=('Bold', 14))
    student_id_entry.pack(side='left', padx=5)

    message_lb = tk.Label(notify_frame, text='Message:', bg="#ffffff", fg='black', font=('Bold', 14))
    message_lb.pack(side='left')

    message_entry = tk.Entry(notify_frame, width=30, font=('Bold', 14))
    message_entry.pack(side='left', padx=5)

    notify_button = tk.Button(notify_frame, text='Notify', bg="#87CEEB", fg='white', font=('Bold', 14), command=lambda: notify_student_page(student_id_entry.get(), message_entry.get()))
    notify_button.pack(side='left', padx=5)

    announcement_button = tk.Button(notify_frame, text='Announcement', bg="#87CEEB", fg='white', font=('Bold', 14), command=announcement_page)
    announcement_button.pack(side='left', padx=5)

    back_button = tk.Button(inner_frame, text='Back', bg="#87CEEB", fg='white', font=('Bold', 14), command=hod_dashboard_page)
    back_button.pack(pady=10)

# Function to notify a student
def notify_student_page(student_id, message):
    connection = connect_to_database()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO notifications (student_id, message) VALUES (%s, %s)"
                cursor.execute(sql, (student_id, message))
                connection.commit()
                messagebox.showinfo("Success", "Notification sent successfully!")
        except pymysql.MySQLError as e:
            messagebox.showerror("Database Error", f"Error notifying student: {e}")
        finally:
            connection.close()

# Function to create the announcement page
def announcement_page():
    clear_frame()
    announcement_frame = tk.Frame(root, bg="#ffffff")
    announcement_frame.pack(pady=30, fill="both", expand=True)

    boundary_frame = tk.Frame(announcement_frame, bg="#ffffff", highlightbackground="#000000", highlightthickness=2)
    boundary_frame.pack(padx=1, pady=1, fill="both", expand=True)

    inner_frame = tk.Frame(boundary_frame, bg="#ffffff")
    inner_frame.pack(pady=10, fill="both", expand=True)

    heading_lb = tk.Label(inner_frame, text='Announcement', bg="#ffffff", fg="#007bff", font=('Bold', 28))
    heading_lb.pack(pady=20)

    announcement_frame = tk.Frame(inner_frame, bg="#ffffff")
    announcement_frame.pack(pady=10, fill="x")

    announcement_text = tk.Text(announcement_frame, width=50, height=10, font=('Bold', 14))
    announcement_text.pack(side='left')

    upload_button = tk.Button(announcement_frame, text='Upload PDF', bg="#87CEEB", fg='white', font=('Bold', 14), command=upload_pdf)
    upload_button.pack(side='left', padx=5)

    post_button = tk.Button(announcement_frame, text='Post', bg="#87CEEB", fg='white', font=('Bold', 14), command=lambda: post_announcement(announcement_text.get("1.0", "end-1c")))
    post_button.pack(side='left', padx=5)

    back_button = tk.Button(inner_frame, text='Back', bg="#87CEEB", fg='white', font=('Bold', 14), command=notify_students_page)
    back_button.pack(pady=10)

# Function to upload a PDF file
def upload_pdf():
    file_path = filedialog.askopenfilename(title="Select PDF File", filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        print(f"PDF file uploaded: {file_path}")

# Function to post an announcement
def post_announcement(announcement_text):
    print(f"Announcement posted: {announcement_text}")

# Function to create the mark attendance page
def mark_attendance_page():
    clear_frame()
    mark_attendance_frame = tk.Frame(root, bg="#ffffff")
    mark_attendance_frame.pack(pady=30, fill="both", expand=True)

    boundary_frame = tk.Frame(mark_attendance_frame, bg="#ffffff", highlightbackground="#000000", highlightthickness=2)
    boundary_frame.pack(padx=1, pady=1, fill="both", expand=True)

    inner_frame = tk.Frame(boundary_frame, bg="#ffffff")
    inner_frame.pack(pady=10, fill="both", expand=True)

    heading_lb = tk.Label(inner_frame, text='Mark Attendance', bg="#ffffff", fg="#007bff", font=('Bold', 28))
    heading_lb.pack(pady=20)

    class_frame = tk.Frame(inner_frame, bg="#ffffff")
    class_frame.pack(pady=10, fill='x')

    class_lb = tk.Label(class_frame, text='Class:', bg="#ffffff", fg='black', font=('Bold', 14))
    class_lb.pack(side='left')

    global class_option, subject_option, subject_menu
    class_option = tk.StringVar(inner_frame)
    class_option.set("Select Class")
    class_menu = tk.OptionMenu(class_frame, class_option, "FE_A", "FE_B", "FE_C", "SE_A", "SE_B", "TE_A", "TE_B", "BE")
    class_menu.pack(side='left', padx=5)

    subject_frame = tk.Frame(inner_frame, bg="#ffffff")
    subject_frame.pack(pady=10, fill="x")

    subject_lb = tk.Label(subject_frame, text='Subject:', bg="#ffffff", fg='black', font=('Bold', 14))
    subject_lb.pack(side='left')

    subject_option = tk.StringVar(inner_frame)
    subject_option.set("Select Subject")
    subject_menu = tk.OptionMenu(subject_frame, subject_option, "")
    subject_menu.pack(side='left', padx=5)

    date_frame = tk.Frame(inner_frame, bg="#ffffff")
    date_frame.pack(pady=10, fill="x")

    date_lb = tk.Label(date_frame, text='Date:', bg="#ffffff", fg='black', font=('Bold', 14))
    date_lb.pack(side='left')

    global month_var, year_var, day_var
    month_var = tk.StringVar()
    month_var.set("January")
    month_option = tk.OptionMenu(date_frame, month_var, "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
    month_option.pack(side='left', padx=10)

    year_var = tk.StringVar()
    year_var.set("2023")
    year_option = tk.OptionMenu(date_frame, year_var, "2022", "2023", "2024", "2025")
    year_option.pack(side='left', padx=10)

    day_var = tk.StringVar()
    day_var.set("1")
    day_option = tk.OptionMenu(date_frame, day_var, *[str(i) for i in range(1, 32)])
    day_option.pack(side='left', padx=10)

    back_button = tk.Button(inner_frame, text='Back', bg="#87CEEB", fg='white', font=('Bold', 14), command=hod_dashboard_page)
    back_button.pack(pady=10)

    student_frame = tk.Frame(inner_frame, bg="#ffffff")
    student_frame.pack(pady=10, fill="both", expand=True)

    student_lb = tk.Label(student_frame, text='Students:', bg="#ffffff", fg='black', font=('Bold', 14))
    student_lb.pack(pady=10)

    student_listbox_frame = tk.Frame(student_frame, bg="#ffffff")
    student_listbox_frame.pack(pady=10, fill="both", expand=True)

    student_canvas = tk.Canvas(student_listbox_frame, bg="#ffffff")
    student_canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(student_listbox_frame, orient="vertical", command=student_canvas.yview)
    scrollbar.pack(side="right", fill="y")

    student_canvas.configure(yscrollcommand=scrollbar.set)
    student_canvas.bind('<Configure>', lambda e: student_canvas.configure(scrollregion=student_canvas.bbox("all")))

    attendance_frame = tk.Frame(student_canvas, bg="#ffffff")
    attendance_frame.pack(pady=10, fill="both", expand=True)

    def display_students(class_name):
        for widget in attendance_frame.winfo_children():
            widget.destroy()

        connection = connect_to_database()
        if connection:
            try:
                with connection.cursor() as cursor:
                    sql = "SELECT name FROM students WHERE class = %s"
                    cursor.execute(sql, (class_name,))
                    result = cursor.fetchall()
                    for row in result:
                        student_name = row[0]
                        student_var = tk.IntVar()
                        student_cb = tk.Checkbutton(attendance_frame, text=student_name, variable=student_var, bg="#ffffff")
                        student_cb.pack(anchor='w', padx=5)
                        student_cb.name = student_name  # Store the student name in the widget's name attribute
            except pymysql.MySQLError as e:
                messagebox.showerror("Database Error", f"Error fetching student list: {e}")
            finally:
                connection.close()

    def update_attendance_list(class_name):
        display_students(class_name)

    class_option.trace_add("write", lambda *args: update_attendance_list(class_option.get()))

    submit_button = tk.Button(student_frame, text='Submit', bg="#007bff", fg='white', font=('Bold', 14), command=lambda: submit_attendance(class_option.get(), subject_option.get(), attendance_frame))
    submit_button.pack(pady=10, fill="x")

    report_button = tk.Button(student_frame, text='Report', bg="#87CEEB", fg='white', font=('Bold', 14), command=lambda: report_page(class_option.get()))
    report_button.pack(pady=10, fill="x")

    # Trace changes to class_option to update subjects
    class_option.trace("w", update_subjects)

# Function to submit attendance
def submit_attendance(class_name, subject_name, attendance_frame):
    date_str = f"{year_var.get()}-{datetime.strptime(month_var.get(), '%B').month}-{day_var.get()}"
    date = datetime.strptime(date_str, "%Y-%m-%d").date()
    connection = connect_to_database()
    if connection:
        try:
            with connection.cursor() as cursor:
                for widget in attendance_frame.winfo_children():
                    if isinstance(widget, tk.Checkbutton):
                        student_name = widget.cget("text")
                        attendance_status = 'Present' if widget.var.get() == 1 else 'Absent'
                        insert_sql = "INSERT INTO attendances (student_id, class, subject, date, attendance) VALUES (%s, %s, %s, %s, %s)"
                        cursor.execute(insert_sql, (student_name, class_name, subject_name, date, attendance_status))
                connection.commit()
        except pymysql.MySQLError as e:
            messagebox.showerror("Database Error", f"Error submitting attendance: {e}")
        finally:
            connection.close()

# Function to create the report page
def report_page(class_name):
    clear_frame()
    report_frame = tk.Frame(root, bg="#ffffff")
    report_frame.pack(pady=30, fill="both", expand=True)

    boundary_frame = tk.Frame(report_frame, bg="#ffffff", highlightbackground="#000000", highlightthickness=2)
    boundary_frame.pack(padx=1, pady=1, fill="both", expand=True)

    inner_frame = tk.Frame(boundary_frame, bg="#ffffff")
    inner_frame.pack(padx=10, pady=10, fill="both", expand=True)

    heading_lb = tk.Label(inner_frame, text='Report', bg="#ffffff", fg="#007bff", font=('Bold', 28))
    heading_lb.pack(pady=20)

    class_frame = tk.Frame(inner_frame, bg="#ffffff")
    class_frame.pack(pady=10, fill='x')

    class_lb = tk.Label(class_frame, text='Class:', bg="#ffffff", fg='black', font=('Bold', 14))
    class_lb.pack(side='left')

    class_var = tk.StringVar()
    class_var.set(class_name)
    class_option = tk.OptionMenu(class_frame, class_var, "FE_A", "FE_B", "FE_C", "SE_A", "SE_B", "TE_A", "TE_B", "BE", command=update_subjects_report)
    class_option.pack(side='left', padx=10)

    subject_frame = tk.Frame(inner_frame, bg="#ffffff")
    subject_frame.pack(pady=10, fill="x")

    subject_lb = tk.Label(subject_frame, text='Subject:', bg="#ffffff", fg='black', font=('Bold', 14))
    subject_lb.pack(side='left')

    subject_var = tk.StringVar()
    subject_var.set("Select Subject")
    subject_option = tk.OptionMenu(subject_frame, subject_var, "")
    subject_option.pack(side='left', padx=10)

    date_frame = tk.Frame(inner_frame, bg="#ffffff")
    date_frame.pack(pady=10, fill="x")

    date_lb = tk.Label(date_frame, text='Date:', bg="#ffffff", fg='black', font=('Bold', 14))
    date_lb.pack(side='left')

    month_var = tk.StringVar()
    month_var.set("January")
    month_option = tk.OptionMenu(date_frame, month_var, "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
    month_option.pack(side='left', padx=10)

    year_var = tk.StringVar()
    year_var.set("2023")
    year_option = tk.OptionMenu(date_frame, year_var, "2022", "2023", "2024", "2025")
    year_option.pack(side='left', padx=10)

    day_var = tk.StringVar()
    day_var.set("1")
    day_option = tk.OptionMenu(date_frame, day_var, *[str(i) for i in range(1, 32)])
    day_option.pack(side='left', padx=10)

    search_button = tk.Button(inner_frame, text='Search', bg="#87CEEB", fg='white', font=('Bold', 14), command=lambda: search_attendance(class_var.get(), subject_var.get(), month_var.get(), year_var.get(), day_var.get()))
    search_button.pack(pady=10)

    monthly_report_button = tk.Button(inner_frame, text='Monthly Report', bg="#87CEEB", fg='white', font=('Bold', 14), command=lambda: monthly_report_page(class_var.get(), subject_var.get(), month_var.get(), year_var.get()))
    monthly_report_button.pack(pady=10)

    back_button = tk.Button(inner_frame, text='Back', bg="#87CEEB", fg='white', font=('Bold', 14), command=lambda: back_to_dashboard(class_name))
    back_button.pack(pady=10)

    # Update subjects based on the initial class selection
    update_subjects_report(class_name)

    # Trace changes to class_option to update subjects
    class_var.trace("w", update_subjects_report)

# Function to update subjects based on the selected class for report
def update_subjects_report(class_name):
    subjects = {
        "FE_A": ["Mathematics I", "Chemistry I", "Physics I", "Mechanics", "Basic Electrical Engineering", "Programming in C"],
        "FE_B": ["Mathematics I", "Chemistry I", "Physics I", "Mechanics", "Basic Electrical Engineering", "Programming in C"],
        "FE_C": ["Mathematics I", "Chemistry I", "Physics I", "Mechanics", "Basic Electrical Engineering", "Programming in C"],
        "SE_A": ["Mathematics II", "Analysis of Algorithms", "Database Management Systems", "Design and Analysis of Algorithms", "Discrete Structures and Graph Theory", "Operating Systems"],
        "SE_B": ["Mathematics II", "Analysis of Algorithms", "Database Management Systems", "Design and Analysis of Algorithms", "Discrete Structures and Graph Theory", "Operating Systems"],
        "TE_A": ["Mathematics III", "Data Structures", "Microprocessors", "Python Programming", "Cryptography and System Security", "Machine Learning"],
        "TE_B": ["Mathematics III", "Data Structures", "Microprocessors", "Python Programming", "Cryptography and System Security", "Machine Learning"],
        "BE": ["Artificial Intelligence and Machine Learning", "Blockchain Technology", "HTML", "Data Analytics", "Mathematics IV", "Cybersecurity Fundamentals"]
    }
    subject_var.set(subjects.get(class_name, [""])[0])
    menu = subject_option['menu']
    menu.delete(0, 'end')
    for subject in subjects.get(class_name, []):
        menu.add_command(label=subject, command=tk._setit(subject_var, subject))

# Function to search attendance
def search_attendance(class_name, subject, month, year, day):
    clear_frame()
    attendance_frame = tk.Frame(root, bg="#ffffff")
    attendance_frame.pack(pady=30, fill="both", expand=True)

    boundary_frame = tk.Frame(attendance_frame, bg="#ffffff", highlightbackground="#000000", highlightthickness=2)
    boundary_frame.pack(padx=1, pady=1, fill="both", expand=True)

    inner_frame = tk.Frame(boundary_frame, bg="#ffffff")
    inner_frame.pack(padx=10, pady=10, fill="both", expand=True)

    heading_lb = tk.Label(inner_frame, text='Attendance', bg="#ffffff", fg="#007bff", font=('Bold', 28))
    heading_lb.pack(pady=20)

    attendance_tree = ttk.Treeview(inner_frame, columns=("Student", "Attendance"), show="headings")
    attendance_tree.pack(pady=10, fill="both", expand=True)

    attendance_tree.heading("Student", text="Student")
    attendance_tree.heading("Attendance", text="Attendance")

    connection = connect_to_database()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT student_id, attendance FROM attendances WHERE class = %s AND subject = %s AND date = %s"
                cursor.execute(sql, (class_name, subject, f"{year}-{month}-{day}"))
                result = cursor.fetchall()
                for row in result:
                    attendance_tree.insert("", "end", values=(row[0], row[1]))
        except pymysql.MySQLError as e:
            messagebox.showerror("Database Error", f"Error fetching attendance: {e}")
        finally:
            connection.close()

    download_button = tk.Button(inner_frame, text='Download Report', bg="#87CEEB", fg='white', font=('Bold', 14), command=lambda: download_report(class_name, subject, month, year, day))
    download_button.pack(pady=10)

    back_button = tk.Button(inner_frame, text='Back', bg="#87CEEB", fg='white', font=('Bold', 14), command=lambda: back_to_dashboard(class_name))
    back_button.pack(pady=10)

# Function to download the attendance report
def download_report(class_name, subject, month, year, day):
    date_str = f"{year}-{month}-{day}"
    date = datetime.strptime(date_str, "%Y-%m-%d").date()
    connection = connect_to_database()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT student_id, attendance FROM attendances WHERE class = %s AND subject = %s AND date = %s"
                cursor.execute(sql, (class_name, subject, date))
                result = cursor.fetchall()
                file_path = f"attendance_report_{class_name}_{subject}_{date}.csv"
                with open(file_path, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Student", "Attendance"])
                    writer.writerows(result)
                messagebox.showinfo("Download", f"Report downloaded successfully: {file_path}")
        except pymysql.MySQLError as e:
            messagebox.showerror("Database Error", f"Error fetching attendance: {e}")
        finally:
            connection.close()

# Function to create the monthly report page
def monthly_report_page(class_name, subject, month, year):
    clear_frame()
    report_frame = tk.Frame(root, bg="#ffffff")
    report_frame.pack(pady=30, fill="both", expand=True)

    boundary_frame = tk.Frame(report_frame, bg="#ffffff", highlightbackground="#000000", highlightthickness=2)
    boundary_frame.pack(padx=1, pady=1, fill="both", expand=True)

    inner_frame = tk.Frame(boundary_frame, bg="#ffffff")
    inner_frame.pack(padx=10, pady=10, fill="both", expand=True)

    heading_lb = tk.Label(inner_frame, text='Monthly Attendance', bg="#ffffff", fg="#007bff", font=('Bold', 28))
    heading_lb.pack(pady=20)

    class_frame = tk.Frame(inner_frame, bg="#ffffff")
    class_frame.pack(pady=10, fill='x')

    class_lb = tk.Label(class_frame, text='Class:', bg="#ffffff", fg='black', font=('Bold', 14))
    class_lb.pack(side='left')

    class_var = tk.StringVar()
    class_var.set(class_name)
    class_option = tk.OptionMenu(class_frame, class_var, "FE_A", "FE_B", "FE_C", "SE_A", "SE_B", "TE_A", "TE_B", "BE", command=update_subjects_report)
    class_option.pack(side='left', padx=10)

    subject_frame = tk.Frame(inner_frame, bg="#ffffff")
    subject_frame.pack(pady=10, fill="x")

    subject_lb = tk.Label(subject_frame, text='Subject:', bg="#ffffff", fg='black', font=('Bold', 14))
    subject_lb.pack(side='left')

    subject_var = tk.StringVar()
    subject_var.set(subject)
    subject_option = tk.OptionMenu(subject_frame, subject_var, "")
    subject_option.pack(side='left', padx=10)

    date_frame = tk.Frame(inner_frame, bg="#ffffff")
    date_frame.pack(pady=10, fill="x")

    date_lb = tk.Label(date_frame, text='Month:', bg="#ffffff", fg='black', font=('Bold', 14))
    date_lb.pack(side='left')

    month_var = tk.StringVar()
    month_var.set(month)
    month_option = tk.OptionMenu(date_frame, month_var, "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
    month_option.pack(side='left', padx=10)

    year_var = tk.StringVar()
    year_var.set(year)
    year_option = tk.OptionMenu(date_frame, year_var, "2022", "2023", "2024", "2025")
    year_option.pack(side='left', padx=10)

    search_button = tk.Button(inner_frame, text='Search', bg="#87CEEB", fg='white', font=('Bold', 14), command=lambda: search_monthly_attendance(class_var.get(), subject_var.get(), month_var.get(), year_var.get()))
    search_button.pack(pady=10)

    back_button = tk.Button(inner_frame, text='Back', bg="#87CEEB", fg='white', font=('Bold', 14), command=lambda: back_to_dashboard(class_name))
    back_button.pack(pady=10)

# Function to search monthly attendance
def search_monthly_attendance(class_name, subject, month, year):
    clear_frame()
    attendance_frame = tk.Frame(root, bg="#ffffff")
    attendance_frame.pack(pady=30, fill="both", expand=True)

    boundary_frame = tk.Frame(attendance_frame, bg="#ffffff", highlightbackground="#000000", highlightthickness=2)
    boundary_frame.pack(padx=1, pady=1, fill="both", expand=True)

    inner_frame = tk.Frame(boundary_frame, bg="#ffffff")
    inner_frame.pack(padx=10, pady=10, fill="both", expand=True)

    heading_lb = tk.Label(inner_frame, text='Monthly Attendance', bg="#ffffff", fg="#007bff", font=('Bold', 28))
    heading_lb.pack(pady=20)

    attendance_tree = ttk.Treeview(inner_frame, columns=("Student", "Attendance"), show="headings")
    attendance_tree.pack(pady=10, fill="both", expand=True)

    attendance_tree.heading("Student", text="Student")
    attendance_tree.heading("Attendance", text="Attendance")

    connection = connect_to_database()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT student_id, attendance FROM attendances WHERE class = %s AND subject = %s AND MONTH(date) = %s AND YEAR(date) = %s"
                cursor.execute(sql, (class_name, subject, datetime.strptime(month, '%B').month, year))
                result = cursor.fetchall()
                for row in result:
                    attendance_tree.insert("", "end", values=(row[0], row[1]))
        except pymysql.MySQLError as e:
            messagebox.showerror("Database Error", f"Error fetching attendance: {e}")
        finally:
            connection.close()

    download_button = tk.Button(inner_frame, text='Download Report', bg="#87CEEB", fg='white', font=('Bold', 14), command=lambda: download_monthly_report(class_name, subject, month, year))
    download_button.pack(pady=10)

    back_button = tk.Button(inner_frame, text='Back', bg="#87CEEB", fg='white', font=('Bold', 14), command=lambda: monthly_report_page(class_name, subject, month, year))
    back_button.pack(pady=10)

# Function to download the monthly attendance report
def download_monthly_report(class_name, subject, month, year):
    connection = connect_to_database()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT student_id, attendance FROM attendances WHERE class = %s AND subject = %s AND MONTH(date) = %s AND YEAR(date) = %s"
                cursor.execute(sql, (class_name, subject, datetime.strptime(month, '%B').month, year))
                result = cursor.fetchall()
                file_path = f"monthly_attendance_report_{class_name}_{subject}_{month}_{year}.csv"
                with open(file_path, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Student", "Attendance"])
                    writer.writerows(result)
                messagebox.showinfo("Download", f"Monthly report downloaded successfully: {file_path}")
        except pymysql.MySQLError as e:
            messagebox.showerror("Database Error", f"Error fetching attendance: {e}")
        finally:
            connection.close()

# Function to navigate back to the dashboard
def back_to_dashboard(class_name=None):
    if class_name:
        report_page(class_name)
    else:
        hod_dashboard_page()

# Function to create the view student details page
def view_student_details_page():
    clear_frame()
    view_student_details_frame = tk.Frame(root, bg="#ffffff")
    view_student_details_frame.pack(pady=30, fill="both", expand=True)

    boundary_frame = tk.Frame(view_student_details_frame, bg="#ffffff", highlightbackground="#000000", highlightthickness=2)
    boundary_frame.pack(padx=1, pady=1, fill="both", expand=True)

    inner_frame = tk.Frame(boundary_frame, bg="#ffffff")
    inner_frame.pack(padx=10, pady=10, fill="both", expand=True)

    heading_lb = tk.Label(inner_frame, text='View Student Details', bg="#ffffff", fg="#007bff", font=('Bold', 28))
    heading_lb.pack(pady=20)

    class_frame = tk.Frame(inner_frame, bg="#ffffff")
    class_frame.pack(pady=10, fill='x')

    class_lb = tk.Label(class_frame, text='Class:', bg="#ffffff", fg='black', font=('Bold', 14))
    class_lb.pack(side='left')

    class_var = tk.StringVar()
    class_var.set("Select Class")
    class_option = tk.OptionMenu(class_frame, class_var, "FE_A", "FE_B", "FE_C", "SE_A", "SE_B", "TE_A", "TE_B", "BE", command=lambda x: display_student_details(x))
    class_option.pack(side='left', padx=10)

    student_details_frame = tk.Frame(inner_frame, bg="#ffffff")
    student_details_frame.pack(pady=10, fill="both", expand=True)

    student_details_tree = ttk.Treeview(student_details_frame, columns=("Photo", "Full Name", "Contact No.", "Email", "Gender", "Age"), show="headings")
    student_details_tree.pack(pady=10, fill="both", expand=True)

    student_details_tree.heading("Photo", text="Photo")
    student_details_tree.heading("Full Name", text="Full Name")
    student_details_tree.heading("Contact No.", text="Contact No.")
    student_details_tree.heading("Email", text="Email")
    student_details_tree.heading("Gender", text="Gender")
    student_details_tree.heading("Age", text="Age")

    def display_student_details(class_name):
        student_details_tree.delete(*student_details_tree.get_children())
        connection = connect_to_database()
        if connection:
            try:
                with connection.cursor() as cursor:
                    sql = "SELECT * FROM students WHERE class = %s"
                    cursor.execute(sql, (class_name,))
                    result = cursor.fetchall()
                    for row in result:
                        student_details_tree.insert("", "end", values=("Photo", row[1], row[4], row[6], row[2], row[3]))
            except pymysql.MySQLError as e:
                messagebox.showerror("Database Error", f"Error fetching student details: {e}")
            finally:
                connection.close()

    back_button = tk.Button(inner_frame, text='Back', bg="#87CEEB", fg='white', font=('Bold', 14), command=lambda: [messagebox.showinfo("Back", "You are going back to the dashboard"), hod_dashboard_page()])
    back_button.pack(pady=10)

# Function to create the upload page
def upload_page(upload_type):
    clear_frame()
    upload_frame = tk.Frame(root, bg="#ffffff")
    upload_frame.pack(pady=30, fill="both", expand=True)

    boundary_frame = tk.Frame(upload_frame, bg="#ffffff", highlightbackground="#000000", highlightthickness=2)
    boundary_frame.pack(padx=1, pady=1, fill="both", expand=True)

    inner_frame = tk.Frame(boundary_frame, bg="#ffffff")
    inner_frame.pack(padx=10, pady=10, fill="both", expand=True)

    heading_lb = tk.Label(inner_frame, text=f'Upload {upload_type}', bg="#ffffff", fg="#007bff", font=('Bold', 28))
    heading_lb.pack(pady=20)

    class_frame = tk.Frame(inner_frame, bg="#ffffff")
    class_frame.pack(pady=10, fill='x')

    class_lb = tk.Label(class_frame, text='Class:', bg="#ffffff", fg='black', font=('Bold', 14))
    class_lb.pack(side='left')

    global class_option, subject_option, subject_menu
    class_option = tk.StringVar(inner_frame)
    class_option.set("Select Class")
    class_menu = tk.OptionMenu(class_frame, class_option, "FE_A", "FE_B", "FE_C", "SE_A", "SE_B", "TE_A", "TE_B", "BE")
    class_menu.pack(side='left', padx=5)

    subject_frame = tk.Frame(inner_frame, bg="#ffffff")
    subject_frame.pack(pady=10, fill="x")

    subject_lb = tk.Label(subject_frame, text='Subject:', bg="#ffffff", fg='black', font=('Bold', 14))
    subject_lb.pack(side='left')

    subject_option = tk.StringVar(inner_frame)
    subject_option.set("Select Subject")
    subject_menu = tk.OptionMenu(subject_frame, subject_option, "")
    subject_menu.pack(side='left', padx=5)

    date_frame = tk.Frame(inner_frame, bg="#ffffff")
    date_frame.pack(pady=10, fill="x")

    date_lb = tk.Label(date_frame, text='Date:', bg="#ffffff", fg='black', font=('Bold', 14))
    date_lb.pack(side='left')

    month_var = tk.StringVar()
    month_var.set("January")
    month_option = tk.OptionMenu(date_frame, month_var, "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
    month_option.pack(side='left', padx=10)

    year_var = tk.StringVar()
    year_var.set("2023")
    year_option = tk.OptionMenu(date_frame, year_var, "2022", "2023", "2024", "2025")
    year_option.pack(side='left', padx=10)

    day_var = tk.StringVar()
    day_var.set("1")
    day_option = tk.OptionMenu(date_frame, day_var, *[str(i) for i in range(1, 32)])
    day_option.pack(side='left', padx=10)

    notes_file_frame = tk.Frame(inner_frame, bg="#ffffff")
    notes_file_frame.pack(pady=10, fill="x")

    notes_file_lb = tk.Label(notes_file_frame, text='Select File:', bg="#ffffff", fg='black', font=('Bold', 14))
    notes_file_lb.pack(side='left')

    notes_file_entry = tk.Entry(notes_file_frame, width=50, font=('Bold', 14))
    notes_file_entry.pack(side='left', padx=5)

    browse_button = tk.Button(notes_file_frame, text='Browse', bg="#87CEEB", fg='white', font=('Bold', 14), command=lambda: browse_file(notes_file_entry))
    browse_button.pack(side='left', padx=5)

    upload_button = tk.Button(inner_frame, text='Upload', bg="#87CEEB", fg='white', font=('Bold', 14), command=lambda: upload_file(notes_file_entry.get(), class_option.get(), subject_option.get(), month_var.get(), year_var.get(), day_var.get(), upload_type))
    upload_button.pack(pady=10)

    back_button = tk.Button(inner_frame, text='Back', bg="#87CEEB", fg='white', font=('Bold', 14), command=hod_dashboard_page)
    back_button.pack(pady=10)

    # Trace changes to class_option to update subjects
    class_option.trace("w", update_subjects)

# Function to browse and select a file
def browse_file(entry):
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf"), ("PPT Files", "*.ppt"), ("PNG Files", "*.png")])
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)

# Function to upload a file
def upload_file(file_path, class_name, subject_name, month, year, day, upload_type):
    print(f"Upload button clicked. File path: {file_path}")  # Debugging statement
    if file_path and file_path.lower().endswith(('.pdf', '.ppt', '.png')):
        print(f"Uploading {upload_type} from: {file_path}")

        # Read the file as binary data
        try:
            with open(file_path, 'rb') as file:
                binary_data = file.read()
            if binary_data:
                save_upload_to_database(binary_data, class_name, subject_name, month, year, day, upload_type)
                messagebox.showinfo("Success", f"{upload_type} uploaded successfully!")
                notify_students(class_name, subject_name, upload_type)
        except Exception as e:
            messagebox.showerror("Error", f"Error reading file: {e}")
    else:
        messagebox.showerror("Error", "Only PDF, PPT, and PNG files are allowed.")

# Function to notify students about the upload
def notify_students(class_name, subject_name, upload_type):
    connection = connect_to_database()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT student_id FROM students WHERE class = %s"
                cursor.execute(sql, (class_name,))
                students = cursor.fetchall()
                for student in students:
                    student_id = student[0]
                    notification_message = f"New {upload_type} uploaded for {subject_name}."
                    insert_sql = "INSERT INTO notifications (student_id, message) VALUES (%s, %s)"
                    cursor.execute(insert_sql, (student_id, notification_message))
                connection.commit()
        except pymysql.MySQLError as e:
            messagebox.showerror("Database Error", f"Error notifying students: {e}")
        finally:
            connection.close()

# Function to save the uploaded file to the database
def save_upload_to_database(binary_data, class_name, subject_name, month, year, day, upload_type):
    connection = connect_to_database()
    if connection:
        try:
            # Map month name to month number
            month_map = {
                "January": "01", "February": "02", "March": "03", "April": "04",
                "May": "05", "June": "06", "July": "07", "August": "08",
                "September": "09", "October": "10", "November": "11", "December": "12"
            }
            month_number = month_map.get(month, "01")  # Default to January if month is not found
            # Format the date as YYYY-MM-DD
            upload_date = f"{year}-{month_number}-{day}"

            with connection.cursor() as cursor:
                sql = """
                INSERT INTO uploads (file_data, class_name, subject_name, upload_date, upload_type)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (binary_data, class_name, subject_name, upload_date, upload_type))
                connection.commit()
            messagebox.showinfo("Success", f"{upload_type} saved to database successfully!")
        except pymysql.MySQLError as e:
            messagebox.showerror("Database Error", f"Error saving {upload_type} to database: {e}")
        finally:
            connection.close()

def view_staff_details_page():
    clear_frame()
    view_staff_details_frame = tk.Frame(root, bg="#ffffff")
    view_staff_details_frame.pack(pady=30, fill="both", expand=True)

    boundary_frame = tk.Frame(view_staff_details_frame, bg="#ffffff", highlightbackground="#000000", highlightthickness=2)
    boundary_frame.pack(padx=1, pady=1, fill="both", expand=True)

    inner_frame = tk.Frame(boundary_frame, bg="#ffffff")
    inner_frame.pack(padx=10, pady=10, fill="both", expand=True)

    heading_lb = tk.Label(inner_frame, text='View Staff Details', bg="#ffffff", fg="#007bff", font=('Bold', 28))
    heading_lb.pack(pady=20)

    staff_frame = tk.Frame(inner_frame, bg="#ffffff")
    staff_frame.pack(pady=10, fill="x")

    staff_lb = tk.Label(staff_frame, text='Staff ID:', bg="#ffffff", fg='black', font=('Bold', 14))
    staff_lb.pack(side="left", padx=10)

    staff_entry = tk.Entry(staff_frame, font=('Bold', 14), width=20)
    staff_entry.pack(side="left", padx=10)

    search_button = tk.Button(staff_frame, text='Search', bg="#87CEEB", fg='white', font=('Bold', 14), command=lambda: search_staff_details(staff_entry.get()))
    search_button.pack(side="left", padx=10)

    def search_staff_details(staff_id):
        connection = connect_to_database()
        if connection:
            try:
                with connection.cursor() as cursor:
                    sql = "SELECT * FROM staff WHERE staff_id = %s"
                    cursor.execute(sql, (staff_id,))
                    result = cursor.fetchone()
                    if result:
                        messagebox.showinfo("Staff Details", f"Name: {result[1]}\nDesignation: {result[3]}\nContact: {result[4]}\nEmail: {result[5]}")
                    else:
                        messagebox.showerror("Error", "Staff ID not found")
            except pymysql.MySQLError as e:
                messagebox.showerror("Database Error", f"Error fetching staff details: {e}")
            finally:
                connection.close()

    back_button = tk.Button(inner_frame, text='Back', bg="#87CEEB", fg='white', font=('Bold', 14), command=lambda: [messagebox.showinfo("Back", "You are going back to the dashboard"), hod_dashboard_page()])
    back_button.pack(pady=10)


# Function to create the generate assignment links page
def generate_assignment_links_page():
    clear_frame()
    generate_assignment_links_frame = tk.Frame(root, bg="#ffffff")
    generate_assignment_links_frame.pack(pady=30, fill="both", expand=True)

    boundary_frame = tk.Frame(generate_assignment_links_frame, bg="#ffffff", highlightbackground="#000000", highlightthickness=2)
    boundary_frame.pack(padx=1, pady=1, fill="both", expand=True)

    inner_frame = tk.Frame(boundary_frame, bg="#ffffff")
    inner_frame.pack(padx=10, pady=10, fill="both", expand=True)

    heading_lb = tk.Label(inner_frame, text='Generate Assignment Links', bg="#ffffff", fg="#007bff", font=('Bold', 28))
    heading_lb.pack(pady=20)

    class_frame = tk.Frame(inner_frame, bg="#ffffff")
    class_frame.pack(pady=10, fill='x')

    class_lb = tk.Label(class_frame, text='Class:', bg="#ffffff", fg='black', font=('Bold', 14))
    class_lb.pack(side='left')

    global class_option, subject_option, subject_menu
    class_option = tk.StringVar(inner_frame)
    class_option.set("Select Class")
    class_menu = tk.OptionMenu(class_frame, class_option, "FE_A", "FE_B", "FE_C", "SE_A", "SE_B", "TE_A", "TE_B", "BE")
    class_menu.pack(side='left', padx=5)

    subject_frame = tk.Frame(inner_frame, bg="#ffffff")
    subject_frame.pack(pady=10, fill="x")

    subject_lb = tk.Label(subject_frame, text='Subject:', bg="#ffffff", fg='black', font=('Bold', 14))
    subject_lb.pack(side='left')

    subject_option = tk.StringVar(inner_frame)
    subject_option.set("Select Subject")
    subject_menu = tk.OptionMenu(subject_frame, subject_option, "")
    subject_menu.pack(side='left', padx=5)

    assignment_name_frame = tk.Frame(inner_frame, bg="#ffffff")
    assignment_name_frame.pack(pady=10, fill="x")

    assignment_name_lb = tk.Label(assignment_name_frame, text='Assignment Name:', bg="#ffffff", fg='black', font=('Bold', 14))
    assignment_name_lb.pack(side='left')

    assignment_name_entry = tk.Entry(assignment_name_frame, width=50, font=('Bold', 14))
    assignment_name_entry.pack(side='left', padx=5)

    generate_link_button = tk.Button(inner_frame, text='Generate Link', bg="#87CEEB", fg='white', font=('Bold', 14), command=lambda: generate_link(class_option.get(), subject_option.get(), assignment_name_entry.get()))
    generate_link_button.pack(pady=10, fill="x")

    back_button = tk.Button(inner_frame, text='Back', bg="#87CEEB", fg='white', font=('Bold', 14), command=hod_dashboard_page)
    back_button.pack(pady=10)

    links_listbox_frame = tk.Frame(inner_frame, bg="#ffffff")
    links_listbox_frame.pack(pady=10, fill="both", expand=True)

    global links_listbox
    links_listbox = tk.Listbox(links_listbox_frame, font=('Bold', 14), width=50)
    links_listbox.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(links_listbox_frame)
    scrollbar.pack(side="right", fill="y")

    links_listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=links_listbox.yview)

    load_links()

    # Trace changes to class_option to update subjects
    class_option.trace("w", update_subjects)

# Function to generate a link and save it to the database
def generate_link(class_name, subject_name, assignment_name):
    if class_name == "Select Class" or subject_name == "Select Subject" or not assignment_name:
        messagebox.showwarning("Input Error", "Please select a class, subject, and enter an assignment name.")
        return
    link = generate_unique_link(class_name, subject_name, assignment_name)
    save_link_to_database(class_name, subject_name, assignment_name, link)
    links_listbox.insert(tk.END, link)
    messagebox.showinfo("Success", f"Link generated: {link}")

# Function to generate a unique link
def generate_unique_link(class_name, subject_name, assignment_name):
    return f"http://campusconnect.com/assignment/{uuid.uuid4()}"

# Function to save the generated link to the database
def save_link_to_database(class_name, subject_name, assignment_name, link):
    connection = connect_to_database()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO assignment_links (class_name, subject_name, assignment_name, link) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (class_name, subject_name, assignment_name, link))
                connection.commit()
        except pymysql.MySQLError as e:
            messagebox.showerror("Database Error", f"Error saving link to database: {e}")
        finally:
            connection.close()

# Function to load links from the database
def load_links():
    connection = connect_to_database()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT link FROM assignment_links"
                cursor.execute(sql)
                links = cursor.fetchall()
                for (link,) in links:
                    links_listbox.insert(tk.END, link)
        except pymysql.MySQLError as e:
            messagebox.showerror("Database Error", f"Error loading links: {e}")
        finally:
            connection.close()


# Function to create the login staff page
def login_staff_page():
    clear_frame()
    login_staff_frame = tk.Frame(root, bg="#ffffff")
    login_staff_frame.pack(pady=30, fill="both", expand=True)

    login_staff_image = Image.open("C:\\Users\\Ashis\\OneDrive\\Desktop\\BG\\login.png")  # Update with your image path
    login_staff_image = login_staff_image.resize((400, 400))
    login_staff_image = ImageTk.PhotoImage(login_staff_image)

    login_staff_label = tk.Label(login_staff_frame, image=login_staff_image, bg="#ffffff")
    login_staff_label.image = login_staff_image
    login_staff_label.pack()

    login_staff_heading_lb = tk.Label(login_staff_frame, text='LOGIN STAFF', bg="#ffffff", fg="#007bff", font=('Bold', 28))
    login_staff_heading_lb.pack(pady=10)

    staff_id_frame = tk.Frame(login_staff_frame, bg="#ffffff")
    staff_id_frame.pack(pady=5, fill='x')

    staff_id_lb = tk.Label(staff_id_frame, text='Staff ID Number:', bg="#ffffff", fg='black', font=('Bold', 20))
    staff_id_lb.pack(side='left')

    staff_id_entry = tk.Entry(staff_id_frame, width=20, font=('Bold', 20))
    staff_id_entry.pack(side='left', padx=5)

    staff_password_frame = tk.Frame(login_staff_frame, bg="#ffffff")
    staff_password_frame.pack(pady=5, fill='x')

    staff_password_lb = tk.Label(staff_password_frame, text='Staff Password:', bg="#ffffff", fg='black', font=('Bold', 20))
    staff_password_lb.pack(side='left')

    staff_password_entry = tk.Entry(staff_password_frame, show='*', width=20, font=('Bold', 20))
    staff_password_entry.pack(side='left', padx=5)

    button_frame = tk.Frame(login_staff_frame, bg="#ffffff")
    button_frame.pack(pady=10)

    def login():
        global staff_id
        staff_id = staff_id_entry.get().strip()
        staff_password = staff_password_entry.get().strip()
        connection = connect_to_database()
        if connection:
            try:
                with connection.cursor() as cursor:
                    sql = "SELECT * FROM staff WHERE staff_id = %s AND password = %s"
                    cursor.execute(sql, (staff_id, staff_password))
                    result = cursor.fetchone()
                    if result:
                        print("Login successful!")
                        login_staff_frame.destroy()
                        staff_dashboard_page()
                    else:
                        print("Invalid Staff ID or Password")
                        messagebox.showerror("Error", "Invalid Staff ID or Password")
            except pymysql.MySQLError as e:
                messagebox.showerror("Database Error", f"Error logging in: {e}")
            finally:
                connection.close()

    login_button = tk.Button(button_frame, text='Login', bg="#87CEEB", fg='white', font=('Bold', 14), command=login)
    login_button.pack(side='left', padx=5)

    forgot_password_button = tk.Button(button_frame, text='Forgot Password', bg="#87CEEB", fg='white', font=('Bold', 14), command=forgot_password_page)
    forgot_password_button.pack(side='left', padx=5)

    home_button_staff = tk.Button(login_staff_frame, text='Home', bg="#87CEEB", fg='white', font=('Bold', 10), command=welcome_page)
    home_button_staff.pack(pady=10)

# Function to create the forgot password page for staff
def forgot_password_page():
    clear_frame()
    forgot_password_frame = tk.Frame(root, bg="#ffffff")
    forgot_password_frame.pack(pady=30, fill="both", expand=True)

    forgot_password_label = tk.Label(forgot_password_frame, text='Forgot Password', bg="#ffffff", fg="#007bff", font=('Bold', 28))
    forgot_password_label.pack(pady=20)

    staff_id_frame = tk.Frame(forgot_password_frame, bg="#ffffff")
    staff_id_frame.pack(pady=5, fill='x')

    staff_id_lb = tk.Label(staff_id_frame, text='Staff ID Number:', bg="#ffffff", fg='black', font=('Bold', 20))
    staff_id_lb.pack(side='left')

    staff_id_entry = tk.Entry(staff_id_frame, width=20, font=('Bold', 20))
    staff_id_entry.pack(side='left', padx=5)

    staff_email_frame = tk.Frame(forgot_password_frame, bg="#ffffff")
    staff_email_frame.pack(pady=5, fill='x')

    staff_email_lb = tk.Label(staff_email_frame, text='Staff Email:', bg="#ffffff", fg='black', font=('Bold', 20))
    staff_email_lb.pack(side='left')

    staff_email_entry = tk.Entry(staff_email_frame, width=20, font=('Bold', 20))
    staff_email_entry.pack(side='left', padx=5)

    button_frame = tk.Frame(forgot_password_frame, bg="#ffffff")
    button_frame.pack(pady=10)

    def reset_password():
        staff_id = staff_id_entry.get().strip()
        staff_email = staff_email_entry.get().strip()
        connection = connect_to_database()
        if connection:
            try:
                with connection.cursor() as cursor:
                    sql = "SELECT * FROM staff WHERE staff_id = %s AND email = %s"
                    cursor.execute(sql, (staff_id, staff_email))
                    result = cursor.fetchone()
                    if result:
                        new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
                        update_sql = "UPDATE staff SET password = %s WHERE staff_id = %s"
                        cursor.execute(update_sql, (new_password, staff_id))
                        connection.commit()

                        # Send email with the new password
                        msg = MIMEMultipart()
                        msg['From'] = 'campusconnect@example.com'
                        msg['To'] = staff_email
                        msg['Subject'] = 'Password Reset'
                        body = f'Your new password is: {new_password}'
                        msg.attach(MIMEText(body, 'plain'))

                        server = smtplib.SMTP('smtp.example.com', 587)
                        server.starttls()
                        server.login('campusconnect@example.com', 'your_password')
                        text = msg.as_string()
                        server.sendmail('campusconnect@example.com', staff_email, text)
                        server.quit()

                        messagebox.showinfo("Success", "A new password has been sent to your email.")
                    else:
                        messagebox.showerror("Error", "Invalid Staff ID or Email")
            except pymysql.MySQLError as e:
                messagebox.showerror("Database Error", f"Error resetting password: {e}")
            finally:
                connection.close()

    reset_password_button = tk.Button(button_frame, text='Reset Password', bg="#87CEEB", fg='white', font=('Bold', 14), command=reset_password)
    reset_password_button.pack(side='left', padx=5)

    back_button = tk.Button(button_frame, text='Back', bg="#87CEEB", fg='white', font=('Bold', 14), command=login_staff_page)
    back_button.pack(side='left', padx=5)

# Function to create the staff dashboard page
def staff_dashboard_page():
    clear_frame()
    dashboard_frame = tk.Frame(root, bg="#ffffff")
    dashboard_frame.pack(pady=30, fill="both", expand=True)

    boundary_frame = tk.Frame(dashboard_frame, bg="#ffffff", highlightbackground="#000000", highlightthickness=2)
    boundary_frame.pack(padx=1, pady=1, fill="both", expand=True)

    inner_frame = tk.Frame(boundary_frame, bg="#ffffff")
    inner_frame.pack(padx=10, pady=10, fill="both", expand=True)

    logo_frame = tk.Frame(inner_frame, bg="#ffffff")
    logo_frame.place(relx=0.5, rely=0.5, anchor="center")

    logo_image = Image.open("C:\\Users\\Ashis\\OneDrive\\Desktop\\BG\\Campusconnect.png")  # Update with your logo path
    logo_image = logo_image.resize((800, 800))
    logo_image = ImageTk.PhotoImage(logo_image)

    logo_label = tk.Label(logo_frame, image=logo_image, bg="#ffffff")
    logo_label.image = logo_image
    logo_label.pack()

    heading_lb = tk.Label(logo_frame, text='Staff Dashboard', bg="#ffffff", fg="#007bff", font=('Bold', 32))
    heading_lb.place(relx=0.5, rely=0.15, anchor="center")

    left_button_frame = tk.Frame(inner_frame, bg="#ffffff")
    left_button_frame.place(x=10, rely=0.5, anchor="w")

    notify_students_button = tk.Button(left_button_frame, text='Notify Students', bg="#ADD8E6", fg='black', font=('Bold', 14), command=notify_students_page)
    notify_students_button.pack(pady=10, fill="x")

    view_student_details_button = tk.Button(left_button_frame, text='View Student Details', bg="#ADD8E6", fg='black', font=('Bold', 14), command=view_student_details_page)
    view_student_details_button.pack(pady=10, fill="x")

    mark_attendance_button = tk.Button(left_button_frame, text='Mark Attendance', bg="#ADD8E6", fg='black', font=('Bold', 14), command=mark_attendance_page)
    mark_attendance_button.pack(pady=10, fill="x")

    upload_notes_button = tk.Button(left_button_frame, text='Upload Notes', bg="#ADD8E6", fg='black', font=('Bold', 14), command=lambda: upload_page("Notes"))
    upload_notes_button.pack(pady=10, fill="x")

    upload_results_button = tk.Button(left_button_frame, text='Upload Results', bg="#ADD8E6", fg='black', font=('Bold', 14), command=lambda: upload_page("Results"))
    upload_results_button.pack(pady=10, fill="x")

    generate_assignment_links_button = tk.Button(left_button_frame, text='Generate Assignment Links', bg="#ADD8E6", fg='black', font=('Bold', 14), command=generate_assignment_links_page)
    generate_assignment_links_button.pack(pady=10, fill="x")

    home_button_dashboard = tk.Button(inner_frame, text='Home', bg="#87CEEB", fg='white', font=('Bold', 10), command=staff_dashboard_page)
    home_button_dashboard.place(relx=0.95, rely=0.95, anchor="se")

    notification_frame = tk.Frame(inner_frame, bg="#ffffff", highlightbackground="#000000", highlightthickness=1)
    notification_frame.place(relx=0.95, rely=0.05, anchor="ne")

    notification_label = tk.Label(notification_frame, text='Notifications', bg="#ffffff", fg="#007bff", font=('Bold', 14))
    notification_label.pack()

    notification_text = tk.Text(notification_frame, width=30, height=5, font=('Bold', 12), state='disabled')
    notification_text.pack()

    def update_notifications(message):
        notification_text.config(state='normal')
        notification_text.insert(tk.END, message + '\n')
        notification_text.config(state='disabled')

    update_notifications("New announcement from HOD: Staff meeting at 3 PM.")

# Function to create the notify students page
def notify_students_page():
    clear_frame()
    notify_students_frame = tk.Frame(root, bg="#ffffff")
    notify_students_frame.pack(pady=30, fill="both", expand=True)

    boundary_frame = tk.Frame(notify_students_frame, bg="#ffffff", highlightbackground="#000000", highlightthickness=2)
    boundary_frame.pack(padx=1, pady=1, fill="both", expand=True)

    inner_frame = tk.Frame(boundary_frame, bg="#ffffff")
    inner_frame.pack(pady=10, fill="both", expand=True)

    heading_lb = tk.Label(inner_frame, text='Notify Students', bg="#ffffff", fg="#007bff", font=('Bold', 28))
    heading_lb.pack(pady=20)

    notify_frame = tk.Frame(inner_frame, bg="#ffffff")
    notify_frame.pack(pady=10, fill="x")

    student_id_lb = tk.Label(notify_frame, text='Student ID:', bg="#ffffff", fg='black', font=('Bold', 14))
    student_id_lb.pack(side='left')

    student_id_entry = tk.Entry(notify_frame, width=20, font=('Bold', 14))
    student_id_entry.pack(side='left', padx=5)

    message_lb = tk.Label(notify_frame, text='Message:', bg="#ffffff", fg='black', font=('Bold', 14))
    message_lb.pack(side='left')

    message_entry = tk.Entry(notify_frame, width=30, font=('Bold', 14))
    message_entry.pack(side='left', padx=5)

    notify_button = tk.Button(notify_frame, text='Notify', bg="#87CEEB", fg='white', font=('Bold', 14), command=lambda: notify_student_page(student_id_entry.get(), message_entry.get()))
    notify_button.pack(side='left', padx=5)

    announcement_button = tk.Button(notify_frame, text='Announcement', bg="#87CEEB", fg='white', font=('Bold', 14), command=announcement_page)
    announcement_button.pack(side='left', padx=5)

    back_button = tk.Button(inner_frame, text='Back', bg="#87CEEB", fg='white', font=('Bold', 14), command=staff_dashboard_page)
    back_button.pack(pady=10)

# Function to notify a student
def notify_student_page(student_id, message):
    connection = connect_to_database()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO notifications (student_id, message) VALUES (%s, %s)"
                cursor.execute(sql, (student_id, message))
                connection.commit()
                messagebox.showinfo("Success", "Notification sent successfully!")
        except pymysql.MySQLError as e:
            messagebox.showerror("Database Error", f"Error notifying student: {e}")
        finally:
            connection.close()

# Function to create the announcement page
def announcement_page():
    clear_frame()
    announcement_frame = tk.Frame(root, bg="#ffffff")
    announcement_frame.pack(pady=30, fill="both", expand=True)

    boundary_frame = tk.Frame(announcement_frame, bg="#ffffff", highlightbackground="#000000", highlightthickness=2)
    boundary_frame.pack(padx=1, pady=1, fill="both", expand=True)

    inner_frame = tk.Frame(boundary_frame, bg="#ffffff")
    inner_frame.pack(pady=10, fill="both", expand=True)

    heading_lb = tk.Label(inner_frame, text='Announcement', bg="#ffffff", fg="#007bff", font=('Bold', 28))
    heading_lb.pack(pady=20)

    announcement_frame = tk.Frame(inner_frame, bg="#ffffff")
    announcement_frame.pack(pady=10, fill="x")

    announcement_text = tk.Text(announcement_frame, width=50, height=10, font=('Bold', 14))
    announcement_text.pack(side='left')

    upload_button = tk.Button(announcement_frame, text='Upload PDF', bg="#87CEEB", fg='white', font=('Bold', 14), command=upload_pdf)
    upload_button.pack(side='left', padx=5)

    post_button = tk.Button(announcement_frame, text='Post', bg="#87CEEB", fg='white', font=('Bold', 14), command=lambda: post_announcement(announcement_text.get("1.0", "end-1c")))
    post_button.pack(side='left', padx=5)

    back_button = tk.Button(inner_frame, text='Back', bg="#87CEEB", fg='white', font=('Bold', 14), command=notify_students_page)
    back_button.pack(pady=10)

# Function to upload a PDF file
def upload_pdf():
    file_path = filedialog.askopenfilename(title="Select PDF File", filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        print(f"PDF file uploaded: {file_path}")

# Function to post an announcement
def post_announcement(announcement_text):
    print(f"Announcement posted: {announcement_text}")

# Function to create the mark attendance page
def mark_attendance_page():
    clear_frame()
    mark_attendance_frame = tk.Frame(root, bg="#ffffff")
    mark_attendance_frame.pack(pady=30, fill="both", expand=True)

    boundary_frame = tk.Frame(mark_attendance_frame, bg="#ffffff", highlightbackground="#000000", highlightthickness=2)
    boundary_frame.pack(padx=1, pady=1, fill="both", expand=True)

    inner_frame = tk.Frame(boundary_frame, bg="#ffffff")
    inner_frame.pack(pady=10, fill="both", expand=True)

    heading_lb = tk.Label(inner_frame, text='Mark Attendance', bg="#ffffff", fg="#007bff", font=('Bold', 28))
    heading_lb.pack(pady=20)

    class_frame = tk.Frame(inner_frame, bg="#ffffff")
    class_frame.pack(pady=10, fill='x')

    class_lb = tk.Label(class_frame, text='Class:', bg="#ffffff", fg='black', font=('Bold', 14))
    class_lb.pack(side='left')

    global class_option, subject_option, subject_menu
    class_option = tk.StringVar(inner_frame)
    class_option.set("Select Class")
    class_menu = tk.OptionMenu(class_frame, class_option, "FE_A", "FE_B", "FE_C", "SE_A", "SE_B", "TE_A", "TE_B", "BE")
    class_menu.pack(side='left', padx=5)

    subject_frame = tk.Frame(inner_frame, bg="#ffffff")
    subject_frame.pack(pady=10, fill="x")

    subject_lb = tk.Label(subject_frame, text='Subject:', bg="#ffffff", fg='black', font=('Bold', 14))
    subject_lb.pack(side='left')

    subject_option = tk.StringVar(inner_frame)
    subject_option.set("Select Subject")
    subject_menu = tk.OptionMenu(subject_frame, subject_option, "")
    subject_menu.pack(side='left', padx=5)

    date_frame = tk.Frame(inner_frame, bg="#ffffff")
    date_frame.pack(pady=10, fill="x")

    date_lb = tk.Label(date_frame, text='Date:', bg="#ffffff", fg='black', font=('Bold', 14))
    date_lb.pack(side='left')

    global month_var, year_var, day_var
    month_var = tk.StringVar()
    month_var.set("January")
    month_option = tk.OptionMenu(date_frame, month_var, "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
    month_option.pack(side='left', padx=10)

    year_var = tk.StringVar()
    year_var.set("2023")
    year_option = tk.OptionMenu(date_frame, year_var, "2022", "2023", "2024", "2025")
    year_option.pack(side='left', padx=10)

    day_var = tk.StringVar()
    day_var.set("1")
    day_option = tk.OptionMenu(date_frame, day_var, *[str(i) for i in range(1, 32)])
    day_option.pack(side='left', padx=10)

    back_button = tk.Button(inner_frame, text='Back', bg="#87CEEB", fg='white', font=('Bold', 14), command=staff_dashboard_page)
    back_button.pack(pady=10)

    student_frame = tk.Frame(inner_frame, bg="#ffffff")
    student_frame.pack(pady=10, fill="both", expand=True)

    student_lb = tk.Label(student_frame, text='Students:', bg="#ffffff", fg='black', font=('Bold', 14))
    student_lb.pack(pady=10)

    student_listbox_frame = tk.Frame(student_frame, bg="#ffffff")
    student_listbox_frame.pack(pady=10, fill="both", expand=True)

    student_canvas = tk.Canvas(student_listbox_frame, bg="#ffffff")
    student_canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(student_listbox_frame, orient="vertical", command=student_canvas.yview)
    scrollbar.pack(side="right", fill="y")

    student_canvas.configure(yscrollcommand=scrollbar.set)
    student_canvas.bind('<Configure>', lambda e: student_canvas.configure(scrollregion=student_canvas.bbox("all")))

    attendance_frame = tk.Frame(student_canvas, bg="#ffffff")
    attendance_frame.pack(pady=10, fill="both", expand=True)

    def display_students(class_name):
        for widget in attendance_frame.winfo_children():
            widget.destroy()

        connection = connect_to_database()
        if connection:
            try:
                with connection.cursor() as cursor:
                    sql = "SELECT name FROM students WHERE class = %s"
                    cursor.execute(sql, (class_name,))
                    result = cursor.fetchall()
                    for row in result:
                        student_name = row[0]
                        student_var = tk.IntVar()
                        student_cb = tk.Checkbutton(attendance_frame, text=student_name, variable=student_var, bg="#ffffff")
                        student_cb.pack(anchor='w', padx=5)
                        student_cb.name = student_name  # Store the student name in the widget's name attribute
            except pymysql.MySQLError as e:
                messagebox.showerror("Database Error", f"Error fetching student list: {e}")
            finally:
                connection.close()

    def update_attendance_list(class_name):
        display_students(class_name)

    class_option.trace_add("write", lambda *args: update_attendance_list(class_option.get()))

    submit_button = tk.Button(student_frame, text='Submit', bg="#007bff", fg='white', font=('Bold', 14), command=lambda: submit_attendance(class_option.get(), subject_option.get(), attendance_frame))
    submit_button.pack(pady=10, fill="x")

    report_button = tk.Button(student_frame, text='Report', bg="#87CEEB", fg='white', font=('Bold', 14), command=lambda: report_page(class_option.get()))
    report_button.pack(pady=10, fill="x")

    # Trace changes to class_option to update subjects
    class_option.trace("w", update_subjects)

# Function to submit attendance
def submit_attendance(class_name, subject_name, attendance_frame):
    date_str = f"{year_var.get()}-{datetime.strptime(month_var.get(), '%B').month}-{day_var.get()}"
    date = datetime.strptime(date_str, "%Y-%m-%d").date()
    connection = connect_to_database()
    if connection:
        try:
            with connection.cursor() as cursor:
                for widget in attendance_frame.winfo_children():
                    if isinstance(widget, tk.Checkbutton):
                        student_name = widget.cget("text")
                        attendance_status = 'Present' if widget.var.get() == 1 else 'Absent'
                        insert_sql = "INSERT INTO attendances (student_id, class, subject, date, attendance) VALUES (%s, %s, %s, %s, %s)"
                        cursor.execute(insert_sql, (student_name, class_name, subject_name, date, attendance_status))
                connection.commit()
        except pymysql.MySQLError as e:
            messagebox.showerror("Database Error", f"Error submitting attendance: {e}")
        finally:
            connection.close()

# Function to create the report page
def report_page(class_name):
    clear_frame()
    report_frame = tk.Frame(root, bg="#ffffff")
    report_frame.pack(pady=30, fill="both", expand=True)

    boundary_frame = tk.Frame(report_frame, bg="#ffffff", highlightbackground="#000000", highlightthickness=2)
    boundary_frame.pack(padx=1, pady=1, fill="both", expand=True)

    inner_frame = tk.Frame(boundary_frame, bg="#ffffff")
    inner_frame.pack(padx=10, pady=10, fill="both", expand=True)

    heading_lb = tk.Label(inner_frame, text='Report', bg="#ffffff", fg="#007bff", font=('Bold', 28))
    heading_lb.pack(pady=20)

    class_frame = tk.Frame(inner_frame, bg="#ffffff")
    class_frame.pack(pady=10, fill='x')

    class_lb = tk.Label(class_frame, text='Class:', bg="#ffffff", fg='black', font=('Bold', 14))
    class_lb.pack(side='left')

    class_var = tk.StringVar()
    class_var.set(class_name)
    class_option = tk.OptionMenu(class_frame, class_var, "FE_A", "FE_B", "FE_C", "SE_A", "SE_B", "TE_A", "TE_B", "BE", command=update_subjects_report)
    class_option.pack(side='left', padx=10)

    subject_frame = tk.Frame(inner_frame, bg="#ffffff")
    subject_frame.pack(pady=10, fill="x")

    subject_lb = tk.Label(subject_frame, text='Subject:', bg="#ffffff", fg='black', font=('Bold', 14))
    subject_lb.pack(side='left')

    subject_var = tk.StringVar()
    subject_var.set("Select Subject")
    subject_option = tk.OptionMenu(subject_frame, subject_var, "")
    subject_option.pack(side='left', padx=10)

    date_frame = tk.Frame(inner_frame, bg="#ffffff")
    date_frame.pack(pady=10, fill="x")

    date_lb = tk.Label(date_frame, text='Date:', bg="#ffffff", fg='black', font=('Bold', 14))
    date_lb.pack(side='left')

    month_var = tk.StringVar()
    month_var.set("January")
    month_option = tk.OptionMenu(date_frame, month_var, "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
    month_option.pack(side='left', padx=10)

    year_var = tk.StringVar()
    year_var.set("2023")
    year_option = tk.OptionMenu(date_frame, year_var, "2022", "2023", "2024", "2025")
    year_option.pack(side='left', padx=10)

    day_var = tk.StringVar()
    day_var.set("1")
    day_option = tk.OptionMenu(date_frame, day_var, *[str(i) for i in range(1, 32)])
    day_option.pack(side='left', padx=10)

    search_button = tk.Button(inner_frame, text='Search', bg="#87CEEB", fg='white', font=('Bold', 14), command=lambda: search_attendance(class_var.get(), subject_var.get(), month_var.get(), year_var.get(), day_var.get()))
    search_button.pack(pady=10)

    monthly_report_button = tk.Button(inner_frame, text='Monthly Report', bg="#87CEEB", fg='white', font=('Bold', 14), command=lambda: monthly_report_page(class_var.get(), subject_var.get(), month_var.get(), year_var.get()))
    monthly_report_button.pack(pady=10)

    back_button = tk.Button(inner_frame, text='Back', bg="#87CEEB", fg='white', font=('Bold', 14), command=lambda: back_to_dashboard(class_name))
    back_button.pack(pady=10)

    # Update subjects based on the initial class selection
    update_subjects_report(class_name)

    # Trace changes to class_option to update subjects
    class_var.trace("w", update_subjects_report)

# Function to update subjects based on the selected class for report
def update_subjects_report(class_name):
    subjects = {
        "FE_A": ["Mathematics I", "Chemistry I", "Physics I", "Mechanics", "Basic Electrical Engineering", "Programming in C"],
        "FE_B": ["Mathematics I", "Chemistry I", "Physics I", "Mechanics", "Basic Electrical Engineering", "Programming in C"],
        "FE_C": ["Mathematics I", "Chemistry I", "Physics I", "Mechanics", "Basic Electrical Engineering", "Programming in C"],
        "SE_A": ["Mathematics II", "Analysis of Algorithms", "Database Management Systems", "Design and Analysis of Algorithms", "Discrete Structures and Graph Theory", "Operating Systems"],
        "SE_B": ["Mathematics II", "Analysis of Algorithms", "Database Management Systems", "Design and Analysis of Algorithms", "Discrete Structures and Graph Theory", "Operating Systems"],
        "TE_A": ["Mathematics III", "Data Structures", "Microprocessors", "Python Programming", "Cryptography and System Security", "Machine Learning"],
        "TE_B": ["Mathematics III", "Data Structures", "Microprocessors", "Python Programming", "Cryptography and System Security", "Machine Learning"],
        "BE": ["Artificial Intelligence and Machine Learning", "Blockchain Technology", "HTML", "Data Analytics", "Mathematics IV", "Cybersecurity Fundamentals"]
    }
    subject_var.set(subjects.get(class_name, [""])[0])
    menu = subject_option['menu']
    menu.delete(0, 'end')
    for subject in subjects.get(class_name, []):
        menu.add_command(label=subject, command=tk._setit(subject_var, subject))

# Function to search attendance
def search_attendance(class_name, subject, month, year, day):
    clear_frame()
    attendance_frame = tk.Frame(root, bg="#ffffff")
    attendance_frame.pack(pady=30, fill="both", expand=True)

    boundary_frame = tk.Frame(attendance_frame, bg="#ffffff", highlightbackground="#000000", highlightthickness=2)
    boundary_frame.pack(padx=1, pady=1, fill="both", expand=True)

    inner_frame = tk.Frame(boundary_frame, bg="#ffffff")
    inner_frame.pack(padx=10, pady=10, fill="both", expand=True)

    heading_lb = tk.Label(inner_frame, text='Attendance', bg="#ffffff", fg="#007bff", font=('Bold', 28))
    heading_lb.pack(pady=20)

    attendance_tree = ttk.Treeview(inner_frame, columns=("Student", "Attendance"), show="headings")
    attendance_tree.pack(pady=10, fill="both", expand=True)

    attendance_tree.heading("Student", text="Student")
    attendance_tree.heading("Attendance", text="Attendance")

    connection = connect_to_database()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT student_id, attendance FROM attendances WHERE class = %s AND subject = %s AND date = %s"
                cursor.execute(sql, (class_name, subject, f"{year}-{month}-{day}"))
                result = cursor.fetchall()
                for row in result:
                    attendance_tree.insert("", "end", values=(row[0], row[1]))
        except pymysql.MySQLError as e:
            messagebox.showerror("Database Error", f"Error fetching attendance: {e}")
        finally:
            connection.close()

    download_button = tk.Button(inner_frame, text='Download Report', bg="#87CEEB", fg='white', font=('Bold', 14), command=lambda: download_report(class_name, subject, month, year, day))
    download_button.pack(pady=10)

    back_button = tk.Button(inner_frame, text='Back', bg="#87CEEB", fg='white', font=('Bold', 14), command=lambda: back_to_dashboard(class_name))
    back_button.pack(pady=10)

# Function to download the attendance report
def download_report(class_name, subject, month, year, day):
    date_str = f"{year}-{month}-{day}"
    date = datetime.strptime(date_str, "%Y-%m-%d").date()
    connection = connect_to_database()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT student_id, attendance FROM attendances WHERE class = %s AND subject = %s AND date = %s"
                cursor.execute(sql, (class_name, subject, date))
                result = cursor.fetchall()
                file_path = f"attendance_report_{class_name}_{subject}_{date}.csv"
                with open(file_path, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Student", "Attendance"])
                    writer.writerows(result)
                messagebox.showinfo("Download", f"Report downloaded successfully: {file_path}")
        except pymysql.MySQLError as e:
            messagebox.showerror("Database Error", f"Error fetching attendance: {e}")
        finally:
            connection.close()

# Function to create the monthly report page
def monthly_report_page(class_name, subject, month, year):
    clear_frame()
    report_frame = tk.Frame(root, bg="#ffffff")
    report_frame.pack(pady=30, fill="both", expand=True)

    boundary_frame = tk.Frame(report_frame, bg="#ffffff", highlightbackground="#000000", highlightthickness=2)
    boundary_frame.pack(padx=1, pady=1, fill="both", expand=True)

    inner_frame = tk.Frame(boundary_frame, bg="#ffffff")
    inner_frame.pack(padx=10, pady=10, fill="both", expand=True)

    heading_lb = tk.Label(inner_frame, text='Monthly Attendance', bg="#ffffff", fg="#007bff", font=('Bold', 28))
    heading_lb.pack(pady=20)

    class_frame = tk.Frame(inner_frame, bg="#ffffff")
    class_frame.pack(pady=10, fill='x')

    class_lb = tk.Label(class_frame, text='Class:', bg="#ffffff", fg='black', font=('Bold', 14))
    class_lb.pack(side='left')

    class_var = tk.StringVar()
    class_var.set(class_name)
    class_option = tk.OptionMenu(class_frame, class_var, "FE_A", "FE_B", "FE_C", "SE_A", "SE_B", "TE_A", "TE_B", "BE", command=update_subjects_report)
    class_option.pack(side='left', padx=10)

    subject_frame = tk.Frame(inner_frame, bg="#ffffff")
    subject_frame.pack(pady=10, fill="x")

    subject_lb = tk.Label(subject_frame, text='Subject:', bg="#ffffff", fg='black', font=('Bold', 14))
    subject_lb.pack(side='left')

    subject_var = tk.StringVar()
    subject_var.set(subject)
    subject_option = tk.OptionMenu(subject_frame, subject_var, "")
    subject_option.pack(side='left', padx=10)

    date_frame = tk.Frame(inner_frame, bg="#ffffff")
    date_frame.pack(pady=10, fill="x")

    date_lb = tk.Label(date_frame, text='Month:', bg="#ffffff", fg='black', font=('Bold', 14))
    date_lb.pack(side='left')

    month_var = tk.StringVar()
    month_var.set(month)
    month_option = tk.OptionMenu(date_frame, month_var, "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
    month_option.pack(side='left', padx=10)

    year_var = tk.StringVar()
    year_var.set(year)
    year_option = tk.OptionMenu(date_frame, year_var, "2022", "2023", "2024", "2025")
    year_option.pack(side='left', padx=10)

    search_button = tk.Button(inner_frame, text='Search', bg="#87CEEB", fg='white', font=('Bold', 14), command=lambda: search_monthly_attendance(class_var.get(), subject_var.get(), month_var.get(), year_var.get()))
    search_button.pack(pady=10)

    back_button = tk.Button(inner_frame, text='Back', bg="#87CEEB", fg='white', font=('Bold', 14), command=lambda: back_to_dashboard(class_name))
    back_button.pack(pady=10)

# Function to search monthly attendance
def search_monthly_attendance(class_name, subject, month, year):
    clear_frame()
    attendance_frame = tk.Frame(root, bg="#ffffff")
    attendance_frame.pack(pady=30, fill="both", expand=True)

    boundary_frame = tk.Frame(attendance_frame, bg="#ffffff", highlightbackground="#000000", highlightthickness=2)
    boundary_frame.pack(padx=1, pady=1, fill="both", expand=True)

    inner_frame = tk.Frame(boundary_frame, bg="#ffffff")
    inner_frame.pack(padx=10, pady=10, fill="both", expand=True)

    heading_lb = tk.Label(inner_frame, text='Monthly Attendance', bg="#ffffff", fg="#007bff", font=('Bold', 28))
    heading_lb.pack(pady=20)

    attendance_tree = ttk.Treeview(inner_frame, columns=("Student", "Attendance"), show="headings")
    attendance_tree.pack(pady=10, fill="both", expand=True)

    attendance_tree.heading("Student", text="Student")
    attendance_tree.heading("Attendance", text="Attendance")

    connection = connect_to_database()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT student_id, attendance FROM attendances WHERE class = %s AND subject = %s AND MONTH(date) = %s AND YEAR(date) = %s"
                cursor.execute(sql, (class_name, subject, datetime.strptime(month, '%B').month, year))
                result = cursor.fetchall()
                for row in result:
                    attendance_tree.insert("", "end", values=(row[0], row[1]))
        except pymysql.MySQLError as e:
            messagebox.showerror("Database Error", f"Error fetching attendance: {e}")
        finally:
            connection.close()

    download_button = tk.Button(inner_frame, text='Download Report', bg="#87CEEB", fg='white', font=('Bold', 14), command=lambda: download_monthly_report(class_name, subject, month, year))
    download_button.pack(pady=10)

    back_button = tk.Button(inner_frame, text='Back', bg="#87CEEB", fg='white', font=('Bold', 14), command=lambda: monthly_report_page(class_name, subject, month, year))
    back_button.pack(pady=10)

# Function to download the monthly attendance report
def download_monthly_report(class_name, subject, month, year):
    connection = connect_to_database()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT student_id, attendance FROM attendances WHERE class = %s AND subject = %s AND MONTH(date) = %s AND YEAR(date) = %s"
                cursor.execute(sql, (class_name, subject, datetime.strptime(month, '%B').month, year))
                result = cursor.fetchall()
                file_path = f"monthly_attendance_report_{class_name}_{subject}_{month}_{year}.csv"
                with open(file_path, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Student", "Attendance"])
                    writer.writerows(result)
                messagebox.showinfo("Download", f"Monthly report downloaded successfully: {file_path}")
        except pymysql.MySQLError as e:
            messagebox.showerror("Database Error", f"Error fetching attendance: {e}")
        finally:
            connection.close()

# Function to navigate back to the dashboard
def back_to_dashboard(class_name=None):
    if class_name:
        report_page(class_name)
    else:
        staff_dashboard_page()

# Function to create the view student details page
def view_student_details_page():
    clear_frame()
    view_student_details_frame = tk.Frame(root, bg="#ffffff")
    view_student_details_frame.pack(pady=30, fill="both", expand=True)

    boundary_frame = tk.Frame(view_student_details_frame, bg="#ffffff", highlightbackground="#000000", highlightthickness=2)
    boundary_frame.pack(padx=1, pady=1, fill="both", expand=True)

    inner_frame = tk.Frame(boundary_frame, bg="#ffffff")
    inner_frame.pack(padx=10, pady=10, fill="both", expand=True)

    heading_lb = tk.Label(inner_frame, text='View Student Details', bg="#ffffff", fg="#007bff", font=('Bold', 28))
    heading_lb.pack(pady=20)

    class_frame = tk.Frame(inner_frame, bg="#ffffff")
    class_frame.pack(pady=10, fill='x')

    class_lb = tk.Label(class_frame, text='Class:', bg="#ffffff", fg='black', font=('Bold', 14))
    class_lb.pack(side='left')

    class_var = tk.StringVar()
    class_var.set("Select Class")
    class_option = tk.OptionMenu(class_frame, class_var, "FE_A", "FE_B", "FE_C", "SE_A", "SE_B", "TE_A", "TE_B", "BE", command=lambda x: display_student_details(x))
    class_option.pack(side='left', padx=10)

    student_details_frame = tk.Frame(inner_frame, bg="#ffffff")
    student_details_frame.pack(pady=10, fill="both", expand=True)

    student_details_tree = ttk.Treeview(student_details_frame, columns=("Photo", "Full Name", "Contact No.", "Email", "Gender", "Age"), show="headings")
    student_details_tree.pack(pady=10, fill="both", expand=True)

    student_details_tree.heading("Photo", text="Photo")
    student_details_tree.heading("Full Name", text="Full Name")
    student_details_tree.heading("Contact No.", text="Contact No.")
    student_details_tree.heading("Email", text="Email")
    student_details_tree.heading("Gender", text="Gender")
    student_details_tree.heading("Age", text="Age")

    def display_student_details(class_name):
        student_details_tree.delete(*student_details_tree.get_children())
        connection = connect_to_database()
        if connection:
            try:
                with connection.cursor() as cursor:
                    sql = "SELECT * FROM students WHERE class = %s"
                    cursor.execute(sql, (class_name,))
                    result = cursor.fetchall()
                    for row in result:
                        student_details_tree.insert("", "end", values=("Photo", row[1], row[4], row[6], row[2], row[3]))
            except pymysql.MySQLError as e:
                messagebox.showerror("Database Error", f"Error fetching student details: {e}")
            finally:
                connection.close()

    back_button = tk.Button(inner_frame, text='Back', bg="#87CEEB", fg='white', font=('Bold', 14), command=lambda: [messagebox.showinfo("Back", "You are going back to the dashboard"), staff_dashboard_page()])
    back_button.pack(pady=10)

# Function to create the upload page
def upload_page(upload_type):
    clear_frame()
    upload_frame = tk.Frame(root, bg="#ffffff")
    upload_frame.pack(pady=30, fill="both", expand=True)

    boundary_frame = tk.Frame(upload_frame, bg="#ffffff", highlightbackground="#000000", highlightthickness=2)
    boundary_frame.pack(padx=1, pady=1, fill="both", expand=True)

    inner_frame = tk.Frame(boundary_frame, bg="#ffffff")
    inner_frame.pack(padx=10, pady=10, fill="both", expand=True)

    heading_lb = tk.Label(inner_frame, text=f'Upload {upload_type}', bg="#ffffff", fg="#007bff", font=('Bold', 28))
    heading_lb.pack(pady=20)

    class_frame = tk.Frame(inner_frame, bg="#ffffff")
    class_frame.pack(pady=10, fill='x')

    class_lb = tk.Label(class_frame, text='Class:', bg="#ffffff", fg='black', font=('Bold', 14))
    class_lb.pack(side='left')

    global class_option, subject_option, subject_menu
    class_option = tk.StringVar(inner_frame)
    class_option.set("Select Class")
    class_menu = tk.OptionMenu(class_frame, class_option, "FE_A", "FE_B", "FE_C", "SE_A", "SE_B", "TE_A", "TE_B", "BE")
    class_menu.pack(side='left', padx=5)

    subject_frame = tk.Frame(inner_frame, bg="#ffffff")
    subject_frame.pack(pady=10, fill="x")

    subject_lb = tk.Label(subject_frame, text='Subject:', bg="#ffffff", fg='black', font=('Bold', 14))
    subject_lb.pack(side='left')

    subject_option = tk.StringVar(inner_frame)
    subject_option.set("Select Subject")
    subject_menu = tk.OptionMenu(subject_frame, subject_option, "")
    subject_menu.pack(side='left', padx=5)

    date_frame = tk.Frame(inner_frame, bg="#ffffff")
    date_frame.pack(pady=10, fill="x")

    date_lb = tk.Label(date_frame, text='Date:', bg="#ffffff", fg='black', font=('Bold', 14))
    date_lb.pack(side='left')

    month_var = tk.StringVar()
    month_var.set("January")
    month_option = tk.OptionMenu(date_frame, month_var, "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
    month_option.pack(side='left', padx=10)

    year_var = tk.StringVar()
    year_var.set("2023")
    year_option = tk.OptionMenu(date_frame, year_var, "2022", "2023", "2024", "2025")
    year_option.pack(side='left', padx=10)

    day_var = tk.StringVar()
    day_var.set("1")
    day_option = tk.OptionMenu(date_frame, day_var, *[str(i) for i in range(1, 32)])
    day_option.pack(side='left', padx=10)

    notes_file_frame = tk.Frame(inner_frame, bg="#ffffff")
    notes_file_frame.pack(pady=10, fill="x")

    notes_file_lb = tk.Label(notes_file_frame, text='Select File:', bg="#ffffff", fg='black', font=('Bold', 14))
    notes_file_lb.pack(side='left')

    notes_file_entry = tk.Entry(notes_file_frame, width=50, font=('Bold', 14))
    notes_file_entry.pack(side='left', padx=5)

    browse_button = tk.Button(notes_file_frame, text='Browse', bg="#87CEEB", fg='white', font=('Bold', 14), command=lambda: browse_file(notes_file_entry))
    browse_button.pack(side='left', padx=5)

    upload_button = tk.Button(inner_frame, text='Upload', bg="#87CEEB", fg='white', font=('Bold', 14), command=lambda: upload_file(notes_file_entry.get(), class_option.get(), subject_option.get(), month_var.get(), year_var.get(), day_var.get(), upload_type))
    upload_button.pack(pady=10)

    back_button = tk.Button(inner_frame, text='Back', bg="#87CEEB", fg='white', font=('Bold', 14), command=staff_dashboard_page)
    back_button.pack(pady=10)

    # Trace changes to class_option to update subjects
    class_option.trace("w", update_subjects)

# Function to browse and select a file
def browse_file(entry):
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf"), ("PPT Files", "*.ppt"), ("PNG Files", "*.png")])
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)

# Function to upload a file
def upload_file(file_path, class_name, subject_name, month, year, day, upload_type):
    print(f"Upload button clicked. File path: {file_path}")  # Debugging statement
    if file_path and file_path.lower().endswith(('.pdf', '.ppt', '.png')):
        print(f"Uploading {upload_type} from: {file_path}")

        # Read the file as binary data
        try:
            with open(file_path, 'rb') as file:
                binary_data = file.read()
            if binary_data:
                save_upload_to_database(binary_data, class_name, subject_name, month, year, day, upload_type)
                messagebox.showinfo("Success", f"{upload_type} uploaded successfully!")
                notify_students(class_name, subject_name, upload_type)
        except Exception as e:
            messagebox.showerror("Error", f"Error reading file: {e}")
    else:
        messagebox.showerror("Error", "Only PDF, PPT, and PNG files are allowed.")

# Function to notify students about the upload
def notify_students(class_name, subject_name, upload_type):
    connection = connect_to_database()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT student_id FROM students WHERE class = %s"
                cursor.execute(sql, (class_name,))
                students = cursor.fetchall()
                for student in students:
                    student_id = student[0]
                    notification_message = f"New {upload_type} uploaded for {subject_name}."
                    insert_sql = "INSERT INTO notifications (student_id, message) VALUES (%s, %s)"
                    cursor.execute(insert_sql, (student_id, notification_message))
                connection.commit()
        except pymysql.MySQLError as e:
            messagebox.showerror("Database Error", f"Error notifying students: {e}")
        finally:
            connection.close()

# Function to save the uploaded file to the database
def save_upload_to_database(binary_data, class_name, subject_name, month, year, day, upload_type):
    connection = connect_to_database()
    if connection:
        try:
            # Map month name to month number
            month_map = {
                "January": "01", "February": "02", "March": "03", "April": "04",
                "May": "05", "June": "06", "July": "07", "August": "08",
                "September": "09", "October": "10", "November": "11", "December": "12"
            }
            month_number = month_map.get(month, "01")  # Default to January if month is not found
            # Format the date as YYYY-MM-DD
            upload_date = f"{year}-{month_number}-{day}"

            with connection.cursor() as cursor:
                sql = """
                INSERT INTO uploads (file_data, class_name, subject_name, upload_date, upload_type)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (binary_data, class_name, subject_name, upload_date, upload_type))
                connection.commit()
            messagebox.showinfo("Success", f"{upload_type} saved to database successfully!")
        except pymysql.MySQLError as e:
            messagebox.showerror("Database Error", f"Error saving {upload_type} to database: {e}")
        finally:
            connection.close()

# Function to create the generate assignment links page
def generate_assignment_links_page():
    clear_frame()
    generate_assignment_links_frame = tk.Frame(root, bg="#ffffff")
    generate_assignment_links_frame.pack(pady=30, fill="both", expand=True)

    boundary_frame = tk.Frame(generate_assignment_links_frame, bg="#ffffff", highlightbackground="#000000", highlightthickness=2)
    boundary_frame.pack(padx=1, pady=1, fill="both", expand=True)

    inner_frame = tk.Frame(boundary_frame, bg="#ffffff")
    inner_frame.pack(padx=10, pady=10, fill="both", expand=True)

    heading_lb = tk.Label(inner_frame, text='Generate Assignment Links', bg="#ffffff", fg="#007bff", font=('Bold', 28))
    heading_lb.pack(pady=20)

    class_frame = tk.Frame(inner_frame, bg="#ffffff")
    class_frame.pack(pady=10, fill='x')

    class_lb = tk.Label(class_frame, text='Class:', bg="#ffffff", fg='black', font=('Bold', 14))
    class_lb.pack(side='left')

    global class_option, subject_option, subject_menu
    class_option = tk.StringVar(inner_frame)
    class_option.set("Select Class")
    class_menu = tk.OptionMenu(class_frame, class_option, "FE_A", "FE_B", "FE_C", "SE_A", "SE_B", "TE_A", "TE_B", "BE")
    class_menu.pack(side='left', padx=5)

    subject_frame = tk.Frame(inner_frame, bg="#ffffff")
    subject_frame.pack(pady=10, fill="x")

    subject_lb = tk.Label(subject_frame, text='Subject:', bg="#ffffff", fg='black', font=('Bold', 14))
    subject_lb.pack(side='left')

    subject_option = tk.StringVar(inner_frame)
    subject_option.set("Select Subject")
    subject_menu = tk.OptionMenu(subject_frame, subject_option, "")
    subject_menu.pack(side='left', padx=5)

    assignment_name_frame = tk.Frame(inner_frame, bg="#ffffff")
    assignment_name_frame.pack(pady=10, fill="x")

    assignment_name_lb = tk.Label(assignment_name_frame, text='Assignment Name:', bg="#ffffff", fg='black', font=('Bold', 14))
    assignment_name_lb.pack(side='left')

    assignment_name_entry = tk.Entry(assignment_name_frame, width=50, font=('Bold', 14))
    assignment_name_entry.pack(side='left', padx=5)

    generate_link_button = tk.Button(inner_frame, text='Generate Link', bg="#87CEEB", fg='white', font=('Bold', 14), command=lambda: generate_link(class_option.get(), subject_option.get(), assignment_name_entry.get()))
    generate_link_button.pack(pady=10, fill="x")

    back_button = tk.Button(inner_frame, text='Back', bg="#87CEEB", fg='white', font=('Bold', 14), command=staff_dashboard_page)
    back_button.pack(pady=10)

    links_listbox_frame = tk.Frame(inner_frame, bg="#ffffff")
    links_listbox_frame.pack(pady=10, fill="both", expand=True)

    global links_listbox
    links_listbox = tk.Listbox(links_listbox_frame, font=('Bold', 14), width=50)
    links_listbox.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(links_listbox_frame)
    scrollbar.pack(side="right", fill="y")

    links_listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=links_listbox.yview)

    load_links()

    # Trace changes to class_option to update subjects
    class_option.trace("w", update_subjects)

# Function to generate a link and save it to the database
def generate_link(class_name, subject_name, assignment_name):
    if class_name == "Select Class" or subject_name == "Select Subject" or not assignment_name:
        messagebox.showwarning("Input Error", "Please select a class, subject, and enter an assignment name.")
        return
    link = generate_unique_link(class_name, subject_name, assignment_name)
    save_link_to_database(class_name, subject_name, assignment_name, link)
    links_listbox.insert(tk.END, link)
    messagebox.showinfo("Success", f"Link generated: {link}")

# Function to generate a unique link
def generate_unique_link(class_name, subject_name, assignment_name):
    return f"http://campusconnect.com/assignment/{uuid.uuid4()}"

# Function to save the generated link to the database
def save_link_to_database(class_name, subject_name, assignment_name, link):
    connection = connect_to_database()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO assignment_links (class_name, subject_name, assignment_name, link) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (class_name, subject_name, assignment_name, link))
                connection.commit()
        except pymysql.MySQLError as e:
            messagebox.showerror("Database Error", f"Error saving link to database: {e}")
        finally:
            connection.close()

# Function to load links from the database
def load_links():
    connection = connect_to_database()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT link FROM assignment_links"
                cursor.execute(sql)
                links = cursor.fetchall()
                for (link,) in links:
                    links_listbox.insert(tk.END, link)
        except pymysql.MySQLError as e:
            messagebox.showerror("Database Error", f"Error loading links: {e}")
        finally:
            connection.close()

# Function to create the view student details page
def view_student_details_page():
    clear_frame()
    view_student_details_frame = tk.Frame(root, bg="#ffffff")
    view_student_details_frame.pack(pady=30, fill="both", expand=True)

    boundary_frame = tk.Frame(view_student_details_frame, bg="#ffffff", highlightbackground="#000000", highlightthickness=2)
    boundary_frame.pack(padx=1, pady=1, fill="both", expand=True)

    inner_frame = tk.Frame(boundary_frame, bg="#ffffff")
    inner_frame.pack(padx=10, pady=10, fill="both", expand=True)

    heading_lb = tk.Label(inner_frame, text='View Student Details', bg="#ffffff", fg="#007bff", font=('Bold', 28))
    heading_lb.pack(pady=20)

    class_frame = tk.Frame(inner_frame, bg="#ffffff")
    class_frame.pack(pady=10, fill='x')

    class_lb = tk.Label(class_frame, text='Class:', bg="#ffffff", fg='black', font=('Bold', 14))
    class_lb.pack(side='left')

    class_var = tk.StringVar()
    class_var.set("Select Class")
    class_option = tk.OptionMenu(class_frame, class_var, "FE_A", "FE_B", "FE_C", "SE_A", "SE_B", "TE_A", "TE_B", "BE", command=lambda x: display_student_details(x))
    class_option.pack(side='left', padx=10)

    student_details_frame = tk.Frame(inner_frame, bg="#ffffff")
    student_details_frame.pack(pady=10, fill="both", expand=True)

    student_details_tree = ttk.Treeview(student_details_frame, columns=("Photo", "Full Name", "Contact No.", "Email", "Gender", "Age"), show="headings")
    student_details_tree.pack(pady=10, fill="both", expand=True)

    student_details_tree.heading("Photo", text="Photo")
    student_details_tree.heading("Full Name", text="Full Name")
    student_details_tree.heading("Contact No.", text="Contact No.")
    student_details_tree.heading("Email", text="Email")
    student_details_tree.heading("Gender", text="Gender")
    student_details_tree.heading("Age", text="Age")

    def display_student_details(class_name):
        student_details_tree.delete(*student_details_tree.get_children())
        connection = connect_to_database()
        if connection:
            try:
                with connection.cursor() as cursor:
                    sql = "SELECT * FROM students WHERE class = %s"
                    cursor.execute(sql, (class_name,))
                    result = cursor.fetchall()
                    for row in result:
                        student_details_tree.insert("", "end", values=("Photo", row[1], row[4], row[6], row[2], row[3]))
            except pymysql.MySQLError as e:
                messagebox.showerror("Database Error", f"Error fetching student details: {e}")
            finally:
                connection.close()

    back_button = tk.Button(inner_frame, text='Back', bg="#87CEEB", fg='white', font=('Bold', 14), command=lambda: [messagebox.showinfo("Back", "You are going back to the dashboard"), staff_dashboard_page()])
    back_button.pack(pady=10)

# Function to navigate back to the dashboard
def back_to_dashboard(class_name=None):
    if class_name:
        report_page(class_name)
    else:
        staff_dashboard_page()

# Global variable to keep track of the last student ID
last_student_id = {
    "FE": 25100000,  # Starting ID for FE students in 2025
    "SE": 25200000   # Starting ID for SE students in 2025
}

# Function to generate a student ID
def generate_student_id(class_type):
    global last_student_id
    last_student_id[class_type] += 1
    return str(last_student_id[class_type])

# Function to create the login student page
def login_student_page():
    clear_frame()
    login_student_frame = tk.Frame(root, bg="#ffffff")
    login_student_frame.pack(pady=30, fill="both", expand=True)

    login_student_image = Image.open("C:\\Users\\Ashis\\OneDrive\\Desktop\\BG\\login.png")  # Update with your image path
    login_student_image = login_student_image.resize((400, 400))
    login_student_image = ImageTk.PhotoImage(login_student_image)

    login_student_label = tk.Label(login_student_frame, image=login_student_image, bg="#ffffff")
    login_student_label.image = login_student_image
    login_student_label.pack()

    login_student_heading_lb = tk.Label(login_student_frame, text='LOGIN STUDENT', bg="#ffffff", fg="#007bff", font=('Bold', 28))
    login_student_heading_lb.pack(pady=10)

    student_id_frame = tk.Frame(login_student_frame, bg="#ffffff")
    student_id_frame.pack(pady=5, fill='x')

    student_id_lb = tk.Label(student_id_frame, text='Student ID Number:', bg="#ffffff", fg='black', font=('Bold', 20))
    student_id_lb.pack(side='left')

    student_id_entry = tk.Entry(student_id_frame, width=20, font=('Bold', 20))
    student_id_entry.pack(side='left', padx=5)

    student_password_frame = tk.Frame(login_student_frame, bg="#ffffff")
    student_password_frame.pack(pady=5, fill='x')

    student_password_lb = tk.Label(student_password_frame, text='Student Password:', bg="#ffffff", fg='black', font=('Bold', 20))
    student_password_lb.pack(side='left')

    student_password_entry = tk.Entry(student_password_frame, show='*', width=20, font=('Bold', 20))
    student_password_entry.pack(side='left', padx=5)

    button_frame = tk.Frame(login_student_frame, bg="#ffffff")
    button_frame.pack(pady=10)

    def login():
        global student_id
        student_id = student_id_entry.get().strip()
        student_password = student_password_entry.get().strip()
        connection = connect_to_database()
        if connection:
            try:
                with connection.cursor() as cursor:
                    sql = "SELECT class FROM students WHERE student_id = %s AND password = %s"
                    cursor.execute(sql, (student_id, student_password))
                    result = cursor.fetchone()
                    if result:
                        global student_class
                        student_class = result[0]
                        print("Login successful!")
                        login_student_frame.destroy()
                        student_dashboard_page()
                    else:
                        print("Invalid Student ID or Password")
                        messagebox.showerror("Error", "Invalid Student ID or Password")
            except pymysql.MySQLError as e:
                messagebox.showerror("Database Error", f"Error logging in: {e}")
            finally:
                connection.close()

    login_button = tk.Button(button_frame, text='Login', bg="#87CEEB", fg='white', font=('Bold', 14), command=login)
    login_button.pack(side='left', padx=5)

    forgot_password_button = tk.Button(button_frame, text='Forgot Password', bg="#87CEEB", fg='white', font=('Bold', 14), command=forgot_password_student_page)
    forgot_password_button.pack(side='left', padx=5)

    home_button_student = tk.Button(login_student_frame, text='Home', bg="#87CEEB", fg='white', font=('Bold', 10), command=welcome_page)
    home_button_student.pack(pady=10)

def forgot_password_student_page():
    clear_frame()
    forgot_password_frame = tk.Frame(root, bg="#ffffff")
    forgot_password_frame.pack(pady=30, fill="both", expand=True)

    forgot_password_label = tk.Label(forgot_password_frame, text='Forgot Password', bg="#ffffff", fg="#007bff", font=('Bold', 28))
    forgot_password_label.pack(pady=20)

    student_id_frame = tk.Frame(forgot_password_frame, bg="#ffffff")
    student_id_frame.pack(pady=5, fill='x')

    student_id_lb = tk.Label(student_id_frame, text='Student ID Number:', bg="#ffffff", fg='black', font=('Bold', 20))
    student_id_lb.pack(side='left')

    student_id_entry = tk.Entry(student_id_frame, width=20, font=('Bold', 20))
    student_id_entry.pack(side='left', padx=5)

    student_email_frame = tk.Frame(forgot_password_frame, bg="#ffffff")
    student_email_frame.pack(pady=5, fill='x')

    student_email_lb = tk.Label(student_email_frame, text='Student Email:', bg="#ffffff", fg='black', font=('Bold', 20))
    student_email_lb.pack(side='left')

    student_email_entry = tk.Entry(student_email_frame, width=20, font=('Bold', 20))
    student_email_entry.pack(side='left', padx=5)

    button_frame = tk.Frame(forgot_password_frame, bg="#ffffff")
    button_frame.pack(pady=10)

    def reset_password():
        student_id = student_id_entry.get().strip()
        student_email = student_email_entry.get().strip()
        connection = connect_to_database()
        if connection:
            try:
                with connection.cursor() as cursor:
                    sql = "SELECT * FROM students WHERE student_id = %s AND email = %s"
                    cursor.execute(sql, (student_id, student_email))
                    result = cursor.fetchone()
                    if result:
                        new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
                        update_sql = "UPDATE students SET password = %s WHERE student_id = %s"
                        cursor.execute(update_sql, (new_password, student_id))
                        connection.commit()

                        # Send email with the new password
                        msg = MIMEMultipart()
                        msg['From'] = 'campusconnect@example.com'
                        msg['To'] = student_email
                        msg['Subject'] = 'Password Reset'
                        body = f'Your new password is: {new_password}'
                        msg.attach(MIMEText(body, 'plain'))

                        server = smtplib.SMTP('smtp.example.com', 587)
                        server.starttls()
                        server.login('campusconnect@example.com', 'your_password')
                        text = msg.as_string()
                        server.sendmail('campusconnect@example.com', student_email, text)
                        server.quit()

                        messagebox.showinfo("Success", "A new password has been sent to your email.")
                    else:
                        messagebox.showerror("Error", "Invalid Student ID or Email")
            except pymysql.MySQLError as e:
                messagebox.showerror("Database Error", f"Error resetting password: {e}")
            finally:
                connection.close()

    reset_password_button = tk.Button(button_frame, text='Reset Password', bg="#87CEEB", fg='white', font=('Bold', 14), command=reset_password)
    reset_password_button.pack(side='left', padx=5)

    back_button = tk.Button(button_frame, text='Back', bg="#87CEEB", fg='white', font=('Bold', 14), command=login_student_page)
    back_button.pack(side='left', padx=5)

# Function to create the student dashboard page

# Function to create the student dashboard page
def student_dashboard_page():
    clear_frame()
    dashboard_frame = tk.Frame(root, bg="#ffffff")
    dashboard_frame.pack(pady=30, fill="both", expand=True)

    boundary_frame = tk.Frame(dashboard_frame, bg="#ffffff", highlightbackground="#000000", highlightthickness=2)
    boundary_frame.pack(padx=1, pady=1, fill="both", expand=True)

    inner_frame = tk.Frame(boundary_frame, bg="#ffffff")
    inner_frame.pack(padx=10, pady=10, fill="both", expand=True)

    logo_frame = tk.Frame(inner_frame, bg="#ffffff")
    logo_frame.place(relx=0.5, rely=0.5, anchor="center")

    logo_image = Image.open("C:\\Users\\Ashis\\OneDrive\\Desktop\\BG\\Campusconnect.png")  # Update with your logo path
    logo_image = logo_image.resize((800, 800))
    logo_image = ImageTk.PhotoImage(logo_image)

    logo_label = tk.Label(logo_frame, image=logo_image, bg="#ffffff")
    logo_label.image = logo_image
    logo_label.pack()

    heading_lb = tk.Label(logo_frame, text='Student Dashboard', bg="#ffffff", fg="#007bff", font=('Bold', 32))
    heading_lb.place(relx=0.5, rely=0.15, anchor="center")

    left_button_frame = tk.Frame(inner_frame, bg="#ffffff")
    left_button_frame.place(x=10, rely=0.5, anchor="w")

    view_courses_button = tk.Button(left_button_frame, text='View Courses', bg="#ADD8E6", fg='black', font=('Bold', 14), command=view_courses_page)
    view_courses_button.pack(pady=10, fill="x")

    apply_for_leave_button = tk.Button(left_button_frame, text='Apply for Leave', bg="#ADD8E6", fg='black', font=('Bold', 14), command=apply_for_leave_page)
    apply_for_leave_button.pack(pady=10, fill="x")

    back_button = tk.Button(inner_frame, text='Back', bg="#87CEEB", fg='white', font=('Bold', 10), command=welcome_page)
    back_button.place(relx=0.95, rely=0.95, anchor="se")

    notification_frame = tk.Frame(inner_frame, bg="#ffffff", highlightbackground="#000000", highlightthickness=1)
    notification_frame.place(relx=0.95, rely=0.05, anchor="ne")

    notification_label = tk.Label(notification_frame, text='Notifications', bg="#ffffff", fg="#007bff", font=('Bold', 14))
    notification_label.pack()

    notification_text = tk.Text(notification_frame, width=30, height=5, font=('Bold', 12), state='disabled')
    notification_text.pack()

    def update_notifications(message):
        notification_text.config(state='normal')
        notification_text.insert(tk.END, message + '\n')
        notification_text.config(state='disabled')

    # Fetch and display notifications for the student
    fetch_and_display_notifications(update_notifications)

# Function to fetch and display notifications for the student
def fetch_and_display_notifications(update_notifications):
    connection = connect_to_database()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT message FROM notifications WHERE student_id = %s"
                cursor.execute(sql, (student_id,))
                notifications = cursor.fetchall()
                for notification in notifications:
                    update_notifications(notification[0])
        except pymysql.MySQLError as e:
            messagebox.showerror("Database Error", f"Error fetching notifications: {e}")
        finally:
            connection.close()

# Function to create the view courses page
def view_courses_page():
    clear_frame()
    view_courses_frame = tk.Frame(root, bg="#ffffff")
    view_courses_frame.pack(pady=30, fill="both", expand=True)

    boundary_frame = tk.Frame(view_courses_frame, bg="#ffffff", highlightbackground="#000000", highlightthickness=2)
    boundary_frame.pack(padx=1, pady=1, fill="both", expand=True)

    inner_frame = tk.Frame(boundary_frame, bg="#ffffff")
    inner_frame.pack(padx=10, pady=10, fill="both", expand=True)

    logo_frame = tk.Frame(inner_frame, bg="#ffffff")
    logo_frame.place(relx=0.5, rely=0.5, anchor="center")

    logo_image = Image.open("C:\\Users\\Ashis\\OneDrive\\Desktop\\BG\\Campusconnect.png")  # Update with your logo path
    logo_image = logo_image.resize((800, 800))
    logo_image = ImageTk.PhotoImage(logo_image)

    logo_label = tk.Label(logo_frame, image=logo_image, bg="#ffffff")
    logo_label.image = logo_image
    logo_label.pack()

    heading_lb = tk.Label(logo_frame, text='View Courses', bg="#ffffff", fg="#007bff", font=('Bold', 32))
    heading_lb.place(relx=0.5, rely=0.15, anchor="center")

    left_button_frame = tk.Frame(inner_frame, bg="#ffffff")
    left_button_frame.place(x=2, rely=0.5, anchor="w")

    subjects_dict = {
        "FE_A": ["Mathematics I", "Chemistry I", "Physics I", "Mechanics", "Basic Electrical Engineering", "Programming in C"],
        "FE_B": ["Mathematics I", "Chemistry I", "Physics I", "Mechanics", "Basic Electrical Engineering", "Programming in C"],
        "FE_C": ["Mathematics I", "Chemistry I", "Physics I", "Mechanics", "Basic Electrical Engineering", "Programming in C"],
        "SE_A": ["Mathematics II", "Analysis of Algorithms", "Database Management Systems", "Design and Analysis of Algorithms", "Discrete Structures and Graph Theory", "Operating Systems"],
        "SE_B": ["Mathematics II", "Analysis of Algorithms", "Database Management Systems", "Design and Analysis of Algorithms", "Discrete Structures and Graph Theory", "Operating Systems"],
        "TE_A": ["Mathematics III", "Data Structures", "Microprocessors", "Python Programming", "Cryptography and System Security", "Machine Learning"],
        "TE_B": ["Mathematics III", "Data Structures", "Microprocessors", "Python Programming", "Cryptography and System Security", "Machine Learning"],
        "BE": ["Artificial Intelligence and Machine Learning", "Blockchain Technology", "HTML", "Data Analytics", "Mathematics IV", "Cybersecurity Fundamentals"]
    }

    student_class = "SE_A"  # Example class; this should be dynamically set in your actual application
    student_subjects = subjects_dict.get(student_class, [])

    for subject in student_subjects:
        subject_button = tk.Button(left_button_frame, text=subject, bg="#ADD8E6", fg='black', font=('Bold', 14), command=lambda s=subject: view_course_details_page(s))
        subject_button.pack(pady=10, fill="x")

    home_button_dashboard = tk.Button(inner_frame, text='Home', bg="#87CEEB", fg='white', font=('Bold', 10), command=student_dashboard_page)
    home_button_dashboard.place(relx=0.95, rely=0.95, anchor="se")

# Function to create the view course details page
def view_course_details_page(subject):
    clear_frame()
    course_frame = tk.Frame(root, bg="#ffffff")
    course_frame.pack(pady=30, fill="both", expand=True)

    boundary_frame = tk.Frame(course_frame, bg="#ffffff", highlightbackground="#000000", highlightthickness=2)
    boundary_frame.pack(padx=1, pady=1, fill="both", expand=True)

    inner_frame = tk.Frame(boundary_frame, bg="#ffffff")
    inner_frame.pack(padx=10, pady=10, fill="both", expand=True)

    logo_frame = tk.Frame(inner_frame, bg="#ffffff")
    logo_frame.place(relx=0.5, rely=0.5, anchor="center")

    logo_image = Image.open("C:\\Users\\Ashis\\OneDrive\\Desktop\\BG\\Campusconnect.png")  # Update with your logo path
    logo_image = logo_image.resize((800, 800))
    logo_image = ImageTk.PhotoImage(logo_image)

    logo_label = tk.Label(logo_frame, image=logo_image, bg="#ffffff")
    logo_label.image = logo_image
    logo_label.pack()

    heading_lb = tk.Label(logo_frame, text=f'{subject}', bg="#ffffff", fg="#007bff", font=('Bold', 32))
    heading_lb.place(relx=0.5, rely=0.15, anchor="center")

    

    # Frame to hold the buttons on the left side
    button_frame = tk.Frame(inner_frame, bg="#ffffff")
    button_frame.place(x=10, y=200, anchor="nw")

    notes_button = tk.Button(button_frame, text='Notes', bg="#87CEEB", fg='white', font=('Bold', 14), command=lambda: view_notes_for_course(subject))
    notes_button.pack(pady=10, fill="x")

    results_button = tk.Button(button_frame, text='Results', bg="#87CEEB", fg='white', font=('Bold', 14), command=lambda: view_results_for_course(subject))
    results_button.pack(pady=10, fill="x")

    submit_assignment_button = tk.Button(button_frame, text='Submit Assignment', bg="#87CEEB", fg='white', font=('Bold', 14), command=lambda: submit_assignment_page(subject))
    submit_assignment_button.pack(pady=10, fill="x")

    view_attendance_button = tk.Button(button_frame, text='View Attendance', bg="#87CEEB", fg='white', font=('Bold', 14), command=lambda: view_attendance_page(subject))
    view_attendance_button.pack(pady=10, fill="x")

    home_button_dashboard = tk.Button(inner_frame, text='Back', bg="#87CEEB", fg='white', font=('Bold', 10), command=view_courses_page)
    home_button_dashboard.place(relx=0.95, rely=0.95, anchor="se")

# Function to create the view notes page
def view_notes_for_course(subject):
    clear_frame()
    notes_frame = tk.Frame(root, bg="#ffffff")
    notes_frame.pack(pady=30, fill="both", expand=True)

    boundary_frame = tk.Frame(notes_frame, bg="#ffffff", highlightbackground="#000000", highlightthickness=2)
    boundary_frame.pack(padx=1, pady=1, fill="both", expand=True)

    inner_frame = tk.Frame(boundary_frame, bg="#ffffff")
    inner_frame.pack(padx=10, pady=10, fill="both", expand=True)

    logo_frame = tk.Frame(inner_frame, bg="#ffffff")
    logo_frame.place(relx=0.5, rely=0.5, anchor="center")

    logo_image = Image.open("C:\\Users\\Ashis\\OneDrive\\Desktop\\BG\\Campusconnect.png")  # Update with your logo path
    logo_image = logo_image.resize((800, 800))
    logo_image = ImageTk.PhotoImage(logo_image)

    logo_label = tk.Label(logo_frame, image=logo_image, bg="#ffffff")
    logo_label.image = logo_image
    logo_label.pack()

    heading_lb = tk.Label(logo_frame, text=f'Notes for {subject}', bg="#ffffff", fg="#007bff", font=('Bold', 32))
    heading_lb.place(relx=0.5, rely=0.15, anchor="center")

    notes_lb = tk.Label(inner_frame, text=f'Notes for {subject} will be displayed here.', bg="#ffffff", fg='black', font=('Bold', 14))
    notes_lb.pack(pady=20)

    # Fetch and display notes for the subject
    fetch_and_display_notes(subject, notes_lb)

    back_button = tk.Button(inner_frame, text='Back', bg="#87CEEB", fg='white', font=('Bold', 10), command=lambda: view_course_details_page(subject))
    back_button.place(relx=0.95, rely=0.95, anchor="se")

# Function to fetch and display notes for a specific course
def fetch_and_display_notes(subject, notes_lb):
    connection = connect_to_database()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT file_data, file_name FROM uploads WHERE subject_name = %s AND upload_type = 'Notes'"
                cursor.execute(sql, (subject,))
                notes = cursor.fetchall()
                if notes:
                    notes_lb.config(text=f'Notes for {subject}:')
                    for note in notes:
                        file_data, file_name = note
                        file_path = f"notes_{subject}_{file_name}"
                        with open(file_path, 'wb') as file:
                            file.write(file_data)
                        notes_lb.config(text=notes_lb.cget("text") + f"\n{file_path}")
                else:
                    notes_lb.config(text=f'No notes available for {subject}.')
        except pymysql.MySQLError as e:
            messagebox.showerror("Database Error", f"Error fetching notes: {e}")
        finally:
            connection.close()

# Function to create the view results page
def view_results_for_course(subject):
    clear_frame()
    results_frame = tk.Frame(root, bg="#ffffff")
    results_frame.pack(pady=30, fill="both", expand=True)

    boundary_frame = tk.Frame(results_frame, bg="#ffffff", highlightbackground="#000000", highlightthickness=2)
    boundary_frame.pack(padx=1, pady=1, fill="both", expand=True)

    inner_frame = tk.Frame(boundary_frame, bg="#ffffff")
    inner_frame.pack(padx=10, pady=10, fill="both", expand=True)

    logo_frame = tk.Frame(inner_frame, bg="#ffffff")
    logo_frame.place(relx=0.5, rely=0.5, anchor="center")

    logo_image = Image.open("C:\\Users\\Ashis\\OneDrive\\Desktop\\BG\\Campusconnect.png")  # Update with your logo path
    logo_image = logo_image.resize((800, 800))
    logo_image = ImageTk.PhotoImage(logo_image)

    logo_label = tk.Label(logo_frame, image=logo_image, bg="#ffffff")
    logo_label.image = logo_image
    logo_label.pack()

    heading_lb = tk.Label(logo_frame, text=f'Results for {subject}', bg="#ffffff", fg="#007bff", font=('Bold', 32))
    heading_lb.place(relx=0.5, rely=0.15, anchor="center")

    results_lb = tk.Label(inner_frame, text=f'Results for {subject} will be displayed here.', bg="#ffffff", fg='black', font=('Bold', 14))
    results_lb.pack(pady=20)

    # Fetch and display results for the subject
    fetch_and_display_results(subject, results_lb)

    back_button = tk.Button(inner_frame, text='Back', bg="#87CEEB", fg='white', font=('Bold', 10), command=lambda: view_course_details_page(subject))
    back_button.place(relx=0.95, rely=0.95, anchor="se")

# Function to fetch and display results for a specific course
def fetch_and_display_results(subject, results_lb):
    connection = connect_to_database()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT file_data, file_name FROM uploads WHERE subject_name = %s AND upload_type = 'Results'"
                cursor.execute(sql, (subject,))
                results = cursor.fetchall()
                if results:
                    results_lb.config(text=f'Results for {subject}:')
                    for result in results:
                        file_data, file_name = result
                        file_path = f"results_{subject}_{file_name}"
                        with open(file_path, 'wb') as file:
                            file.write(file_data)
                        results_lb.config(text=results_lb.cget("text") + f"\n{file_path}")
                else:
                    results_lb.config(text=f'No results available for {subject}.')
        except pymysql.MySQLError as e:
            messagebox.showerror("Database Error", f"Error fetching results: {e}")
        finally:
            connection.close()

# Function to create the submit assignment page
def submit_assignment_page(subject):
    clear_frame()
    submit_assignment_frame = tk.Frame(root, bg="#ffffff")
    submit_assignment_frame.pack(pady=30, fill="both", expand=True)

    boundary_frame = tk.Frame(submit_assignment_frame, bg="#ffffff", highlightbackground="#000000", highlightthickness=2)
    boundary_frame.pack(padx=1, pady=1, fill="both", expand=True)

    inner_frame = tk.Frame(boundary_frame, bg="#ffffff")
    inner_frame.pack(padx=10, pady=10, fill="both", expand=True)

    logo_frame = tk.Frame(inner_frame, bg="#ffffff")
    logo_frame.place(relx=0.5, rely=0.5, anchor="center")

    logo_image = Image.open("C:\\Users\\Ashis\\OneDrive\\Desktop\\BG\\Campusconnect.png")  # Update with your logo path
    logo_image = logo_image.resize((200, 200))
    logo_image = ImageTk.PhotoImage(logo_image)

    logo_label = tk.Label(logo_frame, image=logo_image, bg="#ffffff")
    logo_label.image = logo_image
    logo_label.pack()

    heading_lb = tk.Label(logo_frame, text=f'Submit Assignment for {subject}', bg="#ffffff", fg="#007bff", font=('Bold', 20))
    heading_lb.place(relx=0.5, rely=0.15, anchor="center")

    file_path_var = tk.StringVar()

    file_path_frame = tk.Frame(inner_frame, bg="#ffffff")
    file_path_frame.pack(pady=10, fill="x")

    file_path_lb = tk.Label(file_path_frame, text='Select File:', bg="#ffffff", fg='black', font=('Bold', 14))
    file_path_lb.pack(side='left')

    file_path_entry = tk.Entry(file_path_frame, width=50, font=('Bold', 14), textvariable=file_path_var)
    file_path_entry.pack(side='left', padx=5)

    browse_button = tk.Button(file_path_frame, text='Browse', bg="#87CEEB", fg='white', font=('Bold', 14), command=lambda: browse_file(file_path_var))
    browse_button.pack(side='left', padx=5)

    submit_button = tk.Button(inner_frame, text='Submit Assignment', bg="#87CEEB", fg='white', font=('Bold', 14), command=lambda: submit_assignment(subject, file_path_var.get()))
    submit_button.pack(pady=10)

    back_button = tk.Button(inner_frame, text='Back', bg="#87CEEB", fg='white', font=('Bold', 10), command=lambda: view_course_details_page(subject))
    back_button.pack(pady=10)

# Function to browse and select a file
def browse_file(file_path_var):
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf"), ("PPT Files", "*.ppt"), ("PNG Files", "*.png")])
    if file_path:
        file_path_var.set(file_path)

# Function to submit the assignment
def submit_assignment(subject, file_path):
    if file_path:
        # Upload assignment to the database
        connection = connect_to_database()
        if connection:
            try:
                with open(file_path, 'rb') as file:
                    binary_data = file.read()
                with connection.cursor() as cursor:
                    sql = "INSERT INTO assignments (student_id, subject, file_data, file_name) VALUES (%s, %s, %s, %s)"
                    cursor.execute(sql, (student_id, subject, binary_data, os.path.basename(file_path)))
                    connection.commit()
                    # Debug print statement
                    print("Assignment submitted successfully and uploaded to the database!")
                    # Show success message immediately after commit
                    messagebox.showinfo("Success", f"Assignment for {subject} submitted successfully and uploaded to the database!")
            except pymysql.MySQLError as e:
                messagebox.showerror("Database Error", f"Error submitting assignment: {e}")
            finally:
                connection.close()
    else:
        messagebox.showerror("Error", "Please select a file")


# Function to create the view attendance page
def view_attendance_page(subject):
    clear_frame()
    attendance_frame = tk.Frame(root, bg="#ffffff")
    attendance_frame.pack(pady=30, fill="both", expand=True)

    boundary_frame = tk.Frame(attendance_frame, bg="#ffffff", highlightbackground="#000000", highlightthickness=2)
    boundary_frame.pack(padx=1, pady=1, fill="both", expand=True)

    inner_frame = tk.Frame(boundary_frame, bg="#ffffff")
    inner_frame.pack(padx=10, pady=10, fill="both", expand=True)

    logo_frame = tk.Frame(inner_frame, bg="#ffffff")
    logo_frame.place(relx=0.5, rely=0.5, anchor="center")

    logo_image = Image.open("C:\\Users\\Ashis\\OneDrive\\Desktop\\BG\\Campusconnect.png")  # Update with your logo path
    logo_image = logo_image.resize((800, 800))
    logo_image = ImageTk.PhotoImage(logo_image)

    logo_label = tk.Label(logo_frame, image=logo_image, bg="#ffffff")
    logo_label.image = logo_image
    logo_label.pack()

    heading_lb = tk.Label(logo_frame, text=f'Attendance for {subject}', bg="#ffffff", fg="#007bff", font=('Bold', 32))
    heading_lb.place(relx=0.5, rely=0.15, anchor="center")

    attendance_lb = tk.Label(inner_frame, text=f'Attendance for {subject} will be displayed here.', bg="#ffffff", fg='black', font=('Bold', 14))
    attendance_lb.pack(pady=20)

    month_frame = tk.Frame(inner_frame, bg="#ffffff")
    month_frame.pack(pady=10, fill="x")

    month_lb = tk.Label(month_frame, text='Month:', bg="#ffffff", fg='black', font=('Bold', 14))
    month_lb.pack(side='left')

    month_var = tk.StringVar()
    month_var.set("January")
    month_option = tk.OptionMenu(month_frame, month_var, "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
    month_option.pack(side='left', padx=10)

    fetch_button = tk.Button(inner_frame, text='Fetch Attendance', bg="#87CEEB", fg='white', font=('Bold', 14), command=lambda: fetch_attendance(subject, month_var.get()))
    fetch_button.pack(pady=10)

    attendance_listbox = tk.Listbox(inner_frame, font=('Bold', 14))
    attendance_listbox.pack(pady=20, fill="both", expand=True)

    def fetch_attendance(subject, month):
        connection = connect_to_database()
        if connection:
            try:
                with connection.cursor() as cursor:
                    sql = "SELECT date, attendance FROM attendances WHERE subject = %s AND MONTH(date) = MONTH(%s) AND student_id = %s"
                    cursor.execute(sql, (subject, month, student_id))
                    attendances = cursor.fetchall()
                    attendance_listbox.delete(0, tk.END)
                    for attendance in attendances:
                        attendance_listbox.insert(tk.END, f"{attendance[0]} - {attendance[1]}")
            except pymysql.MySQLError as e:
                messagebox.showerror("Database Error", f"Error fetching attendance: {e}")
            finally:
                connection.close()

    back_button = tk.Button(inner_frame, text='Back', bg="#87CEEB", fg='white', font=('Bold', 10), command=lambda: view_course_details_page(subject))
    back_button.place(relx=0.95, rely=0.95, anchor="se")



# Function to create the apply for leave page
def apply_for_leave_page():
    clear_frame()
    apply_for_leave_frame = tk.Frame(root, bg="#ffffff")
    apply_for_leave_frame.pack(pady=30, fill="both", expand=True)

    boundary_frame = tk.Frame(apply_for_leave_frame, bg="#ffffff", highlightbackground="#000000", highlightthickness=2)
    boundary_frame.pack(padx=1, pady=1, fill="both", expand=True)

    inner_frame = tk.Frame(boundary_frame, bg="#ffffff")
    inner_frame.pack(padx=10, pady=10, fill="both", expand=True)

    logo_frame = tk.Frame(inner_frame, bg="#ffffff")
    logo_frame.place(relx=0.5, rely=0.5, anchor="center")

    logo_image = Image.open("C:\\Users\\Ashis\\OneDrive\\Desktop\\BG\\Campusconnect.png")  # Update with your logo path
    logo_image = logo_image.resize((200, 200))
    logo_image = ImageTk.PhotoImage(logo_image)

    logo_label = tk.Label(logo_frame, image=logo_image, bg="#ffffff")
    logo_label.image = logo_image
    logo_label.pack()

    heading_lb = tk.Label(logo_frame, text='Apply for Leave', bg="#ffffff", fg="#007bff", font=('Bold', 20))
    heading_lb.place(relx=0.5, rely=0.15, anchor="center")

    date_frame = tk.Frame(inner_frame, bg="#ffffff")
    date_frame.place(x=2, rely=0.5, anchor="w")

    date_lb = tk.Label(date_frame, text='Select Date:', bg="#ffffff", fg='black', font=('Bold', 14))
    date_lb.pack(side='left')

    from_date_lb = tk.Label(date_frame, text='From:', bg="#ffffff", fg='black', font=('Bold', 14))
    from_date_lb.pack(side='left', padx=5)

    from_date_entry = tk.Entry(date_frame, width=10, font=('Bold', 14))
    from_date_entry.pack(side='left', padx=5)

    to_date_lb = tk.Label(date_frame, text='To:', bg="#ffffff", fg='black', font=('Bold', 14))
    to_date_lb.pack(side='left', padx=5)

    to_date_entry = tk.Entry(date_frame, width=10, font=('Bold', 14))
    to_date_entry.pack(side='left', padx=5)

    reason_frame = tk.Frame(inner_frame, bg="#ffffff")
    reason_frame.place(x=2, rely=0.55, anchor="w")

    reason_lb = tk.Label(reason_frame, text='Select Reason:', bg="#ffffff", fg='black', font=('Bold', 14))
    reason_lb.pack(side='left')

    reason_var = tk.StringVar()
    reason_var.set("Select Reason")

    reason_option = tk.OptionMenu(reason_frame, reason_var, "Select Reason", "Family Emergency", "Medical Emergency", "Personal Reasons", "Other")
    reason_option.pack(side='left', padx=5)

    other_reason_frame = tk.Frame(inner_frame, bg="#ffffff")
    other_reason_frame.place(x=2, rely=0.6, anchor="w")

    other_reason_lb = tk.Label(other_reason_frame, text='Other Reason:', bg="#ffffff", fg='black', font=('Bold', 14))
    other_reason_lb.pack(side='left')

    other_reason_entry = tk.Entry(other_reason_frame, width=20, font=('Bold', 14))
    other_reason_entry.pack(side='left', padx=5)

    button_frame = tk.Frame(inner_frame, bg="#ffffff")
    button_frame.place(x=2, rely=0.65, anchor="w")

    def submit_application():
        from_date = from_date_entry.get()
        to_date = to_date_entry.get()
        reason = reason_var.get()
        if reason == "Other":
            reason = other_reason_entry.get()
        print(f"Application submitted: From {from_date} to {to_date} for reason {reason}")
        apply_for_leave_frame.destroy()
        student_dashboard_page()

    submit_button = tk.Button(button_frame, text='Submit', bg="#87CEEB", fg='white', font=('Bold', 14), command=submit_application)
    submit_button.pack(side='left', padx=5)

    back_button = tk.Button(button_frame, text='Back', bg="#87CEEB", fg='white', font=('Bold', 14), command=student_dashboard_page)
    back_button.pack(side='left', padx=5)

# Initialize the root window
root = tk.Tk()
root.title("CampusConnect")
root.geometry("1000x700")

# Start the application with the welcome page
welcome_page()
root.mainloop()
