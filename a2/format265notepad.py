#!/usr/bin/env python3

import fileinput

def main():
        try:
                #initialize these so if they aren't changed, then they are 0/empty
                width=0
                margin=0
                spacing = 0
                line_w = []
                formatting = 0
                last=0
                for line in fileinput.input():
                        #if the line is just a new line, then the array will keep it. otherwise, remove all whitespace
                        if (line == '\n'):
                                array = ['\n']
                        else:
                                array = line.split()
                        #look for commands in the arrays
                        if ".LW" in array[0]:
                                width = get_value(array)
                                space_left = width
                                formatting=1
                        elif ".FT" in array[0]:
                                if (array[1] == "off"):
										 if formatting==1:
                                                line_w =print_line(line_w, last)
                                        formatting = 0
                                else:
                                        formatting = 1
                        elif ".LM" in array[0]:
                                margin = find_margin(array, margin, width)
                        elif ".LS" in array[0]:
                                spacing = get_value(array)
                        #do formatting if it is turned on
                        elif (formatting==1 and width>0):
                                for word in array:
                                        #if the word is a new line, print line, do spacing, add new line, more spacing etc
                                        if (word=='\n'):
                                                line_w =print_line(line_w, last)
                                                [print("") for x in range(spacing)]
                                                print("")
                                                [print("") for x in range(spacing)]
                                                space_left= width
                                        #if adding the word would go over space left, print line, do spacing, put word at front of next line
                                        elif (len(word)+1>space_left):
												line_w=print_line(line_w, last)
                                                [print("") for x in range(spacing)]
                                                space_left = put_word_in_front(line_w, margin, word, width)
                                        else:
                                                #if the line is currently empty, put the word in front
                                                if not line_w:
                                                        space_left = put_word_in_front(line_w, margin, word, width)
                                                #the line isn't empty and adding the word doesn't go over space left. put it at end of line
                                                else:
                                                        space_left = space_left - (len(word)+1)
                                                        line_w.append(word)
                        else:
                                print(line, end="")
                #print the last line. print a new line at the very end if there isn't one already there
                if (formatting==1):
                        last=1
                        line_w=print_line(line_w, last)
                        if (array[-1] !='\n'):
                                print("")
        except FileNotFoundError:
                print("file not found")

#putting word in the front of a new line, put in a margin if applicable before adding word
def put_word_in_front(line_w, margin, word, width):
        [line_w.append("") for x in range(margin)]
        line_w.append(word)
        space_left= width - len(word)-(margin)
        return space_left

#print the line and empty the list holding the line.
def print_line(line_w, last):
        formatted=" ".join(line_w)
        #if we're printing bc there are a bunch of new lines one after another, then formatted would be empty. (or we're printing the last line of file)
        #print line without a new line
        if not formatted or last==1:
                print(formatted, end="")
        else:
                #if we're printing the line bc word goes over space left or we want to force print a line bc there's a new line
                # print the line with a new line
                print(formatted)
        line_w=[]
        return line_w

#find out if the .LM command has positive/negative margin to add to existing margin (or if it's setting margin)
def find_margin(array, margin, width):
        margin_value = (array[1])
        if (margin_value[0] == "+"):
                extra_margin = get_value(array)
                margin = margin + extra_margin
                if margin > (width-20):
                        margin = width-20
        elif (margin_value[0] == "-"):
                extra_margin = get_value(array)
                margin = margin + extra_margin
                if margin < 0:
                        margin = 0
        else:
                margin = get_value(array)
        return margin

#get the value after the oommand
def get_value(array):
        temp = int(array[1])
        del array[1], array[0]
        return temp

if __name__=='__main__':
        main()
else:
        print("hello world! you're not in command-line")
