from flask import Flask, render_template,url_for,request,redirect
import mysql.connector
import time

mysql = mysql.connector.connect(user='root', password='', host='localhost', database='cse3330')

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        aid = request.form['id']
        name = request.form['name']
        cur = mysql.cursor()
        #retrieve data from database which has the same name as the name input
        cur.execute("SELECT * FROM ARTIST WHERE name = '"+name+"'")
        result = cur.fetchall()
        mysql.commit()
        cur.close()
        return render_template('display.html',result=result)
    else:
        return render_template('index.html')
    
@app.route('/retrieve',methods=['GET','POST'])
def retrieve():
    if request.method == 'POST':
        commission = request.form['commission']
        name = request.form['name']
        city = request.form['city']
        cur = mysql.cursor()
        if city =='' and name =='' and commission =='':
            cur.execute("SELECT * FROM ARTIST")
        elif city =='' and name =='' :
            cur.execute("SELECT * FROM ARTIST WHERE commission = '"+commission+"'")
        elif city =='' and commission =='' :
            cur.execute("SELECT * FROM ARTIST WHERE name = '"+name+"'")
        elif name =='' and commission =='' :
            cur.execute("SELECT * FROM ARTIST WHERE city = '"+city+"'")
        elif city =='' :
            cur.execute("SELECT * FROM ARTIST WHERE name = '"+name+"' AND commission = '"+commission+"'")
        elif name =='' :
            cur.execute("SELECT * FROM ARTIST WHERE commission = '"+commission+"' AND city = '"+city+"'")
        elif commission =='' :
            cur.execute("SELECT * FROM ARTIST WHERE name = '"+name+"' AND city = '"+city+"'")
        else:
            cur.execute("SELECT * FROM ARTIST WHERE name = '"+name+"' AND commission = '"+commission+"' AND city = '"+city+"'")
        result = cur.fetchall()
        mysql.commit()
        cur.close()
        return render_template('display.html',result=result)
    else:
        return render_template('retrieve.html')


@app.route('/add',methods=['GET','POST'])
def add():
    #uptade the data name,birthDate,deathDate,commission,street,city,stateAb,zipCode to the ARTIST table
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['dob']
        commission = request.form['commission']
        street = request.form['street']
        city = request.form['city']
        stateAb = request.form['stateAb']
        zipCode = request.form['zipCode']
        formatted_date = time.strftime('%Y-%m-%d', time.strptime(date, '%Y-%m-%d'))
        #request.form['dod'] and formatted_dod 
        dod = request.form['dod']
        if dod == '':
            formatted_dod = None
        else:
            formatted_dod = time.strftime('%Y-%m-%d', time.strptime(dod, '%Y-%m-%d'))
        cur = mysql.cursor()
        cur.execute("INSERT INTO ARTIST(name,birthDate,deathDate,commission,street,city,stateAb,zipCode) VALUE(%s,%s,%s,%s,%s,%s,%s,%s)",(name,formatted_date,formatted_dod,commission,street,city,stateAb,zipCode))
        mysql.commit()
        cur.close()
    return render_template('add.html')

@app.route('/delete',methods=['GET','POST'])
def delete():
    if request.method == 'POST':
        name = request.form['name']
        zipCode = request.form['zipCode']
        cur = mysql.cursor()
        #delete the data which has the same name as the name input and the same zipCode as the zipCode input
        cur.execute("DELETE FROM ARTIST WHERE name = '"+name+"' AND zipCode = '"+zipCode+"'")
        mysql.commit()
        cur.close()
        return render_template('retrieve.html')
    return render_template('delete.html')

@app.route('/update',methods=['GET','POST'])
def update():
    if request.method == 'POST':
        name = request.form['name']
        zipCode = request.form['zipCode']
        newnmae = request.form['newname']
        cur = mysql.cursor()
        #update the data which has the same name as the name input and the same zipCode as the zipCode input, set the name to the newname
        cur.execute("UPDATE ARTIST SET name = '"+newnmae+"' WHERE name = '"+name+"' AND zipCode = '"+zipCode+"'")
        return render_template('retrieve.html')
    return render_template('update.html')

if __name__ == '__main__':
    app.run(debug=True)
    