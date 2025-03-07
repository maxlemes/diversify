import pickle

from diversify import Refiner


def refine():
    refiner = Refiner()

    # Define financial statements to process -----------------------
    balance_types = ["income_stmt", "balance_sheet", "cash_flow"]

    for balance_type in balance_types:
        # Load financial statement data
        with open(f"tmp/{balance_type}.pkl", "rb") as f:
            data = pickle.load(f)

        data = refiner.balance(data, balance_type)

        # Save transformed financial data
        with open(f"tmp/{balance_type}_t.pkl", "wb") as f:
            pickle.dump(data, f)
