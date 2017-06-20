import re
import subprocess
import os, sys
import psycopg2
import config

#Functions that retrive data from RNAView output files:
def rv_full(line):
	line = line.lstrip().rstrip()
	return(line)

def rv_interaction(line):
	interactions = re.findall('[sSwWhH\+\-\?\.]{1}/{1}[sSwWhH\+\-\?\.]{1}',line)
	conformation = re.findall('cis|tran', line)
	if ("tran" in conformation):
		interactions[0] = "t" + interactions[0]
	elif ("cis" in conformation):
		interactions[0] = "c" + interactions[0]
	
	return("".join(interactions))

def rv_sanger(line):
    sanger = re.findall('[XVIn/a]+$', line)
    return("".join(sanger))

def rv_chains(line):
    find_chains = re.findall('[A-Z]+',(str(re.findall('[A-Z]{1,1}:',str(line)))))
    return(find_chains)

def rv_nucleotides(line):
	nucleotides = re.findall('[ACGTUacgtu]{1}-[ACGTUacgtu]{1}',line)
	nucleotides = "".join(nucleotides)
	nucleotides = nucleotides.split("-")
	return(nucleotides)

def rv_nr_nucleotides(line):
	nr_nuc = re.findall(' +[0-9]+ +', line)
	for i in range(0,len(nr_nuc)):
		nr_nuc[i] = nr_nuc[i].strip()
	return(nr_nuc)	
	
#--------------------------------------------------------------------------    
 
   
#Functions that retrive data from McAnnotate output files

def mc_full(line):
	line = line.lstrip().rstrip()
	return(line)

def mc_interaction(line):
	interactions = re.findall('[A-Z]+' ,(str(re.findall(' {1}[WHS]{1}[whs]{1}/[WHS]{1}[whs]{1} {1}', str(line)))))
	cut = '/'.join(interactions)
	conformations = re.findall('cis|trans',line)
	
	if ("trans" in conformations):
		cut = 't' + cut
	if ("cis" in conformations):
		cut = 'c' + cut
	
	return(cut)
	
def mc_sanger(line):
	sanger = re.findall(' +[XVI]+', line)
	if (len(sanger) == 1):
		sanger[len(sanger)-1] = sanger[len(sanger)-1].strip()
		return("".join(sanger))
	else:
		return('n/a')
	
def mc_chains(line):
	chains = re.findall('[A-Z]+[0-9]+-{1}[A-Z]+[0-9]+', line)
	chains = "".join(chains)
	find_chains = re.findall('[A-Z]+', chains)	
	return(find_chains)
	
	
def mc_nucleotides(line):
	nucleotides = re.findall('[ACGTUacgut]{1}-{1}[ACGTUacgut]{1}',line)
	nucleotides = "".join(nucleotides)
	nucleotides = nucleotides.split("-")
	return(nucleotides)
    
def mc_nr_nucleotides(line):
	chain_nr = re.findall('[0-9]+',(str(re.findall('[0-9]+-{1}[A-Z]+[0-9]+', str(line)))))
	return(chain_nr)

#-----------------------------------------------------------------------------------------



#Run RNAView
def rv_run(path):
	j = 0
	for a in id_list:
		if (subprocess.run([path, pdb_path + "/" + "pdb" + a + ".ent/" + "data"])):
			j = j + 1

	

#Run MC-Annotate
def mc_run(path):
	for a in id_list:
		f = open(pdb_path + "/" + "pdb" + a + ".ent/" + "mcdata.out", 'w')
		subprocess.run([path, pdb_path + "/" + "pdb" + a + ".ent/" + "data"], stdout = f )
		


#Insert data from programs outputs to database
def insert(table, columns, values):
	connect_data = '\"dbname=\'' + name_db +'\' user=\'' +user_db + '\' host=\'' + host + '\' password=\'' + passwd + '\'\"'
	connection = psycopg2.connect(connect_data)
	mark = connection.cursor()
	statement = 'INSERT INTO ' + table + ' (' + columns + ') VALUES (' + values + ')'
	mark.execute(statement)
	connection.commit()
	return

#Preparation of output files (MC-Annotate) for input into the database
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
		
		if(len(content) == 0) :
			values = '\'' + a + '\'' + ', \''+  'MC-Annotate' +  '\', ' + '\'' + 'n/a' + '\'' + ', \'' +  'n/a' + '\'' + ', \'' + 'n/a' + '\'' + ', \''+ 'n/a' + '\'' + ', \'' + 'n/a' + '\'' + ', \'' + 'n/a' + '\'' + ', \'' + 'n/a' + '\'' + ', ' + '0' + ', ' + '0'
			insert(table, columns, values)
			continue
		
		for j in content:
		
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
				
			if (len(functions.mc_nr_nucleotides(j)) == 2):
				f_nr_nucleotide = functions.mc_nr_nucleotides(j)[0]
				s_nr_nucleotide = functions.mc_nr_nucleotides(j)[1]
			else:
				f_nr_nucleotide = '0'
				s_nr_nucleotide = '0'
				
				
			values = '\'' + a + '\'' + ', \''+  'MC-Annotate' +  '\', ' + '\'' + functions.mc_full(j) + '\'' + ', \'' +  functions.mc_interaction(j) + '\'' + ', \'' + functions.mc_sanger(j) + '\'' + ', \''+ f_chain + '\'' + ', \'' + s_chain + '\'' + ', \'' + f_nucleotide + '\'' + ', \'' + s_nucleotide + '\'' + ', ' + f_nr_nucleotide + ', ' + s_nr_nucleotide
			print(values)
			insert(table, columns, values) 
			
#Preparation of output files (RNAView) for input into the database
def rv_parser() :
	line_nr = 0
	for a in id_list:
		with open(pdb_path + '/pdb' + a + '.ent/' + 'data.out') as f:
			content = f.readlines()
			content = [x.strip() for x in content]
		for i in range(0, len(content)):
			if('BEGIN_base-pair' in content[i]):
				line_nr = i
		del(content[0:line_nr + 1])
		
		for i in range(0, len(content)):
			if('END_base-pair' in content[i]):
				line_nr = i
		del(content[line_nr:len(content)])
	
		if(len(content) == 0) :
			values = '\'' + a + '\'' + ', \''+  'RNAView' +  '\', ' + '\'' + 'n/a' + '\'' + ', \'' +  'n/a' + '\'' + ', \'' + 'n/a' + '\'' + ', \''+ 'n/a' + '\'' + ', \'' + 'n/a' + '\'' + ', \'' + 'n/a' + '\'' + ', \'' + 'n/a' + '\'' + ', ' + '0' + ', ' + '0'
			insert(table, columns, values)
			continue
			
		for j in content:
			if (len(functions.rv_chains(j)) == 2):
				f_chain = functions.rv_chains(j)[0]
				s_chain = functions.rv_chains(j)[1]
			else: 
				f_chain = 'n/a'
				s_chain = 'n/a'
			
			if (len(functions.rv_nucleotides(j)) == 2):
				f_nucleotide = functions.rv_nucleotides(j)[0]
				s_nucleotide = functions.rv_nucleotides(j)[1]
			else:
				f_nucleotide = 'n/a'
				s_nucleotide = 'n/a'
				
			if (len(functions.rv_nr_nucleotides(j)) == 2):
				f_nr_nucleotide = functions.rv_nr_nucleotides(j)[0]
				s_nr_nucleotide = functions.rv_nr_nucleotides(j)[1]
			else:
				f_nr_nucleotide = '0'
				s_nr_nucleotide = '0'
				
			values = '\'' + a + '\'' + ', \''+  'RNAView' +  '\', ' + '\'' + functions.rv_full(j) + '\'' + ', \'' +  functions.rv_interaction(j) + '\'' + ', \'' + functions.rv_sanger(j) + '\'' + ', \''+ f_chain + '\'' + ', \'' + s_chain + '\'' + ', \'' + f_nucleotide + '\'' + ', \'' + s_nucleotide + '\'' + ', ' + f_nr_nucleotide + ', ' + s_nr_nucleotide
			insert(table, columns, values)
			print(values)











    
