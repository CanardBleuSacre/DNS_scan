from datetime import datetime

def save_markdown(domain, tree, filename):
    '''
    Sauvegarde l'arbre de découverte DNS au format Markdown.
    '''
    lines = []
    
    lines.append(f"# 🌐 Rapport de cartographie DNS :  {domain}")
    lines.append(f"\n**Date** : {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}\n")
    lines.append("---\n")
    
    def parcourir_arbre(tree_node, niveau=0):
        '''Parcourt l'arbre et génère le Markdown'''
        label = str(tree_node.label)
        tags_a_retirer = [
            '[bold red]', '[/bold red]', 
            '[cyan]', '[/cyan]',
            '[green]', '[/green]', 
            '[yellow]', '[/yellow]',
            '[blue]', '[/blue]', 
            '[purple]', '[/purple]',
            '[white]', '[/white]', 
            '[magenta]', '[/magenta]',
            '[red]', '[/red]',
            '[bold]', '[/bold]'
        ]
        
        for tag in tags_a_retirer:
            label = label.replace(tag, '')
        
        indent = "  " * niveau
        
        if "→" in label:
            lines.append(f"{indent}- 🔗 {label}")
        elif any(char. isdigit() for char in label) and "." in label: 
            lines.append(f"{indent}- 📍 `{label}`")
        elif label in ["A", "AAAA", "MX", "TXT", "CNAME", "SOA"]:
            lines. append(f"{indent}- **{label}**")
        elif "aucune donnée" in label:
            lines.append(f"{indent}- ❌ {label}")
        else:
            lines.append(f"{indent}- 🌐 **{label}**")
        
        if hasattr(tree_node, 'children'):
            for child in tree_node.children:
                parcourir_arbre(child, niveau + 1)
    
    lines.append("## 📊 Arbre de découverte\n")
    parcourir_arbre(tree)
    
    lines.append("\n---\n")
    lines.append("## 📈 Statistiques\n")
    
    contenu_complet = '\n'.join(lines)
    nb_domaines = contenu_complet.count('🌐')
    nb_ips = contenu_complet. count('📍')
    nb_relations = contenu_complet.count('🔗')
    
    lines.append(f"- **Domaines découverts** : {nb_domaines}")
    lines.append(f"- **Adresses IP découvertes** : {nb_ips}")
    lines.append(f"- **Relations découvertes** : {nb_relations}")
    
    lines.append("\n---\n")
    lines.append("*Rapport généré par DNS_scan*")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"\nRapport Markdown créé : {filename}")
    print(f"Ouvrez-le avec n'importe quel éditeur de texte ou visualiseur Markdown")