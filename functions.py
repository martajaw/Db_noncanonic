import re
#Functions that retrive data from RNAView output files

def rv_full(line):
    return(line)

def rv_interactions(line)
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
def rv_chains(line)
    find_chains = re.findall('[A-Z]{1,1}:',line)
    find_chains[0] = find_chains[0].strip(':')
    find_chains[1] = find_chains[1].strip(':')
    return(find_chains)

def rv_nucleotides(line)
    nucleotides = re.findall('[ACGUacgu]{1}-[ACGUacgu]{1}',line)
    nucleotides = "".join(nucleotides)
    nucleotides = nucleotides.split("-")
    return(nucleotides)

def rv_nr_nucleotides(line)
	nr_nuc = re.findall(' +[0-9]+ +', line)
	nr_nuc[0] = nr_nuc[0].strip()
    nr_nuc[1] = nr_nuc[1].strip()
    return(chain_nr)







#Functions that retrive data from McAnnotate output files

def mc_full(line):
    return(line)

def mc_interaction(line):
	interactions = re.findall(' {1}[WHS]{1}[whs]{1}/[WHS]{1}[whs]{1} {1}', line)
	interactions[0] = interactions[0].strip()
	cut = re.findall('[A-Z]+', interactions[0])
	cut = '/'.join(cut)
	conformations = re.findall('cis|trans',line)
	
	if ("trans" in conformation):
		cut = 't' + cut
	if ("cis" in conformation):
		cut = 'c' + cut
	
	return(cut)
	
def mc_sanger(line):
	sanger = re.findall(' +[XVI]+ +', line)
	sanger[0] = sanger[0].strip()
	return(sanger)


def mc_chains(line):
	chains = re.findall('[A-Z]+[1-9]+-{1}[A-Z]+[1-9]+', line)
	find_chains = re.findall('[A-Z]+', chains[0])
	return(find_chains)
	
	
def mc_nucleotides(line):
	nucleotides = re.findall('[ACGUacgu]{1}-[ACGUacgu]{1}',line)
    nucleotides = "".join(nucleotides)
    nucleotides = nucleotides.split("-")
    return(nucleotides)
    
def mc_nr_nucleotides(line):
	chain_nr = re.findall('[A-Z]+[1-9]+-{1}[A-Z]+[1-9]+', line)
	chain_nr = re.findall('[1-9]+',chain_nr[0])
	return(chain_nr)




#TABLE
#CREATE Table Interactions (
#Structure_Id VARCHAR(10) NOT NULL,
#Method VARCHAR(20) NOT NULL,
#Interaction_full_line NTEXT(20),
#Interaction VARCHAR(20),
#Sanger_classification VARCHAR(20),
#First_chain VARCHAR(1),
#First_nr_nucleotide INT(20),
#Second_chain VARCHAR(1),
#Second_nucleotide VARCHAR(20),
#Second_nr_nucleotide INT(20)
#);

#How to run programs

#import subprocess

#rnaview_path = input("Podaj pełną ścieżkę rnview\n$ ");


#def RNAView(pdb_id)
#    subprocess.run([rnaview_path,"./pdb_files/"+pdb_id+".pdb"])








    
