from flask import Flask, render_template, request #, jsonify

import mysql.connector
mydb = mysql.connector.connect(host="localhost", user="root", password="Admin@1727!", 
    database= "hospital_management")
mycursor = mydb.cursor(buffered=True)

app = Flask(__name__)

@app.route('/hospital')
def get_home_page():
    return render_template("hospital.html")

@app.route('/summary')
def get_summary_page():
    return render_template("summary.html")

@app.route('/userlogin', methods=["GET", "POST"])
def login():
    User = [] 
    # login_username = request.form.get('username')
    # login_password = request.form.get('password')
    # login = [login_username, login_password]
    mycursor.execute("select txt_User_Name, txt_Password from tbl_users") # where txt_User_Name = %s and txt_Password = %s", (login))
    myresult = mycursor.fetchall()
    for i in myresult:
        User.append(i)
    return User 
    # mycursor.execute("USE hospital_management")
    # login_username = request.form.get('login_username')
    # login_password = request.form.get('login_password')

    # check_login = f"select txt_User_Name from tbl_users where txt_User_Name = '{login_username}'"
    # check_password = f"select txt_Password from tbl_users where txt_Password = '{login_password}'"
    # mycursor.execute(check_login)
    # username_result = mycursor.fetchone()

    # mycursor.execute(check_password)
    # password_result = mycursor.fetchone()

    # password = str(*password_result).replace('', '')
    # username = str(*username_result).replace('', '')
    
    # print(*username, sep=',')
    # print (*username)
    # print (*password)
    # print(*password, sep=',')

    # if login_password == password and login_username == username:
    #     # print("Success")
    #     return render_template("summary.html")
    # else: 
    #     print("Login failed, wrong username or password")
#login()      
@app.route('/login')
def get_login_page():
    return render_template("LoginPage.html")

@app.route('/admin')
def get_admin_page():
    return render_template("AdminPage.html")

@app.route('/newDoctor', methods=["POST"])       #Inserting new records in database using post method
def create_new_doctor():
    global doctor
    Id = request.form.get('Id')
    Name = request.form.get('Name')
    DOB = request.form.get('DOB')
    Gender = request.form.get('Gender')
    Phone = request.form.get('Phone')
    AltPhone = request.form.get('AltPhone')
    Email = request.form.get('Email')
    AltEmail = request.form.get('AltEmail')
    Add1 = request.form.get('Add1')
    Add2 = request.form.get('Add2')
    Add3 = request.form.get('Add3')
    CityId = request.form.get('CityId')
    StateId = request.form.get('StateId')
    CountryId = request.form.get('CountryId')
    EduQua = request.form.get('EduQua')
    Experience = request.form.get('Experience')
    DOJ = request.form.get('DOJ')
    Status = request.form.get('Status')
    Created_By = request.form.get('Created_By')
    Created_Date = request.form.get('Created_Date')
    doctor = [(Name, DOB, Gender, Phone, AltPhone, Email, AltEmail, Add1, Add2, Add3, CityId, StateId, CountryId, EduQua, Experience, DOJ, Status, Created_By, Created_Date)]
    stmt = "Insert into tbl_doctor (txt_Doctor_Name, dte_DOB,txt_Gender, txt_Phone, txt_Alt_Phone, txt_Email, txt_Alt_Email, txt_Address1, txt_Address2,\
    txt_Address3, int_City_Id, int_State_Id, int_Country_Id, txt_Educational_Qualification, int_Experience, dte_DOJ, txt_Status, txt_Created_By, dte_Created_Date) \
    values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    mycursor.executemany(stmt, doctor)
    mydb.commit()
    return ''
 
@app.route("/doctorshift")
def get_doctor_list():  
    doctor = [] 
    mycursor.execute("select * from tbl_doctor")
    myresult = mycursor.fetchall()
    for i in myresult:
        output = {
                'id': i[0],
                'name': i[1]}
        doctor.append(output)
    return doctor    

@app.route("/shift")
def get_shift_list():  
    shift = [] 
    mycursor.execute("select * from tbl_shift")
    myresult = mycursor.fetchall()
    for i in myresult:
        output = {
                'id': i[0],
                'name': i[4]}
        shift.append(output)
    return shift 

@app.route("/patientlist")
def get_patient_list():  
    patient = [] 
    mycursor.execute("select * from tbl_patient")
    myresult = mycursor.fetchall()
    for i in myresult:
        output = {
                'id': i[0],
                'name': i[1]}
        patient.append(output)
    return patient 

@app.route('/assignShiftfordoctor', methods=["POST"])     
def create_new_shift_for_doctor():
    global doctor_shift
    DocId = request.form.get('DocId')
    ShiftId = request.form.get('ShiftId')
    ShiftDt = request.form.get('ShiftDt')
    PatientId = request.form.get('PatientId')
    AttendFlag = request.form.get('AttendFlag')
    
    doctor_shift = [(DocId, ShiftId, ShiftDt, PatientId, AttendFlag)]
    stmt = "Insert into tbl_shiftpatientfordoctor (Doctor_Id, Shift_Id, Shift_Date, Patient_Id, attended_Flag) values(%s, %s, %s, %s, %s)"
    mycursor.executemany(stmt, doctor_shift)
    mydb.commit()
    return ''

@app.route('/loaddoctorshift', methods=["POST","GET"])                          
def get_all_doctorshift():
    all_doc_shift = []
    DoctorId  = request.form.get('DoctorId')
    ShiftId   = request.form.get('ShiftId')
    ShiftDt   = request.form.get('ShiftDt') 
    PatientId = request.form.get('PatientId')
    AttendFlag = request.form.get('AttendFlag')
    
    main_query = "select d.txt_Doctor_Name, s.txt_Shift_Type, sd.Shift_Date, p.txt_Patient_Name, \
                  case when sd.attended_Flag = '2' then 'No' when sd.attended_Flag = '1' then 'Yes' end as AttendedFlag \
                     from tbl_shiftpatientfordoctor sd, tbl_doctor d, tbl_patient p, tbl_shift s \
                     where d.int_Doctor_Id = sd.Doctor_Id and p.int_Patient_Id = sd.Patient_Id and sd.Shift_Id = s.int_Shift_Id"
           
    doctor_clause = ''
    shift_clause = '' 
    date_clause = ''
    patient_clause = ''
    attendFlag_clause = ''
             
    if(DoctorId != '0' and DoctorId != ''):
        doctor_clause = ' and d.int_Doctor_Id = '+ DoctorId 
    
    if(ShiftId != '0' and ShiftId != ''):
        shift_clause = ' and s.int_Shift_Id = '+ ShiftId 
    
    if(ShiftDt != '--' and ShiftDt != ''):
        date_clause = ' and sd.Shift_Date = '+ ShiftDt
        
    if(PatientId != '0' and PatientId != ''):
        patient_clause = ' and p.int_Patient_Id = '+ PatientId 
        
    if(AttendFlag != '0' and AttendFlag != ''):
        attendFlag_clause = ' and sd.attended_Flag = '+ AttendFlag 
        
    final_query = main_query + doctor_clause + shift_clause + date_clause + patient_clause + attendFlag_clause
    
    mycursor.execute(final_query)
    myresult = mycursor.fetchall()
    for i in myresult:
        all_doc_shift.append(i)
       
    return all_doc_shift
   
@app.route("/doctorlist")
def load_doctor_list():
    return render_template("doctorShiftAssign.html")

@app.route("/getnurselist")
def get_nurse_shift_list():  
    nurse = [] 
    mycursor.execute("select * from tbl_nurse")
    myresult = mycursor.fetchall()
    for i in myresult:
        output = {
                'id': i[0],
                'name': i[1]}
        nurse.append(output)
    return nurse    

@app.route('/assignShiftfornurse', methods=["POST"])     
def create_new_shift_for_nurse():
    global nurse_shift
    NurseId = request.form.get('NurseId')
    ShiftId = request.form.get('ShiftId')
    ShiftDt = request.form.get('ShiftDt')
    nurse_shift = [(NurseId, ShiftId, ShiftDt)]
    stmt = "Insert into tbl_shiftfornurse (Nurse_Id, Shift_Id, Shift_Date) values(%s, %s, %s)"
    mycursor.executemany(stmt, nurse_shift)
    mydb.commit()
    return ''

@app.route('/loadnurseshift', methods=["POST","GET"])                          
def get_all_nurse_shift():
    all_nurse_shift = []
    NurseId = request.form.get('NurseId')
    ShiftId = request.form.get('ShiftId')
    ShiftDt = request.form.get('ShiftDt') #CAST(sn.Shift_Date AS date) as Sdate
    
    main_query = "select n.txt_Nurse_Name, s.txt_Shift_Type, sn.Shift_Date AS date \
                        from tbl_shiftfornurse sn, tbl_nurse n, tbl_shift s \
                        where n.int_Nurse_Id = sn.Nurse_Id and sn.Shift_Id = s.int_Shift_Id"       
    nurse_clause = ''
    shift_clause = ''
    date_clause = ''
    
    if(NurseId != '0' and NurseId != ''):
        nurse_clause = ' and n.int_Nurse_Id = '+ NurseId 
    
    if(ShiftId != '0' and ShiftId != ''):
        shift_clause = ' and s.int_Shift_Id = '+ ShiftId 
    
    if(ShiftDt != '--'):
        date_clause = ' and sn.Shift_Date = '+ ShiftDt
        
    final_query = main_query + nurse_clause + shift_clause + date_clause
    
    print(final_query)
    
    mycursor.execute(final_query)
    myresult = mycursor.fetchall()
    for i in myresult:
        all_nurse_shift.append(i)
       
    return all_nurse_shift

#get_all_nurse_shift()
@app.route("/nurselist")
def load_nurse_list():
    return render_template("nurseShiftAssign.html")

app.run(host='0.0.0.0')
