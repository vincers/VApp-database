import csv
import json

def readCSV():
	file = open('AME.csv')
	csvreader = csv.reader(file)

	header = []
	header = next(csvreader)

	rows = []
	for row in csvreader:
			rows.append(row[0].split(";"))

	file.close()

#def inserir_BD():


#ART
def IDToCode(ID, art_type):
	ID = str(ID)
	abbr = art_type[int(ID[0])]["abbr"]
	ID.pop(0)
	return abbr + ID

def CodeToID(code, art_type):
	i = 0

	for i in range(len(art_type)):
		if art_type[i]["abbr"] == code[0]:

			idNumber = ""
			for j in range(len(code)):
				if j == 0:
					idNumber = idNumber + str(i + 1)

				else:
					idNumber = idNumber + code[j]

			break

	return int(idNumber)

#Calcular tempo de entrega dependendo do tipo de arte
#Preço de acordo com o tipo de produto


#Update BD com informações Art Type

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
				"shorts": {
					"viral": {"formato":"1080px x 1350px"},
					"reels": {"formato":"1080px x 1920px"},
					"igtv": {"formato":"1080px x 1920px"},
					"audio": {"formato":"1080px x 1350px;1080px x 1920px"}
				}
				},
				{
				"prime": {
					"youtube": {"formato":"1920px x 1080px"},
					"apresentacao": {"formato":"1920px x 1080px"},
					"treinamento": {"formato":"1920px x 1080px"}
				}
				},
				{
				"masterclass": {
					"video de vendas": {"formato":"1920px x 1080px"},
					"aula": {"formato":"1920px x 1080px"},
					"documentario": {"formato":"1920px x 1080px"}
				}
				}
			]
			},

			{
			"name": "imagem",
			"abbr": "m",

			"types": [
				{
				"name": "storie",
				 "formato": "1080px x 1920px"
				},
				{
				"name": "feed",
				"formato": "1080px x 1080px"
				},
				{
				"name": "feed vertical",
				"formato": "1080px x 1350px"
				},
				{
				"name": "feed horizontal",
				"formato": "1920px x 1080px"
				},
				{
				"name": "slide",
				"formato": "1920px x 1080px"
				},
				{
				"name": "ebook",
				"formato":"2560px x 1600px"
				},
				{
				"name": "encarte",
				"formato":"multiplos"
				}
			]
			},

			{
			"name": "padronizacao",
			"abbr": "p",

			"types": [
				{
				"name": "vinheta",
				"formato": "1920px x 1080px"
				},
				{
				"name": "animacao",
				"formato":"1920px x 1080px"
				},
				{
				"name": "capa rede social",
				"formato": "2048px x 1152px",
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
				"duracao maxima": "2min30"
				},
				{
				"name": "categorizacao viral II",
				"duracao maxima": "12min"
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

	writeJSON()
	print("worked")

	with open('data.json', 'r') as openfile:
		json_object = json.load(openfile)

	art_type = json_object['art_type']
	
	c = "c1140"
	s = CodeToID(c, art_type)
	print(s)
	#Criar cards de artes



if __name__ == "__main__":
    main()