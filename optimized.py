import pandas as pd
import time
from itertools import islice


STRATEGIES_MAX_AMOUNT = 1000
FILE = "dataset2_Python+P7.csv"
BEST_STRATEGIES = {}  # format {"Actions 1,n": [total_earnings, total_cost]}
IS_DATASET = True


# region functions
def find_first_subcombinations(
    actions_left: pd.DataFrame,
    current_actions_bought: list[str] = [],
    current_earnings: float = 0,
    current_money_left: float = 500,
    max_result_amount: int = 30,
):
    """Trouve les <STRATEGIES_MAX_AMOUNT> premières stratégies du tableau
    (trié par meilleures actions).

    Args:
        actions_left (pd.DataFrame): Dataframe à renseigner.
        current_actions_bought (list[str], optional): Current actions bought. Defaults to [].
        current_earnings (float, optional): Current earnings. Defaults to 0.
        current_money_left (float, optional): Available money to buy actions. Defaults to 500.
    """
    actions_len = actions_left.shape[0]
    action_index = 0
    max_cost_reached = True
    while action_index < actions_len and len(BEST_STRATEGIES) < max_result_amount:
        this_action = actions_left.iloc[action_index]
        if this_action.cost <= current_money_left:
            max_cost_reached = False
            current_actions_bought.append(this_action.name)
            find_first_subcombinations(
                actions_left=actions_left.iloc[(action_index + 1) : actions_len],
                current_actions_bought=current_actions_bought,
                current_earnings=current_earnings + this_action.earnings,
                current_money_left=current_money_left - this_action.cost,
                max_result_amount=max_result_amount,
            )
            current_actions_bought.pop()

        action_index += 1
    if max_cost_reached:
        action_name = (
            f"Actions {",".join([str(x) for x in sorted(current_actions_bought)])}"
            if IS_DATASET
            else f"Actions {",".join([str(x) for x in sorted([int(y) for y in current_actions_bought])])}"
        )
        BEST_STRATEGIES[action_name] = [
            round(float(current_earnings), 2),
            round(float(current_money_left), 2),
        ]


def take(n, iterable):
    """Return the first n items of the iterable as a list."""
    return list(islice(iterable, n))


def execute_find_strategies_with_sorted(
    actions: pd.DataFrame, sorting_labels: list[str]
):
    for i, sorting_label in enumerate(sorting_labels):
        df = actions.sort_values(by=[sorting_label], ascending=False)
        find_first_subcombinations(
            df,
            max_result_amount=int(
                STRATEGIES_MAX_AMOUNT * (i + 1) / len(sorting_labels)
            ),
        )


# endregion


def main():
    start = time.time()

    df = pd.read_csv(FILE)
    print("File as is:")
    print(df.head())
    print(df.dtypes)

    action_col_name = "name" if IS_DATASET else "Actions #"
    action_prefix = "Share-" if IS_DATASET else "Action-"
    if IS_DATASET:
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
    print("\nColumns renamed & Actions as index:")
    print(df.head())
    print(df.dtypes)

    if not IS_DATASET:
        df.profit = pd.to_numeric(df.profit.str.replace("%", ""))
    df.profit = df.profit / 100
    print("\nProfit column fixed:")
    print(df.head())
    print(df.dtypes)

    df["earnings"] = df.cost + df.profit * df.cost
    print("\nEarnings added:")
    print(df.head())

    execute_find_strategies_with_sorted(df, ["earnings", "profit"])

    sorted_results = dict(
        sorted(
            BEST_STRATEGIES.items(),
            key=lambda item: item[1][0] + item[1][1],
            reverse=True,
        )
    ) # TODO le sort par bénéfice (profit - cout)

    print("\nActions, revenus, argent restant")
    [print(x) for x in take(10, sorted_results.items())]

    print(f"\nTIME: {time.time()-start}\n")


if __name__ == "__main__":
    main()
