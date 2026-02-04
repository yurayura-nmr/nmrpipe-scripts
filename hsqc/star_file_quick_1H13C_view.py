import re
import sys
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

def parse_star_file(filename):
    """
    Parse the STAR NMR assignment file and extract relevant information.
    """
    assignments = {
        'H': [],    # List of (residue, atom, shift)
        'C': []     # List of (residue, atom, shift)
    }
    
    proton_atoms = defaultdict(list)
    carbon_atoms = defaultdict(list)
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
                
            # Split by whitespace
            parts = line.split()
            
            if len(parts) < 11:
                continue
                
            try:
                # The format appears to have fixed columns
                # Index the parts based on the structure
                atom_name = parts[7]  # Atom name
                element = parts[8]    # Element symbol
                isotope = parts[9]    # Isotope number
                chemical_shift = parts[10]  # Chemical shift
                residue_name = parts[6]  # Residue name
                residue_num = parts[4]  # Residue number (5th field)
                
                # Convert chemical shift to float if possible
                try:
                    shift = float(chemical_shift)
                except ValueError:
                    continue
                    
                # Create a unique identifier for the atom
                atom_id = f"{residue_num}:{residue_name}:{atom_name}"
                
                if element == 'H' and isotope == '1':
                    assignments['H'].append({
                        'id': atom_id,
                        'residue': f"{residue_num}:{residue_name}",
                        'atom': atom_name,
                        'shift': shift
                    })
                    proton_atoms[residue_num].append((atom_name, shift))
                    
                elif element == 'C' and isotope == '13':
                    assignments['C'].append({
                        'id': atom_id,
                        'residue': f"{residue_num}:{residue_name}",
                        'atom': atom_name,
                        'shift': shift
                    })
                    carbon_atoms[residue_num].append((atom_name, shift))
                    
            except (IndexError, ValueError) as e:
                continue
    
    return assignments, proton_atoms, carbon_atoms

def pair_hsqc_peaks(proton_atoms, carbon_atoms):
    """
    Pair protons with their directly attached carbons for HSQC.
    Improved pairing logic based on atom naming conventions.
    """
    hsqc_pairs = []
    
    for residue in set(list(proton_atoms.keys()) + list(carbon_atoms.keys())):
        if residue not in proton_atoms or residue not in carbon_atoms:
            continue
            
        protons = proton_atoms[residue]
        carbons = carbon_atoms[residue]
        
        # Create dictionaries for easier lookup
        proton_dict = {atom[0]: atom[1] for atom in protons}
        carbon_dict = {atom[0]: atom[1] for atom in carbons}
        
        # Define common pairings based on standard protein atom names
        # Standard pairs: HA-CA, HB-CB, HG-CG, HD-CD, HE-CE, etc.
        # But note: protons might have numbers (HB2, HB3) while carbons don't
        
        # Create a mapping from carbon atom to possible proton atoms
        carbon_to_proton_map = {
            'CA': ['HA', 'HA2', 'HA3'],
            'CB': ['HB', 'HB2', 'HB3', 'HB1'],
            'CG': ['HG', 'HG2', 'HG3', 'HG1'],
            'CG1': ['HG11', 'HG12', 'HG13', 'HG1'],
            'CG2': ['HG21', 'HG22', 'HG23', 'HG2'],
            'CD': ['HD', 'HD2', 'HD3', 'HD1'],
            'CD1': ['HD11', 'HD12', 'HD13', 'HD1'],
            'CD2': ['HD21', 'HD22', 'HD23', 'HD2'],
            'CE': ['HE', 'HE2', 'HE3', 'HE1'],
            'CE1': ['HE1'],
            'CE2': ['HE2'],
            'CZ': ['HZ'],
            'N': ['HN', 'H'],  # Not for HSQC but for reference
        }
        
        # Special handling for different residue types
        special_pairs = {
            'ALA': {'CB': ['HB1', 'HB2', 'HB3']},
            'VAL': {'CG1': ['HG11', 'HG12', 'HG13'], 'CG2': ['HG21', 'HG22', 'HG23']},
            'ILE': {'CG1': ['HG12'], 'CG2': ['HG21', 'HG22', 'HG23'], 'CD1': ['HD11', 'HD12', 'HD13']},
            'LEU': {'CD1': ['HD11', 'HD12', 'HD13'], 'CD2': ['HD21', 'HD22', 'HD23']},
            'THR': {'CG2': ['HG21', 'HG22', 'HG23']},
            'SER': {'CB': ['HB2', 'HB3']},
            'ASN': {'CB': ['HB2', 'HB3']},
            'GLN': {'CB': ['HB2', 'HB3']},
            'ASP': {'CB': ['HB2', 'HB3']},
            'GLU': {'CB': ['HB2', 'HB3']},
            'LYS': {'CB': ['HB2', 'HB3'], 'CG': ['HG2'], 'CD': ['HD2'], 'CE': ['HE2']},
            'ARG': {'CB': ['HB2', 'HB3'], 'CG': ['HG2'], 'CD': ['HD2']},
            'PHE': {'CD1': ['HD1'], 'CE1': ['HE1']},
            'TYR': {'CD1': ['HD1'], 'CE1': ['HE1']},
            'HIS': {'CD2': ['HD2'], 'CE1': ['HE1']},
            'TRP': {'CD1': ['HD1'], 'NE1': ['HE1']},
            'MET': {'CE': ['HE1', 'HE2', 'HE3']},
            'PRO': {'CB': ['HB2', 'HB3'], 'CG': ['HG2'], 'CD': ['HD2']},
        }
        
        # Try to pair each carbon with appropriate protons
        for carbon_name, carbon_shift in carbons:
            # Get possible proton names for this carbon
            possible_protons = []
            
            # Check standard mapping first
            if carbon_name in carbon_to_proton_map:
                possible_protons.extend(carbon_to_proton_map[carbon_name])
            
            # Look for any proton that starts with the same base name
            # (e.g., CB pairs with HB, HB2, HB3, etc.)
            base_carbon = carbon_name[1:] if carbon_name.startswith('C') else carbon_name
            base_proton = 'H' + base_carbon
            
            # Add variations
            for proton_name, proton_shift in protons:
                if proton_name.startswith(base_proton):
                    possible_protons.append(proton_name)
            
            # Remove duplicates
            possible_protons = list(set(possible_protons))
            
            # Try to find matches
            for proton_name in possible_protons:
                if proton_name in proton_dict:
                    hsqc_pairs.append({
                        'residue': residue,
                        'proton_atom': proton_name,
                        'carbon_atom': carbon_name,
                        'proton_shift': proton_dict[proton_name],
                        'carbon_shift': carbon_shift
                    })
                    # Found a match, break to avoid multiple matches for same carbon
                    break
    
    return hsqc_pairs

def plot_hsqc_spectrum(hsqc_pairs, output_file='hsqc_simulation.png'):
    """
    Plot the HSQC spectrum.
    """
    if not hsqc_pairs:
        print("No HSQC pairs found!")
        return None, None
    
    # Extract shifts
    proton_shifts = [p['proton_shift'] for p in hsqc_pairs]
    carbon_shifts = [p['carbon_shift'] for p in hsqc_pairs]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Create a colormap based on carbon shift regions
    colors = []
    for c_shift in carbon_shifts:
        if c_shift < 30:
            colors.append('blue')  # Aliphatic
        elif c_shift < 60:
            colors.append('green')  # Alpha carbons
        elif c_shift < 110:
            colors.append('orange')  # Aromatic/other
        else:
            colors.append('red')  # Aromatic/backbone carbonyl
    
    # Plot points with different colors
    scatter = ax.scatter(proton_shifts, carbon_shifts, alpha=0.7, s=40, 
                        c=colors, edgecolors='black', linewidths=0.5)
    
    # Add labels for selected points (every 10th point)
    labeled_count = 0
    for i, pair in enumerate(hsqc_pairs):
        # Label every 10th point to avoid overcrowding
        if i % 10 == 0 and labeled_count < 30:
            label = f"{pair['residue']}:{pair['proton_atom']}"
            ax.annotate(label, 
                       (pair['proton_shift'], pair['carbon_shift']),
                       fontsize=6, alpha=0.8,
                       xytext=(5, 5), textcoords='offset points')
            labeled_count += 1
    
    # Set axis limits (typical NMR ranges)
    ax.set_xlim(0, 10)  # 1H typically 0-10 ppm
    ax.set_ylim(0, 200)  # 13C typically 0-200 ppm
    
    # Invert axes (NMR convention)
    ax.invert_xaxis()
    ax.invert_yaxis()
    
    # Add labels and title
    ax.set_xlabel('¹H Chemical Shift (ppm)', fontsize=12)
    ax.set_ylabel('¹³C Chemical Shift (ppm)', fontsize=12)
    ax.set_title('Simulated 1H-13C HSQC Spectrum', fontsize=14, fontweight='bold')
    
    # Add grid
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Add legend for colors
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='blue', edgecolor='black', label='Aliphatic (< 30 ppm)'),
        Patch(facecolor='green', edgecolor='black', label='α-Carbons (30-60 ppm)'),
        Patch(facecolor='orange', edgecolor='black', label='Aromatic/Other (60-110 ppm)'),
        Patch(facecolor='red', edgecolor='black', label='Aromatic/Carbonyl (> 110 ppm)')
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=9)
    
    # Add statistics
    stats_text = f'Total peaks: {len(hsqc_pairs)}\n'
    stats_text += f'1H range: {min(proton_shifts):.1f}-{max(proton_shifts):.1f} ppm\n'
    stats_text += f'13C range: {min(carbon_shifts):.1f}-{max(carbon_shifts):.1f} ppm'
    
    ax.text(0.02, 0.02, stats_text, 
            transform=ax.transAxes, fontsize=9,
            verticalalignment='bottom',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    
    # Save figure
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"HSQC spectrum saved as {output_file}")
    
    # Show plot
    plt.show()
    
    return fig, ax

def generate_hsqc_table(hsqc_pairs, output_file='hsqc_peaks.txt'):
    """
    Generate a table of HSQC peaks.
    """
    with open(output_file, 'w') as f:
        f.write("HSQC Peak List\n")
        f.write("=" * 100 + "\n")
        f.write(f"{'Residue':<12} {'Proton':<10} {'Carbon':<10} {'1H (ppm)':<12} {'13C (ppm)':<12} {'Region':<15}\n")
        f.write("-" * 100 + "\n")
        
        # Sort by carbon shift
        sorted_pairs = sorted(hsqc_pairs, key=lambda x: x['carbon_shift'])
        
        for pair in sorted_pairs:
            # Determine region
            c_shift = pair['carbon_shift']
            if c_shift < 30:
                region = "Aliphatic"
            elif c_shift < 60:
                region = "α-Carbon"
            elif c_shift < 110:
                region = "Aromatic/Other"
            else:
                region = "Aromatic/C=O"
            
            f.write(f"{pair['residue']:<12} "
                   f"{pair['proton_atom']:<10} "
                   f"{pair['carbon_atom']:<10} "
                   f"{pair['proton_shift']:<12.3f} "
                   f"{pair['carbon_shift']:<12.3f} "
                   f"{region:<15}\n")
        
        f.write("=" * 100 + "\n")
        f.write(f"Total peaks: {len(hsqc_pairs)}\n")
    
    print(f"HSQC peak table saved as {output_file}")

def print_summary(hsqc_pairs, proton_atoms, carbon_atoms):
    """
    Print a summary of the parsed data.
    """
    print("\n" + "="*60)
    print("DATA SUMMARY")
    print("="*60)
    
    # Count unique residues
    unique_residues = set(proton_atoms.keys()).union(set(carbon_atoms.keys()))
    
    print(f"Unique residues: {len(unique_residues)}")
    print(f"Total proton assignments: {sum(len(v) for v in proton_atoms.values())}")
    print(f"Total carbon-13 assignments: {sum(len(v) for v in carbon_atoms.values())}")
    print(f"HSQC cross-peaks identified: {len(hsqc_pairs)}")
    
    if hsqc_pairs:
        # Group by residue
        residues_with_pairs = set(p['residue'] for p in hsqc_pairs)
        print(f"Residues with HSQC pairs: {len(residues_with_pairs)}")
        
        # Show example pairs by region
        print("\nExample HSQC peaks by region:")
        aliphatic = [p for p in hsqc_pairs if p['carbon_shift'] < 30]
        alpha_carbon = [p for p in hsqc_pairs if 30 <= p['carbon_shift'] < 60]
        other = [p for p in hsqc_pairs if 60 <= p['carbon_shift'] < 110]
        aromatic = [p for p in hsqc_pairs if p['carbon_shift'] >= 110]
        
        print(f"  Aliphatic (<30 ppm): {len(aliphatic)} peaks")
        if aliphatic:
            for p in aliphatic[:3]:
                print(f"    {p['residue']} {p['proton_atom']}-{p['carbon_atom']}: "
                      f"1H={p['proton_shift']:.2f}, 13C={p['carbon_shift']:.2f}")
        
        print(f"  α-Carbons (30-60 ppm): {len(alpha_carbon)} peaks")
        if alpha_carbon:
            for p in alpha_carbon[:3]:
                print(f"    {p['residue']} {p['proton_atom']}-{p['carbon_atom']}: "
                      f"1H={p['proton_shift']:.2f}, 13C={p['carbon_shift']:.2f}")
        
        print(f"  Other (60-110 ppm): {len(other)} peaks")
        if other:
            for p in other[:3]:
                print(f"    {p['residue']} {p['proton_atom']}-{p['carbon_atom']}: "
                      f"1H={p['proton_shift']:.2f}, 13C={p['carbon_shift']:.2f}")
        
        print(f"  Aromatic/Carbonyl (≥110 ppm): {len(aromatic)} peaks")
        if aromatic:
            for p in aromatic[:3]:
                print(f"    {p['residue']} {p['proton_atom']}-{p['carbon_atom']}: "
                      f"1H={p['proton_shift']:.2f}, 13C={p['carbon_shift']:.2f}")

def main():
    # Get input filename
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = input("Enter the STAR NMR assignment filename: ")
    
    try:
        # Parse the file
        print(f"Parsing {filename}...")
        assignments, proton_atoms, carbon_atoms = parse_star_file(filename)
        
        print(f"\nParsing complete:")
        print(f"  Found {sum(len(v) for v in proton_atoms.values())} proton assignments")
        print(f"  Found {sum(len(v) for v in carbon_atoms.values())} carbon-13 assignments")
        
        # Pair protons and carbons for HSQC
        print("\nPairing protons with carbons for HSQC...")
        hsqc_pairs = pair_hsqc_peaks(proton_atoms, carbon_atoms)
        
        if not hsqc_pairs:
            print("No HSQC pairs could be identified.")
            print("This could be due to:")
            print("  1. Atom naming mismatch between protons and carbons")
            print("  2. Different residue numbering in proton and carbon lists")
            print("  3. Missing carbon assignments for protonated positions")
            return
        
        print(f"Identified {len(hsqc_pairs)} potential HSQC cross-peaks")
        
        # Print summary
        print_summary(hsqc_pairs, proton_atoms, carbon_atoms)
        
        # Generate output files
        generate_hsqc_table(hsqc_pairs)
        
        # Create and display the simulated spectrum
        plot_hsqc_spectrum(hsqc_pairs)
        
        # Ask if user wants to see raw data
        response = input("\nWould you like to see raw atom lists for a specific residue? (y/n): ")
        if response.lower() == 'y':
            residue_num = input("Enter residue number: ")
            if residue_num in proton_atoms:
                print(f"\nProtons in residue {residue_num}:")
                for atom, shift in proton_atoms[residue_num]:
                    print(f"  {atom}: {shift:.3f} ppm")
            if residue_num in carbon_atoms:
                print(f"\nCarbons in residue {residue_num}:")
                for atom, shift in carbon_atoms[residue_num]:
                    print(f"  {atom}: {shift:.3f} ppm")
            
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found!")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
