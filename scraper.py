import requests
import os
from bs4 import BeautifulSoup

def extract_paragraphs(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    paragraphs = [p.get_text() for p in soup.find_all('p')]

    cleaned_paragraphs = []
    for paragraph in paragraphs:
        # Clean the paragraph data here (if needed)
        cleaned_paragraph = paragraph.strip()  # Remove leading/trailing whitespace
        cleaned_paragraph = ' '.join(cleaned_paragraph.split())  # Remove extra spaces
        cleaned_paragraphs.append(cleaned_paragraph)

    return cleaned_paragraphs

urls = [
    #"https://www.cs.stonybrook.edu/admissions/Graduate-Program",
    "https://cse.ucsd.edu/graduate/admissions",
    "https://www.eecs.mit.edu/academics/graduate-programs/admission-process/graduate-admissions-faqs/",
    "https://seas.harvard.edu/prospective-students/prospective-graduate-students/frequently-asked-questions-faqs-graduate"
    ]

paragraphs = []
for url in urls:
    paragraphs.append(extract_paragraphs(url))

f = open("data.txt", "w")
for paragraph in paragraphs:
    for para in paragraph:
        f.write(para)
f.close()

with open('data.txt', 'r') as file:
    while True:
        line = file.readline()
        if not line:
            break
        print(line)