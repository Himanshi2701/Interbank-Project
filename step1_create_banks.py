import numpy as np
import pandas as pd

np.random.seed(42)  # so we get the same "random" numbers every time we run this

# Let's say we have 20 banks total
num_banks = 20
num_big_banks = 5     # 5 big banks, 15 small banks

bank_names = []
bank_type = []
total_assets = []

# Create 5 big banks
for i in range(num_big_banks):
    bank_names.append("Bank_" + str(i))
    bank_type.append("big")
    total_assets.append(np.random.randint(8000, 15000))  # big banks have more money

# Create 15 small banks
for i in range(num_big_banks, num_banks):
    bank_names.append("Bank_" + str(i))
    bank_type.append("small")
    total_assets.append(np.random.randint(500, 2000))  # small banks have less money

# Capital = the "safety cushion" each bank has (say 10% of its assets)
capital = [round(a * 0.10, 2) for a in total_assets]

# Put everything into a table (DataFrame)
banks_df = pd.DataFrame({
    "bank_name": bank_names,
    "type": bank_type,
    "total_assets": total_assets,
    "capital": capital
})

print(banks_df)

# Save this table to a CSV file so we can use it in the next steps
banks_df.to_csv("banks.csv", index=False)
print("\nSaved banks.csv")