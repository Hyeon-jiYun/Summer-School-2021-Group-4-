import random
import datetime as datetime
from numpy import str_
import pandas as pd
import os
import csv
import webbrowser
import smtplib
from email.message import EmailMessage

path = os.path.dirname(__file__)
print(path)

df = pd.read_excel(path + "\Drugs_globaldatabase.xls") ## Read the Global Medicine Database provided by Kaggle
print(df)


class Medicine:
    def __init__(self): ## OOP: class definition
        self.name = ""
        self.QR_code = None
        self.purchase_date = ""
        self.expire_date = "" ## The name, QR code, purchase date and expriation date are empty because they will be defined by the methods below.

    def set_QR_code(self, df):## Takes as an input the Global Medicine Database
        while True:
            print("Please insert here your QR code") ## Ask the user to manually enter a medicine product ID
            qr = input()
            if qr not in df.values:
                print("There is an error, QR code is not in recognised, try again")
            elif qr in df.values:
                self.QR_code = qr
                break
        return self.QR_code

    def get_QR_code(self):
        return self.QR_code

    def get_name(self, df): ## Takes the Global Medicine Database as an input and returns the name of the medicine associated with the product ID just inserted by the user
        qr = self.get_QR_code()
        line = df[df["Product ID"] == qr]
        self.name = line.iloc[0]["Drug Name"]
        return self.name, self.QR_code

    def get_purchase_date(self): ## The purchase date is randomized by assuming that the medicines we have at home were bought in the last one year and a half
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=548)
        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        random_date = start_date + datetime.timedelta(days=random_number_of_days)
        self.purchase_date = random_date
        return self.purchase_date

    def get_expire_date(self): ## By convention, the expiration date is set twelve months after the purchase date
        self.expire_date = self.purchase_date + datetime.timedelta(days=365)
        return self.expire_date


my_list = [] ## The list will contain all the medicine objects the user has at home
def add_medicine():
    medicine = Medicine()
    medicine.set_QR_code(df)
    medicine.get_name(df)
    medicine.get_purchase_date()
    medicine.get_expire_date()
    my_list.append(medicine) ## The medicine object is appended to the list


def prompt_user_to_add_medicine(): ## This function simplifies the process of asking users wheter they want to add a new medicine to their Medibox
    while True:
        print("Do you want to add a medicine to your medibox? Y/N")
        answer = input()
        if answer.upper() == "Y":
            add_medicine()
        elif answer.upper() == "N":
            break
        else:
            print("Please enter only Y or N")        


def update_table(): ## This function convertts the list of medicine objects (i.e., my_list) into a cvs file (i.e., medibox.csv)
    with open(path + "\medibox.csv", "w", newline="") as file:

        writer = csv.writer(file)
        writer.writerow(["Product ID", "Drug Name", "Purchase Date", "Expire Date"])

        for med in my_list:
            writer.writerow(
                [
                    med.QR_code,
                    med.name,
                    med.purchase_date.strftime("%d.%m.%Y."),
                    med.expire_date.strftime("%d.%m.%Y."),
                ]
            )


def add_new_prescription(): ## This function is used when the user buys a new medicine and adds it to the Medibox
    medicine = Medicine() ## We created a new function similar to the previous add_medicine(). Indeed, in this case, we do not want a randomized purchase date since the medicine is bought today
    medicine.set_QR_code(df)
    medicine.get_name(df)
    medicine.purchase_date = datetime.datetime.today()
    medicine.expire_date = datetime.datetime.today() + datetime.timedelta(days = 365)
    my_list.append(medicine) 


def email_alert(subject,body,to): ## This function defines how to send an email notification to the user when a medicine in his Medibox expires
    msg = EmailMessage()
    msg.set_content(body)
    msg["subject"] = subject
    msg["to"] = to
    user = "ciccio.bisceglie90@gmail.com"
    msg["from"] = user
    password = "vhmbcntzyhvofumk"
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    server.quit()


def signal_error(): ## Note that this code has been writen to be executed in a terminal in which typing errors can occur
    print("Error, answer not recognized. Start again!")

prompt_user_to_add_medicine()
update_table()

print("----------")
print("Please present the doctor's prescription.") ## A list of medicine is prescribed by the doctor 
print("----------")

df2 = pd.read_csv(path + "\medibox.csv") ## My Medibox is accessed and read 

dispose_expired_medicine = "https://www.youtube.com/watch?v=agwaF2kYiUA&t=9s" ## Link of FDA's recommendation video on how to safely dispose of expired medicines

while True:
    prescription = [input("Please enter a medication name: ")] ## !Case-sensitive!
    for medication_name in prescription: ## Iterates through presription list (even though 1 element at the time is checked, we could not solve the loop otherwise)
        buy_medicine_url = "https://www.sunstore.ch/de/catalogsearch/result?q=" + medication_name ## Link redirecting to the sunstore web page with the needed medication
        date_today = datetime.datetime.today() 

        if medication_name in df.values: ## Conditional statement verifying if the medicine exists in the global drugs database 

            if medication_name in df2.values: ## Conditional statement verifying if the medicine exists in My Medibox 
                medication_index = df2[df2["Drug Name"] == medication_name].index.values.astype(int)[0] ## Find the row index in My Medibox for the medication 
                ## note that headers does not count as line AND indexation starts with 0 SO index = table row - 2
                
                ## Check if the medication has expired
                expire_date = datetime.datetime.strptime(df2.at[medication_index, "Expire Date"], "%d.%m.%Y.") ## Find the expiration date   
                purchase_date = datetime.datetime.strptime(df2.at[medication_index, "Purchase Date"], "%d.%m.%Y.") ## Find the purchase date 
                if date_today <= expire_date: ## Conditional statement in the case of an expiration date in the future 
                    days_left = expire_date - purchase_date # Object as time delta object --> must change into days and a str
                    str_days_left = str(days_left.days)
                    print("You already have " + medication_name + ". It expires on " + str(expire_date) + ".You have " + str_days_left + " days left before expiration.") ## The expiration date and the days left until that date are printed
                elif date_today > expire_date: ## Conditional statement in the case of an expiration date in the past, i.e. the medication has expired  
                    new_expiration_date = datetime.datetime.today() + datetime.timedelta(days = 365) ## A new expiration date is given if the medication is re purchased  
                    print("Your " + medication_name + " has expired. Please dispose of it by following the FDA recommendations.") ## The user is informed that the medication is expired and is instructed on how to dispose it safely
                    
                    print("See it NOW or LATER? ") ## The user is given the choice on when to watch the instructions
                    response = input()
                    if response.upper() == "NOW":
                        webbrowser.open(dispose_expired_medicine, new=2) ## The user deciding to watch the instructions now gets a browser page with the FDA's video opened 
                    elif response.upper() == "LATER": ## If the user decides to watch the instructions later, the program moves to the next step
                        pass
                    else: 
                        print("As you didn't enter NOW or LATER, the command wasn't understood. If you are still interested, copy and paste the following link: " + dispose_expired_medicine)
                        ## Note that this code has been written to be executed in a terminal in which typing errors can occur. The corresping application should show buttons with "NOW" and "LATER", whereby the "else" statement would not be of any use. 

                    print("Your " + medication_name + " has expired. Please buy it under the following link: " + buy_medicine_url) ## The user is given a link to re purchase the expired medication 
                    
                    print("Buy it NOW or LATER? ") ## The user is given the choice on when to re purchase the medication
                    answer = input()
                    if answer.upper() == "NOW": ## The user deciding to buy the medication now gets the sunstore web page with the needed medication opened in the browser 
                        webbrowser.open(buy_medicine_url, new=2)
                        
                        print("Did you buy the desired medicine? Y/N")  ## The user is asked if the medication was purchased 
                        buy_medication = input()
                        if buy_medication.upper() == "Y": ## If the medication was purchased, the purchase and expiration date are updated in My Medibox
                            df2.at[medication_index, "Expire Date"] = datetime.datetime.strftime(new_expiration_date, "%d.%m.%Y.")
                            df2.at[medication_index, "Purchase Date"] = datetime.datetime.strftime(date_today, "%d.%m.%Y.") 
                            df2.to_csv(path + "\medibox.csv", index=False)
                            break
                        elif buy_medication.upper() == "N": ## If the medication was NOT purchased, the program moves to the next step
                            break
                        else: ## Note that this code has been written to be executed in a terminal in which typing errors can occur. The corresping application should show buttons with "NOW" and "LATER", whereby the "else" statement would not be of any use.
                            signal_error()
                            break

                    elif answer.upper() == "LATER": ## If the user decides to buy the medication later, the program moves to the next step
                        break
                    else: ## "else" statement would not be of any use in the application --> "NOW" and "LATER" buttons 
                        signal_error()
                        break

            else: ## Conditional statement in the case of medicine NOT already existing in My Medibox 
                print("You don’t have " + medication_name + ". Please buy it under the following link:" + buy_medicine_url) ## The user is informed that the medication is NOT in My Medibox and given a link to purchase it 
                print("Buy it NOW or LATER ") ## The user is given the choice on when to re purchase the medication
                while True: ## The while loop ensures that the user answers the question with "NOW" or "LATER" -> NOT necessary in the application with buttons 
                    ## Note that this loop could only be successfully implemented in this part of the code without breaking the order of the nested if statements 
                    answer = input()
                    if answer.upper() == "NOW": ## The user deciding to buy the medication now gets the sunstore web page with the needed medication opened in the browser
                        webbrowser.open(buy_medicine_url, new=2)

                        print("Did you buy the desired medicine? Y/N") ## The user is asked if the medication was purchased
                        buy_medication = input()
                        if buy_medication.upper() == "Y": ## If the medication was purchased, the medication is added in My Medibox, which file is then updated and saved  
                            add_new_prescription()
                            update_table()
                            df2 = pd.read_csv(path + "\medibox.csv")
                            break
                        elif buy_medication.upper() == "N": ## If the medication was NOT purchased, the program moves to the next step
                            break
                        else: ## "else" statement would not be of any use in the application --> "YES" and "NO" buttons
                            signal_error()
                            break

                    elif answer.upper() == "LATER": ## If the user decides to buy the medication later, the program moves to the next step
                        break
                    else: ## "else" statement would not be of any use in the application --> "NOW" and "LATER" buttons
                        print("Please enter only NOW or LATER") 
        else: ## Conditional statement in the case of medication not existing in the global drugs database 
            print("The medication name does not exist.") 
            break ## The user will be asked again to enter a medication name --> back to the top of the loop 

    print("Do you need anything else? Y/N") ## The user is asked if other medication is needed
    more_medication = input()
    if more_medication.upper() == "N": ## If the prescription does NOT cointain other medication, the program says goodbye, breaks the loop and goes to the next step
        print("Goodbye")
        break
    elif more_medication.upper() == "Y": ## If the prescription DOES cointain other medication, the loop starts again with the entry of a medication name
        continue
    else: ## "else" statement would not be of any use in the application --> "YES" and "NO" buttons
        signal_error()

print("----------")

df2 = pd.read_csv(path + "\medibox.csv") ## The csv file is read again as, through the process, new medicines may have been added to the Medibox or updated
## In the part of code below we implemented a push notification function warning the user that a medicine in his Medibox has expired
for expired_med in df2['Drug Name'].values: ## For each drug in the Medibox, the expiration date is checked 
    date_today = datetime.datetime.today()
    medication_index = df2[df2['Drug Name'] == expired_med].index.values.astype(int)[0]
    expire_date_int = datetime.datetime.strptime(df2.at[medication_index, "Expire Date"], "%d.%m.%Y.")
    while True:
        if date_today > expire_date_int: ## When the current date is after the expiration date of a medicine, a push notification is sent to the user
            print(expire_date_int)
            print (expired_med + " has expired, you should buy a new one.")
            date_today = date_today + datetime.timedelta(days = 1) ## Here, together with the loop, we simulated the passing of time 
            if __name__ == "__main__": ## The email function is recalled and an email is sent to the user 
                email_alert("Expiration alert", expired_med + " just expired today. Buy it at: https://www.sunstore.ch/de/catalogsearch/result?q=. Please dispose of it by following the FDA recommendations: " + dispose_expired_medicine, "ciccio.bisceglie90@gmail.com")
            break
        else:
            date_today = date_today + datetime.timedelta(days = 1)
