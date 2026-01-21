import argparse
import sys
from rich.tree import Tree
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn

from config import console
from explorer import explore

def main():
    '''
    Point d'entrée principal pour l'outil de cartographie DNS.
    '''
    parser = argparse.ArgumentParser(
        description="Outil de cartographie DNS écrit en Python",
        epilog="Exemple : python scan.py oracle.com 1"
    )
    parser.add_argument(
        "domain", 
        help="Nom de domaine à scanner"
    )
    parser.add_argument(
        "depth", 
        type=int, 
        nargs="?", 
        default=2, 
        help="Profondeur de récursion (défaut: 2)"
    )
    parser.add_argument(
        "--version", 
        action="version", 
        version="DNS_scan 1.0"
    )
    args = parser.parse_args()
    start_domain = args.domain.rstrip(".")
    
    if not start_domain or "." not in start_domain:
        console.print(f"[bold red]Erreur:[/bold red] '{start_domain}' n'est pas un domaine valide")
        sys.exit(1)

    max_depth = args.depth
    if max_depth < 1:
        console.print(f"[bold red]Erreur:[/bold red] La profondeur ne peut pas être négative.")
        sys.exit(1)

    root = Tree(f"[bold red]{start_domain}[/bold red]")
    with Progress(
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TextColumn("[bold]{task.completed}[/bold] domaines explorés"),
        TimeElapsedColumn()
    ) as progress:
        task = progress.add_task("Initialisation.. .", total=None)
        explore(start_domain, root, depth=0, max_depth=max_depth, progress=progress, task=task)
    console.print(root)

if __name__ == "__main__": 
    main()