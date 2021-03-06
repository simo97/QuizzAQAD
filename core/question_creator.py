import csv
from core.models import Question, Choice
from datetime import datetime as dt


def proceed():
	data_tab = []
	with open('upload.csv') as csvfile:
		readCSV = csv.reader(csvfile,delimiter = ',')
		for row in readCSV:
			if (len(row) != 9):
				raise IndexError
			data_tab.append(row) # adding to data tab for futher usage
	print(data_tab)
	for line in data_tab:
		q = line_to_question(line)
		q.month = 2
		q.year = 2018
		q.value=5
		q.save()
		for choice in line_to_choice(q,line):
			choice.save()
	return True


def line_to_question(line = []):
	return Question(
		text=line[1],
		image_link= line[6] if line[6] is not None else None,
		topic = line[0],
		tags=line[7],
		scheduled_day=dt.strptime(line[8], '%d/%m/%y')
	)


def line_to_choice(question,line=[]):
	return [
		Choice(text=line[2],is_correct=True,question=question),
		Choice(text=line[3],question=question),
		Choice(text=line[4],question=question),
		Choice(text=line[5],question=question)
	]

