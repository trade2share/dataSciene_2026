import pandas as pd
import numpy as np
from collections import defaultdict, Counter
from itertools import combinations

class FPNode:
    """Knoten für den FP-Tree"""
    def __init__(self, item, count, parent):
        self.item = item
        self.count = count
        self.parent = parent
        self.children = {}
        self.node_link = None  # Verlinkung zu nächstem Knoten mit gleichem Item

class FPTree:
    """FP-Tree Struktur"""
    def __init__(self):
        self.root = FPNode(None, 0, None)
        self.header_table = {}  # item -> erster Knoten mit diesem Item
        
    def add_transaction(self, transaction, count=1):
        """Fügt eine Transaktion zum FP-Tree hinzu"""
        current = self.root
        
        for item in transaction:
            if item in current.children:
                current.children[item].count += count
            else:
                new_node = FPNode(item, count, current)
                current.children[item] = new_node
                
                # Header Table aktualisieren
                if item not in self.header_table:
                    self.header_table[item] = new_node
                else:
                    # Zur letzten Node mit diesem Item verlinken
                    node = self.header_table[item]
                    while node.node_link is not None:
                        node = node.node_link
                    node.node_link = new_node
            
            current = current.children[item]
    
    def get_paths(self, item):
        """Gibt alle Pfade vom Root zu Knoten mit gegebenem Item zurück"""
        paths = []
        node = self.header_table.get(item)
        
        while node is not None:
            path = []
            path_count = node.count
            current = node.parent
            
            while current.item is not None:
                path.append(current.item)
                current = current.parent
            
            if path:
                paths.append((path, path_count))
            
            node = node.node_link
        
        return paths

class FPGrowth:
    """FP-Growth Algorithmus für häufige Itemsets und Assoziationsregeln"""
    
    def __init__(self, min_support=0.01, min_confidence=0.5):
        """
        Args:
            min_support: Minimale Support-Schwelle (0.01 = 1%)
            min_confidence: Minimale Confidence-Schwelle (0.5 = 50%)
        """
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.frequent_itemsets = []
        self.association_rules = []
        
    def _prepare_transactions(self, df):
        """Bereitet Transaktionen aus DataFrame vor"""
        # Gruppiere nach Invoice und sammle alle Items (Description)
        transactions = df.groupby('Invoice')['Description'].apply(list).tolist()
        
        # Entferne NaN-Werte und konvertiere zu Sets für schnelleren Zugriff
        transactions = [[item for item in trans if pd.notna(item)] for trans in transactions]
        
        return transactions
    
    def _get_frequent_items(self, transactions):
        """Findet häufige Items basierend auf min_support"""
        item_counts = Counter()
        total_transactions = len(transactions)
        
        for transaction in transactions:
            for item in set(transaction):  # Set um Duplikate zu vermeiden
                item_counts[item] += 1
        
        min_count = self.min_support * total_transactions
        frequent_items = {item: count for item, count in item_counts.items() 
                         if count >= min_count}
        
        # Sortiere nach Häufigkeit (absteigend)
        sorted_items = sorted(frequent_items.items(), key=lambda x: x[1], reverse=True)
        
        return dict(sorted_items)
    
    def _build_fptree(self, transactions, frequent_items):
        """Baut den FP-Tree auf"""
        # Sortiere Items in jeder Transaktion nach Häufigkeit
        item_order = {item: idx for idx, item in enumerate(frequent_items.keys())}
        
        tree = FPTree()
        
        for transaction in transactions:
            # Filtere nur häufige Items und sortiere
            filtered = [item for item in transaction if item in frequent_items]
            filtered.sort(key=lambda x: item_order[x])
            
            if filtered:
                tree.add_transaction(filtered)
        
        return tree
    
    def _mine_fptree(self, tree, prefix, frequent_items, min_count):
        """Mine häufige Itemsets rekursiv aus dem FP-Tree"""
        # Sortiere Items nach Häufigkeit
        sorted_items = sorted(frequent_items.items(), key=lambda x: x[1])
        
        for item, count in sorted_items:
            new_prefix = prefix + [item]
            support = count / self.total_transactions
            self.frequent_itemsets.append((frozenset(new_prefix), support))
            
            # Erstelle Conditional Pattern Base
            paths = tree.get_paths(item)
            
            if paths:
                # Erstelle Conditional FP-Tree
                conditional_transactions = []
                for path, path_count in paths:
                    conditional_transactions.extend([path] * path_count)
                
                # Zähle Items im Conditional Tree
                conditional_counts = Counter()
                for path in conditional_transactions:
                    for path_item in set(path):
                        conditional_counts[path_item] += 1
                
                # Filtere nach min_count
                conditional_frequent = {item: count for item, count in conditional_counts.items() 
                                      if count >= min_count}
                
                if conditional_frequent:
                    conditional_tree = self._build_fptree(conditional_transactions, conditional_frequent)
                    self._mine_fptree(conditional_tree, new_prefix, conditional_frequent, min_count)
    
    def fit(self, df):
        """Trainiert das Modell auf den Daten"""
        print("Bereite Transaktionen vor...")
        transactions = self._prepare_transactions(df)
        self.total_transactions = len(transactions)
        print(f"Anzahl Transaktionen: {self.total_transactions}")
        
        min_count = self.min_support * self.total_transactions
        print(f"Minimale Support-Anzahl: {min_count:.0f}")
        
        print("Finde häufige Items...")
        frequent_items = self._get_frequent_items(transactions)
        print(f"Anzahl häufiger Items: {len(frequent_items)}")
        
        print("Baue FP-Tree auf...")
        tree = self._build_fptree(transactions, frequent_items)
        
        print("Mine häufige Itemsets...")
        self.frequent_itemsets = []
        self._mine_fptree(tree, [], frequent_items, min_count)
        print(f"Gefundene häufige Itemsets: {len(self.frequent_itemsets)}")
        
        print("Generiere Assoziationsregeln...")
        self._generate_rules()
        print(f"Generierte Assoziationsregeln: {len(self.association_rules)}")
    
    def _get_support(self, itemset):
        """Berechnet Support für ein Itemset"""
        for itemset_frozen, support in self.frequent_itemsets:
            if itemset_frozen == itemset:
                return support
        return 0.0
    
    def _generate_rules(self):
        """Generiert Assoziationsregeln aus häufigen Itemsets"""
        self.association_rules = []
        
        # Erstelle Dictionary für schnellen Support-Zugriff
        support_dict = {itemset: support for itemset, support in self.frequent_itemsets}
        
        for itemset, support in self.frequent_itemsets:
            if len(itemset) < 2:
                continue
            
            # Generiere alle möglichen Regeln
            itemset_list = list(itemset)
            for i in range(1, len(itemset_list)):
                for antecedent in combinations(itemset_list, i):
                    antecedent = frozenset(antecedent)
                    consequent = itemset - antecedent
                    
                    if len(consequent) == 0:
                        continue
                    
                    # Berechne Confidence
                    antecedent_support = support_dict.get(antecedent, 0.0)
                    if antecedent_support == 0:
                        continue
                    
                    confidence = support / antecedent_support
                    
                    if confidence >= self.min_confidence:
                        # Berechne Lift
                        consequent_support = support_dict.get(consequent, 0.0)
                        if consequent_support == 0:
                            lift = 0.0
                        else:
                            lift = confidence / consequent_support
                        
                        # Berechne Conviction
                        if confidence == 1.0:
                            conviction = float('inf')
                        else:
                            conviction = (1 - consequent_support) / (1 - confidence)
                        
                        self.association_rules.append({
                            'antecedent': set(antecedent),
                            'consequent': set(consequent),
                            'support': support,
                            'confidence': confidence,
                            'lift': lift,
                            'conviction': conviction
                        })
        
        # Sortiere nach Confidence (absteigend)
        self.association_rules.sort(key=lambda x: x['confidence'], reverse=True)
    
    def get_rules(self, top_n=None):
        """Gibt Assoziationsregeln zurück"""
        if top_n:
            return self.association_rules[:top_n]
        return self.association_rules
    
    def print_rules(self, top_n=20):
        """Druckt die Top-N Assoziationsregeln"""
        print(f"\n{'='*80}")
        print(f"TOP {min(top_n, len(self.association_rules))} ASSOZIATIONSREGELN")
        print(f"{'='*80}\n")
        
        for i, rule in enumerate(self.association_rules[:top_n], 1):
            antecedent = ', '.join(list(rule['antecedent'])[:3])
            if len(rule['antecedent']) > 3:
                antecedent += f" (+{len(rule['antecedent'])-3} weitere)"
            
            consequent = ', '.join(list(rule['consequent'])[:3])
            if len(rule['consequent']) > 3:
                consequent += f" (+{len(rule['consequent'])-3} weitere)"
            
            print(f"Regel {i}:")
            print(f"  Wenn gekauft: {antecedent}")
            print(f"  Dann wird auch gekauft: {consequent}")
            print(f"  Support: {rule['support']:.4f} ({rule['support']*100:.2f}%)")
            print(f"  Confidence: {rule['confidence']:.4f} ({rule['confidence']*100:.2f}%)")
            print(f"  Lift: {rule['lift']:.4f}")
            conviction_str = '∞' if rule['conviction'] == float('inf') else f"{rule['conviction']:.4f}"
            print(f"  Conviction: {conviction_str}")
            print()

# Hauptprogramm
if __name__ == "__main__":
    # Daten einlesen
    print("Lade Daten...")
    df = pd.read_csv('online_retail_II_cutdown.csv')

    print(f"\nDaten-Info:")
    print(f"Anzahl Zeilen: {len(df):,}")
    print(f"Anzahl eindeutige Rechnungen: {df['Invoice'].nunique():,}")
    print(f"Anzahl eindeutige Produkte: {df['Description'].nunique():,}")
    
    # FP-Growth Algorithmus initialisieren
    # min_support: 0.01 = 1% der Transaktionen
    # min_confidence: 0.5 = 50% Confidence
    fpgrowth = FPGrowth(min_support=0.01, min_confidence=0.5)
    
    # Modell trainieren
    fpgrowth.fit(df)
    
    # Regeln ausgeben
    fpgrowth.print_rules(top_n=20)
    
    # Regeln als DataFrame speichern (optional)
    rules_df = pd.DataFrame(fpgrowth.get_rules())
    if len(rules_df) > 0:
        rules_df['antecedent'] = rules_df['antecedent'].apply(lambda x: ', '.join(list(x)[:5]))
        rules_df['consequent'] = rules_df['consequent'].apply(lambda x: ', '.join(list(x)[:5]))
        print(f"\nAlle Regeln wurden in 'association_rules.csv' gespeichert.")
        rules_df.to_csv('association_rules.csv', index=False)
