import re
import subprocess

pdb_path = '/home/marta/Licencjat/pdb_gz'
rv_path = '/home/marta/RNAVIEW/bin/rnaview'
mc_path = '/home/marta/Licencjat/Licencjat/MC-annotate/MC-Annotate'

ids = open('lista_testowa').read()
id_list = re.findall('\'{1}[0-9]+[A-Z 0-9]+\'{1}', ids)

i = 0
for a in id_list:
	id_list[i] = a.strip('\'').lower()
	i = i + 1
	
print(len(id_list))




def rv(path):
	j = 0
	for a in id_list:
		if (subprocess.run([path, pdb_path + "/" + "pdb" + a + ".ent/" + "data"])):
			j = j + 1
	print(j)
	print(len(id_list))
	



rv(mc_path)
	

