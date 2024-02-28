class colors:
    SUCCESS = "\033[92m"  # green
    INFO = "\033[94m"  # blue
    WARNING = "\033[93m"  # yellow
    DANGER = "\033[91m"  # red
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

ignored_domains = [
    # r"@mail.com\b",
]
