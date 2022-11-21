import os

#   Tiedostojen lukemiseen tarkoitettu luokka    #
#   -----------------------------------------    #
# Tätä luokkaa käytetään erilaisten tiedostojen  #
# ja hakemistojen lukemiseen                     #

class FileReader:

    # Palauttaa tiedostot, jotka päättyvät tiettyyn merkkijonoon
    # kansio luodaan, jos sitä ei ole ja "create" on tosi
    @staticmethod
    def get_files(path, suffix = "", create = False):
        
        if not os.path.exists(path):
            if create: os.makedirs(path)
            else: return []

        files = os.listdir(path)
        if suffix != "": files = [f for f in files if f.endswith(suffix)]

        return files

        