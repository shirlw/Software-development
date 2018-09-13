#!/usr/bin/env python3

import re
import fileinput

class Formatter(object):

        def __init__(self, filename, string_list):
                #initialize these so if they aren't changed, then they are 0/empty
                self.filename = filename
                self.width = 0
                self.margin = 0
                self.spacing = 0
                self.line_w = []
                self.formatting = 0
                self.last =0
                self.finished = []
                self.string_list = string_list
                self.line_num = 0

        def get_lines(self):
                #if a filename is provided, format it. If not, formate the list of strings
                if (self.filename):
                        the_input = fileinput.input()
                else:
                        the_input = self.string_list
                try:
                        for line in the_input:
                                #if the line is just a new line, then the array will keep it. otherwise, remove all whitespace
                                self.line_num = self.line_num +1
                                if (line == '\n'):
                                        array = ['\n']
                                else:
                                        array = line.split()
                                #look for commands in the arrays and check for errors in the input
                                if re.match("^\.LW (\d+)", line):
                                        try:
                                                self.width = self.get_value(array)
                                                space_left = self.width
                                                self.formatting = 1
                                                self.check_errors(line)
                                        except ZeroWidthError:
                                                self.print_zero_width_msg()
                                                self.print_with_no_nl(line)
                                        except WordAfterCommandError:
												self.print_word_after_msg()
                                                return []
                                elif re.match("^\.FT (off|on)", line):
                                        try:
                                                self.formatting_on_or_off(array)
                                                if re.match("^\.FT (off|on) (\w)*", line):
                                                        raise WordAfterCommandError
                                        except WordAfterCommandError:
                                                print_word_after_msg()
                                                return []
                                elif re.match("^\.LM ((\+|-)?\d+)", line):
                                        try:
                                                self.find_margin(array)
                                                self.check_errors(line)
                                        except ZeroWidthError:
                                                self.print_zero_width_msg()
                                                self.print_with_no_nl(line)
                                        except WordAfterCommandError:
                                                self.print_word_after_msg()
                                                return []
                                elif re.match("^\.LS (\d+)", line):
                                        try:
                                                self.spacing = self.get_value(array)
                                                self.check_errors(line)
                                        except ZeroWidthError:
                                                self.print_zero_width_msg()
                                                self.print_with_no_nl(line)
                                        except WordAfterCommandError:
                                                self.print_word_after_msg()
                                                return []
                                #format if it's turned on
                                elif (self.formatting ==1):
                                        for word in array:
                                                #if the word is a new line, print line, do spacing, add new line, more spacing etc
                                                if (word == '\n'):
                                                        self.print_line()
                                                        self.new_line_spacing()
                                                        space_left = self.width
                                                #if adding the word goes over space left, print line, do spacing, put word at front of next line
                                                elif (len(word)+1>space_left):
                                                        self.print_line()
                                                        [self.finished.append("") for x in range(self.spacing)]
                                                        try:
                                                                space_left = self.put_word_in_front(word)
																if space_left < 0:
                                                                        raise WidthSmallerThanWordError
                                                        except WidthSmallerThanWordError:
                                                                self.print_width_smaller_msg()
                                                                return self.finished
                                                else:
                                                        #if the line is currently empty, put the word in front
                                                        if not self.line_w:
                                                                try:
                                                                        space_left = self.put_word_in_front(word)
                                                                        if space_left < 0:
                                                                                raise WidthSmallerThanWordError
                                                                except WidthSmallerThanWordError:
                                                                        self.print_width_smaller_msg()
                                                                        return self.finished
                                                        #the line isn't empty and adding the word doesn't go over space left. put it at end of line
                                                        else:
                                                                space_left = space_left - (len(word)+1)
                                                                self.line_w.append(word)
                                else:
                                        self.print_with_no_nl(line)
                        #print the last line.
                        if (self.formatting ==1):
                                self.last = 1
                                self.print_line()
                        return self.finished
                except FileNotFoundError:
                        print("error: the file provided was not found")
                        return []
                except PermissionError:
                        print("error: does not have file permissions")
                        return []
                finally:
                        fileinput.close()

        #error messages
        def print_width_smaller_msg(self):
                print("error: the width provided is smaller than a word in the file. \nThis error occurred on line", self.line_num, "in the input file")


        def print_word_after_msg(self):
                print("error: a command was not on line by itself. \nThis error occurred on line", self.line_num, "in the input file")

        def print_zero_width_msg(self):
			print("error: zero width provided for .LW. This error occurred on line", self.line_num, "in the input file")

        def check_errors(self, line):
                if self.width == 0:
                        raise ZeroWidthError("width 0 is a no-no")
                if re.match("^(\.\w+)* (\w+)* (\w)*", line):
                        raise WordAfterCommandError

        #print the line with no new line attached at end
        def print_with_no_nl(self, line):
                self.formatting = 0
                line_no_new = line.strip('\n')
                self.finished.append(line_no_new)

        #do spacing around a new line
        def new_line_spacing(self):
                [self.finished.append("") for x in range(self.spacing)]
                self.finished.append("")
                [self.finished.append("") for x in range(self.spacing)]

        #turn formatting on or off
        def formatting_on_or_off(self, array):
                if (array[1] == "off" and self.formatting ==1):
                        self.print_line()
                        self.formatting =0
                elif array[1] == "off":
                        self.formatting =0
                else:
                        self.formatting =1

        #put word in front of new line. put a margin if applicable
        def put_word_in_front(self, word):
                [self.line_w.append("") for x in range(self.margin)]
                self.line_w.append(word)
                space_left = self.width - len(word) - (self.margin)
                return space_left

        #print the line and empty the list holding the line
        def print_line(self):
                formatted= " ".join(self.line_w)
                #if we're printing bc there are a bunch of new lines one after another, then formatted would be empty (or we're printing the last line of file)
                #print line without a new line
                if not formatted or self.last ==1:
                        formatted_no_new = formatted.strip('\n')
						if (formatted_no_new):
                                self.finished.append(formatted_no_new)
                else:
                        #if we're printing the line bc word goes over space left or we want to force print a line bc there's a new line
                        #print the line with a new line
                        self.finished.append(formatted)
                self.line_w = []

        #find out if the .LM command has a positive/negative margin to add to existing margin (or if it's setting margin)
        def find_margin(self, array):
                margin_value = array[1]
                if (margin_value[0] == "+"):
                        extra_margin = self.get_value(array)
                        self.margin = self.margin + extra_margin
                elif (margin_value[0] == "-"):
                        extra_margin = self.get_value(array)
                        self.margin = self.margin + extra_margin
                else:
                        self.margin = self.get_value(array)
                if self.margin> (self.width-20):
                        try:
                                self.margin = self.width - 20
                                if self.margin <0:
                                        raise NegativeError()
                        except NegativeError:
                                print("error: the margin was greater than page width- 20 and page width-20 is negative, so the margin was set to 0.")
                                print("This error occured on line", self.line_num, "in the input file.")
                                self.margin = 0
                elif self.margin <0:
                        self.margin = 0

        #get the value after the command
        def get_value(self, array):
                temp = int(array[1])
                del array[1], array[0]
                return temp

#Exception classes
#if the margin is negative
class NegativeError(Exception):
        pass
		
#if the width is set to zero is not provided
class ZeroWidthError(Exception):
        pass

#if the width is smaller than a single word
class WidthSmallerThanWordError(Exception):
        pass

#if there is text after a correct command
class WordAfterCommandError(Exception):
        pass

