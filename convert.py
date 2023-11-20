import csv

# Read data from output.csv
csv_file = 'output.csv'

# Initialize an empty list to store CSV data
csv_data = []

# Read CSV file and extract data
with open(csv_file, newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        csv_data.append(row)

# Template for Lua code
lua_template = """
local ItemDB = {{
{}
}}
"""

lua_entry_template = """    [{}] = {{
        ilvl = {}, -- Item level
        players = {{
{}
        }},
    }},
"""

# Function to generate Lua code for ItemDB
def generate_lua_code(data):
    item_db_entries = {}
    
    for entry in data:
        item_id = int(entry["Item ID"])
        name = entry["Nickname"]
        percentage = float(entry["Percentage Difference"])  # Parse as float instead of int
        item_level = int(entry["Item Level"])  # Parse item level
        
        if item_id not in item_db_entries:
            item_db_entries[item_id] = {"players": [], "ilvl": item_level}
        
        item_db_entries[item_id]["players"].append({"name": name, "percentage": percentage})
    
    lua_entries = []
    for item_id, data in item_db_entries.items():
        players_data = ""
        for player in data["players"]:
            players_data += "            {{name = '{}', percentage = {}}},\n".format(player["name"], player["percentage"])
        players_data = players_data[:-2]  # Remove the trailing comma and newline
        
        lua_entry = lua_entry_template.format(item_id, data["ilvl"], players_data)
        lua_entries.append(lua_entry)
    
    return lua_template.format("".join(lua_entries))

# Generate Lua code for ItemDB
lua_code = generate_lua_code(csv_data)

# Read content from existing.lua
existing_lua_content = ''
with open('snippet.lua', 'r') as existing_lua_file:
    existing_lua_content = existing_lua_file.read()

# Combine existing Lua code with generated ItemDB
combined_lua_code = f"{lua_code}\n\n{existing_lua_content}"  # lua_code contains generated ItemDB

# Save combined Lua code to a file named 'combined.lua'
with open('tooltip.lua', 'w') as combined_lua_file:
    combined_lua_file.write(combined_lua_code)
