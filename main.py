import apiFunctions as api
from datetime import datetime
from dateutil import parser
import geocoder

def main():
	print('='*80)
	print("\n\t\tWelcome to the Whatsgoodly Scraper!\n")
	print('='*80)

	try:
		# If location already set in past, read file
		f = open("defaultlocation", "r")
		fileinput = f.read()
		f.close()
		
		# Extract location coordinates and name from file
		coords = fileinput.split('\n')
		
		defLat = coords[0]
		defLon = coords[1]

		# Set Coordinates to Defaults in File
		api.setLocation(defLat, defLon)
		print('Location Set to Lat: {}, Lon: {}\n'.format(defLat, defLon))

		
	except:
		# Ask the user for a default location for Python2 and 3
		try:
			default = raw_input("\nEnter default address or coordinates: ")
		except SyntaxError:
			default = input("\nEnter default address or coordinates: ")
		
		defCoords = geocoder.google(default[:])

		# Save the default location
		saveDefaultLocation(defCoords.latlng[0], defCoords.latlng[1])

		# Set the location
		api.setLocation(defCoords.latlng[0], defCoords.latlng[1])
		print('Default Location Set to Lat: {}, Lon: {}\n'.format(defCoords.latlng[0], defCoords.latlng[1]))
		

	# Print User Info Text
	print("Logging into Whatsgoodly...\n")
	online = True
	try:
		print('Successful!')
	except:
		print("Error: Not connected to the Internet\n")
		online = False
	if online:
		print("Use the commands below.")
		
		currentPolls = []
		
		# While loop for terminal UI.
		while True:
			
			# Attempt to get a user choice for Python 2 or 3.
			try:
				choice = raw_input("\t*Read Polls\t\t(R)\n\n\t*Set Location\t\t(A <address or coordinates>)\n\n\t*Quit App\t\t(Q)\n\n->")
			except SyntaxError:
				choice = input("\t*Read Polls\t\t(R)\n\n\t*Set Location\t\t(A <address or coordinates>)\n\n\t*Quit App\t\t(Q)\n\n->")
			
			# Read Polls
			if choice.upper() == 'R':
				currentPolls = api.getPolls()
				pollPrint(currentPolls)

			# Set Location via Address or Coordinates
			elif choice[0].upper() == 'L':
				g = geocoder.google(choice[2:])
				api.setLocation(g.latlng[0], g.latlng[1])
				print('Changed Location to Lat: {}, Lon: {}\n'.format(g.latlng[0], g.latlng[1]))

			# Quit App
			elif choice.upper() == 'Q':
				break;

# A function for prettily printing the polls
def pollPrint(allPolls):
	for poll in allPolls:
		print('-'*80)
		date = parser.parse(poll.created_date)
		print('Poll #{} Posted: {}\nQuestion: {}\nOptions:'.format(poll.id, date, poll.question))
		for i in range(0, len(poll.options)):
			print('\t{} | Votes: {}'.format(poll.options[i], poll.option_counts[i]))

		print('-'*80)

def saveDefaultLocation(lat, lon):
	try:	
		# Create file if it does not exist and write
		f = open("defaultlocation", 'w+')
		defaultString = str(lat) + '\n' + str(lon)
		f.write(defaultString)
		f.close()
	except:
		print("Unable to get location.")


main()