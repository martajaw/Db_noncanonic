#Wartości zmiennych - do zadeklarowania
#'pdb_path' - ścieżka dostępu do katalogu z plikami pdb
#'rv_path' - ścieżka dostępu do programu RNAView
#'mc_path' - ścieżka dostępu do programu MC-Annotate
#'table' - nazwa tabeli
#'columns' - nazwy kolumn w tabeli 'table'
#DANE DO POŁĄCZENIA Z BAZĄ:
#'name_db'- nazwa bazy danych
#'user_db' - nazwa użytkownika bazy danych
#'host' - np 'localhost'
#'passwd' - hasło dostępu
#Przykładowe wartości:

pdb_path = '/home/marta/Licencjat/pdb_gz'
rv_path = '/home/marta/RNAVIEW/bin/rnaview'
mc_path = '/home/marta/Licencjat/Licencjat/MC-annotate/MC-Annotate'
table = 'Interactions'
columns = 'id, method, full_line, interaction, sanger, f_chain, s_chain, f_nuc, s_nuc, nr_f_nuc, nr_s_nuc'
name_db = 'Interactions'
user_db = 'postgres'
host = 'localhost'
passwd = 'minusz'


