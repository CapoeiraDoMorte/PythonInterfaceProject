# https://apuntes.de/python/expresiones-regulares-y-busqueda-de-patrones-en-python-poder-y-flexibilidad/#gsc.tab=0
# https://rico-schmidt.name/pymotw-3/pickle/index.html
# https://stackoverflow.com/questions/55809976/seek-on-pickled-data
# https://www.reddit.com/r/learnpython/comments/pgfj63/sorting_a_table_with_pysimplegui/
# https://www.geeksforgeeks.org/python-sorted-function/
# https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Table_Element_Header_or_Cell_Clicks.py
# https://github.com/PySimpleGUI/PySimpleGUI/issues/5646
# https://docs.python.org/3/howto/sorting.html
import os
from SportEvent import SportEvent
import PySimpleGUI as sg
from SerializeFile import save_sport_event, read_sport_event
import re
import operator
import pandas as pd



# List that will store SportEvent objects read from the CSV file
l_sport_event = []

# Definition of regular expression patterns for validation
pattern_id = r"\d+"  # Example pattern for ID
pattern_name = r".+"  # Example pattern for name
pattern_location = r".+"  # Example pattern for location
pattern_date = r"\d{4}-\d{2}-\d{2}"  # Example pattern for date (YYYY-MM-DD)
pattern_status = r".+"  # Example pattern for status


# Function to add a new sport event to the list and save the data to a CSV file
def add_sport_event(l_sport_event, t_sport_event_interface, new_event, window):
    # Save the new sport event to the CSV file
    save_sport_event('database.csv', new_event)

    # Add the new sport event to the list
    l_sport_event.append(new_event)

    # Update the GUI table
    t_sport_event_interface.append(
        [new_event.id, new_event.name, new_event.location, new_event.date, new_event.status, new_event.pos_file])
    window['-Table-'].update(values=t_sport_event_interface)


# Function to delete a sport event from the list and update the interface and CSV file
def del_sport_event(l_sport_event, t_sport_event_interface, pos_in_table):
    # Read the CSV file and store the data in a DataFrame
    df = pd.read_csv('database.csv')

    # Find the row that has the same ID as the sport event to be deleted
    mask = df['id'] == t_sport_event_interface[pos_in_table][0]

    # If such a row is found, change the value of 'erased' to True
    df.loc[mask, 'erased'] = True

    # Save the DataFrame back to the CSV file
    df.to_csv('database.csv', index=False)

    # Update the list of sport events in memory
    for o in l_sport_event:
        if o.id == t_sport_event_interface[pos_in_table][0]:
            o.erased = True
            break

    # Remove the sport event from the interface's list
    t_sport_event_interface.remove(t_sport_event_interface[pos_in_table])


# Function to update a sport event in the list and the CSV file
def update_sport_event(l_sport_event, t_row_sport_event_interface, pos_in_file):
    # Read the CSV file and store the data in a DataFrame
    df = pd.read_csv('database.csv')

    # Convert the ID to string before comparison
    event_id = str(t_row_sport_event_interface[0])
    df['id'] = df['id'].astype(str)

    # Find the row that has the same ID as the sport event to be updated
    mask = df['id'] == event_id

    # If such a row is found, update the values of that row with the new values of the sport event
    if df.loc[mask].shape[0] > 0:
        df.loc[mask, 'name'] = t_row_sport_event_interface[1]
        df.loc[mask, 'location'] = t_row_sport_event_interface[2]
        df.loc[mask, 'date'] = t_row_sport_event_interface[3]
        df.loc[mask, 'status'] = t_row_sport_event_interface[4]

        # Save the DataFrame back to the CSV file
        df.to_csv('database.csv', index=False)

        # Update the list of sport events in memory
        for o in l_sport_event:
            if o.id == event_id:
                o.name = t_row_sport_event_interface[1]
                o.location = t_row_sport_event_interface[2]
                o.date = t_row_sport_event_interface[3]
                o.status = t_row_sport_event_interface[4]
                o.erased = False  # Make sure the 'erased' state is set to False
                break
    else:
        print("Error: No sport event with the provided ID was found.")


# Function to handle the event of adding a sport event
def handle_add_event(event, values, l_sport_event, table_data, window):
    # Simplified validation; add full validation logic as needed.
    if re.match(pattern_id, values['-id-']) and \
            re.match(pattern_name, values['-name-']) and \
            re.match(pattern_location, values['-location-']) and \
            re.match(pattern_date, values['-date-']) and \
            re.match(pattern_status, values['-status-']):
        # Create a new SportEvent object with the provided values.
        new_event = SportEvent(values['-id-'], values['-name-'], values['-location-'],
                               values['-date-'], values['-status-'], len(l_sport_event), False)

        # Call the function to add the new sports event.
        add_sport_event(l_sport_event, table_data, new_event, window)


# Function to handle the event of deleting a sport event
def handle_delete_event(event, values, l_sport_event, table_data, window):
    if len(values['-Table-']) > 0:
        del_sport_event(l_sport_event, table_data, values['-Table-'][0])
        window['-Table-'].update(table_data)


# Function to handle the event of modifying a sport event
def handle_modify_event(event, values, l_sport_event, table_data, window):
    valid = False
    if re.match(pattern_id, values['-id-']) and \
            re.match(pattern_name, values['-name-']) and \
            re.match(pattern_location, values['-location-']) and \
            re.match(pattern_date, values['-date-']) and \
            re.match(pattern_status, values['-status-']):
        valid = True

    if valid:
        row_to_update = None
        for t in table_data:
            if str(t[0]) == values['-id-']:
                row_to_update = t
                t[1], t[2], t[3], t[4] = values['-name-'], values['-location-'], values['-date-'], values['-status-']
                break

        if row_to_update is None:
            print("Error: No sport event with the provided ID was found in the event.")
            return

        update_sport_event(l_sport_event, row_to_update, int(values['-pos_file-']))
        window['-Table-'].update(table_data)
        window['-id-'].update(disabled=False)


# Function to sort the table by multiple columns
def sort_table(table, cols):
    for col in reversed(cols):
        try:
            table = sorted(table, key=operator.itemgetter(col))
        except Exception as e:
            sg.popup_error('Error in sort_table', 'Exception in sort_table', e)
    return table


def purge_database(file_path):
    temp_file_path = file_path.replace('.csv', '_temp.csv')
    new_file_path = file_path.replace('.csv', '_new.csv')

    # Verify files if exists
    if not os.path.exists(file_path):
        print(f"Error: El archivo {file_path} no se encontró.")
        return


    df = pd.read_csv(file_path)
    df_filtered = df[df['erased'] == False]

    df_filtered.to_csv(new_file_path, index=False)

    # Save the filtered records to a new file.
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)
    os.remove(file_path)

    # Rename the new file to the original name.
    os.rename(new_file_path, file_path)

    print(f"Archivo purgado y renombrado con éxito.")


# Main function that defines the graphical interface and handles events
def interface():
    font1, font2 = ('Arial', 14), ('Arial', 16)

    sg.theme_background_color('#FFFFFF')  # Blanco
    sg.theme_text_element_background_color('#FFFFFF')  # Blanco
    sg.theme_input_background_color('#FFFFFF')  # Blanco
    sg.theme_text_color('#000000')  # Negro
    sg.theme_input_text_color('#000000')  # Negro
    sg.theme_button_color(('white', 'red'))
    sg.set_options(font=font1)

    table_data = []
    row_to_update = []

    # Load the sports events from the CSV file.
    l_sport_event = read_sport_event('database.csv')

    # Fill the data list for the table.
    for o in l_sport_event:
        table_data.append([o.id, o.name, o.location, o.date, o.status, o.pos_file, o.erased])

    # Create input rows based on the defined fields.
    input_rows = [[sg.Text(text, size=(15, 1), font=font2), sg.Input(key=key, font=font2)]
                  for key, text in SportEvent.fields.items()]

    button_size = (7, 1)
    button_font = ('Arial', 12, 'bold')
    buttons = [
        sg.Button(button, size=button_size, font=button_font, button_color=('white', 'red'), border_width=2)
        for button in ('Add', 'Delete', 'Modify', 'Clear')
    ]

    # Definition of the interface layout
    layout = [
        [sg.Push(), sg.Text('My SportEvent Library', font=('Arial', 20, 'bold'), text_color='red'), sg.Push()],
        *input_rows,
        [sg.Push(), *buttons, sg.Push()],
        [sg.Table(values=table_data, headings=SportEvent.headings, max_col_width=50, num_rows=10,
                  background_color='black', text_color='white', header_background_color='red',
                  header_text_color='white', font=font2, key='-Table-')],
        [sg.Button('Purge', size=button_size, font=button_font, button_color=('white', 'red'), border_width=2),
         sg.Push(),
         sg.Button('Sort File', size=button_size, font=button_font, button_color=('white', 'red'), border_width=2)]
    ]

    # Create the PySimpleGUI window
    window = sg.Window('My SportEvent Library', layout, finalize=True)
    window['-Table-'].update(values=table_data)
    window['-Table-'].bind("<Double-Button-1>", " Double")

    # Main loop to handle interface events
    while True:
        event, values = window.read()

        # When the 'Sort File' button is pressed
        if event == 'Sort File':
            # Popup to choose the sorting field
            sort_column = sg.popup_get_text('Enter the field to sort by:',
                                            'Sort Events',
                                            default_text='name',
                                            keep_on_top=True)

            if sort_column and sort_column in SportEvent.headings:
                # Find the index of the column to sort by
                col_idx = SportEvent.headings.index(sort_column)
                table_data.sort(key=lambda x: x[col_idx])
                window['-Table-'].update(values=table_data)
            else:
                sg.popup_error('Invalid field or cancelled operation', keep_on_top=True)

        # Handle the event of closing the window
        if event == sg.WIN_CLOSED:
            break

        if event == 'Purge':
            purge_database('database.csv')

            # Update the data in the user interface
            l_sport_event = read_sport_event('database.csv')  # Asumiendo que esta función lee los datos actualizados
            table_data = [[o.id, o.name, o.location, o.date, o.status, o.pos_file, o.erased] for o in l_sport_event]
            window['-Table-'].update(values=table_data)

        # Handle the event of adding a sport event
        if event == 'Add':
            handle_add_event(event, values, l_sport_event, table_data, window)

        # Handle the event of deleting a sport event
        if event == 'Delete':
            handle_delete_event(event, values, l_sport_event, table_data, window)

        # Handle the event of double-clicking on the table
        if event == '-Table- Double':
            if len(values['-Table-']) > 0:
                row = values['-Table-'][0]
                window['-id-'].update(disabled=True)
                window['-id-'].update(str(table_data[row][0]))
                window['-name-'].update(str(table_data[row][1]))
                window['-location-'].update(str(table_data[row][2]))  # Changed from '-platform-'
                window['-date-'].update(str(table_data[row][3]))  # Changed from '-hours-'
                window['-status-'].update(str(table_data[row][4]))  # Changed from '-progress-'
                window['-pos_file-'].update(str(table_data[row][5]))

        # Handle the event of clearing fields
        if event == 'Clear':
            window['-id-'].update(disabled=False)
            window['-id-'].update('')
            window['-name-'].update('')
            window['-location-'].update('')  # Changed from '-platform-'
            window['-date-'].update('')  # Changed from '-hours-'
            window['-status-'].update('')  # Changed from '-progress-'
            window['-pos_file-'].update('')

        # Handle the event of modifying a sport event
        if event == 'Modify':
            handle_modify_event(event, values, l_sport_event, table_data, window)

        # Handle the event of clicking on the table to sort
        if isinstance(event, tuple):
            if event[0] == '-Table-':
                if event[2][0] == -1:  # Header was clicked
                    col_num_clicked = event[2][1]
                    table_data = sort_table(table_data, (col_num_clicked, 0))
                    window['-Table-'].update(table_data)

    # Close the window when exiting the loop
    window.close()


# Call the main function
interface()

