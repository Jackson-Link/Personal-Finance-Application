# Get Paycheck for current period
income = float(input("Give me your paycheck for this period: $:"))

# Possible accounts person can pick from
available_accounts = {
    "1": "Checking",
    "2": "Saving/Emergency Fund",
    "3": "High-Yield Saving",
    "4": "Brokerage",
    "5": "Roth IRA",
    "6": "Travel Fund",
    "7": "Debt Payments",
    "8": "Charity",
}

available_presets = {
    "1": {
        "name": "Standard 50/30/20 Rule",
        "allocations": {
            "Checking": 50,
            "High-Yield Saving": 30,
            "Roth IRA": 20
        }
    },
    "2": { 
        "name": "Aggressive Investor (40/10/50)",
        "allocations": {
            "Checking": 40,
            "Roth IRA": 10,
            "Brokerage": 50
        }
    },
    "3": {
        "name": "College Student Setup (70/30)",
        "allocations": {
            "Checking": 70,
            "Saving/Emergency Fund": 30
        }
    },
}

print ("\nSelect a Budget Preset:")
for number, preset_info in available_presets.items():
    print(f"{number}: {preset_info['name']}")
print("4: Custom")
budget_choices_input = input("\n Enter the preset number you want to use (1-4): ")

allocations = {}

if budget_choices_input in available_presets:
    selected_preset = available_presets[budget_choices_input]
    print(f"\nApplying Preset: {selected_preset['name']}")

    allocations = selected_preset['allocations']

elif budget_choices_input == "4":
    # Asks for distribution and which accounts
    print ("\nWhere would you like to distribute your money?")
    for number, name in available_accounts.items():
        print(f"{number}: {name}")
    choices_input = input("\n Enter the number of the accounts you want to use, seperate using commas.")

    # Which accounts they chose
    selected_keys = [key.strip() for key in choices_input.split(",")]

    chosen_accounts = []
    for key in selected_keys:
        if key in available_accounts:
            chosen_accounts.append(available_accounts[key])

    if len(chosen_accounts) == 0:
        print("Error: You didn't select any valid accounts!")
    else:
        print("\nNow, let's set your percentages for these selected accounts.")
        total_percentage = 0
        for account in chosen_accounts:
            percent = float(input(f"What percent for {account}? "))
            allocations[account] = percent
            total_percentage += percent

        if total_percentage > 100:
            print(f"\nError: Percentages add up to {total_percentage:.0f}%. Cannot exceed 100%!")
            allocations = {} # Clear it so the program doesn't try to run calculations

# If they typed something completely invalid
else:
    print("Error: Invalid choice selected.")

# 7. Do the Math and Display the Results (This block works for BOTH Presets and Custom!)
if len(allocations) > 0:
    print(f"\n--- Your Financial Breakdown ---")
    total_percentage_used = 0
    
    for account, percent in allocations.items():
        decimal_pct = percent / 100
        amount = income * decimal_pct
        total_percentage_used += percent
        print(f"{account} ({percent:.0f}%): ${amount:.0f}")

    # Calculate leftover cash if they didn't use 100%
    if total_percentage_used < 100:
        leftover_pct = 100 - total_percentage_used
        leftover_amount = income * (leftover_pct / 100)
        print(f"Leftover Cash ({leftover_pct:.0f}%): ${leftover_amount:.0f}")