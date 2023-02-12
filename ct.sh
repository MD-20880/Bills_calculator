USER1=$1
USER2=$2

if [ $3 -z ]; then
    FILENAME="queryResult.txt"
else
    FILENAME=$3
fi

cat $FILENAME | grep $USER1 | grep $USER2


