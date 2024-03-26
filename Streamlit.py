import streamlit as st
import mysql.connector
import pandas as pd

config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database':'project'
}

def create_connection():
    """Create a connection to the MySQL database."""
    db = mysql.connector.connect(**config)
    return db

def insert_student_record(db, ID, Name, contact, section, AID ):
    """Insert a new student record into the 'students' table."""
    cursor = db.cursor()

    cursor.execute("USE project")
    
    insert_student_query = """
    INSERT INTO student (ID, Name, contact, AID, section)
    VALUES (%s, %s, %s, %s, %s)
    """
    student_data = (ID, Name, contact,AID,section)
    cursor.execute(insert_student_query, student_data)

    insert_attendance_query = """
    INSERT INTO attendance (ID, dbms,AID)
    VALUES (%s, %s, %s)
    """
    student_data = (ID, '0', AID)
    cursor.execute(insert_attendance_query, student_data)
    
    insert_login_query = """
    INSERT INTO student_login (ID,password1)
    VALUES (%s, %s)
    """
    student_data = (ID,ID)
    cursor.execute(insert_login_query, student_data)

    db.commit()
    st.write("Student record inserted successfully.") 

def delete_student_record(db,delete_value):
    """Delete a student record from the 'student' table based on ID, name"""
    cursor = db.cursor()
    cursor.execute("USE project")
    delete_patient_query = "DELETE FROM student_login WHERE id = %s"
    cursor.execute(delete_patient_query, (delete_value,))
    cursor.execute("USE project")
    delete_patient_query = "DELETE FROM attendance WHERE id = %s"
    cursor.execute(delete_patient_query, (delete_value,))
    delete_patient_query = "DELETE FROM student WHERE id = %s"
    
    cursor.execute(delete_patient_query, (delete_value,))
    db.commit()
    st.write("Student record deleted successfully.")

def update_attendence(db, ID):

    cursor = db.cursor()

    cursor.execute("USE project")

    select_query = """
    SELECT dbms
    FROM attendance where id = %s
    """
    cursor.execute(select_query,(ID,))
    record = cursor.fetchone()
    if(record == None):
       st.write("Student don't exist")
    else:
        update_student_query = """
        UPDATE attendance
        SET dbms = %s
        WHERE id = %s
        """
        student_data = (str(record[0]+1),ID)
        cursor.execute(update_student_query, student_data)
        db.commit()
        st.write("student record updated successfully.")

def fetch_all_Students(db):
    cursor = db.cursor()

    cursor.execute("USE project")
    select_query = """
    SELECT student.id, name, contact,section,attendance.dbms
    FROM student inner join attendance on student.id = attendance.id
    """
    cursor.execute(select_query)
    records = cursor.fetchall()

    if records:
        st.subheader("All Students")
        df = pd.DataFrame(records, columns=['ID        ', 'Name      ', 'Contact     ', 'Section      ','DBMS'])
        st.dataframe(df)
        
    else:
        st.write("No students found")  


def show_main_page():
    menu = ["Attendance"]
    st.title("Welcome Back!!  " + st.session_state['username'])
    db = create_connection()
    cursor = db.cursor()

    cursor.execute("USE project")
    select_query = """
    SELECT attendance.dbms
    FROM student inner join attendance on student.id = attendance.id
    where student.id = %s
    """
    cursor.execute(select_query,(st.session_state['username'],))
    records = cursor.fetchone()
    st.write("Your DBMS ATTENDANCE IS "+str(records[0])+"%")
    show_logout_page()

def show_main_page2():
    st.title("Welcome Back!! ")
    db = create_connection()
    menu = ["All students","Add Student","Delete Student","Update Attendance","Logout"]
    options = st.sidebar.radio("Select an Option:",menu)

    
    if options == "All students":
        fetch_all_Students(db)
    elif options == "Add Student":
       
       st.subheader("Enter Student details :")
       ID = st.text_input("Enter ID of student",key = "ID")
       Name = st.text_input("Enter name of student",key = "Name")
       contact = st.text_input("Enter contact of student",key = "contact")
       section = st.text_input("Enter section of student",key = "section")
       AID = st.text_input("Enter your Admin id",key = "AID")

       if st.button("add student record"):
          cursor = db.cursor()
          select_query = """
          SELECT * FROM student WHERE ID=%s
          """
          cursor.execute(select_query,(contact,))
          existing_patient = cursor.fetchone()
          if existing_patient:
            st.warning("A student with the same id already exist")
          else:  
            insert_student_record(db, ID, Name, contact, section, AID)

    elif options=="Delete Student":
        delete_value = st.text_input("Enter delete value", key="delete_value")
        if st.button("Delete"):
            delete_student_record(db,delete_value)
       
    elif options == "Update Attendance":
        st.subheader("Enter Student details :")
        ID = st.text_input("Enter ID of student",key = "ID")
        if st.button("add student attendance"):
            update_attendence(db, ID)
    elif options == "Logout":
        st.session_state['ADMIN'] = 0
        show_logout_page()
    db.close()
    
        
def LoggedOut_Clicked():
    st.session_state['loggedIn'] = False
    
def show_logout_page():
    st.button ("Log Out", key="logout", on_click=LoggedOut_Clicked)
    
def LoggedIn_Clicked(userName, password):
    flag = 1
    if (userName is None):
        flag = 0
    select_student_query = "select id,password1 from student_login where id like %s"
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    cursor.execute("USE project")
    cursor.execute(select_student_query, (userName,))
    student = cursor.fetchone()
    X = 1
    if(student is None):
        flag = 0
        X =0
    if(X):
        if(student[1] != password):
            flag = 0
    print(userName,password)
    if(userName == "ADMIN" and password == "ADMIN"):
        st.session_state['admin'] = 1
        flag = 1
    if(flag):
        st.session_state['loggedIn'] = True
    else:
        st.session_state['loggedIn'] = False
        st.error("Invalid user name or password")
    
def show_login_page():
    st.title("LOGIN")
    if st.session_state['loggedIn'] == False:
        userName = st.text_input (label="", value="", placeholder="Enter your user name")
        st.session_state['username'] = userName
        password = st.text_input (label="", value="",placeholder="Enter password", type="password")
        st.button ("Login", on_click=LoggedIn_Clicked, args= (userName, password))


def main():
    if 'loggedIn' not in st.session_state:
        st.session_state['admin'] = 0
        st.session_state['loggedIn'] = False
        show_login_page() 
    else:
        if st.session_state['loggedIn']:
            if st.session_state['admin'] == 1:
                show_main_page2()   
            else:
                show_main_page()  
        else:
            show_login_page() 
if __name__ == "__main__":
    main()








