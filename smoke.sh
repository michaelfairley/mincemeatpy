EXPECTED="{'a': 2, 'on': 1, 'great': 1, 'Humpty': 3, 'again': 1, 'wall': 1, 'Dumpty': 2, 'men': 1, 'had': 1, 'all': 1, 'together': 1, \"King's\": 2, 'horses': 1, 'All': 1, \"Couldn't\": 1, 'fall': 1, 'and': 1, 'the': 2, 'put': 1, 'sat': 1}"

python example.py > output &
SERVER_PID=$!
sleep 1
python mincemeat.py -p changeme localhost
sleep 1
kill $! 2>/dev/null

diff <(cat output) <(echo $EXPECTED)
