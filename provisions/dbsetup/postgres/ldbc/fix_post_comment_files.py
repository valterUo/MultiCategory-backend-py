import csv
import collections
from os import error
import nltk
import random
nltk.download('gutenberg')
gutenberg_sentences = dict()
fieldids = nltk.corpus.gutenberg.fileids()

for id in fieldids:
    for sentence in nltk.corpus.gutenberg.sents(id):
        try:
            gutenberg_sentences[id].append(" ".join(sentence))
        except KeyError:
            gutenberg_sentences[id] = []
        

## This script fixies the problems with message

# Header of comment
# creationDate|deletionDate|id|locationIP|browserUsed|content|length|creator|place|replyOfPost|replyOfComment

# Header of post
# creationDate|deletionDate|id|imageFile|locationIP|browserUsed|language|content|length|creator|Forum.id|place

# Header of post arranged
# creationDate|deletionDate|id|locationIP|browserUsed|content|length|creator|place|imageFile|language|ForumID

# Combined version of comment and post: common part .. comment part .. post part
# creationDate|deletionDate|id|locationIP|browserUsed|content|length|creator|place| .. replyOfPost|replyOfComment| .. imageFile|language|ForumID

combined_comment_post = open("C://Users//Valter Uotila//Desktop//ldbc_snb_implementations//postgres//test-data//dynamic//message_0_0.csv", "w", encoding="utf-8")
combined_header = ["creationDate", "deletionDate", "id", "locationIP", "browserUsed", "content", "length", "creator", "place", "replyOfPost", "replyOfComment", "imageFile", "language", "ForumID"]

combined_comment_post.write("|".join(combined_header) + "\n")

def generate_content():
    random_file = random.choice(fieldids)
    sents = gutenberg_sentences[random_file]
    random_sents = random.sample(sents, random.randint(1, 10))
    return " ".join(random_sents)

def handle_reader(reader, header):
    for i, row in enumerate(reader):
        if i % 1000 == 0:
            print(i)
        row_dict = collections.OrderedDict()
        for j, head in enumerate(header):
            row_dict[head] = row[j]
        if row_dict["content"] == "" or row_dict["content"] == " ":
            row_dict["content"] = generate_content()
        combined_row = []
        for c_head in combined_header:
            if c_head in row_dict.keys():
                combined_row.append(row_dict[c_head])
            elif c_head == "ForumID":
                if "Forum.id" in row_dict.keys():
                    combined_row.append(row_dict["Forum.id"])
                else:
                    combined_row.append("")
            else:
                combined_row.append("")
        if len(combined_row) != 14:
            raise SyntaxError
        combined_comment_post.write("|".join(combined_row) + "\n")

with open("C://Users//Valter Uotila//Desktop//ldbc_snb_implementations//postgres//test-data//dynamic//comment_0_0.csv", "r", encoding="utf-8") as comment_f:
    comment_reader = csv.reader(comment_f, delimiter='|')
    comment_header = next(comment_reader)
    handle_reader(comment_reader, comment_header)


with open("C://Users//Valter Uotila//Desktop//ldbc_snb_implementations//postgres//test-data//dynamic//post_0_0.csv", "r", encoding="utf-8") as post_f:
    post_reader = csv.reader(post_f, delimiter='|')
    post_header = next(post_reader)
    handle_reader(post_reader, post_header)

combined_comment_post.close()
