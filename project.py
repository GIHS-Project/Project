print("Importing Libraries..")
import random
import pandas as pd
import matplotlib.pyplot as pl
import mysql.connector as myconn
info = pd.read_csv('Pokemons.csv')
df = pd.DataFrame(info)
pd.set_option('display.max_rows', 800)
pd.set_option('display.max_column', 15)

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
    else:
        pass
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
        Signup()
    elif n_passwd!=c_passwd:
        print("Passwords don't match.")
        Signup()
    else:
        try:
            insert_user=(f"insert into Users value('{n_user}','{n_passwd}',50)")
            mycon.execute(insert_user)
            create_table=(f"create table {n_user}(Name varchar(25),Type_1 varchar(20),Type_2 varchar(20),Total int,Health_Points int,Attack int,Defense int,Special_Attack int,Special_defense int,Speed int,Generation int,Legendery char(5));")
            mycon.execute(create_table)
            sql.commit()
            print("Successfuly created an account.")
        except:
            print("User_name already taken.\nTry another User_name.")
            Signup()
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
        print("****************************")
        print("Error:Account Doesn't Exist")
        Login()
def Main():
    print("================Main Menu================")
    print("Choose an option from below to Continue:")
    print("1.Take a Draw for pokemones.")
    print("2.View your pokemones.")
    print("3.Match.")
    print("4.Check my balance.")
    #print("5.Sell your pokemones")
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
        Match()
        Main()
    if response == 4:
        print("*********************************************")
        print("Your Balance: ",coin())
        print("*********************************************")
        input("Press enter to continue..")
        Main()
    #if response == 5:
    #    sell_pokemone()
    #    Main()
    if response ==5:
        print("Thankyou for using the program")
def random_poki():
    mycoin=coin()
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
def Pokemones():
    print("===========View Pokemones===========")
    print("1.See names of all your pokemones.")
    print("2.See names of all your Legendery Pokemones")
    print("3.See full details of all your pokemones")
    print("4.See all the pokemones in the server")
    r=int(input("Select an option: "))
    if r == 1:
        pk=pd.read_sql(f"select Name,total from {user} order by total",sql)
        print(pk)
        input("Press Enter to continue...")
        Main()
    if r == 2:
        print(pd.read_sql(f"select name,total from {user} where legendery='true' order by total",sql))
        input("Press Enter to continue...")
        Main()
    if r == 3:
        pk=pd.read_sql(f"select * from {user} order by total",sql)
        print(pk)
        input("Press Enter to continue...")
        Main()
    if r == 4:
        print(df)
def sell_pokemone():
    mycoin=coin()
    pk=pd.read_sql(f"select * from {user} order by total;",sql)
    print(pk)
    try:
        no=int((input("Select the Pokemone you wish to sell: ")))
    except:
        print("expected input was as integer")
    name=pk.iloc[no,0]
    gen=pk.iloc[no,10]
    sell=(f'delete from {user} where name="{name}"')
    mycon.execute(sell)
    if gen==1:
        gain=0.36
    if gen==2:
        gain=0.41
    if gen==3:
        gain=0.50
    if gen==4:
        gain=0.62
    if gen==5:
        gain=0.78
    if gen==6:
        gain=0.95
    balance=mycoin+gain
    refund=(f"update users set coins={balance} where User_name='{user}")
    mycon.execute(refund)
    sql.commit()
    print("*******************************************")
    print(f"{name} was sold.")
    print(f"{gain} have been credited to your account.")
    print("*******************************************")
    Main()
def Match():
    print("===========Match===========")
    print("1.Practice - Free")
    print("2.Match - Entry fee :2,double back after win")
    print("3.Match -Hard Mode- Entry fee :5, double back after win")
    try:
        r=int((input("Select Your Pokemone: ")))
    except:
        print("expected input was as integer")
    if r == 1:
        Practice()
    if r == 2:
        normal_Match()
    if r == 3:
        hard_match()
def Base_Match():
    pk=pd.read_sql(f"select * from {user} order by total;",sql)
    lists=mycon.execute(f"select * from {user} order by total;")
    print(lists)
    try:
        u=int((input("Select Your Pokemone: ")))
    except:
        print("expected input was as integer")
    my_name=pk.iloc[u,0]
    my_hp=pk.iloc[u,4]
    my_attack=pk.iloc[u,5]
    my_defense=pk.iloc[u,6]
    my_sp_atk=pk.iloc[u,7]
    my_sp_def=pk.iloc[u,8]
    my_speed=pk.iloc[u,9]
    x = random.randint(1, 799)
    name=df.iloc[x,1]
    hp=df.iloc[x,5]
    attack=df.iloc[x,6]
    defense=df.iloc[x,7]
    sp_atk=df.iloc[x,8]
    sp_def=df.iloc[x,9]
    speed=df.iloc[x,10]
    print("******************************")
    print("Your pokemone:")
    print("Name: ",my_name)
    print("Health Points: ",my_hp)
    print("Attack: ",my_attack)
    print("Defence: ",my_defense)
    print("Special_Attack:",my_sp_atk)
    print("Special_Defence:",my_sp_def)
    print("Speed: ",my_speed)
    print("******************************")
    print("Opponent:")
    print("Name: ",name)
    print("Health Points: ",hp)
    print("Attack: ",attack)
    print("Defence: ",defense)
    print("Special_Attack:",sp_atk)
    print("Special_Defence:",sp_def)
    print("Speed: ",speed)
    print("******************************")
    while hp>0 and my_hp>0:
        print("1.Attack")
        print("2.special_Attack")
        print("3.Special_Attack charge")
        print("4.defence charge")
        print("5.Special_Defence")
        try:
            x=int(input("Enter Your Move: "))
        except:
            print("*****************************")
            print("Enter a integer in range 1-5")
            print("*****************************")
        print("**************************************************")
        if x == 1:
            print("You:Attack")
            y=random.randint(1,3)
            if y==1:
                print('Opponent: Special Deffence')
                a=sp_def/2
                my_hp=my_hp-a
                b=my_attack-sp_def
                if b>=0:
                    hp-b
                elif b<0:
                    my_hp-abs(b/8)
                    hp-my_attack/8
            if y==2:
                print("Opponent: Attack")
                a=my_attack-attack
                if a<0:
                    my_hp-abs(a)
                if a>=0:
                    hp-a
            if y==3:
                print("Opponent:Defence")
                a=my_attack-defense
                if a>=0:
                    hp-a
                if a<0:
                    b=defense/4
                    my_hp-b
        if x == 2:
            print("You: Special Attack")
            y=random.randint(1,3)
            if y == 1:
                print("Opponent: Special Defence")
                a=sp_def/2
                my_hp=my_hp-a
                b=my_sp_atk-sp_def
                if b>=0:
                    hp=hp-b
                elif b<0:
                    my_hp=my_hp-abs(b/8)
                    hp=hp-my_attack/8
            if y == 2:
                print("Opponent:Defence")
                a=my_sp_atk-defense
                if a>=0:
                    hp=hp-a
                if a<0:
                    b=defense/4
                    my_hp=my_hp-b
            if y == 3:
                print("Opponent: Special Attack")
                a=my_sp_atk-sp_atk
                if a>0:
                    hp=hp-a
                if a<0:
                    my_hp=my_hp-abs(a)
        if x == 3:
            print("You: Run & Special_Attack")
            y=random.randint(1,3)
            if y==1:
                print("Opponent: Special Defence")
                a=my_sp_atk+(speed//3)
                b=a-sp_def
                if b>0:
                    hp=hp-b//2
                if b<0:
                    my_hp=my_hp-abs(b)-(speed//4)
            if y==2:
                print("Opponent: deffence")
                a=my_sp_atk+(speed//3)
                b=a-defense
                if b>0:
                    hp=hp-b
                    my_hp=my_hp-(a//6)
                if b<0:
                    my_hp=my_hp-abs(b)-(speed//4)
            if y==3:
                print("Opponent: Attack")
                a=my_sp_atk+(speed//3)
                hp=hp-speed
                my_hp=my_hp-(speed//2)
        if x == 4:
            print("You: deffence charge")
            y=random.randint(1,3)
            if y==1:
                print("Opponent: knockdown")
                a=(defense+speed)//5
                hp=hp-a
            if y==2 or 3:
                print("Opponent: Special Attack")
                my_hp=my_hp-(sp_atk-speed)
                hp=hp-my_sp_atk-speed//2
        if x == 5:
            print("You: Special Defence")
            y=random.randint(1,3)
            if y==1:
                print("Opponent: Special Attack Charge")
                a=sp_atk+speed
                b=my_sp_def-a
                if b<0:
                    my_hp=my_hp-a
                if b>0:
                    hp=hp-my_sp_def
            if y==2 or 3:
                print("Opponent: Special Defence")
                my_hp=my_hp-5
                hp=hp-5
        if my_hp<0:
            my_hp=0
        if hp<0:
            hp=0
        print("**************************************************")
        print(f"your HP:{my_hp}                 Opponent HP:{hp}")
        print("**************************************************")
    if hp<=0 and my_hp<=0:
        result=1
    elif my_hp<=0:
        result=2
    elif hp<=0:
        result=3
    return(result)
def Practice():
    result=Base_Match()
    if result == 1:
        print("**********")
        print("   Draw!  ")
        print("**********")
        Main()
    if result == 2:
        print("**********")
        print("*  Lost! *")
        print("**********")
        Main()
    if result == 3:
        print("**********")
        print("*  Won!  *")
        print("**********")
        Main()
def normal_Match():
    result=Base_Match()
    mycoin=coin()
    if result==1:
        print("**********")
        print("   Draw!  ")
        print("**********")
    if result==2:
        print("**********")
        print(" You Lost ")
        print("**********")
        mycon.execute(f"update users set coins={mycoin-2} where User_name='{user}';")
        sql.commit
    if result==3:
        print("**********")
        print(" You Won ")
        print("**********")
        mycon.execute(f"update users set coins={mycoin+2} where User_name='{user}';")
        sql.commit
    Main()
def hard_match():
    result=Base_Match()
    mycoin=coin()
    if result==1:
        print("**********")
        print("   Draw!  ")
        print("**********")
    if result==2:
        print("**********")
        print(" You Lost ")
        print("**********")
        mycon.execute(f"update users set coins={mycoin-5} where User_name='{user}';")
        sql.commit
    if result==3:
        print("**********")
        print(" You Won ")
        print("**********")
        mycon.execute(f"update users set coins={mycoin+5} where User_name='{user}';")
        sql.commit
    Main()
Startup()
user=Login()
Main()