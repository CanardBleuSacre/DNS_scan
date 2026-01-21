import sys
from rich.tree import Tree
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn

from config import console
from explorer import explore

def main():
    if len(sys.argv) < 2:
        console.print("[bold red]Erreur:[/bold red] Nom de domaine manquant.")
        console.print("[bold yellow]Usage:[/bold yellow] python scan.py [domain] [depth]")
        exit(1)

    start_domain = sys.argv[1].rstrip(".")
    
    if not start_domain or "." not in start_domain:
        console.print(f"[bold red]Erreur:[/bold red] '{start_domain}' n'est pas un domaine valide")
        exit(1)
    try:
        max_depth = int(sys.argv[2]) if len(sys.argv) > 2 else 2
        if max_depth < 1:
            console.print(f"[bold red]Erreur:[/bold red] La profondeur ne peut pas être négative.")
            exit(1)
    except ValueError:
        console.print(f"[bold red]Erreur:[/bold red] La profondeur doit être un nombre entier.")
        exit(1)

    root = Tree(f"[bold red]{start_domain}[/bold red]")
    with Progress(
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TextColumn("[bold]{task.completed}[/bold] domaines explorés"),
        TimeElapsedColumn()
    ) as progress:
        task = progress.add_task("Initialisation...", total=None)
        explore(start_domain, root, depth=0, max_depth=max_depth, progress=progress, task=task)
    console.print(root)

if __name__ == "__main__":
    main()