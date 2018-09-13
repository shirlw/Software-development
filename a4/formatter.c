/*
 * UVic SENG 265, Fall 2016,  A#4
 *
 * This will contain the bulk of the work for the fourth assignment. It
 * provide similar functionality to the class written in Python for
 * assignment #3.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "formatter.h"
#include <assert.h>

/*gets rid of new line char and replaces with null char*/
void chomp(char *line){
        assert(line != NULL);
        int len = strlen(line);
        if (line[len-1] == '\n'){
                line[len-1] = '\0';
        }
}

/*put in margin spaces into cp*/
char* margin_lines(char* cp, int margin){
        int i;
        for (i=0;i<margin;i++){
                strncpy(cp, " ", 1);
                cp++;
        }
        return cp;
}

/*allocating memory for result*/
char **change_result_size(int result_size,char **result){
        result = (char**) realloc(result, sizeof(char*)*result_size);
        if (!result){ abort();}
        return result;
}

/*allocating memory for result[position*/
char *change_result_position(int width, char **result, int position){
        result[position] = (char*) malloc (sizeof(char*)*(width+1));
        if (!result[position]){ abort();}
        return result[position];
}

/*for when you're going to a new line part 1. put a null at the end of result[position] where cp is*/
/*change the size of result by doubling if there isn't enough space, then increase position*/
char **go_to_new_line1(char **cp, int *result_size, int *position, char **result){
        strncpy(*cp,"\0", 1);
        if (*result_size <= (*position+1)){
                *result_size = *result_size*2;
                result = change_result_size(*result_size, result);
        }
        *position = *position +1;
        return result;
}

/*for when you're going to a new line part 2. change the size of result[position] according to width*/
/*then set the cp to point at the beginning of result{position]*/
char *go_to_new_line2(char **cp, int position, char **result, int width){
        result[position] = change_result_position(width, result, position);
        *cp = result[position];
        return result[position];
}

/*tekenize the line and return word*/
char *tokenize_line(char *line, char *word){
        word= strtok(line, " ");
        word= strtok(NULL, " ");
        return word;

}

/*find margin, whether pos, neg, or normal*/
int find_margin(char *word, int margin){
        char *pos_margin_exists = strchr(word, '+');
        char * neg_margin_exists = strchr(word, '-');
        if (pos_margin_exists){
                int pos_margin = atoi(word);
                margin = margin+pos_margin;
        }else if (neg_margin_exists){
                int neg_margin = atoi(word);
                margin = margin+neg_margin;
        }else{
                margin = atoi(word);
        }
        return margin;
}

/*check if formatting should be on or off*/
int formatting_on_or_off(char *word){
        char off[4] ="off";
        int format;
        if (strncmp(word, off, 3) ==0){
                format=0;
        }else{
                format = 1;
        }
        return format;
}

/*put the word at the beginning of the new line, ie result[position]*/
char *put_word_in_front(char *cp, int margin, char *word, int *space_left, int width){
        cp = margin_lines(cp, margin);
        strncpy(cp,word, strlen(word));
        cp = cp+strlen(word);
        *space_left = width - strlen(word)-margin;
        return cp;
}

/*takes in a file stream*/
char **format_file(FILE *infile) {
        char *line = NULL;
        size_t len = 0;
        ssize_t read;
        int result_size = 1;
        int position = 0;
        char lw[4]=".LW";
        char lm[4]=".LM";
        char ls[4]=".LS";
        char ft[4]=".FT";
        char* word;
        int space_left;
        int  width = 0;
        int margin = 0;
        int spacing = 0;
        int format = 0;
        char* cp;
        char **result = (char**) malloc(sizeof(char*)*result_size);
        if (infile == NULL){
                fprintf(stderr, "Unable to open file");
                exit(1);
        }
        while ((read = getline(&line, &len, infile)) != -1){
                /*for case where it prints unformatted lines*/
                /*if position is at end of result_size, double result*/
                if (result_size <= position){
                        result_size = result_size*2;
                        result = change_result_size(result_size, result);
                }
                /*if result[position] is null, allocate some memory and for it and point cp at it*/
                if (!result[position]){
                        result[position] = go_to_new_line2(&cp, position, result, read-1);
                }
                /*check for commands*/
                if (strncmp(line, lw, 3) ==0){
                        format=1;
                        word = tokenize_line(line, word);
                        /*change string of width into int, put a null char at buffer[width] as safety*/
                        width = atoi(word);
                        space_left = width;
                }else if (strncmp(line, lm, 3) ==0){
                        word = tokenize_line(line, word);
                        margin = find_margin(word, margin);
                }else if (strncmp(line, ls, 3) ==0){
                        word = tokenize_line(line, word);
                        spacing = atoi(word);
                }else if (strncmp(line, ft, 3) ==0){
                        word = tokenize_line(line, word);
                        format = formatting_on_or_off(word);
                /*if formatting is turned on*/
                }else if (format==1 && width>0){
                        /*in case formatting was off and result[position] was malloced to "read" (ie length of line). we realloc to width+1*/
                        result[position] = (char*) realloc (result[position], sizeof(char*)*(width+1));
                        if (!result[position]){ abort();}
                        /*don't chomp line if it's a new line by itself. This'll make word= \n*/
                        if (!(line[0]=='\n')){
                                chomp(line);
                        }
                        word=strtok(line, " ");
                        while (word !=NULL){
                                /*if the word is a new line, print the buffer, then word plus another new line. cp is ready at this next line*/
                                if(*word=='\n') {
                                        if (result[position][0] !='\0'){
                                                result = go_to_new_line1(&cp, &result_size, &position, result);
                                                result[position] = go_to_new_line2(&cp, position, result, width);
                                        }
                                        int i;
                                        for (i=0;i<spacing;i++){
                                                result = go_to_new_line1(&cp, &result_size, &position, result);
                                                result[position] = go_to_new_line2(&cp, position, result, width);
                                        }
                                        result = go_to_new_line1(&cp, &result_size, &position, result);
                                        result[position] = go_to_new_line2(&cp, position, result, width);
                                        for (i=0;i<spacing;i++){
                                                result = go_to_new_line1(&cp, &result_size, &position, result);
                                                result[position] = go_to_new_line2(&cp, position, result, width);
                                        }
                                        space_left = width;
                                /*if the word plus space is greater then space left, put a null char at cp at result[position]*/
                                /*set cp to result[position+1]  then copy the word into the beginning of result[position]*/
                                } else if (strlen(word)+1>space_left){
                                        result = go_to_new_line1(&cp, &result_size, &position, result);
                                        result[position] = go_to_new_line2(&cp, position, result, width);
                                        /*put spaces between the outputted line and new one if applicable*/
                                        int i;
                                        for (i=0;i<(spacing);i++){
                                                result = go_to_new_line1(&cp, &result_size, &position, result);
                                                result[position] = go_to_new_line2(&cp, position, result, width);
                                        }
                                        /*put margin in front of line if applicable*/
                                        cp = put_word_in_front(cp, margin, word, &space_left, width);
                                /*if you get here, there is still space in result[position] for word and space. so put it in*/
                                } else{
                                        /*the first word in result[position] shouldn't have a space before it, everything else should*/
                                        if (!(cp == result[position])){
                                                strncpy(cp, " ", 1);
                                                cp++;
                                                space_left= space_left- (strlen(word)+1);
                                                strncpy(cp, word,  strlen(word));
                                                cp = cp + strlen(word);
                                        }else {
                                                /*word will be put at beginning of result[position], put in margin lines*/
                                                cp = put_word_in_front(cp, margin, word, &space_left, width);
                                        }
                                }
                                word=strtok(NULL, " ");
                        }
                }else{
                        /*no formatting will take place, just print out the line*/
                        strncpy(result[position], line, read-1);
                        cp = cp+(read-1);
                        strncpy(cp,"\0", 1);
                        position++;
                }

        }
        /*if formatting is on and cp is pointing at a beginning of result[position], remove it bc it's an extra new line*/
        if (format==1 && cp == result[position]){
                result[position] = NULL;
        }
        if (line){
                free(line);
        }
        return result;
}

/*takes in a double pointer and the number of lines in it*/
char **format_lines(char **lines, int num_lines) {
        char **result;
#ifdef DEBUG
        result = (char **)malloc(sizeof(char *) * 2);
        if (result == NULL) {
                return NULL;
        }

        result[0] = (char *)malloc(sizeof(char) * 80);
        if (result[0] == NULL) {
                return NULL;
        }
        strncpy(result[0], "(machine-like voice) EXTERMINATE THEM!", 79);

        result[1] = (char *)malloc(sizeof(char) * 2);
        if (result[1] == NULL) {
                return NULL;
        }
        result[1][0] = '\0';
#endif
        /*write the lines array into a txt file*/
        FILE *f = fopen("lines.txt", "w");
        int i;
        for (i=0; i<num_lines; i++){
                fprintf(f, "%s\n", lines[i]);
        }
        fclose(f);
        /*open that text file and format with format_file*/
        FILE *data_fp = fopen("lines.txt", "r");
        if (data_fp == NULL){
                fprintf(stderr, "Unable to open lines.txt");
                exit(1);
        }
        result = format_file(data_fp);
        return result;
}
