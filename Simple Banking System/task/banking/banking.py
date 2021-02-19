# Write your code here
import secrets
import string
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS card(
id INTEGER,
number TEXT,
pin TEXT,
balance INTEGER DEFAULT 0)""")
conn.commit()


def luhn(in_num):
    in_num = [int(in_num[i]) * 2 if i % 2 == 0 else int(in_num[i]) for i in range(len(in_num))]
    in_num = sum([x - 9 if x > 9 else x for x in in_num])
    return str(10 - in_num % 10) if in_num % 10 else str(0)


accounts = {}
flag = 0
user_num = 0
while 1:
    choice = input("""1. Create an account
2. Log into account
0. Exit
""")
    print()
    if choice == "0":
        print("Bye!")
        break
    elif choice == "1":
        user_num += 1
        credit_card_num = "400000" + "".join(secrets.choice(string.digits) for _ in range(9))
        credit_card_num = credit_card_num + luhn(credit_card_num)
        pin = "".join(secrets.choice(string.digits) for _ in range(4))
        bal = 0
        cur.execute("INSERT INTO card VALUES ({}, {}, {}, {})".format(user_num, credit_card_num, pin, bal))
        print("""Your card has been created
Your card number:
{}
Your card PIN:
{}\n""".format(credit_card_num, pin))
        accounts[credit_card_num] = {"pin": pin, "balance": bal}
        conn.commit()
    elif choice == "2":
        cc_num = input("Enter your card number:\n")
        peen = input("Enter your PIN:\n")
        print()
        if cc_num not in accounts.keys() or peen != accounts[cc_num]["pin"]:
            print("Wrong card number or PIN:\n")
            continue
        print('You have successfully logged in!\n')
        while 1:
            acc_choice = input("""1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit
""")
            print()
            if acc_choice == "0":
                flag = 1
                break
            elif acc_choice == "1":
                cur.execute("SELECT balance FROM card WHERE number = {}".format(cc_num))
                print("Balance: {}\n".format(cur.fetchone()[0]))
            elif acc_choice == "2":
                cur.execute("SELECT balance FROM card WHERE number = {}".format(cc_num))
                bal = cur.fetchone()[0] + int(input("Enter income:\n"))
                print(bal)
                cur.execute("""UPDATE card
                SET balance = {}
                WHERE number = {}""".format(bal, cc_num))
                conn.commit()
                print("Income was added!\n")
            elif acc_choice == "3":
                dest_card = input("Transfer\nEnter card number:\n")
                if cc_num == dest_card:
                    print("You can't transfer money to the same account!\n")
                    continue
                if luhn(dest_card) != "0":
                    print("Probably you made a mistake in the card number. Please try again!\n")
                else:
                    cur.execute("SELECT balance FROM card WHERE number = {}".format(dest_card))
                    dest_balance = cur.fetchone()
                    if not dest_balance:
                        print("Such a card does not exist\n")
                    else:
                        cur.execute("SELECT balance FROM card WHERE number = {}".format(cc_num))
                        source_balance = cur.fetchone()[0]
                        transfer_amount = int(input("Enter how much money you want to transfer:\n"))
                        if source_balance < transfer_amount:
                            print("Not enough money!\n")
                        else:
                            dest_balance = dest_balance[0]
                            sent = source_balance - transfer_amount
                            received = dest_balance + transfer_amount
                            cur.execute("UPDATE card SET balance = {} WHERE number = {}".format(received, dest_card))
                            cur.execute("UPDATE card SET balance = {} WHERE number = {}".format(sent, cc_num))
                            conn.commit()
                            print("Success!\n")
            elif acc_choice == "4":
                cur.execute("DELETE FROM card WHERE number = {}".format(cc_num))
                print("The account has been closed!\n")
                conn.commit()
                break
            elif acc_choice == "5":
                print("You have successfully logged out!\n")
                break
        if flag:
            break
