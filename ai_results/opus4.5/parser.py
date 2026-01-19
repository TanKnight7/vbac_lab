import sqlite3
import re
def get_data(table):
    conn = sqlite3.connect("databasetestinggg.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    data = cursor.fetchall()
    conn.close()
    return data


scenarios = get_data("scenarios")
scenarios = [scenario for scenario in scenarios if "posts" not in scenario[1]]
if __name__ == "__main__":
    print("=== SCENARIO GENERATED ===")
    for idx, scenario in enumerate(sorted(scenarios, key=lambda x: x[1])):
        print(f"{str(idx+1).ljust(3,' ')}. {scenario[1]}")