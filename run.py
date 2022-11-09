from datetime import datetime
from getpass import getpass
from authorize import Account, Transaction

MERCHANT_ACCOUNTS = ('mcdonalds', 'bobs')
USER_ACCOUNTS = [Account(available_limit=1000), Account(available_limit=1000)]
USER_ACCOUNTS[1].history = [Transaction(merchant='bobs',
                                        amount=1500,
                                        time=datetime.now().timestamp()-120),
                            Transaction(merchant='mcdonalds',
                                        amount=1000,
                                        time=datetime.now().timestamp())]


def validate_pass(account, password):
    # TODO: write password validation
    return True


def main():
    print("Welcome to transaction authorizer.\n")

    merchant = ""
    while True:
        merchant = input("Merchant account:")
        password = getpass()
        if merchant.lower() in MERCHANT_ACCOUNTS and validate_pass(merchant, password):
            break
        print("Invalid merchant, try again\n")

    client_id = -1
    while True:
        try:
            client_id = int(input("Input client id:"))
            if 0 <= client_id < len(USER_ACCOUNTS):
                break
            print("This client id is invalid.")
        except ValueError:
            print("You must type a number.\n")

    client = USER_ACCOUNTS[client_id]

    while True:
        print(
            f"Client {client_id}'s available limit: {client.available_limit}.\n")
        action = input(
            f"Type anything to charge a new transaction to client {client_id}. "
            "Press enter without typing to close the terminal.\n")
        if not action:
            print("Thanks for testing the system!")
            return

        amount = 0
        try:
            reais, cents = map(int, input("Input the amount as a decimal"
                                          " number: \nR$ ").split('.'))
            amount = reais * 100 + cents
        except ValueError:
            print("Something went wrong when reading the transaction value. "
                  "Please try again.")
            continue

        result = client.authorize(Transaction(merchant=merchant,
                                              amount=amount,
                                              time=datetime.now().timestamp()))
        if result['violations']:
            print("Adding the transaction failed. Violation(s):")
            for violation in result['violations']:
                print(violation())
        else:
            print("Successfully charged the client.")
        print("The system is ready to add more transactions.\n")


if __name__ == '__main__':
    main()
