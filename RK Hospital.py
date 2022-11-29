from flask import Flask, render_template, request, jsonify

import mysql.connector
mydb = mysql.connector.connect(host="localhost", user="root", password="Admin@1727!", 
    database= "hospital_management")
mycursor = mydb.cursor(buffered=True)

app = Flask(__name__)
@app.route('/hospital')
def get_home_page():
    return render_template("hospital.html")


@app.route('/login')
def get_login_page():
    return render_template("LoginPage.html")

# @app.route('/summary')
# def get_summary_page():
#     return render_template("summary.html")

@app.route('/userlogin', methods=["POST", "GET"])
def login():
    mycursor.execute("USE hospital_management")
    login_username = request.form.get('login_username')
    login_password = request.form.get('login_password')

    check_login = f"select txt_User_Name from tbl_users where txt_User_Name = '{login_username}'"
    check_password = f"select txt_Password from tbl_users where txt_Password = '{login_password}'"
    mycursor.execute(check_login)
    username_result = mycursor.fetchone()

    mycursor.execute(check_password)
    password_result = mycursor.fetchone()

    password = str(*password_result).replace('', '')
    username = str(*username_result).replace('', '')
    
    # print(*username, sep=',')
    # print (*username)
    # print (*password)
    # print(*password, sep=',')

    if login_password == password and login_username == username:
        # print("Success")
        return render_template("summary.html")
    else: 
        print("Login failed, wrong username or password")
# login()      

# @app.route("/doctor", methods=["POST", "GET"])
# def city():
#     #if request.method == "GET":
#         citys = []
#         mycursor.execute("select * from tbl_city")
#         myresult = mycursor.fetchall()
#         for i in myresult:
#             citys.append(i)
#         # return city
#         return render_template("doctorMaster.html", citys=citys)
 

# @app.route("/doctor",methods=["POST","GET"])
# def ajaxpost():    
#     global city
#     if request.method == 'POST':
#         city = []
#         queryString = request.form['queryString']
#         print(queryString)
#         query = "SELECT * from tbl_city WHERE value LIKE '{}%' LIMIT 10".format(queryString)
#         mycursor.execute(query)
#         mycursor.fetchall()
#     return jsonify({'htmlresponse': render_template('doctorMaster.html', city=city)})

@app.route("/doctor")
def database():
    # c, conn = connectionDB()

    compDB = mycursor.execute("SELECT * FROM tbl_city")
    compDB = mycursor.fetchall()

    return render_template("doctorMaster.html", 
                            compDB = compDB)



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

app.run(host='0.0.0.0')
