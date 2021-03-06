import csv
import json
import mysql.connector
from datetime import datetime, timedelta, date

def readCSV():
	file = open('AME.csv')
	csvreader = csv.reader(file)

	header = []
	header = next(csvreader)

	rows = []
	for row in csvreader:
			rows.append(row[0].split(";"))

	file.close()
	return rows

#ART
def IDToCode(ID, art_type):
	ID = str(ID)
	abbr = art_type[int(ID[0])]["abbr"]
	ID.pop(0)
	return abbr + ID

def CodeToID(code, art_type):
	i = 0

	if code[0].lower() == "a":
		idNumber = ""
		for j in range(len(code)):
			if j == 0:
				idNumber = "6"
				continue

			if j == 1 and code[1].lower() == 'v':
				continue

			else:
				idNumber = idNumber + code[j]

		return int(idNumber)

	for i in range(len(art_type)):
		if art_type[i]["abbr"] == code[0].lower():

			idNumber = ""
			for j in range(len(code)):
				if j == 0:
					idNumber = idNumber + str(i + 1)

				else:
					idNumber = idNumber + code[j]

			return int(idNumber)

#Calcular tempo de entrega dependendo do tipo de arte
#Preço de acordo com o tipo de produto

#Update BD com informações Art Type
def DadosArtType(data, mycursor):

	sql = "INSERT INTO Art_Type (name, specification) VALUES (%s, %s)"

	for i in data:
		name = i["name"]
		spec = json.dumps(i["types"])

		val = (name, spec)
		mycursor.execute(sql, val)

#TODO - colocar limite de final de semana e limite de horário para entrega (fazer os pulos certos)
def CalcularPrazo(duration):
	duration = duration.split(":")
	return datetime.now() + timedelta(hours= int(duration[0]), minutes= int(duration[1]), seconds= int(duration[2]))

def EncontrarEspecifico(tipo, data):

	if tipo.lower() == "feed":
		return data['art_type'][0]['types'][0]['types'][0]

	if tipo.lower() == "stories":
		return data['art_type'][0]['types'][0]['types'][0]

	if tipo.lower() == "igtv":
		return data['art_type'][0]['types'][0]['types'][2]

	if tipo.lower() == "reels":
		return data['art_type'][0]['types'][0]['types'][1]

	if tipo.lower() == "audio":
		return data['art_type'][0]['types'][0]['types'][3]

	else:
		return data['art_type'][0]['types'][0]['types'][0]

def DadosArt(data, mycursor):

	artes = readCSV()

	type_id = 0
	client_id = 4
	creator_id = 3

	sql = "INSERT INTO Art (art_id, type_id, specification, client_id, creator_id, title, description, files, delivery_time, status, final_file) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

	for i in range(len(artes)):
		try:
			art_id = CodeToID(artes[i][0], data['art_type'])
			spec = EncontrarEspecifico(artes[i][3], data)
			specification = json.dumps(spec)
			title = artes[i][1]
			description = artes[i][2]
			files = "Vídeo base: " + artes[i][6]
			status = artes[i][4]
			final_file = artes[i][5]
			delivery_time = CalcularPrazo(spec["eta"]["level 2"])

			val = (art_id, type_id, specification, client_id, creator_id, title, description, files, delivery_time, status, final_file)
			
			mycursor.execute(sql, val)

		except:
			continue
		

def writeJSON():

	#Dicionários
	data = {
		'user_type' : ["Admin", "Creator", "Client Master", "Client Worker"],
		
		'art_type' : [
			{
			"name": "video",
			"abbr": "v",

			"types": [
				{
				"name": "shorts",
				"types": [
					{
					"name": "viral",
					"formato":"1080px x 1350px",
					"eta": {"level 1": "30:00:00", "level 2": "54:00:00","level 3": "78:00:00"}
					},
					{
					"name": "reels",
					"formato":"1080px x 1920px",
					"eta": {"level 1": "30:00:00", "level 2": "54:00:00","level 3": "78:00:00"}
					},
					{
					"name": "igtv",
					"formato":"1080px x 1920px",
					"eta": {"level 1": "30:00:00", "level 2": "54:00:00","level 3": "78:00:00"}
					},
					{
					"name": "audio",
					"formato": ["1080px x 1350px", "1080px x 1920px"],
					"eta": {"level 1": "30:00:00", "level 2": "54:00:00","level 3": "78:00:00"}
					}
				]
				},

				{
				"name": "prime",
				"tipes": [
					{
					"name": "youtube",
					"formato":"1920px x 1080px",
					"eta": {"level 1": "54:00:00", "level 2": "102:00:00","level 3": "126:00:00"}
					},
					{
					"name": "apresentacao",
					"formato":"1920px x 1080px",
					"eta": {"level 1": "54:00:00", "level 2": "102:00:00","level 3": "126:00:00"}
					},
					{
					"name": "treinamento",
					"formato":"1920px x 1080px",
					"eta": {"level 1": "54:00:00", "level 2": "102:00:00","level 3": "126:00:00"}
					}
				]
				},
				{
				"name": "masterclass",
				"types":  [
					{
					"name": "video de vendas",
					"formato": "1920px x 1080px",
					"eta": {"level 1": "102:00:00", "level 2": "126:00:00","level 3": "174:00:00"}
					},
					{
					"name": "aula",
					"formato": "1920px x 1080px",
					"eta": {"level 1": "102:00:00", "level 2": "126:00:00","level 3": "174:00:00"}
					},
					{
					"name": "documentario",
					"formato": "1920px x 1080px",
					"eta": {"level 1": "102:00:00", "level 2": "126:00:00","level 3": "174:00:00"}
					}
				]
				}
			]
			},

			{
			"name": "imagem",
			"abbr": "m",

			"types": [
				{
				"name": "storie",
				"formato": "1080px x 1920px",
				"eta": {"level 1": "18:00:00", "level 2": "30:00:00","level 3": "42:00:00"}
				},
				{
				"name": "feed",
				"formato": "1080px x 1080px",
				"eta": {"level 1": "18:00:00", "level 2": "30:00:00","level 3": "42:00:00"}
				},
				{
				"name": "feed vertical",
				"formato": "1080px x 1350px",
				"eta": {"level 1": "18:00:00", "level 2": "30:00:00","level 3": "42:00:00"}
				},
				{
				"name": "feed horizontal",
				"formato": "1920px x 1080px",
				"eta": {"level 1": "18:00:00", "level 2": "30:00:00","level 3": "42:00:00"}
				},
				{
				"name": "slide",
				"formato": "1920px x 1080px",
				"eta": {"level 1": "54:00:00", "level 2": "102:00:00","level 3": "126:00:00"}
				},
				{
				"name": "ebook",
				"formato":"2560px x 1600px",
				"eta": {"level 1": "54:00:00", "level 2": "102:00:00","level 3": "126:00:00"}
				},
				{
				"name": "encarte",
				"formato":"multiplos",
				"eta": {"level 1": "18:00:00", "level 2": "30:00:00","level 3": "42:00:00"}
				}
			]
			},

			{
			"name": "padronizacao",
			"abbr": "p",

			"types": [
				{
				"name": "vinheta",
				"formato": "1920px x 1080px",
				"eta": "126:00:00"
				},
				{
				"name": "animacao",
				"formato":"1920px x 1080px",
				"eta": "126:00:00"
				},
				{
				"name": "capa rede social",
				"formato": "2048px x 1152px",
				"eta": "54:00:00",
				"corte central": "1235px x 338px",
				"margens": {"vertical": "406,5px; 1641,5px", "horizontal": "745px; 407px"}
				}
			]
			},
			{
			"name": "conteudo",
			"abbr": "c",

			"types": [
				{
				"name": "categorizacao viral I",
				"duracao maxima": "2min30",
				"eta": "54:00:00"
				},
				{
				"name": "categorizacao viral II",
				"duracao maxima": "12min",
				"eta": "54:00:00"
				}
			]
			}
		]
	}

    # Serializing json 
	json_object = json.dumps(data, indent = 4)
	  
	# Writing to sample.json
	with open("data.json", "w", encoding='utf-8') as outfile:
	    outfile.write(json_object)

def main():

	#Conectar banco de dados
	mydb = mysql.connector.connect(
		host="database-vapp.cmtdb9vnteq9.sa-east-1.rds.amazonaws.com",
		user="admin",
		password="nidryf-3Jewro-pydbud",
		database="VApp"
	)
	mycursor = mydb.cursor()

	#Criar arquivo JSON
	#writeJSON()
	#print("worked")

	#Ler arquivo JSON
	with open('data.json', 'r') as openfile:
		data = json.load(openfile)

	#Criar Art Type Table
	#art_type = data['art_type']
	#DadosArtType(art_type, mycursor)

	#Criar cards de artes
	DadosArt(data, mycursor)
	mydb.commit()
	print("Data uploaded")

	#Printar tudo
	mycursor.execute("SELECT * FROM Art")
	myresult = mycursor.fetchall()
	for x in myresult:
  		print(x)

	


if __name__ == "__main__":
    main()