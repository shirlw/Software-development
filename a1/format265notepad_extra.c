/*I included a command that allows you to indent the first sentence of a paragraph by a certain amount. It is called with ".ID width" where width is the amount to indent. The first line of the file will be indented as well as the first line of text after a new line by itself*/

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>

#define MAX_LINE_LEN 132

/*gets rid of new line char and replaces it with null char*/
void chomp(char *line){
        assert(line != NULL);

        int len=strlen(line);
        if (line[len-1] == '\n'){
                line[len-1] = '\0';
        }
}

/*puts the correct number of spaces between lines*/
void space_lines(char* cp, int spacing){
        int i;
        for (i=0;i<spacing;i++){
                fprintf(stdout, "\n");
        }
}

/*puts the indent in, moves and returns pointer*/
char* indent_lines(char* cp, int indent){
        int i;
        for (i=0;i<indent;i++){
                strncpy(cp, " ", 1);
                cp = cp + 1;
        }
        return cp;
}

/*puts the margin in, moves and returns pointer*/
char* margin_lines(char* cp, int margin){
        int i;
        for (i=0;i<margin;i++){
                strncpy(cp, " ", 1);
                cp = cp + 1;
        }
		
/*puts a null char where pointer is, print buffer*/
void force_print(char* cp, char buffer[MAX_LINE_LEN]){
        strncpy(cp,"\0", 1);
        fprintf(stdout, "%s", buffer);

}

int main (int argc, char* argv[]){
        /*to make sure file opens correctly*/
        if (argc<2){
                fprintf(stderr, "You must provide a filename\n");
                exit(1);
        }
        FILE *data_fp = fopen(argv[1], "r");
        if (data_fp == NULL){
                fprintf(stderr, "Unable to open %s\n", argv[1]);
                exit(1);
        }
        /* INITIALIZATION*/
        char line[MAX_LINE_LEN];
        char buffer[MAX_LINE_LEN];
        char *cp=buffer;
        char* word;
        int  width = 0;
        int margin = 0;
        int spacing = 0;
        int indent = 0;
        int format = 0;
        int first_word = 0;
        int new_line = 0;
        char lw[4]=".LW";
        char lm[4]=".LM";
        char ls[4]=".LS";
        char id[4]=".ID";
        char ft[4]=".FT";
        char off[4] = "off";
        int space_left;

        /*get each line of the file one by one*/
        while (fgets(line,MAX_LINE_LEN, data_fp) !=NULL){
				/*checks if the first 3 characters of line is a command*/
                if (strncmp(line, lw, 3) ==0){
                        format=1;
                        word= strtok(line, " ");
                        word= strtok(NULL, " ");
                        /*change string of width into int, put a null char at buffer[width] as safety*/
                        width = atoi(word);
                        buffer[width]='\0';
                        space_left = width;
                }else if ( strncmp(line, lm, 3) ==0){
                        format=1;
                        word= strtok(line, " ");
                        word= strtok(NULL, " ");
                        margin = atoi(word);
                }else if ( strncmp(line, ls, 3) ==0){
                        format=1;
                        word= strtok(line, " ");
                        word= strtok(NULL, " ");
                        spacing = atoi(word);
                }else if ( strncmp(line, id, 3) ==0){
                        format=1;
                        word= strtok(line, " ");
                        word= strtok(NULL, " ");
                        indent = atoi(word);
                        /*make sure to keep track of first word*/
                        first_word=1;
                }else if (strncmp(line, ft, 3)==0){
                        word= strtok(line, " ");
                        word= strtok(NULL, " ");
                        if (strncmp(word, off, 3)==0){
                                /*turn formatting off*/
                                format=0;
                        } else{
                                format=1;
                        }
                /*if you get here, it's a line with no commands in it*/
                }else{
                        /*if formatting is turned on*/
                         if (format==1 && width>0){
								/*don't chomp line if it's a new line by itself. This'll make word= \n*/
                                if (!(line[0]=='\n')){
                                        chomp(line);
                                }
                                word=strtok(line, " ");
                                while (word !=NULL){
                                        /*if the word is a new line, print the buffer, then word plus another new line. cp is ready at this next line*/
                                        if(*word=='\n') {
                                                force_print(cp, buffer);
                                                /*print spaces between lines if applicable*/
                                                space_lines(cp, spacing);
                                                fprintf(stdout, "\n\n");
                                                space_lines(cp, spacing);
                                                cp=buffer;
                                                cp =indent_lines(cp, indent);
                                                new_line=1;
                                                space_left = width-indent;
                                        /*if the word plus space is greater then space left, print buffer, new line, and set cp to beginning of buffer*/
                                        /* then copy the word into the beginning of buffer*/
                                        } else if (strlen(word)+1>space_left){
                                                force_print(cp, buffer);
                                                fprintf(stdout, "\n");
                                                /*put spaces between the outputted line and new one if applicable*/
                                                space_lines(cp, spacing);
                                                cp=buffer;
                                                /*put margin in front of line if applicable*/
                                                cp = margin_lines(cp, margin);
                                                strncpy(cp,word, strlen(word));
                                                cp = cp+strlen(word);
                                                space_left = width - strlen(word)-margin;
                                        /*if you get here, there is still space in buffer for word and space. so put it in*/
                                        } else{
                                                if (cp == buffer || new_line ==1){
                                                        /*word will be put at beginning of buffer, put in margin lines*/
                                                        if (first_word==1){
                                                                first_word=0;
                                                                cp = indent_lines(cp, indent);
                                                        }
                                                        space_left= space_left- strlen(word)-margin-indent;
                                                        cp= margin_lines(cp, margin);
                                                        new_line=0;

                                                /*the first word in buffer shouldn't have a space before it, everything else should*/
                                                }else{
														strncpy(cp, " ", 1);
                                                        cp = cp + 1;
                                                        space_left= space_left- (strlen(word)+1);
                                                }
                                                strncpy(cp, word,  strlen(word));
                                                cp = cp + strlen(word);
                                        }
                                        word=strtok(NULL, " ");
                                }
                        }else{
                                /*no formatting will take place, just print out the line*/
                                fprintf(stdout, "%s", line);
                        }
                }

        }
        /*print out the last line of buffer*/
        if (format==1){
                /*if the last char before null is a space, replace it with new line*/
                cp=cp-2;
                if (*cp == ' '){
                        strncpy(cp, "\n", 1);
                        cp=cp+1;
                        strncpy(cp,"\0", 1);
                }else{
                        cp=cp+2;
                        /*if the pointer is at the beginning of buffer, it's on an extra line. Remove line*/
                        if (cp==buffer){
                                cp=cp-1;
                                strncpy(cp,"\0", 1);

                        }
                        /*put a new line at the end*/
                        strncpy(cp,"\n", 1);
                        cp=cp+1;
                        strncpy(cp,"\0", 1);
                }
                fprintf(stdout, "%s", buffer);
        }
        exit(0);
}
