import functions
import re
import subprocess
import os, sys
import psycopg2

pdb_path = '/home/marta/Licencjat/pdb_gz'
rv_path = '/home/marta/RNAVIEW/bin/rnaview'
mc_path = '/home/marta/Licencjat/Licencjat/MC-annotate/MC-Annotate'
table = 'Interactions'
columns = 'structure_id, method, interaction_full_line, interaction, sanger_classification, first_chain, second_chain, first_nucleotide, second_nucleotide, first_nr_nucleotide, second_nr_nucleotide'


ids = open('lista_testowa').read()
id_list = re.findall('\'{1}[0-9]+[A-Z 0-9]+\'{1}', ids)
indirectory = os.listdir(pdb_path)


i = 0
for a in id_list:
	id_list[i] = a.strip('\'').lower()
	i = i + 1
	
j = 0
for a in id_list:
	b = 'pdb' + a + '.ent'
	if ((b in indirectory) == False):
		del(id_list[j])
	j = j + 1




def rv(path):
	j = 0
	for a in id_list:
		if (subprocess.run([path, pdb_path + "/" + "pdb" + a + ".ent/" + "data"])):
			j = j + 1
	print(j)
	print(len(id_list))
	


def mc(path):
	for a in id_list:
			
			f = open(pdb_path + "/" + "pdb" + a + ".ent/" + "mcdata.out", 'w')
			subprocess.run([path, pdb_path + "/" + "pdb" + a + ".ent/" + "data"], stdout = f )
		



def insert(table, columns, values):
    connection = psycopg2.connect("dbname='Interactions' user='postgres' host='localhost' password='minusz'")
    mark = connection.cursor()
    statement = 'INSERT INTO ' + table + ' (' + columns + ') VALUES (' + values + ')'
    mark.execute(statement)
    connection.commit()
    return


def mc_parser()	:
	line_nr = 0
	for a in id_list:
		with open(pdb_path + '/pdb' + a + '.ent/' + 'mcdata.out') as f:
			content = f.readlines()
			content = [x.strip() for x in content]
		for i in range(0, len(content)):
			if('Base-pairs' in content[i]):
				line_nr = i
		del(content[0:line_nr + 1])
		lines = content
		for j in lines:
		
			if (len(functions.mc_chains(j)) == 2):
				f_chain = functions.mc_chains(j)[0]
				s_chain = functions.mc_chains(j)[1]
			else: 
				f_chain = 'n/a'
				s_chain = 'n/a'
			
			if (len(functions.mc_nucleotides(j)) == 2):
				f_nucleotide = functions.mc_nucleotides(j)[0]
				s_nucleotide = functions.mc_nucleotides(j)[1]
			else:
				f_nucleotide = 'n/a'
				s_nucleotide = 'n/a'
				
			if (len(functions.mc_nr_nucleotides(i)) == 2):
				f_nr_nucleotide = functions.mc_nr_nucleotides(j)[0]
				s_nr_nucleotide = functions.mc_nr_nucleotides(j)[1]
			else:
				f_nr_nucleotide = 'n/a'
				s_nr_nucleotide = 'n/a'
				
				
			values = '\'' + a + '\'' + ', \''+  'MC-Annotate' +  '\', ' + '\'' + functions.mc_full(j) + '\'' + ', \'' +  functions.mc_interaction(j) + '\'' + ', \'' + functions.mc_sanger(j) + '\'' + ', \''+ f_chain + '\'' + ', \'' + s_chain + '\'' + ', \'' + f_nucleotide + '\'' + ', \'' + s_nucleotide + '\'' + ', ' + f_nr_nucleotide + ', ' + s_nr_nucleotide
			insert(table, columns, values)
			 

	
mc_parser()



