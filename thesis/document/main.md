---
lang: en-GB
author: Kacper Kotlewski
title: The CLI tool - managing environment variables in projects
document_class: ENGINEERING DIPLOMA THESIS
album_no: 338854
supervisor: Dr Hab. Łukasz Machura
location: Chorzów
date: 2024
university: UNIVERSITY OF SILESIA IN KATOWICE
faculty: |
  FACULTY OF SCIENCE AND TECHNOLOGY,\\
  AUGUST CHEŁKOWSKI INSTITUTE OF PHYSICS
field_of_study: Applied Computer Science

geometry: margin=2.5cm
fontsize: 14.5pt

bibliography: references.bib
toc: true
toc-depth: 2

header-includes: |
    \usepackage{hyperref}
    \usepackage{listings}
    
    \usepackage{xcolor}
    
    \usepackage{tabulary}
    
    \definecolor{codegreen}{rgb}{0,0.6,0}
    \definecolor{codegray}{rgb}{0.5,0.5,0.5}
    \definecolor{codepurple}{rgb}{0.58,0,0.82}
    \definecolor{backcolour}{rgb}{0.95,0.95,0.92}

    \lstdefinestyle{mystyle}{
        backgroundcolor=\color{backcolour},
        commentstyle=\color{codegreen},
        keywordstyle=\color{magenta},
        numberstyle=\tiny\color{codegray},
        stringstyle=\color{codepurple},
        basicstyle=\ttfamily\footnotesize,
        breakatwhitespace=false,
        breaklines=true,
        captionpos=b,
        keepspaces=true,
        numbersep=5pt,
        showspaces=false,
        showstringspaces=false,
        showtabs=false,
        tabsize=2
    }

    \lstset{style=mystyle}

    \setlength{\parindent}{5mm}
    


    \renewcommand{\maketitle}{
      \begin{titlepage}
        \centering
        \textbf{
          \large
          $university$\\
          \small
          $faculty$\\
        }
        \normalsize
        $field_of_study$\\

        \vspace{4 cm}
      
        \begin{center}
        \vspace{0.5 cm}
        \large
        $author$\\
        ALBUM NO: $album_no$\\
        \vspace*{0.5 cm}
        \huge
        $title$\\

        \small
        \vspace{4 cm}
        \begin{flushleft}
          $document_class$\\
          Supervisor: $supervisor$\\
        \end{flushleft}

        \vspace{4 cm}
        \small 
        $location$ $date$\\
        \end{center}
        \clearpage
      \end{titlepage}
    }
---
\newpage



!import: ./content.md
\newpage


\section*{Bibliography}