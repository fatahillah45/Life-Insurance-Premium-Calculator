# Life-Insurance-Premium-Calculator
Automated life insurance premium calculator for Term, Whole Life, and Endowment products using Python and TMI. My first project while exploring GitHub.

## 🚀 Features
- **Multiple Products:** Term Life, Whole Life, and Endowment insurance.
- **Gender-Specific:** Supports separate mortality tables (TMI Pria & Wanita).
- **Flexible Payments:** Supports limited payment periods ($k < n$).
- **Clean Interface:** Interactive terminal input with data validation.

## 🧮 Actuarial Formulas
The program calculates the **Expected Present Value (EPV)** using commutation functions:
- $D_x = v^x \cdot l_x$
- $N_x = \sum D_x$
- $M_x = \sum C_x$

For **Endowment Insurance**, the Net Single Premium (NSP) is calculated as:
$$A_{x:\bar{n}|} = \frac{(M_x - M_{x+n}) + D_{x+n}}{D_x}$$
