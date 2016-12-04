import re
from sinopy import sinopy

infile = open('wang-1980-raw-2.txt')
poem, stanza = 0, 0
warnings = 0
def aline(line, warnings):

    comment = ''
    problem = False
    problems = ['']
    rhymewords = []
    reconstruction = ''
    previous = ''
    inbrackets, incomment = False, False
    stripped_line = ''
    for char in line:
        if char == ' ':
            pass
        elif char == '<':
            problem = True
        elif char == '>':
            problem = False
            problems += ['']
        elif char == '[':
            inbrackets = True
        elif inbrackets and char != ']':
            reconstruction += char
        elif char == ']':
            inbrackets=False
            if rhymewords:
                rhymewords[-1] += [reconstruction]
            else:
                rhymewords += [['???', previous, reconstruction]]
                warnings += 1
            reconstruction = ''
        elif char in '(（':
            incomment = True
        elif char in ')）':
            incomment = False
        elif incomment:
            comment += char
        else:
            if problem:
                problems[-1] += char
            elif sinopy.is_chinese(char):
                previous = char
                stripped_line += char
            elif char in '?ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz':
                rhymewords += [[previous, char]]
    return stripped_line, rhymewords, comment, warnings, ','.join(problems)

D = {}
idx = 1
ecount = 0
for i, line in enumerate(infile):
    ln = line.strip('\n')
    if line[0].isdigit():
        poem = line[:line.index('.')]
        name = line[line.index('.')+1:].strip()

        stanza = 0
    elif ln:
        print(i, ln)
        ecount = 0
        if not stanza:
            stanza = 1
        
        if ecount <= 1 and poem:
            lines = ln.split('、')
            for i, l in enumerate(lines):
                s, r, c, warnings, problems = aline(l, warnings)
                print(s, len(r), c, warnings)
                if r:
                    for recs in r:
                        if len(recs) != 3:
                            recs = recs + ['???', '???', '???']
                        D[idx] = [poem, name, stanza, i, l, s, recs[0], recs[1],
                                recs[2], c, problems]
                        idx += 1
                else:
                    D[idx] = [poem, name, stanza, i, l, s, '', '', '', c,
                            problems]
                    idx += 1
    else:
        ecount += 1
        stanza += 1

with open('Wang1980.tsv', 'w') as f:
    f.write('ID\tPOEM_NUMBER\tPOEM_NAME\tSTANZA\tLINE_IN_SOURCE\tLINE\tRHYME\tRHYMEWORD\tRECONSTRUCTION\tCOMMENT\tCATEGORY\tPROBLEMS\n')
    for k in sorted(D):
        f.write(str(k)+'\t'+'\t'.join([str(x) for x in D[k]])+'\n')
