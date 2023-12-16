class SportEvent:
    # Class variables
    headings = ['ID', 'Event Name', 'Location', 'Date', 'Status']
    fields = {
        '-id-': 'SportEvent ID:',
        '-name-': 'SportEvent Name:',
        '-location-': 'Location:',
        '-date-': 'Date:',
        '-status-': 'Status:',
        '-pos_file-': 'Position into File'
    }

    # Constructor method
    def __init__(self, id, name, location, date, status, pos_file, erased=False):
        # Instance attributes
        self.id = id
        self.name = name
        self.location = location
        self.date = date
        self.status = status
        self.pos_file = pos_file
        self.erased = erased

    # Equality comparison method
    def __eq__(self, other):
        return other.pos_file == self.pos_file

    # String representation method
    def __str__(self):
        return (
                str(self.id) + str(self.name) + str(self.location) +
                str(self.date) + str(self.status) + str(self.pos_file)
        )

    # Method to check if the sport event is in a specific position
    def sport_event_in_pos(self, pos):
        return self.pos_file == pos

    # Method to set sport event attributes
    def set_sport_event(self, name, location, date, status):
        self.name = name
        self.location = location
        self.date = date
        self.status = status
