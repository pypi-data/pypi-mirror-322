from argparse import ArgumentParser, Namespace

class Args():
    def __init__(self) -> None:
        self.parser: ArgumentParser = ArgumentParser(
                                            prog = "pseudocode",
                                            description = "run various pseudocode specifications."
        )

        self.parser.add_argument(
            "pseudocode_file", help = "enter file name in which the pseudocode is written."
        )
        
        self.parser.add_argument(
            "output_file", help = "[optional] enter file name in which the pseudocode will be transpiled to python.", default = None, nargs = '?'
        )
        self.args: Namespace = self.parser.parse_args()
 