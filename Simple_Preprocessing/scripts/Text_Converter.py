# the program starts opening the file containing the text to convert 
# 
# to preserve the \n in the original txt document, it's performed an iteration 
# by lines and not words 
# 
# using a list of lists called lines the program stores: 
# 1) in the FIRST column: a counter of characters to check if the line length 
# requirement of python is met 
# 2) in the SECOND column: each line of the new converted text in a comment 
# form (with '# ') 
print("ciao/n")
f = open("archive/text_to_convert.txt","r+")
lines = [[0]]
i = 0
for line in f.read().splitlines():
    for word in line.split(" "):
        if lines[i][0] == 0:
            lines[i].append('# ')
            lines[i][0] += 2
        if 2 + len(word) > 79:
            f.close()
            raise ValueError("the text file contains a word too long for the python line length standards")
        if lines[i][0] + len(word) <= 79:
            lines[i][1] += word + ' '
            lines[i][0] += len(word) + 1
        else:
            lines.append([2+len(word)+1, '# '+word+' '])
            i += 1
    lines.append([2, '# '])
    i += 1
f.close()

option = 0
if option != 0:
    for i in range(len(lines)):
        lines[i][1] = lines[i][1][2:]

f = open("archive/text_converted.txt", "w")
for i in range(len(lines)-1):
    f.write("%s\n" % lines[i][1])
f.close()