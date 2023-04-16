"""
Parameters      
----------      
use_file : a boolean keyword used to choose if the convertsion will be done 
from the text_to_convert.txt file (True) or from an input by the user (False) 

option : a boolean keyword used to choose if in the converted file is added 
an # at each line (True) or if the conversion will happen without the # 

"""

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
import os

def convert_text(use_file=True, option=True):
    if use_file:
        # Get the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the path to the text file
        text_file_path = os.path.join(current_dir, 'archive', 'text_to_convert.txt')

        # Open the text file
        
        with open(text_file_path, "r+") as f:
            lines = [[0]]
            i = 0
            for line in f.read().splitlines():
                for word in line.split(" "):
                    if lines[i][0] == 0:
                        lines[i].append("# ")
                        lines[i][0] += 2
                    if 2 + len(word) > 79:
                        raise ValueError("the text file contains a word too long for the python line length standards")
                    if lines[i][0] + len(word) <= 79:
                        lines[i][1] += word + " "
                        lines[i][0] += len(word) + 1
                    else:
                        lines.append([2 + len(word) + 1, "# " + word + " "])
                        i += 1
                lines.append([2, "# "])
                i += 1
    else:
        user_input = input("Enter the comment to convert: ")
        lines = [[0, "# " + user_input]]
        i = 0
        for word in user_input.split(" "):
            if lines[i][0] == 0:
                lines[i][0] += 2
            if 2 + len(word) > 79:
                raise ValueError("the text contains a word too long for the python line length standards")
            if lines[i][0] + len(word) <= 79:
                lines[i][1] += word + " "
                lines[i][0] += len(word) + 1
            else:
                lines.append([2 + len(word) + 1, "# " + word + " "])
                i += 1
            lines.append([2, "# "])
            i += 1
    
    if option != True:
        for i in range(len(lines)):
            lines[i][1] = lines[i][1][2:]
    current_dir = os.path.dirname(os.path.abspath(__file__))

    text_file_path = os.path.join(current_dir, 'archive', 'text_converted.txt')
    with open(text_file_path, "w") as f:
        for i in range(len(lines) - 1):
            f.write("%s\n" % lines[i][1])


convert_text(use_file=True, option=False)


