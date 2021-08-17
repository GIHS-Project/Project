print("Importing Libraries..")
import random
import pandas as pd
import matplotlib.pyplot as pl
import mysql.connector as myconn
info = pd.read_csv('Pokemons.csv')
df = pd.DataFrame(info)
print("MySQL:Connecting to Database")
sql=myconn.connect(host="localhost",user="root",passwd="12345678",database="project")
mycon=sql.cursor()
if sql.is_connected():
    print("MySQL: Connected")
else:
    print("MySQL: Unable to connect")

def Startup():
    print("Welcome")
    print("1.Login\n2.Signup")
    r=int(input())
    if r==2:
        Signup()
    
def Signup():
    print("******Signup******")
    print("Create a User_name")
    n_user=input()
    print("Create Password")
    n_passwd=input()
    print("Confirm Password")
    c_passwd=input()
    if len(n_passwd)<8:
        print("Password must contain atleast 8 characters.")
    elif n_passwd!=c_passwd:
        print("Passwords don't match.")
    else:
        try:
            insert_user=(f"insert into Users value('{n_user}','{n_passwd}',50)")
            mycon.execute(insert_user)
            create_table=(f"create table {n_user}(Name varchar(25),Type_1 varchar(20),Type_2 varchar(20),Total int,Health_Points int,Attack int,Defense int,Special_Attack int,Special_defense int,Speed int,Generation int,Legendery char(5));")
            mycon.execute(create_table)
            sql.commit()
            print("Successfuly created an account.")
        except:
            print("User_name already taken.\nTry again")
def Login():
    print("*******Login*******")
    print("Enter Username")
    user=input()
    print("Enter Password")
    pa=input()
    passwd=(f"('{pa}',)")
    mycon.execute(f"select password from users where User_name='{user}';")
    mypass=mycon.fetchone()
    print(mypass)
    print(user,mypass,passwd)
    if passwd != mypass:
        print("Incorrect User_name or Password")
        Login()
    else:
        print(f"Signed in as {user}")
        return(user)
def Main():
    print(f"welcome,{user_name}")
    print("Choose an option from below to Continue:")
    print("1.Take a Draw for pokemones.")
    print("2.View all your pokemones.")#m_stephin
    print("3.Match.")
    print("4.Check my balance.")#JJ
def random_poki():
    print("Your Coins:{coins}")
    print("Cost per draw: 1 coin")
    print("Enter the number of draw u would like to take.")
    a = int(input())
    y = 1
    for i in range(0, a):
        x = random.randint(1, 799)
        name=df.iloc[x,1]
        type_1=df.iloc[x,2]
        type_2=df.iloc[x,3]
        total=df.iloc[x,4]
        hp=df.iloc[x,5]
        attack=df.iloc[x,6]
        defense=df.iloc[x,7]
        sp_atk=df.iloc[x,8]
        sp_def=df.iloc[x,9]
        speed=df.iloc[x,10]
        generation=df.iloc[x,11]
        print("Draw No ", y,f": {name}")
        ids=['Total', 'Health', 'Attack', 'Defense', 'special_attack', 'Special_Defense', 'Speed']
        values=[total,hp,attack,defense,sp_atk,sp_def,speed]
        insert=(f"insert into {user_name} value('{name}','{type_1}','{type_2}',{total},{hp},{attack},{defense},{sp_atk},{sp_def},{speed},{generation},'{legendary}')")
        mycon.execute(sql)
        sql.commit()
        y = y+1
        pl.barh(ids,values,)
        if df.iloc[x,12]==True:
            pl.title(f"{df.iloc[x, 1]},Legendary\nGeneration:{df.iloc[x, 11]}")
            pl.show()
        else:
            pl.title(f"{df.iloc[x, 1]}\nGeneration:{df.iloc[x, 11]}")
            pl.show()
Startup()
user_name=Login()
