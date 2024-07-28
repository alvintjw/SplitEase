import csv
import sys

def main():
    #Take in the input file in Command Line Arguement
    input_file_name = get_input_csv()
    #Read the input file and return the data in a suitable format
    data = read_csv(input_file_name)
    #print(data)
    #Calculate the total amount paid by each person
    total_amount, average_amount = calculate_total_amount(data)
    #print(total_amount)
    instructions = find_optimal_transfers(total_amount, average_amount)
    print("Instructions:")
    for instruction in instructions:
        print(instruction)



#Function to retrieve the input file
def get_input_csv():
    #Expecting the input file to be the first command line arguement
    if(len(sys.argv) < 2):
        sys.exit("Too few command-line arguements")
    elif(len(sys.argv) > 2):
        sys.exit("Too many command-line arguements")

    inputfilename = sys.argv[1]

    if not inputfilename.endswith(".csv"):
        sys.exit("Not a CSV file")

    return inputfilename

#Function to read the input file and return the data in a suitable format
def read_csv(input_file_name):
    """
    Reads a CSV file and returns the data in a suitable format.
    
    Args:
        file_path (str): Path to the CSV file.
    
    Returns:
        dict: Dictionary with names as keys and lists of amounts paid as values.
    """
    # Initialize an empty dictionary to store the data
    data = {}
    with open(input_file_name, mode='r') as file:
        # Create a CSV reader object using DictReader
        csv_reader = csv.DictReader(file)
        
        # Iterate over each row in the CSV file
        for row in csv_reader:
            # Iterate over each column in the row
            for name, amount in row.items():
                # If the name is not already a key in the dictionary, add it with an empty list
                if name not in data:
                    data[name] = []
                # Treat empty fields as 0
                if amount == '' or None:
                    amount = 0
                else:
                    amount = int(amount)
                # Append the amount to the list corresponding to the name
                data[name].append(amount)
    
    
    return data
        
#Function to calculate the total amount paid by each person
def calculate_total_amount(data):
    """
    Calculates the total amount paid by each person and the average amount each person should have paid.
    
    Args:
        data (dict): Dictionary with names as keys and lists of amounts paid as values.
    
    Returns:
        tuple: A tuple containing two elements:
            - dict: Dictionary with names as keys and total amounts paid as values.
            - float: The average amount each person should have paid.
    """
    # Initialize an empty dictionary to store the total amounts paid by each person
    total_amounts = {}
    
    # Iterate over each name and list of amounts in the data dictionary
    for name, amounts in data.items():
        # Calculate the total amount paid by summing the amounts in the list
        total_amount = sum(amounts)
        # Add the total amount to the dictionary with the name as the key
        total_amounts[name] = total_amount
    
    trip_total_amount = 0
    trip_total_amount = sum(total_amounts[name] for name in total_amounts)
    print(f"Total Trip amount is {trip_total_amount}")
    average_payment = trip_total_amount/len(total_amounts)
    print(f"Everyone should have paid {average_payment}")
    for(name, amount) in total_amounts.items():
        print(f"{name} paid {amount}")
        
    print("\n")
    return total_amounts, average_payment 


def find_optimal_transfers(total_amount, average_payment):
    """
    Determines the most efficient way to settle the debts.
    
    Args:
        balances (dict): Dictionary with names as keys and net balances as values.
    
    Returns:
        list of str: List of instructions for transferring amounts.
    """


    creditors = []
    debtors = []

    #Determine Creditors and Debtors
    for name, amount in total_amount.items():
        balance = amount - average_payment
        if(balance > 0):
            creditors.append((name, balance))
        elif(balance < 0):
            debtors.append((name, -balance))

    #Sort the Creditors and Debtors
    creditors = sorted(creditors, key=lambda x: x[1], reverse=True)
    debtors = sorted(debtors, key=lambda x: x[1], reverse = True)

    #print(creditors, debtors, sep="\n")

    #Initialize the instructions list
    instructions = []

    #Initiate the transfer process
    while(creditors and debtors):
        creditor = creditors[0]
        debtor = debtors[0]

        #Determine the amount to be transferred
        transfer_amount = min(creditor[1], debtor[1])

        #Update the balances
        creditor_balance = creditor[1] - transfer_amount
        debtor_balance = debtor[1] - transfer_amount

        #Update the instructions
        instructions.append(f"{debtor[0]} pays {transfer_amount} to {creditor[0]}")

        #Update the balances
        creditors[0] = (creditor[0], creditor_balance)
        debtors[0] = (debtor[0], debtor_balance)

        #Remove the creditor or debtor if the balance is 0
        if creditor_balance == 0:
            creditors.pop(0)
        if debtor_balance == 0:
            debtors.pop(0)

    return instructions
 

    


if __name__ == '__main__':
    main()