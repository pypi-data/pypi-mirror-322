class Color:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


class Display:
    @staticmethod
    def printb(*args, **kwargs):
        # Use join to handle multiple arguments and apply bold to all of them
        print(Color.BOLD + " ".join(map(str, args)) + Color.END, **kwargs)

    @staticmethod
    def printgreen(*args, **kwargs):
        print(Color.GREEN + " ".join(map(str, args)) + Color.END, **kwargs)

    @staticmethod
    def printred(*args, **kwargs):
        print(Color.RED + " ".join(map(str, args)) + Color.END, **kwargs)
