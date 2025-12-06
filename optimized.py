from typing import List
import time
import pandas as pd


STARTING_MONEY = 500
FILE1 = "datasets/liste1.csv"
FILE2 = "datasets/dataset1_Python+P7.csv"
FILE3 = "datasets/dataset2_Python+P7.csv"


def get_data(
    file_name: str, is_dataset: bool = True, show_df_formatting: bool = True
) -> pd.DataFrame:
    """Reading file content and returning DataFrame sorted by profits and filtered from bad data.

    Format is:

    Index: Action number(str)

    Columns: ['cost','profit','earnings']

    Args:
        file_name (str): Name of file to analyse.
        is_dataset (bool, optional): Used for column names. False if file is liste1.csv.
            Defaults to True.
        show_df_formatting (bool, optional): Print DataFrame formatting steps. Defaults to True.

    Returns:
        pd.DataFrame: Sorted DataFrame (format in func docstring)
    """
    df = pd.read_csv(file_name)
    if show_df_formatting:
        print("File as is:")
    if show_df_formatting:
        print(df.head())
    if show_df_formatting:
        print(df.dtypes)

    action_col_name = "name" if is_dataset else "Actions #"
    action_prefix = "Share-" if is_dataset else "Action-"
    if is_dataset:
        df = df.rename(columns={"price": "cost"})
    else:
        df = df.rename(
            columns={
                "Coût par action (en euros)": "cost",
                "Bénéfice (après 2 ans)": "profit",
            }
        )
    df = df.set_index(action_col_name)
    df.index = df.index.str.replace(action_prefix, "")
    if show_df_formatting:
        print("\nColumns renamed & Actions as index:")
    if show_df_formatting:
        print(df.head())
    if show_df_formatting:
        print(df.dtypes)

    if not is_dataset:
        df.profit = pd.to_numeric(df.profit.str.replace("%", ""))
    df.profit = df.profit / 100
    if show_df_formatting:
        print("\nProfit column fixed:")
    if show_df_formatting:
        print(df.head())
    if show_df_formatting:
        print(df.dtypes)

    df["earnings"] = df.profit * df.cost
    if show_df_formatting:
        print("\nEarnings added:")
    if show_df_formatting:
        print(df.head())

    df = df.loc[
        (df.cost > 0) & (df.cost <= STARTING_MONEY) & (df["earnings"] > 0)
    ].sort_values(by=["profit"], ascending=False)

    return df


def algorithm(
    df: pd.DataFrame, current_money: float = STARTING_MONEY
) -> List[str | float | float | float]:
    """With dataframe sorted by profits, buy every possible action until no_money_left.

    Args:
        df (pd.DataFrame): DataFrame to process.
        current_money (float, optional): Available money to buy actions with.. Defaults to 500.

    Returns:
        List[str | float | float | float]: First possible combination spending all money.
    """

    # list of arrays [name, cost, profit, earnings]
    first_possible_combination = []
    minimum_action_cost = df.cost.min()

    # Index: Action number(str)

    # Columns: ['cost','profit','earnings']
    for i, action in df.iterrows():
        # if current action is buyable (best first because df is sorted)
        if current_money - action.cost >= 0:
            # add action to solution
            first_possible_combination += [
                [
                    action.name,
                    action.cost,
                    action.profit,
                    action.earnings,
                ]
            ]

            current_money -= action.cost

            # if no more money, stop forloop
            if current_money < minimum_action_cost:
                break

    return first_possible_combination


def print_results(algo_result: List[str | float | float | float]):
    """Gather results and print actions chosen as well as earnings and costs sums.

    Args:
        algo_result (List[str  |  float  |  float  |  float]): Result of algorithm function.
    """

    # make a df from result arrays
    df_from_result = pd.DataFrame(
        data=algo_result, columns=["name", "cost", "profit", "earnings"]
    ).set_index("name")

    actions_sum = df_from_result.cost.sum()
    earnings_sum = df_from_result.earnings.sum()

    # display all rows
    pd.set_option("display.max_rows", None)

    print("\nDataFrame :")
    print(df_from_result)

    print(f"Money spent: {round(actions_sum, 2)}€")
    print(f"Total earnings: {round(earnings_sum, 2)}€")


def time_since(timestamp: float, rounded_to: int = 3) -> float:
    """Time since timestamp rounded to two decimals.

    Args:
        timestamp (float): Time to compare.

    Returns:
        float: Time since timestamp rounded to two decimals.
    """
    return round(time.time() - timestamp, rounded_to)


def main():
    start = time.time()

    for file, is_dataset in {FILE1: False, FILE2: True, FILE3: True}.items():
        dataset_processing_time = time.time()
        df = get_data(file, is_dataset, show_df_formatting=False)
        results = algorithm(df)
        print_results(results)
        print(
            f"\nExecution time of file {file}: {time_since(dataset_processing_time)}\n"
        )

    print(f"\nCOMPLETE TIME: {time_since(start)}\n")


if __name__ == "__main__":
    main()
