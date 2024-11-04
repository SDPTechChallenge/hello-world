from langchain_text_splitters import RecursiveCharacterTextSplitter
import pymupdf as fitz

pathname = "paper.pdf"

splitter = RecursiveCharacterTextSplitter(is_separator_regex=False, 
                                          chunk_size=2200, chunk_overlap=200, 
                                          length_function=len, 
                                          strip_whitespace=True,
                                          separators=[".", " ",'\n', '\n\n'])

doc = fitz.open('paper.pdf')

splits = []
text = ""

for page in doc:
    text += page.get_text()
    
splits = splitter.split_text(text)
print(f'Got {len(splits)} splits of {len(splits[5])} chars each.')



