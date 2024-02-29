# Architecture

## Legend:
**?** - optional / not yet implemented
**!** - important

## Domain Model

### Files in domain
- [x] ! - **dotEnv** (.env, .env.example, .env.test, .env.development, .env.production)
- [x] ! - **schema** (.env.schema)
- [ ] ? - **vaults** (.env.vault)
- [ ] ? - **preferences & settings** (config.json)

### DotEnv files:
DotEnv files are the main part of the domain model. They are the files that are used to store environment variables. They are used to store sensitive information, such as API keys, database passwords, etc. They are also used to store configuration settings for the application. Goal of the tool is to provide a way to manage these files in a structured and secure way.
- [x] ! - handle comments (with #)
- [x] ! - handle empty lines
- [x] ! - handle keys with values
- [x] ! - handle empty values
- [ ] ? - handle lists
- [ ] ? - handle quoted values
- [ ] ? - handle escaped characters

### Schema files:
Schema files are used to define the structure of the environment variables. They are used to define the keys, their types, default values, descriptions, etc. They are used to define the structure of the environment variables and to provide a way to generate the environment variables files. This is the most important part of the domain model, files are secure and structured. They will be easy to maintain and to generate new files from them for different environments, projects, and users. Tool need to guide the user to create a schema file and to generate the environment variables files from it.
- [x] ! - handle schema CLI version
- [x] ! - handle schema info:
  - [x] ! - environment schema name
  - [x] ! - environment schema version
  - [x] ! - environment schema author
  - [x] ! - environment schema license
  - [x] ! - environment schema version
- [x] ! - handle text comments:
  - [x] ! - Header, Section, Subsection, Message
  - [x] ! - Space, Divider
- [x] ! - handle fields:
  - [x] ! - field key
  - [x] ! - field default value
  - [x] ! - field display name
  - [x] ! - field description
  - [x] ? - field example value
  - [ ] ? - field hint
  - [ ] ? - field type:
    - [x] ! - string
    - [ ] ! - number
    - [ ] ! - uuid
    - [ ] ? - list of types
  - [ ] ! - field regex
  - [ ] ? - field error message
  - [ ] ! - field props:
    - [ ] ! - required
    - [ ] ! - hidden
  - [ ] ? - field generate options:
    - [ ] ? - length - in case of string
    - [ ] ? - range - in case of number
    - [ ] ? - list length - in case of list

### Vaults:
currently not implemented - they are not as important as the other parts of the domain model

### Preferences & Settings:
currently not implemented - they are not as important as the other parts of the domain model

## CLI
Usually CLI consists of the following structure:

`` Program [Options] [Arguments] ``
or
`` Program Command [Options] [Arguments] ``
or
`` Program Module Command [Arguments] [Options] ``
or
`` Program Module [Arguments] [Options] ``

In this tool you will also find user interfaces options that will be set in the program module. But more on that later

### Modularity
Based on that structure above we can define the following modules models:
- [ ] ! - **Module Abstract** - consists of a set of options and arguments, key (calling name), name, description, help, selected ui
  - [ ] ! - **Command** - interface depended, consists of the steps
  - [ ] ! - **Module** - consists of a set of commands and submodules
    - [ ] ! - **Program** - root module, consists of a set of modules, commands, options, and interfaces
- [ ] **Module Handler** - register and handle modules

### Options
Based on the structure above we can define the following options models:
- [ ] ! - **Option Abstract** - consists of a set of keys (calling name), name, description
  - [ ] ! - **Option** - build from the key and value
    - [ ] ! - **Argument** - build from the value only
    - [ ] ! - **Flag** - build from the key only

### Interfaces
Based on the structure above we can define the following interfaces models:
- [ ] ! - **Interface Abstract** - consists of a set of keys (calling name), name, description, handlers
  - [ ] ! - **UserInterface** - Abstract class, consists of a set of methods to handle the user input and output
    - Methods:
      - [ ] ! - **Prompt** - method to prompt the user for input
      - [ ] ! - **Select** - method to select the user from the list
      - [ ] ! - **Confirm** - method to confirm the user
      - [ ] ? - **Alert** - method to alert the user
      - [ ] ! - **Output** - method to output the data to the user
    - Fields:
      - [ ] ! - **Actions** - list of actions that can be executed
      - [ ] ! - **Data** - list of data that can be selected
      - [ ] ! - **Steps** - list of steps that can be executed
    - Inherited classes:
      - [ ] ! - **DataDrivenUI** - Executing commands that need UI in the data-driven way, based on the data provided for example from the schema file, then the user will choose the data from the list and choose the action to execute
      - [ ] ? - **MenuDrivenUI** - Executing commands that need UI in the menu-driven way, based on the menu made from actions, then selected action ask to choose data from the list