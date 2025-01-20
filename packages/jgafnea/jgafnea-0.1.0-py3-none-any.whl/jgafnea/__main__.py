from rich.console import Console
from rich.panel import Panel


def main() -> None:
    console = Console()

    content = """
Hi, I'm John. 👋

📬 jgafnea@gmail.com
"""

    # Display the panel with content
    console.print(Panel(content, title="jgafnea", border_style="cyan", expand=False))

if __name__ == '__main__':
    main()
