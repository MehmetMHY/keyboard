# CSCI 250 Capstone Final Project Bash Script

# Example Run:
#	bash musicFile.sh "file_name" "c' e' g' e'"

##########################
###INPUT Variables Here###
##########################
FN=$1
pdfLocation=SHEETS
##########################
##--geometry COLxROW+X+Y##
##########################
COL=500
ROW=500
X=200
Y=200
##########################
###INPUT Variables Here###
##########################

if [ -d "$pdfLocation" ]
then
	echo "$pdfLocation Exists!"
else
	echo "Creating new $pdfLocation"
	mkdir $pdfLocation
fi

FILENAME=$FN.ly
touch $FILENAME

> $FILENAME

# these values can be changed for LilyPond:
echo "\version "2.18.2"" >> $FILENAME
echo "{" >> $FILENAME
echo "	\time 4/4" >> $FILENAME
echo "	\bass" >> $FILENAME
echo "	$2" >> $FILENAME
echo "}" >> $FILENAME

lilypond $FILENAME

rm $FILENAME

FILENAME=$FN.pdf

mv *.pdf $pdfLocation

cd $pdfLocation

qpdfview $FILENAME -geometry $COLx$ROW-$X+$Y

clear ; clear ; clear

#kill $$
