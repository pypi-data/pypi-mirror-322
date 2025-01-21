# FinancialCalculator-Balbir

The `FinancialCalculator-Balbir` package provides a set of tools for performing various financial calculations, including future value, present value, loan amortization, compound interest, and more. It is designed to be easy to use for financial analysis, personal finance management, and educational purposes.

## Features

This package includes the following financial calculation functions:

- Future Value Calculation
- Present Value Calculation
- Compound Interest Calculation
- Simple Interest Calculation
- Loan Amortization Schedule
- Net Present Value
- Internal Rate of Return
- Breakeven Point Analysis
- Capital Asset Pricing Model (CAPM)
- Currency Conversion

## Installation

To install the `FinancialCalculator-Balbir`, simply run the following command:

```bash
pip install FinancialCalculator-Balbir
```

## Usage

Here is how to use the functions in the FinancialCalculator-Balbir package:

```python
from FinancialCalculator_Balbir import future_value, present_value, compound_interest

# Example usage:
fv = future_value(1000, 0.05, 10)  # Future value of $1000 at 5% for 10 years
pv = present_value(1000, 0.05, 10) # Present value of $1000 due in 10 years at 5%
ci = compound_interest(1000, 0.05, 1, 10)  # Compound interest for $1000 at 5% compounded annually for 10 years

print(f"Future Value: {fv}")
print(f"Present Value: {pv}")
print(f"Compound Interest: {ci}")
```

## License 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details.
