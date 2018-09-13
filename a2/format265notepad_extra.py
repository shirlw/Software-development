#!/usr/bin/env python3

#CHANGES: I added heading lines which you can put around words. Use it with ".HD length" where length is how long you want the heading line to be
#There is also a center line or right align command. Center the line with ".CL on" or ".CL off". When centering, if there cannot be an even number of spaces in
#front and behind the line, then there will be one less space in front. Use ".RA on" or ".RA off" to make the line align along the right side. If both ".CL on"
#and ".RA on" are present then ".CL on" takes precedence
# An example of heading lines:

#.LW 30
#.LM 5
#This is a short sentence.
#
#.HD 7
#TITLE
#.HD 6
#This is under the heading line.

#The above input becomes:
#     This is a short sentence
#
#     -------
#     TITLE
#     ------
#     This is under the heading
#     line.

#see in01_extra.txt, in02_extra.txt, and in03_extra.txt for more tests

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
                length = 0
                center = 0
                right = 0
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
                                if array[1] == "off" and formatting ==1:
                                        line_w =print_line(line_w, last, center, right, width)
                                formatting = on_or_off(array)
                        elif ".CL" in array[0]:
                                if array[1] == "off" and center ==1:
                                        line_w =print_line(line_w, last, center, right, width)
                                center = on_or_off(array)
                        elif ".RA" in array[0]:
                                if array[1] == "off" and right ==1:
                                        line_w =print_line(line_w, last, center, right, width)
                                right = on_or_off(array)
                        elif ".LM" in array[0]:
                                margin = find_margin(array, margin, width)
                        elif ".LS" in array[0]:
                                spacing = get_value(array)
                        elif ".HD" in array[0]:
                                length = get_value(array)
                                #if we should be putting in a heading, then do that first
                                if (length>0):
                                        line_w =print_line(line_w, last, center, right, width)
                                        [print("") for x in range(spacing)]
                                        line_w =print_line(insert_heading(length, margin), last, center, right, width)
                                        length=0
                        #do formatting if it is turned on
                        elif (formatting==1 and width>0):
                                for word in array:
                                        #if the word is a new line, print line, do spacing, add new line, more spacing etc
                                        if (word=='\n'):
                                                line_w =print_line(line_w, last, center, right, width)
                                                print_new_line(spacing)
                                                space_left= width
                                        #if adding the word would go over space left, print line, do spacing, put word at front of next line
                                        elif (len(word)+1>space_left):
                                                line_w=print_line(line_w, last, center, right, width)
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
                        line_w=print_line(line_w, last, center, right, width)
                        if (array[-1] !='\n'):
                                print("")
        except FileNotFoundError:
                print("file not found")

#put a heading into line_w
def insert_heading(length, margin):
        line_w = []
        [line_w.append("") for x in range(margin)]
        [line_w.append("-") for x in range(length)]
        return line_w

#determine if the command is off or on
def on_or_off(array):
        if (array[1] == "off"):
                value = 0
        else:
                value =1
        return value

#print the lines for new lines
def print_new_line(spacing):
        [print("") for x in range(spacing)]
        print("")
        [print("") for x in range(spacing)]

#print a space with no new line
def print_space():
        print(" ", end="")

#putting word in the front of a new line, put in a margin if applicable before adding word
def put_word_in_front(line_w, margin, word, width):
        [line_w.append("") for x in range(margin)]
        line_w.append(word)
        space_left= width - len(word)-(margin)
        return space_left

#print the line and empty the list holding the line.
def print_line(line_w, last, center, right, width):
        formatted=" ".join(line_w)
        #if we're printing bc there are a bunch of new lines one after another, then formatted would be empty. (or we're printing the last line of file)
        #print line without a new line
        if not formatted or last==1:
                print(formatted, end="")
        else:
                num_spaces = 0
                #find the number of spaces to align by
                if center ==1:
                        num_spaces = int((width - len(formatted))/2)
                elif right ==1:
                        num_spaces = width - len(formatted)
                [print_space() for x in range(num_spaces)]
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
