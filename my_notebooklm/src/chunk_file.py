from langchain_text_splitters import CharacterTextSplitter
from read_file import readFile

def splitter():
    return CharacterTextSplitter(
    separators=["\n\n", "\n", " ", ""],
    chunk_size = 500,
    chunk_overlap = 50
    )

def chunkData(file_content):
    text_splitter = splitter()  
    return text_splitter.split_text(file_content)

def main():
    file_content = readFile()
    if file_content:
        chunks = chunkData(file_content)
        print(f"Total chunks created: '{len(chunks)}'")
        print(chunks[0])

if __name__ == "__main__":
    main()    