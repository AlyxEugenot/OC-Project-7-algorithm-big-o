import pandas as pd
import time
from itertools import islice


global LAST_STEP_TIME
LAST_STEP_TIME = start = time.time()


df = pd.read_csv("datasets/liste1.csv")
print("File as is:")
print(df.head())
print(df.dtypes)

df = df.rename(
    columns={"Coût par action (en euros)": "cost", "Bénéfice (après 2 ans)": "profit"}
)
df = df.set_index("Actions #")
df.index = df.index.str.replace("Action-", "")
print("\nColumns renamed & Actions as index:")
print(df.head())
print(df.dtypes)

df.profit = pd.to_numeric(df.profit.str.replace("%", ""))
df.profit = df.profit / 100
print("\nProfit column fixed:")
print(df.head())
print(df.dtypes)

df["earnings"] = df.cost + df.profit * df.cost
print("\nEarnings added:")
print(df.head())

all_combinations = {}


def find_all_subcombinations(
    actions_left: pd.DataFrame,
    current_actions_bought: list[str],
    current_earnings: float,
    current_money_left: int,
):
    actions_len = actions_left.shape[0]
    for action_index in range(actions_len):
        this_action = actions_left.iloc[action_index]
        if this_action.cost <= current_money_left:
            current_actions_bought.append(this_action.name)
            find_all_subcombinations(
                actions_left=actions_left.iloc[(action_index + 1) : actions_len],
                current_actions_bought=current_actions_bought,
                current_earnings=current_earnings + this_action.earnings,
                current_money_left=current_money_left - this_action.cost,
            )
            if actions_len == 20:
                print(
                    f"Time after all {this_action.name}s have been processed is: {time.time()-start} ({time.time()-globals()["LAST_STEP_TIME"]})"
                )
                globals()["LAST_STEP_TIME"] = time.time()
            current_actions_bought.pop()

    all_combinations[f"Actions {",".join(current_actions_bought)}"] = round(
        float(current_earnings), 2
    )


def take(n, iterable):
    """Return the first n items of the iterable as a list."""
    return list(islice(iterable, n))


print(f"\n\ntime before all calculations: {time.time()-start}\n")
find_all_subcombinations(
    actions_left=df,
    current_actions_bought=[],
    current_earnings=0,
    current_money_left=500,
)
LAST_STEP_TIME = time.time()
sorted_combinations = dict(
    sorted(all_combinations.items(), key=lambda item: item[1], reverse=True)
)
print(f"\ntime sorting all results: {time.time()-LAST_STEP_TIME}")

[print(x) for x in take(10, sorted_combinations.items())]

print(f"\nEND TIME: {time.time()-start}\n")
