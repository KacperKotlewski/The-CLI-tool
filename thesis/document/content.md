<!---------------------------------------------------------------------->
<!----------------             Introduction             ---------------->
<!---------------------------------------------------------------------->
\section*{Introduction}
\label{sec:introduction}
\addcontentsline{toc}{section}{\nameref{sec:introduction}}

\subsection*{Background}
\label{sec:background}
\addcontentsline{toc}{subsection}{\nameref{sec:background}}

In modern software development, command line interface (CLI) tools are essential for automating tasks, managing dependencies, and deploying applications. These tools provide a convenient way to interact with software systems and perform various operations, such as building, testing, and deploying code. Examples of popular CLI tools include npm, yarn, and git, which are widely used in web development and version control. Similarly, dotEnv (.env) files are used to store configuration settings and environment variables for applications. These files are used to define key-value pairs that can be accessed by the application during runtime, allowing developers to manage sensitive information, such as API keys and database credentials, without hardcoding them into the codebase. The combination of CLI tools and dotEnv files is a common practice in modern software development, and understanding how to use and manage them is crucial for developers. Therefore, the development of a CLI tool for managing dotEnv files can provide significant value to the development community by simplifying the process of working with environment variables and configuration settings. This engineering work aims to develop a CLI tool that will support managing environment variables in projects, using the Python 3 programming language to implement the tool. The primary purpose of the tool will be to facilitate and streamline work with environment variables by ensuring efficiency, intuitiveness, ease of use, scalability, and shareability. To achieve this goal, the tool will use serializers to create schema files and deserialize dotEnv files, and regular expressions (regex) as fields in the schema file. This approach will enable developers to define and manage environment variables in a structured and organized manner, making it easier to work with configuration settings and share them across different environments and projects. By providing a user-friendly and efficient way to manage environment variables, the CLI tool will contribute to improving the development workflow and enhancing the overall productivity of developers. The tool will also address common challenges associated with managing environment variables, such as maintaining consistency, ensuring security, and simplifying the process of updating and sharing configuration settings. Overall, the development of the CLI tool for managing environment variables in projects will provide a valuable resource for developers, enabling them to work more effectively and efficiently with environment variables and dotEnv files in their projects. The tool will be designed to be flexible, extensible, and easy to integrate into existing development workflows, making it a valuable addition to the toolkit of modern software developers. By addressing the needs of developers and providing a user-friendly solution for managing environment variables, the CLI tool will contribute to the advancement of best practices in software development and help developers achieve better outcomes in their projects.


\subsection*{Motivation}
\label{sec:motivation}
\addcontentsline{toc}{subsection}{\nameref{sec:motivation}}


The development of the CLI tool for managing environment variables in projects is motivated by the need to address common challenges and limitations associated with working with environment variables and dotEnv files. Environment variables are commonly used in various areas related to IT, such as configuring operating systems, virtual machines, external servers, databases, and API endpoints. However, setting up and managing environment variables can be time-consuming, especially when working on multiple devices and different environments. The use of dotEnv files has become a popular approach for managing environment variables, but it has limitations, such as security concerns and difficulties in sharing configuration settings. Therefore, there is a need for a more efficient and secure solution for managing environment variables in projects. The motivation to research and improve the management of environment variables in projects is driven by the need to provide better workflow and guidelines based on existing solutions, such as dotEnv files. The goal is to develop a powerful tool that can improve the management of environment variables and provide developers with a more effective way to work with configuration settings. The CLI tool will be designed to address the limitations of existing solutions and provide a user-friendly and secure approach to managing environment variables. The tool will be built as a Command Line Interface (CLI) tool, leveraging the widespread use of CLI tools in various IT applications, such as package management, version control, and media processing. The development of the CLI tool will follow SOLID methodologies to ensure proper adapters, fabricators, and other good practices for easy maintenance and extendability of future features. By developing the CLI tool for managing environment variables in projects, this engineering work aims to provide a valuable resource for developers, enabling them to work more effectively and efficiently with environment variables and dotEnv files in their projects. The tool will be designed to be flexible, extensible, and easy to integrate into existing development workflows, making it a valuable addition to the toolkit of modern software developers. The motivation behind the development of the CLI tool is to contribute to the advancement of best practices in software development and help developers achieve better outcomes in their projects.


\subsection*{Objectives}
\label{sec:objectives}
\addcontentsline{toc}{subsection}{\nameref{sec:objectives}}

The main objective of this engineering work is to develop a CLI tool for managing environment variables in projects, using the Python programming language to implement the tool. The tool will be designed to facilitate and streamline work with environment variables by ensuring efficiency, intuitiveness, ease of use, scalability, and shareability. The specific objectives of the engineering work are as follows:

  - To research and analyze the existing solutions for managing environment variables and dotEnv files.
    
    > This objective will involve reviewing the current state of the art in environment variable management and CLI tools, including an examination of the features, limitations, and advantages of existing solutions. The goal is to identify the best practices and common challenges associated with managing environment variables and dotEnv files, as well as to understand the needs and requirements of developers in this area. The research will provide the foundation for the development of the CLI tool and ensure that it addresses the most relevant issues and provides valuable features to the development community.
    
  - To design and develop a CLI tool for managing environment variables in projects with Python 3.

    > This objective will involve designing the architecture and functionality of the CLI tool, including its main features, capabilities, and user interface. The development of the tool will follow best practices in software engineering, including SOLID principles, design patterns, and clean code practices. The tool will be implemented using the Python 3 programming language, leveraging its rich ecosystem of libraries and frameworks for building command line applications. The development process will include stages such as planning, design, implementation, testing, and validation, ensuring that the tool meets the requirements and objectives of the engineering work.


  - To test and validate the CLI tool to ensure its functionality, reliability, and usability.

    > This objective will involve creating a test plan and test cases for the CLI tool, including unit tests, integration tests, and user acceptance testing. The goal is to ensure that the tool performs as expected, meets the quality standards, and provides a user-friendly experience for developers. The test results and analysis will be used to validate the functionality and reliability of the tool, as well as to identify any potential issues or areas for improvement.

  - To compare the CLI tool with alternative solutions and analyze its impact on the domain and the community.

    > This objective will involve comparing the CLI tool with similar tools and alternative solutions, including an analysis of their features, limitations, and advantages. The goal is to understand how the CLI tool stands out from existing solutions and provides unique value to the development community. The impact of the CLI tool on the domain and the community will be analyzed to assess its potential benefits and contributions to the field of environment variable management.

  - To draw conclusions and provide recommendations for future work based on the findings of the engineering work.

    > This objective will involve summarizing the main findings and insights from the research and development of the CLI tool, as well as drawing conclusions on its strengths, limitations, and potential for future improvements. The goal is to provide valuable recommendations for future work, including potential enhancements to the tool, additional features, and possible extensions to its functionality. The conclusions will highlight the significance of the CLI tool and its potential impact on the domain and the community, as well as the importance of the work in advancing best practices in software development.

\subsection*{Scope}
\label{sec:scope}
\addcontentsline{toc}{subsection}{\nameref{sec:scope}}

The scope of this engineering work is focused on the development of a CLI tool for managing environment variables in projects, this program will help developers to manage environment variables in a structured and organized manner, making it easier to work with configuration settings and share them across different environments and projects. The tool will be designed to be flexible, extensible, and easy to integrate into existing development workflows, making it a valuable addition to the toolkit of modern software developers. This thesis will provide a comprehensive overview of the development process, including the research, design, implementation, testing, and validation of the CLI tool. The research will involve an analysis of the existing solutions for managing environment variables and dotEnv files, as well as an examination of the related research works in this area.


\subsection*{Document Structure}
\label{sec:document_structure}
\addcontentsline{toc}{subsection}{\nameref{sec:document_structure}}

This paper consist 5 chapters, not including the introduction and the implications. The first chapter is the state of the art, where the key concepts and terminologies are explained, and the overview of alternative to the tool is presented. In the second chapter, the technical description of the tool is presented, including its functionality, architecture, implementation details, and interfaces. Third chapter will present the methodology used for designing and developing the tool, including the design approach, development process, and testing strategy. In the fourth chapter, the test and validation of the tool will be presented, including the test plan, test cases, and test results. Finally, the fifth chapter will discuss and analyze the tool, including a comparison with alternatives, limitations and challenges, and the impact of the work. Below all five chapters is the implications section, which will provide a summary of findings, conclusions, and recommendations for future work based on the findings of the engineering work. The document structure is designed to provide a comprehensive overview of the development process and the main insights from the research and development of the CLI tool.

\newpage
<!---------------------------------------------------------------------->
<!----------------           State of the Art           ---------------->
<!---------------------------------------------------------------------->
# State of the Art

## Key Concepts and Terminologies
Explanation of the key concepts and terminologies relevant to the development of the CLI tool, including environment variables, dotEnv files, and CLI tools, as well as other relevant concepts and terminologies that will be used throughout the document.

### Environment Variables
Environment variables are dynamic-named values that can affect the way running processes will behave on a computer. They are part of the environment in which a process runs. For example, in node.js based frameworks it is common to use environment variables to store sensitive information, such as API keys, database credentials, and other configuration settings. I will deep dive this example by taking the Vue.js framework that is running on node.js, in this framework you can set environment variable of *VUE_APP_TITLE* to value *Web dev portfolio* in .env file and then access it in the code by using ``process.env.VUE_APP_TITLE``. This is a common practice in modern software development, as it allows developers to manage sensitive information without hardcoding it into the codebase. Environment variables are also used to define system-wide settings, such as the location of executable files, the default editor, and the default shell. They are used by the operating system and all the processes that run on it. Environment variables are typically set at the time of login, for example, when a user logs in to a computer, the operating system may set environment variables for that user. They can also be set by the running process, or by the user, or by the system. They are used to pass information to programs and to the system itself. According to an sources from wikipedia about unix 7 [link](https://en.wikipedia.org/wiki/Version_7_Unix), as well as environment variables[link](https://en.wikipedia.org/wiki/Environment_variable), and also article of PhD Eli Thorkelson [link](https://decasia.org/tech/2023/03/where-do-env-vars-come-from.html) environment variables were introduced in their modern form in 1979 with Version 7 Unix, and you can find them in all Unix operating system families including Linux and macOS. In Microsoft OS family it was adopted in PC DOS 2.0 in 1982, and it is used up to this day in all widely spread operating systems.

### dotEnv Files
DotEnv or .env files are used to store configuration settings and environment variables for applications. They are simple text files that contain key-value pairs, with each pair representing an environment variable and its value. For example, a .env file might contain the following key-value pairs:

```env
API_KEY=abc123
DB_HOST=localhost
DB_USER=admin
DB_PASS=password
```

These key-value pairs can be accessed by the application during runtime, allowing developers to manage sensitive information without hardcoding it into the codebase. The use of .env files has become a popular approach for managing environment variables, as it provides a convenient way to define and access configuration settings for applications. According to the official documentation of the node.js dotenv library [link](https://www.dotenv.org/docs/security/env.html), the .env file format was introduced by Heroku in 2012 and popularized by the dotenv node module in 2013. The .env file format provides a secure place to store sensitive application secrets, and it is widely used in modern software development to manage environment variables and configuration settings. The .env file format is simple and easy to use, making it a popular choice for developers who want to manage environment variables in a structured and organized manner. The use of .env files has become a common practice in modern software development, and understanding how to use and manage them is crucial for developers.

### CLI Tools
Command Line Interface (CLI) tools are essential for automating tasks, managing dependencies, and deploying applications. They provide a convenient way to interact with software systems and perform various operations, such as building, testing, and deploying code. Concept of CLI tools is the idea of a command line interface, which allows users to interact with the tool by entering commands and arguments into a terminal or console. Examples of this type of programs and tools starts from ping command, ifconfig/ipconfig up to git, docker, npm, python, and many more. CLI tools are used to execute commands and scripts from the command line, allowing developers to perform a wide range of tasks without the need for a graphical user interface. They are commonly used in software development to automate repetitive tasks, manage project dependencies, and interact with version control systems. The use of CLI tools is widespread in modern software development, and understanding how to use and manage them is crucial for developers. Few examples of CLI programs that are widely used in software development are git, docker, npm, python, and many more. Git is a distributed version control system that is widely used in software development to manage source code and track changes. Docker is a platform for developing, shipping, and running applications using containerization. Npm is a package manager for the JavaScript programming language, used to install, manage, and publish packages. Python is a high-level programming language that is widely used in software development for web development, data analysis, machine learning, and many other applications. These CLI tools are essential for modern software development, and understanding how to use and manage them is crucial for developers.


### Python
Python is a high-level programming language that is widely used in software development for web development, data analysis, machine learning, and many other applications. It is known for its simplicity and readability, making it an ideal language for beginners and experienced developers alike. Python has a rich ecosystem of libraries and frameworks that make it easy to build command line applications, web applications, and other software systems. It is widely used in software development for its simplicity, readability, and rich ecosystem of libraries and frameworks. Python is a versatile language that can be used for a wide range of applications, including web development, data analysis, machine learning, and many others. It is known for its simplicity and readability, making it an ideal language for beginners and experienced developers alike. Python is widely used in software development, and understanding how to use and manage it is crucial for developers. For purpose of this engineering work, the Python 3 programming language will be used to implement the CLI tool for managing environment variables in projects because of its attributes mentioned above.

## Overview of Alternative to the Tool

<!-- 
Vault by HashiCorp:

Opis: Narzędzie do zarządzania sekretami umożliwiające bezpieczne przechowywanie, dostęp i audytowanie poufnych danych.
Funkcjonalności: Dynamiczne sekrety, szyfrowanie danych, zaawansowane zarządzanie politykami dostępu.
Ograniczenia: Wymaga zaawansowanej wiedzy technicznej do konfiguracji i zarządzania.
Zalety: Wysoki poziom bezpieczeństwa, elastyczność, wsparcie dla wielu dostawców usług chmurowych.
Doppler:

Opis: Platforma do centralnego zarządzania sekretami i konfiguracjami aplikacji.
Funkcjonalności: Centralne przechowywanie, wersjonowanie konfiguracji, łatwa integracja z narzędziami deweloperskimi.
Ograniczenia: Możliwe ograniczenia w kompatybilności z niektórymi specyficznymi środowiskami.
Zalety: Prostota użytkowania, wspiera bezpieczne wdrażanie i zarządzanie konfiguracją w różnych środowiskach.

Vault by HashiCorp to zaawansowane narzędzie do zarządzania sekretami, które umożliwia dynamiczne generowanie sekretów, szyfrowanie danych przechowywanych i przesyłanych, oraz szczegółowe zarządzanie politykami dostępu. Vault jest wysoce konfigurowalny i zaprojektowany z myślą o bezpieczeństwie na najwyższym poziomie. Oferuje również możliwości takie jak leasing i odnawianie sekretów, co umożliwia automatyczne zarządzanie ich cyklem życia. Jego modularna architektura pozwala na łatwą integrację z istniejącymi systemami. Wadą może być skomplikowana konfiguracja i wymóg głębokiej wiedzy technicznej do efektywnego wykorzystania wszystkich funkcji.

Doppler zapewnia centralne miejsce do zarządzania wszystkimi sekretami i konfiguracjami aplikacji, umożliwiając ich bezpieczne przechowywanie, dostęp i synchronizację między różnymi środowiskami i zespołami. Jest łatwy w użyciu i integruje się z wieloma popularnymi narzędziami i platformami deweloperskimi. Doppler oferuje również wersjonowanie konfiguracji, co ułatwia zarządzanie zmianami i wprowadzanie aktualizacji. Jednak, jak każde narzędzie, może mieć ograniczenia związane z kompatybilnością z niektórymi specyficznymi środowiskami lub narzędziami.


 -->

### Vault by HashiCorp

Vault by HashiCorp is an advanced tool for managing secrets that enables secure storage, access, and auditing of confidential data. It provides features such as dynamic secrets, data encryption, and advanced access policy management. Vault is highly configurable and designed with security at the highest level. It also offers capabilities such as leasing and renewing secrets, enabling automatic lifecycle management. Its modular architecture allows for easy integration with existing systems. However, it may require advanced technical knowledge to effectively utilize all of its features.

### Doppler

Doppler provides a central place for managing all application secrets and configurations, enabling their secure storage, access, and synchronization across different environments and teams. It is easy to use and integrates with many popular developer tools and platforms. Doppler also offers configuration versioning, making it easier to manage changes and introduce updates. However, like any tool, it may have limitations related to compatibility with specific environments or tools.

## Examination of Related Research Works
Summary of academic and industry research relevant to CLI development and usage as well as research on the specific domain of the tool.


\newpage
<!---------------------------------------------------------------------->
<!----------------  Technical Description of the Tool   ---------------->
<!---------------------------------------------------------------------->
# Technical Description of the Tool

## Functionality
What the tool does, including its main features and capabilities.

## Architecture
High-level architecture of the tool, including major components and their interactions.

## Implementation Details
Technical details of the tool's implementation, including programming languages, libraries, and frameworks used.

## Interfaces

### Command Line Interface (CLI)
How the CLI is used, including its commands, options, and arguments.

### Web Interface
How the web interface is used, including its features and capabilities.

## Security
Security features and mechanisms implemented in the tool.

\newpage
<!---------------------------------------------------------------------->
<!----------------             Methodology              ---------------->
<!---------------------------------------------------------------------->
# Methodology

## Design Approach
The methodology used for designing the tool, including any design patterns or principles.

## Development Process
Stages of development, from initial planning to final implementation.

## Testing Strategy
Approach to testing, including unit tests, integration tests, and user acceptance testing.


\newpage
<!---------------------------------------------------------------------->
<!----------------         Test and Validation          ---------------->
<!---------------------------------------------------------------------->
# Test and Validation

## Test plan
Overview of the unit tests test cases and the integration tests test cases, including the test environment and the test data.

## Test results and analysis
Summary of the test results and analysis of the test coverage and the test results.

\newpage
<!---------------------------------------------------------------------->
<!----------------       Discussion and Analysis        ---------------->
<!---------------------------------------------------------------------->
# Discussion and Analysis

## Comparison with alternatives
Comparison of similar tools and their features.

## Limitations and challenges
Limitations and challenges of the tool, including its potential drawbacks and issues.

## Impact of the Work
Potential impact of the tool on the domain and the community.

\newpage
<!---------------------------------------------------------------------->
<!----------------             Conclusions              ---------------->
<!---------------------------------------------------------------------->
\section*{Implications}
\label{sec:implications}
\addcontentsline{toc}{section}{\nameref{sec:implications}}

\subsection*{Summary of Findings}
\label{sec:summary_of_findings}
\addcontentsline{toc}{subsection}{\nameref{sec:summary_of_findings}}

Recap of the main findings and the key insights from the research and the development of the tool, how the tool meets the requirements and the objectives, and the main contributions of the tool.

\subsection*{Conclusions}
\label{sec:conclusions}
\addcontentsline{toc}{subsection}{\nameref{sec:conclusions}}

Final thoughts on the tool, including its strengths and limitations, and the potential for future improvements and extensions.

\subsection*{Future Work}
\label{sec:future_work}
\addcontentsline{toc}{subsection}{\nameref{sec:future_work}}

Suggestions for future work, including potential improvements to the tool, additional features, and possible extensions to the tool's functionality.

\subsection*{Final Remarks}
\label{sec:final_remarks}
\addcontentsline{toc}{subsection}{\nameref{sec:final_remarks}}

Closing remarks on the tool and its significance, including its potential impact on the domain and the community, and the importance of the work.