from pyswip import Prolog

# Initialize Prolog
prolog = Prolog()

# Load Prolog rules from the .pl file
prolog.consult('water_source_rules.pl')

# Define a function to get user input for each attribute
def get_attribute_value(attribute_name):
    return input(f"Enter {attribute_name}: ")

# Define a function to query the Prolog expert system
def query_expert_system():
    for attribute in ["LakeDistance", "RiverDistance", "RainfallIntensity", "SandyAquifer", "BeachDistance"]:
        value = get_attribute_value(attribute)
        prolog.assertz(f"{attribute}({value}).")
    
    # Query the suitable water source
    result = list(prolog.query("water_source(Source)."))
    
    if result:
        source = result[0]["Source"]
        print(f"The recommended water source is: {source}")
    else:
        print("No suitable water source found for the given conditions.")

# Main interactive loop
while True:
    try:
        query_expert_system()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        break
    except ValueError as e:
        print(f"Error: {e}\nPlease enter attribute values in the correct format (e.g., '10').")
