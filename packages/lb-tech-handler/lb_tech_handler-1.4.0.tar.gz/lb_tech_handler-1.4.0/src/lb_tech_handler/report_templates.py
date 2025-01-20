from pylatex import Document,NoEscape,Command

DEFAULT_FONT_SIZE = "10pt"

DEFAULT_COMPILER = "pdflatex"

DEFAULT_REPORT_GEOMETRY = {
    "top": "1.2cm",
    "bottom" : "2.2cm",
    "left" : "0.5cm",
    "right" : "0.5cm"
}

REPORT_PACKAGES_LATEX = r"""
\usepackage[T1]{fontenc}%
\usepackage[utf8]{inputenc}%
\usepackage{lmodern}%
\usepackage{textcomp}%
\usepackage{lastpage}%
\usepackage{geometry}%
\usepackage{lmodern}                % For various font options
\usepackage{textcomp}               % For various text symbols
\usepackage{lastpage} 
\usepackage[ddmmyyyy]{datetime}
\usepackage[none]{hyphenat}         % For prevents hyphenation throughout the document
\usepackage{draftwatermark}         % Grey textual watermark on document pages
\usepackage{xcolor}                 % For color options
\usepackage{ragged2e}               % For changing the typeset alignment of text
\usepackage{array}                  % Extended implementation of the array and tabular environments which extends the options for column formats
\usepackage{longtable}              % Allows you to write tables that continue to the next page.
\usepackage{fancyhdr}               % Constructing and controlling page headers and footers
\usepackage{float}                  % Place the figure at that exact location in the page
\usepackage[hidelinks]{hyperref}    % Creating a clickable link
\usepackage{pgfplots}               % For creating plots and graphics
\usepackage{multicol}               % For dividing the pages into columns
\usepackage{multirow}               % For combining the rows and columns in the tables
\usepackage{colortbl}               % Changing the color of the table cells
\usepackage{pgffor}
\usepackage{pifont}                 %For correct and wrong symbols for ding{}
\usepackage{tabularx}               %For correct and wrong symbols for ding{}

\setlength{\headheight}{1.2cm}

"""

def add_watermark(text:str="Learn Basics", opacity:float=0.95,scale:float=0.7):

    water_mark_text = r"""\SetWatermarkLightness{ """ + str(opacity) + r"""}
    \SetWatermarkText{ """ + text + r""" }
    \SetWatermarkScale{ """ + str(scale) + r"""}"""

    return water_mark_text

def add_header_footer(report_name,school_name,logopath,school_acronym):

    header_footer_code = r'''
    \pagestyle{fancy}

    \fancyhf{}

            \fancyhfinit{%
            
            \renewcommand{\footrulewidth}{0.7pt}%

            \fancyhead[L]{%
                \includegraphics[width = 3.0cm, height=1cm]{'''+logopath+r'''}
            }%

            \fancyhead[C]{%
                
                \Large  \textbf{''' + school_name + r'''} \\
                \textbf{''' + report_name + r'''}
                \vspace{-0.1cm}
            }%

            \fancyhead[R]{%
                
            }%
            
                        
            \fancyfoot[L]{
                Learn Basics | ''' + school_acronym + r'''
                
            }

            \fancyfoot[C]{
                ''' +report_name + r''' - \thepage
            }

            \fancyfoot[R]{%
                \today \; \currenttime
            }%

            \renewcommand{\headrulewidth}{1pt}%

            \renewcommand{\footrulewidth}{1pt}%        

        }'''
    
    return header_footer_code

class BaseA4PotraitReport(Document):

    def __init__(self,font_size=DEFAULT_FONT_SIZE,geometry_options=DEFAULT_REPORT_GEOMETRY):
        super().__init__(geometry_options=geometry_options)

        self.documentclass = Command('documentclass', options=[font_size, 'a4paper'], arguments=['article'])

        self.preamble.append(NoEscape(REPORT_PACKAGES_LATEX))

        self.append(NoEscape(add_watermark()))

class BaseA4LandscapeReport(Document):

    def __init__(self,font_size=DEFAULT_FONT_SIZE,geometry_options=DEFAULT_REPORT_GEOMETRY):
        super().__init__(geometry_options=geometry_options)

        self.documentclass = Command('documentclass', options=[font_size, 'a4paper','landscape'], arguments=['article'])

        self.preamble.append(NoEscape(REPORT_PACKAGES_LATEX))

        self.append(NoEscape(add_watermark()))

class BaseA3LandscapeReport(Document):

    def __init__(self,font_size=DEFAULT_FONT_SIZE,geometry_options=DEFAULT_REPORT_GEOMETRY):
        super().__init__(geometry_options=geometry_options)

        self.documentclass = Command('documentclass', options=[font_size, 'a3paper','landscape'], arguments=['article'])

        self.preamble.append(NoEscape(REPORT_PACKAGES_LATEX))

        self.append(NoEscape(add_watermark()))
    
class BaseA3PotraitReport(Document):

    def __init__(self,font_size=DEFAULT_FONT_SIZE,geometry_options=DEFAULT_REPORT_GEOMETRY):
        super().__init__(geometry_options=geometry_options)

        self.documentclass = Command('documentclass', options=[font_size, 'a3paper'], arguments=['article'])

        self.preamble.append(NoEscape(REPORT_PACKAGES_LATEX))

        self.append(NoEscape(add_watermark()))

