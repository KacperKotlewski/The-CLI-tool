# get main.md file
# import all elements that contains <!-- import: xyz.md --> and replace them with the content of the file
# save the file as md
# convert to pdf
import os

def split_path(path:str) -> (str, str):
    name = path.split("/")[-1]
    directory = "/".join(path.split("/")[:-1])
    
    return (directory, name)

class MarkdownFile:
    directory:str
    name:str
    markdown:str = ""
    
    def __init__(self, directory:str, name:str):
        self.directory = directory
        self.name = name

    @classmethod
    def fromPath(cls, path:str):
        directory, name = split_path(path)
        return MarkdownFile(directory, name)
    
    def get_child_content(self, child_dir:str):
        child = MarkdownFile.fromPath(child_dir)
        child.read_line_by_line()
        return child.markdown
    
    def read_line_by_line(self):
        if not os.path.exists(f"{self.directory}/{self.name}"):
            raise FileNotFoundError(f"{self.directory}/{self.name} not found")
        
        with open(f"{self.directory}/{self.name}", "r") as f:
            for line in f.readlines():
                if line.strip().startswith("!import:"):
                    stripped = line.split(":")[1].strip()                    
                    if stripped.startswith("./"):
                        stripped = self.directory + stripped[1:]
                    self.markdown += self.get_child_content(stripped) +"\n"
                else:
                    self.markdown += line
                    
    def save(self):
        with open(f"{self.directory}/{self.name}", "w") as f:
            f.write(self.markdown)
            
    def save_as(self, path:str):
        directory, name = split_path(path)
        
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        with open(f"{directory}/{name}", "w") as f:
            f.write(self.markdown)

def convert_md_file_to_pdf(input_file:str, output_file:str = None):
    global PDF_FILE_NAME
    if not output_file:
        output_file = PDF_FILE_NAME
    os.system(f'pandoc -s --citeproc --bibliography=references.bib --csl=csl/ieee-with-url.csl {input_file} -o {output_file} --toc --toc-depth=2')


MD_FILE_NAME = "combined_document.md"
PDF_FILE_NAME = "thesis.pdf"
SAVE_DIRECTORY = "build"

def main():
    global MD_FILE_NAME
    global PDF_FILE_NAME
    global SAVE_DIRECTORY
    
    main_md = MarkdownFile("./document", "main.md")
    main_md.read_line_by_line()

    filepath_md = f"./{SAVE_DIRECTORY}/{MD_FILE_NAME}"
    print(f"save to {filepath_md}")
    main_md.save_as(filepath_md)
    
    filepath_pdf = f"./{SAVE_DIRECTORY}/{PDF_FILE_NAME}"
    print(f"Converting {filepath_md} to {filepath_pdf}")
    convert_md_file_to_pdf(filepath_md, filepath_pdf)
    
    
if __name__ == "__main__":
    main()