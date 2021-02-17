# Write your code here
import secrets
import string


def luhn(in_num):
    in_num = [int(in_num[i]) * 2 if i % 2 == 0 else int(in_num[i]) for i in range(len(in_num))]
    in_num = sum([x - 9 if x > 9 else x for x in in_num])
    return str(10 - in_num % 10) if in_num % 10 else str(0)


accounts = {}
flag = 0
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
        credit_card_num = "400000" + "".join(secrets.choice(string.digits) for _ in range(9))
        credit_card_num = credit_card_num + luhn(credit_card_num)
        pin = "".join(secrets.choice(string.digits) for _ in range(4))
        bal = 0
        print("""Your card has been created
Your card number:
{}
Your card PIN:
{}\n""".format(credit_card_num, pin))
        accounts[credit_card_num] = {"pin": pin, "balance": bal}
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
2. Log out
0. Exit
""")
            print()
            if acc_choice == "0":
                flag = 1
                break
            elif acc_choice == "1":
                print("Balance: {}\n".format(bal))
            elif acc_choice == "2":
                print("You have successfully logged out!\n")
                break
        if flag:
            break
