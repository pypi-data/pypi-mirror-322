class BNF():
    """Generates a LL Parser for given bnf"""
    def __init__(self, language: str="edexcel") -> None:
        """
        Initialises the BNF class for generating a parser

        Args:
            language (str, optional): The language of the bnf. Four languages are available: 
                - cie 
                - edexcel 
                - aqa  
                - ocr
        """
    
    @staticmethod
    def import_bnf(language: str):
        with open(f"igcse_cs/transpilation/{language}.bnf") as bnf:
            bnf = bnf.read()
        print(bnf)