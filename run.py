import functions
import config


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

rv_run(rv_path)
mc_run(mc_path)
mc_parser()
rv_parser()




































