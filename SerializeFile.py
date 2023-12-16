# Import the necessary modules and classes
from SportEvent import SportEvent
import pandas as pd
import os  # Import os module for checking file existence


# Function to save a SportEvent to a CSV file
def save_sport_event(csv_filename, sport_event):
    try:
        # Create a dictionary with SportEvent data
        sport_event_data = {
            "id": [sport_event.id],
            "name": [sport_event.name],
            "location": [sport_event.location],
            "date": [sport_event.date],
            "status": [sport_event.status],
            "pos_file": [sport_event.pos_file],
            "erased": [sport_event.erased]
        }

        # Convert the dictionary to a DataFrame
        df = pd.DataFrame(sport_event_data)

        # Append the DataFrame to a CSV file, creating the file if it doesn't exist
        df.to_csv(csv_filename, mode='a', index=False, header=not os.path.exists(csv_filename))

        # Print a success message
        print("Evento guardado correctamente.")
    except Exception as e:
        print("Error al guardar el evento:", e)


# Function to modify a SportEvent in a CSV file
def modify_sport_event(csv_filename, sport_event):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_filename)

    # Identify the row corresponding to the SportEvent ID
    mask = df['id'] == sport_event.id

    # Update the values in the identified row
    df.loc[mask, ['id', 'name', 'location', 'date', 'status', 'pos_file']] = [
        sport_event.id, sport_event.name, sport_event.location, sport_event.date,
        sport_event.status, sport_event.pos_file
    ]

    # Save the updated DataFrame back to the CSV file
    df.to_csv(csv_filename, index=False)


# Function to read SportEvents from a CSV file
def read_sport_event(csv_filename):
    try:
        df = pd.read_csv(csv_filename)
    except FileNotFoundError:
        print(f"Error: The file {csv_filename} was not found.")
        return []

    if df is None or df.empty:
        print("Warning: The DataFrame is empty.")
        return []

    sport_event_list = []
    expected_columns = ['id', 'name', 'location', 'date', 'status', 'pos_file', 'erased']

    missing_columns = [col for col in expected_columns if col not in df.columns]
    if missing_columns:
        print(f"Error: The following columns were not found in the CSV file: {missing_columns}")
        return []

    for index, row in df.iterrows():
        if row['erased'] is False:  # Only add to the list if 'erased' is False
            sport_event_list.append(
                SportEvent(row['id'], row['name'], row['location'], row['date'], row['status'], row['pos_file'],
                           row['erased']))

    return sport_event_list

