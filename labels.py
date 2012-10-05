import imaplib
import sys


def extract_label(groups, label_string):
    parts = label_string.split("/")
    root = groups
    for part in parts:
        if len(part) > 0:
            if part not in root:
                root[part] = {}
            else:
                root = root[part]

def gmail_labels(labels):
    groups = {}
    for label in labels:
        r = []
        label = label.strip()
        seen_start = False
        seen_end = False
        for c in label:
            if seen_start and seen_end and c != ' ' and c != '"':
                r.append(c)
            if not seen_start and c == '(':
                seen_start = True
            if not seen_end and c == ')':
                seen_end = True
        
        extract_label(groups, "".join(r))
    return groups

def print_labels(s, labels, n):
    for k,v in labels.iteritems():
        if v:
            print print_labels(s + " " + k , v, n+1)
        else:
            print s + " " + k
        
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(sys.argv[1],sys.argv[2])
labels = mail.list()
if labels[0] == 'OK':
    labels = gmail_labels(labels[1])
    print_labels("",labels,0)

