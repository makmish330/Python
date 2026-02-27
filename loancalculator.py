mport math
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--principal", type=float, help="Loan principal")
    parser.add_argument("--payment", type=float, help="Annuity monthly payment")
    parser.add_argument("--periods", type=int, help="Number of moths to repay")
    parser.add_argument("--interest", type=float, help="Annual interest rate in percents")
    parser.add_argument("--type", type=str, help="Type of loan")
    args= parser.parse_args()

    # Create a list of all provided arguments that are not None
    provided_args = [v for k, v in vars(args).items() if v is not None]

    # VALIDATION CHECKS
    # 1. Fewer than 4 parameters provided
    if len(provided_args) < 4:
        print("Incorrect parameters")
        return

    # 2. Check for any negative numeric values
    for val in provided_args:
        if isinstance(val, (int, float)) and val < 0:
            print("Incorrect parameters")
            return

    # 3. Incorrect type or missing interest
    if args.type not in ["diff", "annuity"] or args.interest is None:
        print("Incorrect parameters")
        return

    # 4. Differentiated payments cannot be combined with a fixed payment amount
    if args.type == "diff" and args.payment is not None:
        print("Incorrect parameters")
        return

    # Nominal monthly interest rate
    i = args.interest / (12 * 100)

    # --- DIFFERENTIATED PAYMENTS ---
    if args.type == "diff":
        p = args.principal
        n = args.periods
        total_paid = 0
        for m in range(1, n + 1):
            d_m = math.ceil(p/n + i * (p - (p * (m - 1)/n)))
            total_paid += d_m
            print(f"Month {m}: payment is {d_m}")

        overpayment = math.floor(total_paid - p)
        print(f"\nOverpayment = {overpayment}")

    # --- ANNUITY PAYMENTS ---
    elif args.type == "annuity":
        # Case A: Missing Periods (n)
        if args.periods is None:
            p = args.principal
            a = args.payment

            n = math.ceil(math.log(a / (a - i * p), 1 + i))

            years = n // 12
            months = n % 12
            time_parts = []
            if years > 0:
                time_parts.append(f"{years} year{'s' if years > 1 else ''}")
            if months > 0:
                time_parts.append(f"{months} month{'s' if months > 1 else ''}")
            print(f"It will take {' and '.join(time_parts)} to repay this loan!")
            overpayment_annuity_calc(a, n, p)

        # Case B: Missing Monthly Payment (a)
        elif args.payment is None:
            p = args.principal
            n = args.periods

            a = math.ceil(p * (i * math.pow(1 + i, n))/ (math.pow(1 + i, n) - 1))
            print(f"Your annuity payment = {a}!")
            overpayment_annuity_calc(a, n, p)

        # Case C: Missing Loan Principal (p)
        elif args.principal is None:
            a = args.payment
            n = args.periods

            p = math.floor(a / ((i * math.pow(1 + i, n)) / (math.pow(1 + i, n) - 1)))
            print(f"Your loan principal = {p}!")
            overpayment_annuity_calc(a, n, p)

def overpayment_annuity_calc(a, n, p):
    overpayment = math.floor((a * n) - p)
    print(f"Overpayment = {overpayment}")

if __name__ == "__main__":
    main()
