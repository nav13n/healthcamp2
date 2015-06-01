import csv

class CSVCollection:

	headers = []
	data = []
	def __init__(self, filename, delimiter = ",", has_headers = True):
		rows = []
		data = []
		header_flag = False
		with open(filename, "r") as f:
			for row in csv.reader(f, delimiter = delimiter):
				if not header_flag and has_headers:
					self.headers = [col for col in row]
					header_flag = True
				else:
					self.data.append([col for col in row])
	
	def get_row(self, index):
		if len(self.data) > index + 1:
			return self.data[index]
	
	def get_column(self, column):
		if type(column) is str:
			index = self.headers.index(column_name)
		else:
			index = int(column)
		return [row[index] for row in self.data]

			
if __name__ == "__main__":
	collection = CSVCollection("factors.csv")
	print collection.data