import re
#Functions that retrive data from RNAView output files

def rv_full(line):
	line = line.lstrip().rstrip()
	return(line)

def rv_interactions(line):
	interactions = re.findall('[sSwWhH\+\-\?\.]{1}/{1}[sSwWhH\+\-\?\.]{1}',line)
	conformation = re.findall('cis|tran', line)
	if ("tran" in conformation):
		interactions[0] = "t" + interactions[0]
	elif ("cis" in conformation):
		interactions[0] = "c" + interactions[0]
	
	return(interactions)

def rv_sanger(line):
    sanger = re.findall('[XVIn/a]+$', line)
    return(sanger)

#return first and second chains
def rv_chains(line):
    find_chains = re.findall('[A-Z]{1,1}:',line)
    find_chains[0] = find_chains[0].strip(':')
    find_chains[1] = find_chains[1].strip(':')
    return(find_chains)

def rv_nucleotides(line):
	nucleotides = re.findall('[ACGUacgu]{1}-[ACGUacgu]{1}',line)
	nucleotides = "".join(nucleotides)
	nucleotides = nucleotides.split("-")
	print(nucleotides)

def rv_nr_nucleotides(line):
	nr_nuc = re.findall(' +[0-9]+ +', line)
	for i in renge(0,len(nr_nuc)):
		nr_nuc[i] = nr_nuc[i].strip()
	return(nr_nuc)	
    
    







#Functions that retrive data from McAnnotate output files

def mc_full(line):
	line = line.lstrip().rstrip()
	return(line)

def mc_interaction(line):
	interactions = re.findall(' {1}[WHS]{1}[whs]{1}/[WHS]{1}[whs]{1} {1}', line)
	interactions[0] = interactions[0].strip()
	cut = re.findall('[A-Z]+', interactions[0])
	cut = '/'.join(cut)
	conformations = re.findall('cis|trans',line)
	
	if ("trans" in conformations):
		cut = 't' + cut
	if ("cis" in conformations):
		cut = 'c' + cut
	
	return(cut)
	
def mc_sanger(line):
	if (' +[XVI]+ +' in line):
		sanger = re.findall(' +[XVI]+ +', line)
		if (len(sanger) == 1):
			sanger[len(sanger)-1] = sanger[len(sanger)-1].strip()
			return(sanger)
		else:
			return('n/a')
	else:
			return('n/a')


def mc_chains(line):
	chains = re.findall('[A-Z]+[1-9]+-{1}[A-Z]+[1-9]+', line)
	chains = "".join(chains)
	find_chains = re.findall('[A-Z]+', chains)	
	return(find_chains)
	
	
def mc_nucleotides(line):
	nucleotides = re.findall('[ACGTUacgut]{1}-{1}[ACGTUacgut]{1}',line)
	nucleotides = "".join(nucleotides)
	nucleotides = nucleotides.split("-")
	return(nucleotides)
    
def mc_nr_nucleotides(line):
	chain_nr = re.findall('[A-Z]+[1-9]+-{1}[A-Z]+[1-9]+', line)
	chain_nr = "".join(chain_nr)
	chains = re.findall('[1-9]+',chain_nr)
	return(chains)


linia = "A1-B24 : C-G Ww/Ww pairing antiparallel cis XIX"
a = mc_nucleotides(linia)
print(a)



#TABLE
#CREATE Table Interactions (
#Structure_Id VARCHAR(10) NOT NULL,
#Method VARCHAR(20) NOT NULL,
#Interaction_full_line TEXT,
#Interaction VARCHAR(20),
#Sanger_classification VARCHAR(20),
#First_chain VARCHAR(1),
#Second_chain VARCHAR(1),
#First_nucleotide VARCHAR(20),
#Second_nucleotide VARCHAR(20),
#First_nr_nucleotide INTEGER,
#Second_nr_nucleotide INTEGER
#);

#How to run programs

#import subprocess

#rnaview_path = input("Podaj pełną ścieżkę rnview\n$ ");


#def RNAView(pdb_id)
#    subprocess.run([rnaview_path,"./pdb_files/"+pdb_id+".pdb"])








    
