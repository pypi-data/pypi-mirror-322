from lb_tech_handler import report_templates
from pylatex import NoEscape

class SampleReport(report_templates.BaseA4LandscapeReport):
    def __init__(self,*args,**kwargs):

        super().__init__(*args,**kwargs)
        
        self.append(NoEscape("Hello World"))

        self.add_header_footer(right_footer_latex=self.CURRENT_PAGE_NO,left_footer_latex=self.CURRENT_PAGE_NO)

        self.generate_pdf(filepath='test.pdf',clean_tex=False,compiler=report_templates.DEFAULT_COMPILER)

if __name__ == "__main__":
    SampleReport()