import sqlite3
import re
def get_data(table):
    conn = sqlite3.connect("mcp_database.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    data = cursor.fetchall()
    conn.close()
    return data

def parse_role(scenario):
    for role in roles:
        id = role[0]
        role_name = role[1]
        permissions = role[2]
        role_id = re.findall(r"Role (\d+)", scenario)
        if not role_id:
            continue
        
        if int(role_id[0]) == id:
            return role_name
    return scenario
def parse_endpoint(scenario):
    for endpoint in api_endpoints:
        id = endpoint[0]
        method = endpoint[1]
        path = endpoint[2]
        endpoint_id = re.findall(r"Endpoint (\d+)", scenario)

        if not endpoint_id:
            continue
        
        if int(endpoint_id[0]) == id:
            return f"{method} {path}"
    return scenario


scenarios = get_data("scenarios")
api_endpoints = get_data("api_endpoint")
roles = get_data("roles")
if __name__ == "__main__":
    print("=== SCENARIO GENERATED ===")
    for idx, scenario in enumerate(scenarios):
        endpoint = parse_endpoint(scenario[1])
        role = parse_role(scenario[1])
        print(f"{(str(idx+1)).ljust(3,' ')}. {role.ljust(15,' ')} - {endpoint}")