---
lang: en-GB
author: Name Surname
title: Project
document_class: ENGINEERING DIPLOMA THESIS
album_no: 000000
supervisor: DSc. John Doe
location: Poland
date: 2024
affiliation: University

bibliography: references.bib
toc: true
toc-depth: 2

header-includes: |
    \renewcommand{\maketitle}{
      \begin{titlepage}
        \centering
        \textbf{$affiliation$}
        \vspace{1 cm}
      
        \begin{center}
        \vspace{0.5 cm}
        \large
        $author$\\
        ALBUMU NO: $album_no$\\
        \vspace*{0.5 cm}
        $title$\\
        %\textbf {Something clever}\\
        %\vspace*{0.5 cm}
        %\vspace*{2.0 cm}
        \small
        \vspace*{2.0 cm}
        $document_class$\\
        \vspace*{2.0 cm}
        Supervisor: $supervisor$\\
        %\vspace{0.5 cm}
        \vspace{5.0 cm}
        \small 
        $location$ $date$\\
        \end{center}
        \clearpage
      \end{titlepage}
    }
---
\newpage

some reference to the introduction [@aiOverview]


!import: ./1_introduction/_main.md
\newpage



\section*{Bibliography}