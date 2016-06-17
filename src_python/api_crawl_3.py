# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 14:15:42 2016
@author: Pareen Jain
"""

# runfile('D:/wd/api_crawl.py', wdir='D:/wd')

import os
import requests
import csv
import json
#import pandas
from requests.auth import HTTPBasicAuth

os.chdir("D:/wd")

def getData(url):
	r = requests.get(url, auth = HTTPBasicAuth('pareenj', 'temporary67'))
	return r.json()

# define api URL
base_url = "https://services.worlddancesport.org/api/1/"


events_data = getData(base_url + "competition?format=json")
#with open('events_data' + '.json', 'w') as outfile:
#		json.dump(events_data, outfile)
events_count = len(events_data)

# EventsColumns = ['event_id', 'event_name', 'event_date', 'event_location', 'event_country', 'event_status', 'event_type', 'event_discipline', 'event_division', 'event_coefficient', 'event_last_modified_date', 'event_eventId', 'event_groupId']
# Events = pandas.DataFrame(columns = EventsColumns)
# PlacementsColumns = ['couple_event_id', 'event_id', 'couple_id', 'couple_placement', 'couple_basepoints', 'couple_status', 'couple_number']
# Placements = pandas.DataFrame(columns = PlacementsColumns)
# JudgeEventColumns = ['event_judge_id', 'event_id', 'judge_id', 'judge_name', 'judge_task', 'judge_country']
# JudgeEvents = pandas.DataFrame(columns = JudgeEventColumns)
# MarksColumns = ['event_id', 'couple_id', 'round_name', 'dance_name', 'judge_id', 'mark_given']
# Marks = pandas.DataFrame(columns = MarksColumns)

#i = 0
i = 1684
#	event = events_data[k]
#for event in events_data:
for k in range(1684, events_count):
	event = events_data[k]
	i = i + 1
	print(i, 'out of', events_count, 'events:\n')
	
	event_self = getData(event['link'][0]['href'] + '?format=json')
	with open('event' + str(i) + '_self.json', 'w') as outfile:
		json.dump(event_self, outfile)
	if 'Code' not in event_self.keys():
		row = {}
		row['event_id'] = event_self['id']
		row['event_name'] = event['name']
		row['event_agegroup'] = event_self['age']
		row['event_date'] = event_self['date']
		row['event_location'] = event_self['location']
		row['event_country'] = event_self['country']
		row['event_type'] = event_self['type']
		row['event_discipline'] = event_self['discipline']
		row['event_division'] = event_self['division']
		row['status'] = event_self['status']
		row['event_coefficient'] = event_self['coefficient']
		row['event_last_modified_date'] = event_self['lastmodifiedDate']
		row['event_eventId'] = event_self['eventId']
		row['event_groupId'] = event_self['groupId']
		#Events = Events.append(row, ignore_index = True)
		if not os.path.isfile("Events.csv"):
			with open("Events.csv", "a") as csvfile:
				writer = csv.DictWriter(csvfile, delimiter = ',', lineterminator = '\n', fieldnames = row.keys())
				writer.writeheader()
				writer.writerow(row)
		else:
			with open("Events.csv", "a") as csvfile:
				writer = csv.DictWriter(csvfile, delimiter = ',', lineterminator = '\n', fieldnames = row.keys())
				writer.writerow(row)
	else:
		print('Error:', event_self['Code'], '\n', 'Message:', event_self['Message'], '\n')
	

	event_participants = getData(event['link'][1]['href'] + '&format=json')
	with open('event' + str(i) + '_participants.json', 'w') as outfile:
		json.dump(event_participants, outfile)
	if type(event_participants) == list:
		j = 0
		#j = 60
		# for j in range(23, len(event_participants)):
		# 	participant = event_participants[j]
		for participant in event_participants:
			j = j + 1
			participant_self = getData(participant['link'][0]['href'] + '?format=json')
			with open('participant' + str(i) + '_' + str(j) + '_self.json', 'w') as outfile:
				json.dump(participant_self, outfile)
			if 'Code' not in participant_self.keys():
				row = {}
				row['couple_event_id'] = participant_self['id']
				row['event_id'] = participant_self['competitionId']
				row['couple_id'] = participant_self['coupleId']
				row['couple_placement'] = participant_self['rank']
				row['couple_basepoints'] = participant_self['basepoints']
				row['couple_status'] = participant_self['status']
				row['couple_number'] = participant['number']

				#Placements = Placements.append(row, ignore_index = True)
				if not os.path.isfile("Placements.csv"):
					with open("Placements.csv", "a") as csvfile:
						writer = csv.DictWriter(csvfile, delimiter = ',', lineterminator = '\n', fieldnames = row.keys())
						writer.writeheader()
						writer.writerow(row)
				else:
					with open("Placements.csv", "a") as csvfile:
						writer = csv.DictWriter(csvfile, delimiter = ',', lineterminator = '\n', fieldnames = row.keys())
						writer.writerow(row)

				participant_rounds = participant_self['rounds']
				for rounds in participant_rounds:
					for dance in rounds['dances']:
						for scores in dance['scores']:
							row = {}
							row['event_id'] = participant_self['competitionId']
							row['couple_id'] = participant_self['coupleId']
							row['round_name'] = rounds['name']
							row['dance_name'] = dance['name']
							row['judge_id'] = scores['adjudicator']
							if row['round_name'] == 'F':
								row['mark_given'] = scores['rank']
							else:
								row['mark_given'] = scores['kind']

							#Marks = Marks.append(row, ignore_index = True)
							if not os.path.isfile("Marks.csv"):
								with open("Marks.csv", "a") as csvfile:
									writer = csv.DictWriter(csvfile, delimiter = ',', lineterminator = '\n', fieldnames = row.keys())
									writer.writeheader()
									writer.writerow(row)
							else:
								with open("Marks.csv", "a") as csvfile:
									writer = csv.DictWriter(csvfile, delimiter = ',', lineterminator = '\n', fieldnames = row.keys())
									writer.writerow(row)

			else:
				print('Error:', participant_self['Code'], '\n', 'Message:', participant_self['Message'], '\n')
		print('Placements and Marks updated\n')
	elif 'Code' in event_participants.keys():
		print('Error:', event_participants['Code'], '\n', 'Message:', event_participants['Message'], '\n')
	else:
		print('Unknown Error\n')
	

	event_officials = getData(event['link'][2]['href'] + '&format=json')
	with open('event_officials' + str(i) + '.json', 'w') as outfile:
				json.dump(participant_self, outfile)
	if type(event_officials) == list:
		j = 0
		for official in event_officials:
			j = j + 1
			official_self = getData(official['link'][0]['href'] + '?format=json')
			with open('official' + str(i) + '_' + str(j) + '_self.json', 'w') as outfile:
				json.dump(official_self, outfile)
			if('Code' not in official_self.keys()):
				row = {}
				row['event_judge_id'] = official_self['id']
				row['event_id'] = official_self['competitionId']
				row['judge_id'] = official_self['min']
				row['judge_name'] = official_self['name']
				row['judge_task'] = official_self['task']		
				row['judge_country'] = official_self['country']

				#JudgeEvents = JudgeEvents.append(row, ignore_index = True)
				if not os.path.isfile("JudgeEvents.csv"):
					with open("JudgeEvents.csv", "a") as csvfile:
						writer = csv.DictWriter(csvfile, delimiter = ',', lineterminator = '\n', fieldnames = row.keys())
						writer.writeheader()
						writer.writerow(row)
				else:
					with open("JudgeEvents.csv", "a") as csvfile:
						writer = csv.DictWriter(csvfile, delimiter = ',', lineterminator = '\n', fieldnames = row.keys())
						writer.writerow(row)
			else:
				print('Error:', official_self['Code'], '\n', 'Message:', official_self['Message'], '\n')
		print('JudgeEvents updated\n\n')
	elif 'Code' in event_officials.keys():
		print('Error:', event_officials['Code'], '\n', 'Message:', event_officials['Message'], '\n')
	else:
		print('Unknown Error\n')

couples_data = getData(base_url + 'couple?status=any&format=json')
with open('couples_data' + '.json', 'w') as outfile:
		json.dump(couples_data, outfile)
couples_count = len(couples_data)

# CouplesColumns = ['couple_id', 'couple_name', 'couple_country', 'couple_division', 'couple_agegroup', 'couple_status', 'athlete_male_id', 'athlete_female_id', 'couple_national_reference']
# Couples = pandas.DataFrame(columns = CouplesColumns)

i = 0
for couple in couples_data:
	i = i + 1
	print(i, 'out of', couples_count, 'couples:\n')

	couple_self = getData(couple['link'][0]['href'] + '?format=json')
	with open('couple' + str(i) + '_self.json', 'w') as outfile:
		json.dump(couple_self, outfile)
	if 'Code' not in couple_self.keys():
		row = {}
		row['couple_id'] = couple_self['id']
		row['couple_name'] = couple_self['name']
		row['event_country'] = couple_self['country']
		row['event_division'] = couple_self['division']
		row['event_agegroup'] = couple_self['age']
		row['status'] = couple_self['status']
		row['athlete_male_id'] = couple_self['man']
		row['athlete_female_id'] = couple_self['woman']
		row['couple_national_reference'] = couple_self['nationalReference']
		row['couple_retire_date'] = couple_self['retireOn']

		#Couples = Couples.append(row, ignore_index = True)
		if not os.path.isfile("Couples.csv"):
			with open("Couples.csv", "a") as csvfile:
				writer = csv.DictWriter(csvfile, delimiter = ',', lineterminator = '\n', fieldnames = row.keys())
				writer.writeheader()
				writer.writerow(row)
		else:
			with open("Couples.csv", "a") as csvfile:
				writer = csv.DictWriter(csvfile, delimiter = ',', lineterminator = '\n', fieldnames = row.keys())
				writer.writerow(row)
	else:
		print('Error:', couple_self['Code'], '\n', 'Message:', couple_self['Message'])
print('\n')


athletes_data = getData(base_url + 'person?status=Any&type=Athlete&format=json')
with open('athletes_data' + '.json', 'w') as outfile:
		json.dump(athletes_data, outfile)
athletes_count = len(athletes_data)

# AthletesColumns = ['athlete_id', 'athlete_name', 'athlete_surname', 'athlete_country', 'athlete_nationality', 'athlete_sex', 'athlete_agegroup', 'athlete_national_reference']
# Athletes = pandas.DataFrame(columns = AthletesColumns)

i = 0
for athlete in athletes_data:
	i = i + 1
	print(i, 'out of', athletes_count, 'judges:\n')

	athlete_self = getData(athlete['link'][0]['href'] + '?format=json')
	with open('athlete' + str(i) + '_self.json', 'w') as outfile:
		json.dump(athlete_self, outfile)
	if 'Code' not in athlete_self.keys():
		row = {}
		row['athlete_id'] = athlete_self['id']
		row['athlete_name'] = athlete_self['name']
		row['athlete_surname'] = athlete_self['surname']
		row['athlete_country'] = athlete_self['country']
		row['athlete_nationality'] = athlete_self['nationality']
		row['athlete_sex'] = athlete_self['sex']
		row['athlete_agegroup'] = athlete_self['ageGroup']
		row['athlete_national_reference'] = athlete_self['nationalReference']

		#Athletes = Athletes.append(row, ignore_index = True)
		if not os.path.isfile("Athletes.csv"):
			with open("Athletes.csv", "a") as csvfile:
				writer = csv.DictWriter(csvfile, delimiter = ',', lineterminator = '\n', fieldnames = row.keys())
				writer.writeheader()
				writer.writerow(row)
		else:
			with open("Athletes.csv", "a") as csvfile:
				writer = csv.DictWriter(csvfile, delimiter = ',', lineterminator = '\n', fieldnames = row.keys())
				writer.writerow(row)
	else:
		print('Error:', athlete_self['Code'], '\n', 'Message:', athlete_self['Message'])
print('\n')


judges_data = getData(base_url + 'person?status=Any&type=Adjudicator&format=json')
with open('judges_data' + '.json', 'w') as outfile:
		json.dump(judges_data, outfile)
judges_count = len(judges_data)

# JudgesColumns = ['judge_id', 'judge_name', 'judge_surname', 'judge_country', 'judge_nationality', 'judge_sex', 'judge_agegroup', 'judge_licenses', 'judge_national_reference']
# Judges = pandas.DataFrame(columns = JudgesColumns)

i = 0
for judge in judges_data:
	i = i + 1
	print(i, 'out of', judges_count, 'judges:\n')

	judge_self = getData(judge['link'][0]['href'] + '?format=json')
	with open('judge' + str(i) + '_self.json', 'w') as outfile:
		json.dump(judge_self, outfile)
	if 'Code' not in judge_self.keys():
		row = {}
		row['judge_id'] = judge_self['id']
		row['judge_name'] = judge_self['name']
		row['judge_surname'] = judge_self['surname']
		row['judge_country'] = judge_self['country']
		row['judge_nationality'] = judge_self['nationality']
		row['judge_sex'] = judge_self['sex']
		row['judge_agegroup'] = judge_self['ageGroup']
		row['judge_licenses'] = judge_self['licenses']
		row['judge_national_reference'] = judge_self['nationalReference']

		#Judges = Judges.append(row, ignore_index = True)
		if not os.path.isfile("Judges.csv"):
			with open("Judges.csv", "a") as csvfile:
				writer = csv.DictWriter(csvfile, delimiter = ',', lineterminator = '\n', fieldnames = row.keys())
				writer.writeheader()
				writer.writerow(row)
		else:
			with open("Judges.csv", "a") as csvfile:
				writer = csv.DictWriter(csvfile, delimiter = ',', lineterminator = '\n', fieldnames = row.keys())
				writer.writerow(row)
	else:
		print('Error:', judge_self['Code'], '\n', 'Message:', judge_self['Message'])
print('\n')


# Events.to_csv("Events1.csv")
# Placements.to_csv("Placements1.csv")
# Marks.to_csv("Marks1.csv")
# JudgeEvents.to_csv("JudgeEvents1.csv")
# Couples.to_csv("Couples1.csv")
# Athletes.to_csv("Athletes1.csv")
# Judges.to_csv("Judges1.csv")
  
# define resource URI
# resources = ["competition", "person", "couple", "team", "ranking", "country", "age"]
# for resource in resources:
# 	# make the data request
# 	r = requests.get(base_url + resource + '?format=json', auth=HTTPBasicAuth('pareenj', 'temporary67'))
# 	# write the received data to file
# 	with open(resource + '.json', 'w') as outfile:
# 		json.dump(r.json(), outfile)
  
# competition_response = requests.get(base_url + "competition?format=json", auth = HTTPBasicAuth('pareenj', 'temporary67'))
# competition_json = competition_response.json()

# competition_ids = []
# for i in range(len(competition_json)):
# 	competition_ids.append(competition_json[i]['id'])