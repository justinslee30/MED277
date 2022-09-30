import re

def file_line_count(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
        return i+1

def find_hpi_sections(fname):
    iterator = 0
    iterator2 = 0
    start =[]
    end = []
    input_find_sentences = []
    with open(fname) as f:
        for i, line in enumerate(f):
            line = line.strip()
            if re.match('^HPI:',line):
                print("hpi start line:",i+1)
                start.append(i)
                iterator += 1
            if re.match('Allergies:$',line):
                print("hpi end line:",i)
                end.append(i)
        print("number of HPI sections:",iterator)
        f.seek(0)
        for i, line in enumerate(f):
            if i >= start[iterator2] and i <= end[iterator2]:
                print(line)
                if iterator2 == 0:
                    input_find_sentences.append(line)
            if i == end[iterator2] and iterator2 < iterator-1:
                iterator2 += 1
                print("\n\n\n------------------------------------------\n\n")
        print("\n\n\n------------------------------------------\n\n")
        return ' '.join(input_find_sentences)
    
def find_sentences(input_text):
    input_redact_numbers = []
    print("number of sentences:",len(re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s+',input_text)))
    lines = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)\.\s+',input_text)
    for i,line in enumerate(lines):
        print(line)
        print()
        if i == 0:
            input_redact_numbers.append(line)
    return ''.join(input_redact_numbers)
    
def redact_numbers(input_text):
    p = re.compile('\d')
    print(p.sub('[nums]', input_text))
    
file = 'find_hpi.csv'
print ("file:"+file+"\nline count:", file_line_count(file))
input_find_sentences = find_hpi_sections(file)
input_redact_numbers = find_sentences(input_find_sentences)
redact_numbers(input_redact_numbers)