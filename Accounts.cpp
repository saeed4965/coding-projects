#include <iostream>
#include <cstdlib>
#include <ctime>
#include <iomanip>
#include <algorithm>
#include <numeric> // Include for std::accumulate
using namespace std;

// Function prototypes
int getNumAccounts();
string generateTransactionType();
long generateTransactionAmount();
void displayStats(string transactionTypes[], long transactionAmounts[], int numAccounts);

int main() {
    srand(time(0)); // Seed for random number generation

    // Step 1: Get the number of bank accounts
    int numAccounts = getNumAccounts();

    // Step 2: Declare and populate arrays
    string transactionTypes[numAccounts];
    long transactionAmounts[numAccounts];

    for (int i = 0; i < numAccounts; ++i) {
        transactionTypes[i] = generateTransactionType();
        transactionAmounts[i] = generateTransactionAmount();
    }

    // Step 3: Display simulation statistics
    displayStats(transactionTypes, transactionAmounts, numAccounts);

    return 0;
}

// Function to get the number of bank accounts
int getNumAccounts() {
    int numAccounts;
    do {
        cout << "Enter the number of bank accounts (between 5 and 100): ";
        cin >> numAccounts;

        if (numAccounts < 5 || numAccounts > 100) {
            cout << "Error, invalid number of accounts entered. Please try again.\n";
        }

    } while (numAccounts < 5 || numAccounts > 100);

    return numAccounts;
}

// Function to generate a random transaction type
string generateTransactionType() {
    int randomNum = rand() % 2 + 1; // Generate a random number between 1 and 2

    // Return "deposit" for 1, "withdrawal" for 2
    return (randomNum == 1) ? "deposit" : "withdrawal";
}

// Function to generate a random transaction amount between $5 and $10000
long generateTransactionAmount() {
    return rand() % 995 + 5; // Generate a random number between 5 and 10000
}

void displayStats(string transactionTypes[], long transactionAmounts[], int numAccounts) {
    cout << setw(10) << "Account" << setw(15) << "Transaction" << setw(15) << "Amount" << endl;

    // Display transaction details
    for (int i = 0; i < numAccounts; ++i) {
        cout << setw(10) << (i + 1) << setw(15) << transactionTypes[i] << setw(15) << transactionAmounts[i] << endl;
    }

    // Debugging output
    cout << "Debugging Output:\n";
    for (int i = 0; i < numAccounts; ++i) {
        cout << "Amount[" << i << "]: " << transactionAmounts[i] << endl;
    }

    // Calculate and display statistics
    int totalTransactions = numAccounts;
    int totalDeposits = count(transactionTypes, transactionTypes + numAccounts, "deposit");
    int totalWithdrawals = count(transactionTypes, transactionTypes + numAccounts, "withdrawal");

    long totalAmountDeposited = accumulate(transactionAmounts, transactionAmounts + numAccounts, 0,
                                           [](long sum, long amount) { return (amount >= 0) ? sum + amount : sum; });

    long totalAmountWithdrawn = accumulate(transactionAmounts, transactionAmounts + numAccounts, 0,
                                            [](long sum, long amount) { return (amount < 0) ? sum + amount : sum; });

    long totalAmountTransacted = accumulate(transactionAmounts, transactionAmounts + numAccounts, 0);

    cout << "\nSimulation Statistics:\n";
    cout << "Total Number of Transactions: " << totalTransactions << endl;
    cout << "Total Number of Deposits: " << totalDeposits << endl;
    cout << "Total Number of Withdrawals: " << totalWithdrawals << endl;
    cout << "Average Amount per Deposit: " << fixed << setprecision(2) << (totalAmountDeposited / totalDeposits) << endl;

    if (totalWithdrawals > 0) {
        cout << "Average Amount per Withdrawal: " << fixed << setprecision(2) << (totalAmountWithdrawn / totalWithdrawals) << endl;
    } else {
        cout << "Average Amount per Withdrawal: N/A (No withdrawals)" << endl;
    }

    cout << "Average Amount per Transaction: " << fixed << setprecision(2) << (totalAmountTransacted / totalTransactions) << endl;
    cout << "Total Amount Deposited: " << totalAmountDeposited << endl;
    cout << "Total Amount Withdrawn: " << totalAmountWithdrawn << endl;
    cout << "Total Amount Transacted: " << totalAmountTransacted << endl;
}
