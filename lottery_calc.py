import matplotlib.pyplot as plt
from state_taxes import lottery_tax_rates
import os
os.environ['QT_LOGGING_RULES'] = '*.debug=false;qt.qpa.*=false'

# Define lottery calculation parameters
def calculate_lottery_payments(jackpot, state_tax):
    lump_sum_percentage = 0.4725
    lump_sum = jackpot * lump_sum_percentage
    federal_withholding_percentage = 0.37
    federal_withholding = lump_sum * federal_withholding_percentage
    state_witholding = lump_sum * state_tax
    return lump_sum - federal_withholding - state_witholding

# Custom autopct to prevent rounding errors
def make_autopct(values):
    def autopct(pct):
        return f'{pct:.1f}%'
    return autopct

# Program execution

print() # For formatting only
print("Welcome to the Lottery Payment Calculator!")
print("=" * 63)

while True:
    try:
        j = float(input('Enter a jackpot amount ($): '))
        
        # Validate jackpot amount
        if j <= 0:
            print('The jackpot amount must be greater than 0. Please try again.')
            continue
        else:
            while True:
                state_code = input('Enter your two-letter state code (e.g. WV for West Virginia): ').strip().upper()
                if state_code not in lottery_tax_rates:
                    print('Invalid state code. Please try again.')
                    print('') # For formatting only
                elif lottery_tax_rates[state_code]['rate_pct'] is None:
                    print(f'{lottery_tax_rates[state_code]["name"]} does not allow lottery play. Please try again.')
                    print('') # For formatting only
                else:
                    s = lottery_tax_rates[state_code]['rate_pct'] / 100
                    payout = calculate_lottery_payments(j, s)
                    break
            break  # Exit the main loop after valid state code is entered
    
    except ValueError:
        print('Invalid input. Please enter a numeric value for the jackpot amount.')
        continue

# Statement Variables
lump_sum = 0.4725
federal_tax = 0.37

l = j * lump_sum
f = l * federal_tax
st = l * s

# Output calculations:
print(' ') # For formatting only
print('Lottery Payment Breakdown:')
print('=' * 63)
print(f"""
      {'Jackpot Amount:':<35}${j:>15,.0f}
      {'Lump Sum Amount:':<35}${l:>15,.0f}
      {'Federal Withholding (37%):':<35}${f:>15,.0f}
      {f'{lottery_tax_rates[state_code]["name"]} Withholding ({lottery_tax_rates[state_code]["rate_pct"]}%):':<35}${st:>15,.0f}
      {'Winnings after Taxes:':<35}${payout:>15,.0f}
        """)

print('=' * 63)

# Output Visual of Lottery Calculation Breakdowns

# Pie chart data
lump_sum_discount = j - l

labels     = ['Lump Sum Discount', 'Federal Tax', 'State Tax', 'Winnings after Tax']
categories = [lump_sum_discount, f, st, payout]
colors     = ['#7A9EB5','#A8BFC9','#B0B0B0','#000080']

# Filter out zero-value slices (e.g. states with 0% tax)
filtered = [(la, ca, co) for la, ca, co in zip(labels, categories, colors) if ca > 0]
labels_f, categories_f, colors_f = zip(*filtered)

# Dynamic explode — only pops the Winnings after Tax slice
explode = tuple(0.1 if la == 'Winnings after Tax' else 0 for la in labels_f)

# Build chart
plt.figure(figsize=(10, 10))
plt.pie(categories_f, colors=colors_f, explode=explode, autopct=make_autopct(categories_f),
        textprops={'weight': 'bold', 'color': 'white'}, startangle=140)
plt.title(f'{lottery_tax_rates[state_code]["name"]} Lottery Winnings Breakdown\n\nJackpot: ${j:,.0f}\nCash Value: ${l:,.0f}\nWinnings after Taxes: ${payout:,.0f}',
          fontweight='bold')
plt.legend(labels_f, title='Breakdown', loc='lower right')
plt.show()