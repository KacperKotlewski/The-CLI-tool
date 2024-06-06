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
        child.read()
        return child.deep_read()
    
    def deep_read(self, overwrite:bool=False) -> str:
        new_markdown = ""
        for line in self.markdown.split("\n"):
            if "(./" in line:
                start = line.find("(./")
                end = line.find(")", start)
                img_dir = line[start+1:end]
                new_img_dir = self.directory + img_dir[1:]
                line = line[:start+1] + new_img_dir + line[end:]
                
            if line.strip().startswith("!import:"):
                stripped = line.split(":")[1].strip()                    
                if stripped.startswith("./"):
                    stripped = self.directory + stripped[1:]
                new_markdown += self.get_child_content(stripped) +"\n"
            else:
                new_markdown += line + "\n"
                
        if overwrite:
            self.markdown = new_markdown
        return new_markdown
    
    def read(self):
        if not os.path.exists(f"{self.directory}/{self.name}"):
            raise FileNotFoundError(f"{self.directory}/{self.name} not found")
        
        #read utf-8
        with open(f"{self.directory}/{self.name}", "r", encoding="utf-8") as f:
            for line in f.readlines():
                self.markdown += line
    
    def append_globals(self, overwrite:bool=False):
        #from markdown import globals in --- --- block in yaml format
        from yaml import safe_load
        
        globals = None
        new_markdown = self.markdown
        if new_markdown.startswith("---"):
            splited_file = self.markdown.split("---")
            headers = splited_file[1]
            content = splited_file[2]
            globals = safe_load(headers)
                       
        if globals:     
            for key in globals:
                content = content.replace(f"${key}$", str(globals[key]))
                
                if "header-includes" in globals.keys():
                    splited_headers = headers.split("header-includes")
                    includes = splited_headers[1]
                    
                    new_includes = ""
                    for line in includes.split("\n"):
                            spacing = len(line) - len(line.lstrip())
                            line = line.replace(f"${key}$", str(globals[key]))
                            if "\n" in line:
                                line = line.replace("\n", "\n"+ " " * spacing )
                            new_includes += line + "\n"
                    includes = new_includes
                            
                    splited_headers[1] = includes
                    headers = "header-includes".join(splited_headers)
                    
            splited_file[1] = headers
            splited_file[2] = content
                    
            new_markdown = "---".join(splited_file)
            
            if overwrite:
                self.markdown = new_markdown
            
        return new_markdown
                    
    def save(self):
        with open(f"{self.directory}/{self.name}", "w") as f:
            f.write(self.markdown)
            
    def save_as(self, path:str, delete_old_file:bool = True):
        directory, name = split_path(path)
        
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        if os.path.exists(f"{directory}/{name}") and delete_old_file:
            os.remove(f"{directory}/{name}")
            
        #utf-8
        with open(f"{directory}/{name}", "w", encoding="utf-8") as f:
            f.write(self.markdown)

def convert_md_file_to_pdf(input_file:str, output_file:str = None, delete_old_file:bool = True):
    global PDF_FILE_NAME
    if not output_file:
        output_file = PDF_FILE_NAME
    
    if os.path.exists(f"{output_file}") and delete_old_file:
        os.remove(f"{output_file}")
        
    output = os.system(f'pandoc -s --citeproc --csl=csl/ieee-with-url.csl {input_file} -o {output_file} --number-sections  --listings')
    
    if output != 0:
        print(f"Error: {output}")
        exit(1)


MD_FILE_NAME = "combined_document.md"
PDF_FILE_NAME = "thesis.pdf"
SAVE_DIRECTORY = "build"

def main():
    global MD_FILE_NAME
    global PDF_FILE_NAME
    global SAVE_DIRECTORY
    
    main_md = MarkdownFile("./document", "main.md")
    main_md.read()
    main_md.append_globals(overwrite=True)
    main_md.deep_read(overwrite=True)

    filepath_md = f"./{SAVE_DIRECTORY}/{MD_FILE_NAME}"
    print(f"save to {filepath_md}")
    main_md.save_as(filepath_md, False)
    
    filepath_pdf = f"./{SAVE_DIRECTORY}/{PDF_FILE_NAME}"
    print(f"Converting {filepath_md} to {filepath_pdf}")
    convert_md_file_to_pdf(filepath_md, filepath_pdf, False)
    
    
if __name__ == "__main__":
    main()