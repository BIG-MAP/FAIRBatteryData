import pandas as pd
import json
import numpy as np




def csv_to_jsonld_organizations():
    # Read data from CSV file
    df = pd.read_csv('scripts\BatteryExpertsData_organizations.csv', sep=";")


    # Create a list to hold the JSON-LD data
    json_data = []

    # Iterate through each row in the CSV file
    for index, row in df.iterrows():
        # Create a dictionary to hold the JSON-LD data for this entity
        entity_data = {
            "@context": {"schema":"https://schema.org/"},
            "@id": row['id'],
            "@type": row['type'],
            "schema:name": row['schema:name'],
            "schema:alternateName": row['schema:alternateName']
        }
        # Append the entity data to the JSON list
        json_data.append(entity_data)


    # Write the JSON-LD data to a file
    with open('organizations.json', 'w') as outfile:
        json.dump(json_data, outfile, indent=2)


def csv_to_jsonld_experts():
    # Read data from CSV file
    df = pd.read_csv('scripts\BatteryExpertsData_experts.csv', sep=";")    
    df = df.replace(np.nan, None, regex=True)

    # Create a list to hold the JSON-LD data
    json_data = []

    # Iterate through each row in the CSV file
    for index, row in df.iterrows():
        # Create a dictionary to hold the JSON-LD data for this entity
        entity_data = {
            "@context": {"schema":"https://schema.org/"},
            "@id": row['id'],
            "@type": "schema:Researcher",
            "schema:familyName": row['schema:familyName'],
            "schema:additionalName": row['schema:additionalName'] ,
            "schema:givenName": row['schema:givenName'],
            "schema:email": row['schema:email'] ,
            "schema:gender": row['schema:gender'] ,
            "schema:affiliation": row['schema:affiliation'] ,
            "schema:image": row['schema:image']
        }
        # Append the entity data to the JSON list
        json_data.append(entity_data)


    # Write the JSON-LD data to a file
    with open('experts.json', 'w') as outfile:
        json.dump(json_data, outfile, indent=2)

if __name__ == "__main__":
    csv_to_jsonld_organizations()
    csv_to_jsonld_experts()