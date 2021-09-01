print("Importing Libraries..")
import random
from numpy import select
import pandas as pd
import matplotlib.pyplot as pl
import mysql.connector as myconn
info = pd.read_csv('Pokemons.csv')
df = pd.DataFrame(info)
print("MySQL:Connecting to Database")
try:
    sql=myconn.connect(host="localhost",user="root",passwd="12345678",database="project")
    mycon=sql.cursor()
    if sql.is_connected():
        print("MySQL: Connected")
    else:
        print("MySQL: Unable to connect")
except:
    print("MySQL: Connection Error")
    print("Check your Mysql Config.")
    quit()
def Startup():
    print("==========Pokemones==========")
    print("1.Login\n2.Signup")
    try:
        r=int(input("Select an option: "))
    except:
        print("Expected an integer.")
        Startup()
    if r==2:
        Signup()
def coin():
    mycon.execute(f"select Coins from users where User_name='{user}';")
    coins=mycon.fetchone()
    for i in coins:
        mycoins=i
    return(mycoins)
def Signup():
    print("******Signup******")
    n_user=input("Create a User_name: ")
    n_passwd=input("Create Password: ")
    c_passwd=input("Confirm Password: ")
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
    user=input("Enter Username: ")
    passwd=input("Enter Password: ")
    mycon.execute(f"select password from users where User_name='{user}';")
    mypassd=mycon.fetchone()
    try:
        for i in mypassd:
            mypass=i
        if passwd != mypass:
            print("Incorrect User_name or Password")
            Login()
        else:
            print(f"Signed in as {user}")
        return(user)
    except:
        print("Error:Account Doesn't Exist")
        Login()
def Main():
    print("===========Main Menu===========")
    print("Choose an option from below to Continue:")
    print("1.Take a Draw for pokemones.")
    print("2.View your pokemones.")#m_stephin
    print("3.Match.")
    print("4.Check my balance.")#JJ
    print("5.Close")
    try:
        response=int(input("Select an option: "))
    except:
        print("Expected an integer.")
        Main()
    if response==1:
        random_poki()
        Main()
    if response ==2:
        Pokemones()
        Main()
    if response ==3:
        print("Match")
        Main()
    if response == 4:
        print(coin())
        input("Press enter to continue..")
        Main()
    if response ==5:
        quit()
def random_poki():
    print("=======Pokemone_Draw=======")
    print(f"Your Coins:{mycoin}")
    print("Cost per draw: 1 coin")
    print("Enter the number of draw u would like to take.")
    a = int(input())
    if a>coin():
        print(f"U donot have enough Coins to make {a} draws!")
        random_poki()
    else:
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
            legendary=df.iloc[x,12]
            print("Draw No ", y,f": {name}")
            ids=['Total', 'Health', 'Attack', 'Defense', 'special_attack', 'Special_Defense', 'Speed']
            values=[total,hp,attack,defense,sp_atk,sp_def,speed]
            insert=(f"insert into {user} value('{name}','{type_1}','{type_2}',{total},{hp},{attack},{defense},{sp_atk},{sp_def},{speed},{generation},'{legendary}')")
            mycon.execute(insert)
            sql.commit()
            y = y+1
            pl.barh(ids,values,)
            if df.iloc[x,12]==True:
                pl.title(f"{df.iloc[x, 1]},Legendary\nGeneration:{df.iloc[x, 11]}")
                pl.show()
            else:
                pl.title(f"{df.iloc[x, 1]}\nGeneration:{df.iloc[x, 11]}")
                pl.show()
        balance=mycoin-(y-1)
        new_balance=(f"update users set coins={balance} where User_name='{user}'")
        mycon.execute(new_balance)
        sql.commit()
    Main()
def Pokemones():
    print("===========View Pokemones===========")
    print("1.See names of all your pokemones.")
    print("2.See names of all your Legendery Pokemones")
    print("3.see full details of all your pokemones")
    r=int(input())
    if r == 1:
        pokemones=pd.read_sql(f"select Name,total from {user} order by total",sql)
        print(pokemones)
        Main()
    if r == 2:
        pokemones=pd.read_sql(f"select name,total from {user} where legendery='true' order by total",sql)
        print(pokemones)
        Main()
    if r == 3:
        pokemones=pd.read_sql(f"select * from {user} order by total",sql)
        print(pokemones)
        Main()
def Match():
    print("===========Match===========")
    print("1.Practice - Free")
    print("2.Match - Entry fee :2,double back after win")
    print("3.Match -Hard Mode- Entry fee :5, double back after win")
def Practice_Match():
    print("===========Practice===========")
    print("Select your pokemone:")

Startup()
user=Login()
mycoin=coin()
Main()