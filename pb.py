import os

def runLilyPond(pattern, fileName="sheet music"):
    maincommand = str("bash musicFile.sh " + fileName + ' "')

    maincommand = maincommand + pattern + '"'

    # bash musicFile.sh file_name "c' e' g' e'"
    os.system(maincommand)