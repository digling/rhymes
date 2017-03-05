from lingpy import *
from collections import defaultdict
from sinopy import sinopy
import re

csv1 = csv2list('2017-02-18-Behr-1-197-draft-2-western.csv', strip_lines=False)
csv2 = csv2list('2017-02-18-Behr-1-197-draft-2-eastern.csv', strip_lines=False)

chars = defaultdict(list)

for i, line in enumerate(csv2[1:]+csv1[1:]):
    if len(line) > 7:
        if '+' in line[5] or '>' in line[5] or '{' in line[5] or len(line[5].strip()) > 1:
            chars[line[5]] += [(i+1, line[2], line[3])]

guessed = 0
with open('characters.md', 'w') as f:
    f.write('## Problematic Chars in Behr 2008\n\n')
    f.write('number | first page | character | conversion | occurrences | pages \n') 
    f.write('--- | --- | --- | --- | --- | --- | --- \n')
    for i, (char, vals) in enumerate(sorted(chars.items(), key=lambda x:
        x[1][0][0])):
        guess = '?'
        if len(char) == 3:
            guess = sinopy.character_from_structure(char[1]+char[0]+char[2])
            if guess != '?':
                guessed += 1
        else:
            _guess = char
            composed = re.findall('{(.*?)}', char)
            for c in composed:
                if len(c) == 3:
                    r = sinopy.character_from_structure(c[1]+c[0]+c[2])
                    if r != '?':
                        _guess = _guess.replace('{'+c+'}', r)
            if _guess != char:
                guessed += 1
                if len(_guess) == 3:
                    guess2 = sinopy.character_from_structure(_guess[1]+_guess[0]+_guess[2])
                    if guess2 != '?':
                        guess = guess2
                    else:
                        guess = _guess
        f.write('{0} | {1} | {2} | {3} | {4} | {5} \n'.format(
            i+1,
            vals[0][1], 
            char, 
            guess,
            len(vals),
            ', '.join(['{0}: {1}'.format(y, z) for x, y, z in vals])
            ))
    

