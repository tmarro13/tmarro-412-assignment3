from django.db import models
import os
from datetime import datetime

# Voter model stores data for a registered voter in Newton, MA
class Voter(models.Model):
    # Identification fields
    voter_id_number = models.CharField(max_length=20)  # Unique identifier for the voter
    first_name = models.TextField()  # First name of the voter
    last_name = models.TextField()  # Last name of the voter

    # Address fields
    street_number = models.TextField()  # House/street number
    street_name = models.TextField()  # Street name
    apartment_number = models.TextField(null=True, blank=True)  # Optional apartment number
    zip_code = models.TextField()  # Postal zip code

    # Date fields
    date_of_birth = models.DateField(null=True, blank=True)  # Voter's birth date
    date_of_registration = models.DateField(null=True, blank=True)  # Registration date

    # Party affiliation and precinct information
    party_affiliation = models.TextField()  # Political party affiliation
    precinct_number = models.TextField()  # Precinct within the town

    # Voting history fields for recent elections
    v20state = models.BooleanField()  # Participation in 2020 state election
    v21town = models.BooleanField()  # Participation in 2021 town election
    v21primary = models.BooleanField()  # Participation in 2021 primary election
    v22general = models.BooleanField()  # Participation in 2022 general election
    v23town = models.BooleanField()  # Participation in 2023 town election
    voter_score = models.IntegerField()  # Total number of elections the voter participated in

    def __str__(self):
        """Return a string with the voter's name and primary address details."""
        return f'{self.first_name} {self.last_name} ({self.street_name}, {self.zip_code})'


# Function to load voter data from a CSV file into the Voter model
def load_data(csv_path="newton_voters.csv"):
    """Read voter data from a CSV file and save each record as a Voter instance."""
    # Clear existing records to prevent duplicates
    Voter.objects.all().delete()
    
    # Define file path for CSV
    app_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(app_dir, csv_path)
    
    # Open the CSV file and read the headers
    with open(filename, encoding='utf-8') as f:
        headers = f.readline()  
        print(f'Headers: {headers}')
        
        for line in f:
            try:
                fields = line.strip().split(',')  
                # Skip lines with fewer than expected fields
                if len(fields) < 17:
                    print(f'Skipping line due to incorrect field count: {line}')
                    continue

                def parse_bool(value):
                    """Convert string to Boolean."""
                    return value.strip().lower() in ('1', 'true', 'yes')

                def parse_date(value):
                    """Convert string to date, if possible."""
                    try:
                        return datetime.strptime(value.strip(), '%Y-%m-%d').date()
                    except (ValueError, TypeError):
                        return None

                # Create and save a Voter instance with the parsed CSV data
                voter = Voter(
                    voter_id_number=fields[0].strip(),
                    last_name=fields[1].strip(),
                    first_name=fields[2].strip(),
                    street_number=fields[3].strip(),
                    street_name=fields[4].strip(),
                    apartment_number=fields[5].strip() if fields[5].strip() else None,
                    zip_code=fields[6].strip(),
                    date_of_birth=parse_date(fields[7]),
                    date_of_registration=parse_date(fields[8]),
                    party_affiliation=fields[9].strip(),
                    precinct_number=fields[10].strip(),
                    v20state=parse_bool(fields[11]),
                    v21town=parse_bool(fields[12]),
                    v21primary=parse_bool(fields[13]),
                    v22general=parse_bool(fields[14]),
                    v23town=parse_bool(fields[15]),
                    voter_score=int(fields[16].strip()),
                )
                voter.save()  
                print(f'Created voter: {voter}')

            except Exception as e:
                # Log any errors that occur during processing
                print(f"Exception on line: {line}")
                print(f"Error: {e}")
