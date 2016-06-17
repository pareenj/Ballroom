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

os.chdir("/home/pareenj/Ballroom_Python/3")

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
i = 4000
#	event = events_data[k]
#for event in events_data:
for k in range(4000, 5000):
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