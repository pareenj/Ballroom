# -*- coding: utf-8 -*-
u"""
Created on Mon Jun 13 14:15:42 2016
@author: Pareen Jain
"""

# runfile('D:/wd/api_crawl.py', wdir='D:/wd')

from __future__ import with_statement
from __future__ import absolute_import
import os
import requests
import csv
import json
#import pandas
from requests.auth import HTTPBasicAuth
from io import open

os.chdir(u"D:/wd")

def getData(url):
	r = requests.get(url, auth = HTTPBasicAuth(u'pareenj', u'temporary67'))
	return r.json()

# define api URL
base_url = u"https://services.worlddancesport.org/api/1/"


events_data = getData(base_url + u"competition?format=json")
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
i = 1623
#	event = events_data[k]
#for event in events_data:
for k in xrange(1623, 1672):
	event = events_data[k]
	i = i + 1
	print i, u'out of', events_count, u'events:\n'
	
	event_self = getData(event[u'link'][0][u'href'] + u'?format=json')
	with open(u'event' + unicode(i) + u'_self.json', u'w') as outfile:
		json.dump(event_self, outfile)
	if u'Code' not in event_self.keys():
		row = {}
		row[u'event_id'] = event_self[u'id']
		row[u'event_name'] = event[u'name']
		row[u'event_agegroup'] = event_self[u'age']
		row[u'event_date'] = event_self[u'date']
		row[u'event_location'] = event_self[u'location']
		row[u'event_country'] = event_self[u'country']
		row[u'event_type'] = event_self[u'type']
		row[u'event_discipline'] = event_self[u'discipline']
		row[u'event_division'] = event_self[u'division']
		row[u'status'] = event_self[u'status']
		row[u'event_coefficient'] = event_self[u'coefficient']
		row[u'event_last_modified_date'] = event_self[u'lastmodifiedDate']
		row[u'event_eventId'] = event_self[u'eventId']
		row[u'event_groupId'] = event_self[u'groupId']
		#Events = Events.append(row, ignore_index = True)
		if not os.path.isfile(u"Events.csv"):
			with open(u"Events.csv", u"a") as csvfile:
				writer = csv.DictWriter(csvfile, delimiter = u',', lineterminator = u'\n', fieldnames = row.keys())
				writer.writeheader()
				writer.writerow(row)
		else:
			with open(u"Events.csv", u"a") as csvfile:
				writer = csv.DictWriter(csvfile, delimiter = u',', lineterminator = u'\n', fieldnames = row.keys())
				writer.writerow(row)
	else:
		print u'Error:', event_self[u'Code'], u'\n', u'Message:', event_self[u'Message'], u'\n'
	

	event_participants = getData(event[u'link'][1][u'href'] + u'&format=json')
	with open(u'event' + unicode(i) + u'_participants.json', u'w') as outfile:
		json.dump(event_participants, outfile)
	if type(event_participants) == list:
		j = 0
		#j = 60
		# for j in range(23, len(event_participants)):
		# 	participant = event_participants[j]
		for participant in event_participants:
			j = j + 1
			participant_self = getData(participant[u'link'][0][u'href'] + u'?format=json')
			with open(u'participant' + unicode(i) + u'_' + unicode(j) + u'_self.json', u'w') as outfile:
				json.dump(participant_self, outfile)
			if u'Code' not in participant_self.keys():
				row = {}
				row[u'couple_event_id'] = participant_self[u'id']
				row[u'event_id'] = participant_self[u'competitionId']
				row[u'couple_id'] = participant_self[u'coupleId']
				row[u'couple_placement'] = participant_self[u'rank']
				row[u'couple_basepoints'] = participant_self[u'basepoints']
				row[u'couple_status'] = participant_self[u'status']
				row[u'couple_number'] = participant[u'number']

				#Placements = Placements.append(row, ignore_index = True)
				if not os.path.isfile(u"Placements.csv"):
					with open(u"Placements.csv", u"a") as csvfile:
						writer = csv.DictWriter(csvfile, delimiter = u',', lineterminator = u'\n', fieldnames = row.keys())
						writer.writeheader()
						writer.writerow(row)
				else:
					with open(u"Placements.csv", u"a") as csvfile:
						writer = csv.DictWriter(csvfile, delimiter = u',', lineterminator = u'\n', fieldnames = row.keys())
						writer.writerow(row)

				participant_rounds = participant_self[u'rounds']
				for rounds in participant_rounds:
					for dance in rounds[u'dances']:
						for scores in dance[u'scores']:
							row = {}
							row[u'event_id'] = participant_self[u'competitionId']
							row[u'couple_id'] = participant_self[u'coupleId']
							row[u'round_name'] = rounds[u'name']
							row[u'dance_name'] = dance[u'name']
							row[u'judge_id'] = scores[u'adjudicator']
							if row[u'round_name'] == u'F':
								row[u'mark_given'] = scores[u'rank']
							else:
								row[u'mark_given'] = scores[u'kind']

							#Marks = Marks.append(row, ignore_index = True)
							if not os.path.isfile(u"Marks.csv"):
								with open(u"Marks.csv", u"a") as csvfile:
									writer = csv.DictWriter(csvfile, delimiter = u',', lineterminator = u'\n', fieldnames = row.keys())
									writer.writeheader()
									writer.writerow(row)
							else:
								with open(u"Marks.csv", u"a") as csvfile:
									writer = csv.DictWriter(csvfile, delimiter = u',', lineterminator = u'\n', fieldnames = row.keys())
									writer.writerow(row)

			else:
				print u'Error:', participant_self[u'Code'], u'\n', u'Message:', participant_self[u'Message'], u'\n'
		print u'Placements and Marks updated\n'
	elif u'Code' in event_participants.keys():
		print u'Error:', event_participants[u'Code'], u'\n', u'Message:', event_participants[u'Message'], u'\n'
	else:
		print u'Unknown Error\n'
	

	event_officials = getData(event[u'link'][2][u'href'] + u'&format=json')
	with open(u'event_officials' + unicode(i) + u'.json', u'w') as outfile:
				json.dump(participant_self, outfile)
	if type(event_officials) == list:
		j = 0
		for official in event_officials:
			j = j + 1
			official_self = getData(official[u'link'][0][u'href'] + u'?format=json')
			with open(u'official' + unicode(i) + u'_' + unicode(j) + u'_self.json', u'w') as outfile:
				json.dump(official_self, outfile)
			if(u'Code' not in official_self.keys()):
				row = {}
				row[u'event_judge_id'] = official_self[u'id']
				row[u'event_id'] = official_self[u'competitionId']
				row[u'judge_id'] = official_self[u'min']
				row[u'judge_name'] = official_self[u'name']
				row[u'judge_task'] = official_self[u'task']		
				row[u'judge_country'] = official_self[u'country']

				#JudgeEvents = JudgeEvents.append(row, ignore_index = True)
				if not os.path.isfile(u"JudgeEvents.csv"):
					with open(u"JudgeEvents.csv", u"a") as csvfile:
						writer = csv.DictWriter(csvfile, delimiter = u',', lineterminator = u'\n', fieldnames = row.keys())
						writer.writeheader()
						writer.writerow(row)
				else:
					with open(u"JudgeEvents.csv", u"a") as csvfile:
						writer = csv.DictWriter(csvfile, delimiter = u',', lineterminator = u'\n', fieldnames = row.keys())
						writer.writerow(row)
			else:
				print u'Error:', official_self[u'Code'], u'\n', u'Message:', official_self[u'Message'], u'\n'
		print u'JudgeEvents updated\n\n'
	elif u'Code' in event_officials.keys():
		print u'Error:', event_officials[u'Code'], u'\n', u'Message:', event_officials[u'Message'], u'\n'
	else:
		print u'Unknown Error\n'

couples_data = getData(base_url + u'couple?status=any&format=json')
with open(u'couples_data' + u'.json', u'w') as outfile:
		json.dump(couples_data, outfile)
couples_count = len(couples_data)

# CouplesColumns = ['couple_id', 'couple_name', 'couple_country', 'couple_division', 'couple_agegroup', 'couple_status', 'athlete_male_id', 'athlete_female_id', 'couple_national_reference']
# Couples = pandas.DataFrame(columns = CouplesColumns)

i = 0
for couple in couples_data:
	i = i + 1
	print i, u'out of', couples_count, u'couples:\n'

	couple_self = getData(couple[u'link'][0][u'href'] + u'?format=json')
	with open(u'couple' + unicode(i) + u'_self.json', u'w') as outfile:
		json.dump(couple_self, outfile)
	if u'Code' not in couple_self.keys():
		row = {}
		row[u'couple_id'] = couple_self[u'id']
		row[u'couple_name'] = couple_self[u'name']
		row[u'event_country'] = couple_self[u'country']
		row[u'event_division'] = couple_self[u'division']
		row[u'event_agegroup'] = couple_self[u'age']
		row[u'status'] = couple_self[u'status']
		row[u'athlete_male_id'] = couple_self[u'man']
		row[u'athlete_female_id'] = couple_self[u'woman']
		row[u'couple_national_reference'] = couple_self[u'nationalReference']
		row[u'couple_retire_date'] = couple_self[u'retireOn']

		#Couples = Couples.append(row, ignore_index = True)
		if not os.path.isfile(u"Couples.csv"):
			with open(u"Couples.csv", u"a") as csvfile:
				writer = csv.DictWriter(csvfile, delimiter = u',', lineterminator = u'\n', fieldnames = row.keys())
				writer.writeheader()
				writer.writerow(row)
		else:
			with open(u"Couples.csv", u"a") as csvfile:
				writer = csv.DictWriter(csvfile, delimiter = u',', lineterminator = u'\n', fieldnames = row.keys())
				writer.writerow(row)
	else:
		print u'Error:', couple_self[u'Code'], u'\n', u'Message:', couple_self[u'Message']
print u'\n'


athletes_data = getData(base_url + u'person?status=Any&type=Athlete&format=json')
with open(u'athletes_data' + u'.json', u'w') as outfile:
		json.dump(athletes_data, outfile)
athletes_count = len(athletes_data)

# AthletesColumns = ['athlete_id', 'athlete_name', 'athlete_surname', 'athlete_country', 'athlete_nationality', 'athlete_sex', 'athlete_agegroup', 'athlete_national_reference']
# Athletes = pandas.DataFrame(columns = AthletesColumns)

i = 0
for athlete in athletes_data:
	i = i + 1
	print i, u'out of', athletes_count, u'judges:\n'

	athlete_self = getData(athlete[u'link'][0][u'href'] + u'?format=json')
	with open(u'athlete' + unicode(i) + u'_self.json', u'w') as outfile:
		json.dump(athlete_self, outfile)
	if u'Code' not in athlete_self.keys():
		row = {}
		row[u'athlete_id'] = athlete_self[u'id']
		row[u'athlete_name'] = athlete_self[u'name']
		row[u'athlete_surname'] = athlete_self[u'surname']
		row[u'athlete_country'] = athlete_self[u'country']
		row[u'athlete_nationality'] = athlete_self[u'nationality']
		row[u'athlete_sex'] = athlete_self[u'sex']
		row[u'athlete_agegroup'] = athlete_self[u'ageGroup']
		row[u'athlete_national_reference'] = athlete_self[u'nationalReference']

		#Athletes = Athletes.append(row, ignore_index = True)
		if not os.path.isfile(u"Athletes.csv"):
			with open(u"Athletes.csv", u"a") as csvfile:
				writer = csv.DictWriter(csvfile, delimiter = u',', lineterminator = u'\n', fieldnames = row.keys())
				writer.writeheader()
				writer.writerow(row)
		else:
			with open(u"Athletes.csv", u"a") as csvfile:
				writer = csv.DictWriter(csvfile, delimiter = u',', lineterminator = u'\n', fieldnames = row.keys())
				writer.writerow(row)
	else:
		print u'Error:', athlete_self[u'Code'], u'\n', u'Message:', athlete_self[u'Message']
print u'\n'


judges_data = getData(base_url + u'person?status=Any&type=Adjudicator&format=json')
with open(u'judges_data' + u'.json', u'w') as outfile:
		json.dump(judges_data, outfile)
judges_count = len(judges_data)

# JudgesColumns = ['judge_id', 'judge_name', 'judge_surname', 'judge_country', 'judge_nationality', 'judge_sex', 'judge_agegroup', 'judge_licenses', 'judge_national_reference']
# Judges = pandas.DataFrame(columns = JudgesColumns)

i = 0
for judge in judges_data:
	i = i + 1
	print i, u'out of', judges_count, u'judges:\n'

	judge_self = getData(judge[u'link'][0][u'href'] + u'?format=json')
	with open(u'judge' + unicode(i) + u'_self.json', u'w') as outfile:
		json.dump(judge_self, outfile)
	if u'Code' not in judge_self.keys():
		row = {}
		row[u'judge_id'] = judge_self[u'id']
		row[u'judge_name'] = judge_self[u'name']
		row[u'judge_surname'] = judge_self[u'surname']
		row[u'judge_country'] = judge_self[u'country']
		row[u'judge_nationality'] = judge_self[u'nationality']
		row[u'judge_sex'] = judge_self[u'sex']
		row[u'judge_agegroup'] = judge_self[u'ageGroup']
		row[u'judge_licenses'] = judge_self[u'licenses']
		row[u'judge_national_reference'] = judge_self[u'nationalReference']

		#Judges = Judges.append(row, ignore_index = True)
		if not os.path.isfile(u"Judges.csv"):
			with open(u"Judges.csv", u"a") as csvfile:
				writer = csv.DictWriter(csvfile, delimiter = u',', lineterminator = u'\n', fieldnames = row.keys())
				writer.writeheader()
				writer.writerow(row)
		else:
			with open(u"Judges.csv", u"a") as csvfile:
				writer = csv.DictWriter(csvfile, delimiter = u',', lineterminator = u'\n', fieldnames = row.keys())
				writer.writerow(row)
	else:
		print u'Error:', judge_self[u'Code'], u'\n', u'Message:', judge_self[u'Message']
print u'\n'


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