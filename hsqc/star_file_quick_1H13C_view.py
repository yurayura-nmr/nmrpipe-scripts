import re
import sys
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from matplotlib.patches import Rectangle

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
        
        # Try to pair each carbon with appropriate protons
        for carbon_name, carbon_shift in carbons:
            # Skip carbonyl carbons (backbone C) as they don't have attached protons
            if carbon_name == 'C':
                continue
            
            # Look for proton with similar base name
            base_name = carbon_name
            if base_name.startswith('C'):
                base_name = base_name[1:]  # Remove C prefix
            
            # Possible proton names to check
            possible_names = []
            
            # Check for exact match (e.g., CA -> HA)
            possible_names.append('H' + base_name)
            
            # Check for numbered protons (e.g., CB -> HB2, HB3)
            for proton_name in proton_dict.keys():
                if proton_name.startswith('H' + base_name):
                    possible_names.append(proton_name)
            
            # Remove duplicates
            possible_names = list(set(possible_names))
            
            # Try to find matches
            for proton_name in possible_names:
                if proton_name in proton_dict:
                    hsqc_pairs.append({
                        'residue': residue,
                        'residue_num': int(residue) if residue.isdigit() else 0,
                        'proton_atom': proton_name,
                        'carbon_atom': carbon_name,
                        'proton_shift': proton_dict[proton_name],
                        'carbon_shift': carbon_shift
                    })
                    # Found a match, break to avoid multiple matches for same carbon
                    break
    
    return hsqc_pairs

def plot_hsqc_spectrum(hsqc_pairs, label_option='all', output_file='hsqc_simulation.png', figsize=(16, 12)):
    """
    Plot the HSQC spectrum with customizable labeling options.
    
    Parameters:
    -----------
    label_option : str
        'none' - no labels
        'some' - label selected peaks (every 5th, less crowded)
        'all' - label all peaks
        'region' - label only peaks in specific regions
        'residues' - label only selected residues
    """
    if not hsqc_pairs:
        print("No HSQC pairs found!")
        return None, None
    
    # Extract shifts
    proton_shifts = [p['proton_shift'] for p in hsqc_pairs]
    carbon_shifts = [p['carbon_shift'] for p in hsqc_pairs]
    
    # Create figure
    fig, ax = plt.subplots(figsize=figsize)
    
    # Create a colormap based on carbon shift regions
    colors = []
    regions = []
    for c_shift in carbon_shifts:
        if c_shift < 30:
            colors.append('blue')
            regions.append('Aliphatic')
        elif c_shift < 60:
            colors.append('green')
            regions.append('α-Carbon')
        elif c_shift < 110:
            colors.append('orange')
            regions.append('Aromatic/Other')
        else:
            colors.append('red')
            regions.append('Aromatic/C=O')
    
    # Plot points with different colors
    scatter = ax.scatter(proton_shifts, carbon_shifts, alpha=0.7, s=50, 
                        c=colors, edgecolors='black', linewidths=0.5)
    
    # Label peaks based on option
    if label_option != 'none':
        label_all_peaks(ax, hsqc_pairs, regions, label_option)
    
    # Set axis limits (typical NMR ranges)
    ax.set_xlim(0, 10)  # 1H typically 0-10 ppm
    ax.set_ylim(0, 200)  # 13C typically 0-200 ppm
    
    # Invert axes (NMR convention)
    ax.invert_xaxis()
    ax.invert_yaxis()
    
    # Add labels and title
    ax.set_xlabel('¹H Chemical Shift (ppm)', fontsize=12)
    ax.set_ylabel('¹³C Chemical Shift (ppm)', fontsize=12)
    ax.set_title(f'Simulated 1H-13C HSQC Spectrum ({label_option} labels)', fontsize=14, fontweight='bold')
    
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
    stats_text += f'13C range: {min(carbon_shifts):.1f}-{max(carbon_shifts):.1f} ppm\n'
    stats_text += f'Labeling: {label_option}'
    
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

def label_all_peaks(ax, hsqc_pairs, regions, label_option='all'):
    """
    Label peaks based on the selected option.
    """
    fontsize = 6
    alpha = 0.7
    
    if label_option == 'all':
        # Label every peak
        for i, (pair, region) in enumerate(zip(hsqc_pairs, regions)):
            label = f"{pair['residue_num']}:{pair['proton_atom']}"
            ax.annotate(label, 
                       (pair['proton_shift'], pair['carbon_shift']),
                       fontsize=fontsize, alpha=alpha,
                       xytext=(2, 2), textcoords='offset points',
                       ha='left', va='bottom')
    
    elif label_option == 'some':
        # Label every 5th peak and important ones
        for i, (pair, region) in enumerate(zip(hsqc_pairs, regions)):
            # Label backbone HA-CA peaks (important)
            if pair['proton_atom'] == 'HA' and pair['carbon_atom'] == 'CA':
                label = f"{pair['residue_num']}:HA"
                ax.annotate(label, 
                           (pair['proton_shift'], pair['carbon_shift']),
                           fontsize=fontsize+1, alpha=0.9, color='darkgreen',
                           xytext=(3, 3), textcoords='offset points',
                           ha='left', va='bottom')
            # Label every 5th peak
            elif i % 5 == 0:
                label = f"{pair['residue_num']}:{pair['proton_atom']}"
                ax.annotate(label, 
                           (pair['proton_shift'], pair['carbon_shift']),
                           fontsize=fontsize, alpha=alpha,
                           xytext=(2, 2), textcoords='offset points',
                           ha='left', va='bottom')
    
    elif label_option == 'region':
        # Label only peaks in specific regions
        for i, (pair, region) in enumerate(zip(hsqc_pairs, regions)):
            # Label only alpha-carbons and aromatic regions
            if region in ['α-Carbon', 'Aromatic/C=O']:
                label = f"{pair['residue_num']}:{pair['proton_atom']}"
                ax.annotate(label, 
                           (pair['proton_shift'], pair['carbon_shift']),
                           fontsize=fontsize, alpha=alpha,
                           xytext=(2, 2), textcoords='offset points',
                           ha='left', va='bottom')
    
    elif label_option == 'residues':
        # Label only specific residues (first, last, and every 10th)
        for i, (pair, region) in enumerate(zip(hsqc_pairs, regions)):
            res_num = pair['residue_num']
            # Label first residue, last residue, and every 10th residue
            if res_num == 1 or res_num == max(p['residue_num'] for p in hsqc_pairs) or res_num % 10 == 0:
                label = f"{pair['residue_num']}:{pair['proton_atom']}"
                ax.annotate(label, 
                           (pair['proton_shift'], pair['carbon_shift']),
                           fontsize=fontsize, alpha=alpha,
                           xytext=(2, 2), textcoords='offset points',
                           ha='left', va='bottom')

def plot_hsqc_with_zoom(hsqc_pairs, label_option='all'):
    """
    Create a figure with both full spectrum and zoomed regions.
    """
    if not hsqc_pairs:
        print("No HSQC pairs found!")
        return
    
    # Create figure with subplots
    fig = plt.figure(figsize=(18, 12))
    
    # Main HSQC spectrum
    ax1 = plt.subplot2grid((2, 3), (0, 0), colspan=2, rowspan=2)
    plot_on_axes(ax1, hsqc_pairs, label_option, is_main=True)
    
    # Zoom 1: Aliphatic region
    ax2 = plt.subplot2grid((2, 3), (0, 2))
    plot_on_axes(ax2, hsqc_pairs, label_option, 
                 xlim=(0.5, 4.5), ylim=(10, 50), 
                 title="Aliphatic Region (0.5-4.5 ppm 1H, 10-50 ppm 13C)")
    
    # Zoom 2: Aromatic region
    ax3 = plt.subplot2grid((2, 3), (1, 2))
    plot_on_axes(ax3, hsqc_pairs, label_option,
                 xlim=(6.5, 9.5), ylim=(110, 140),
                 title="Aromatic Region (6.5-9.5 ppm 1H, 110-140 ppm 13C)")
    
    plt.tight_layout()
    
    # Save figure
    output_file = f"hsqc_with_zoom_{label_option}_labels.png"
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"HSQC spectrum with zoom saved as {output_file}")
    
    plt.show()
    
    return fig

def plot_on_axes(ax, hsqc_pairs, label_option, is_main=False, xlim=None, ylim=None, title=None):
    """
    Plot HSQC data on a given axes object.
    """
    # Extract shifts
    proton_shifts = [p['proton_shift'] for p in hsqc_pairs]
    carbon_shifts = [p['carbon_shift'] for p in hsqc_pairs]
    
    # Create a colormap based on carbon shift regions
    colors = []
    regions = []
    for c_shift in carbon_shifts:
        if c_shift < 30:
            colors.append('blue')
            regions.append('Aliphatic')
        elif c_shift < 60:
            colors.append('green')
            regions.append('α-Carbon')
        elif c_shift < 110:
            colors.append('orange')
            regions.append('Aromatic/Other')
        else:
            colors.append('red')
            regions.append('Aromatic/C=O')
    
    # Plot points
    scatter = ax.scatter(proton_shifts, carbon_shifts, alpha=0.7, s=40, 
                        c=colors, edgecolors='black', linewidths=0.5)
    
    # Label peaks if it's the main plot or zoomed region
    if label_option != 'none' and not is_main:
        # For zoomed regions, label all peaks
        for i, (pair, region) in enumerate(zip(hsqc_pairs, regions)):
            # Only label if in the zoom region
            if xlim and ylim:
                if (xlim[0] <= pair['proton_shift'] <= xlim[1] and 
                    ylim[0] <= pair['carbon_shift'] <= ylim[1]):
                    label = f"{pair['residue_num']}:{pair['proton_atom']}"
                    ax.annotate(label, 
                               (pair['proton_shift'], pair['carbon_shift']),
                               fontsize=5, alpha=0.8,
                               xytext=(1, 1), textcoords='offset points',
                               ha='left', va='bottom')
    
    # Set axis limits
    if xlim and ylim:
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
    else:
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 200)
    
    # Invert axes
    ax.invert_xaxis()
    ax.invert_yaxis()
    
    # Add labels
    if is_main or not title:
        ax.set_xlabel('¹H Chemical Shift (ppm)', fontsize=10)
        ax.set_ylabel('¹³C Chemical Shift (ppm)', fontsize=10)
        ax.set_title(f'HSQC Spectrum ({label_option} labels)', fontsize=12)
    else:
        ax.set_title(title, fontsize=10)
    
    ax.grid(True, alpha=0.3, linestyle='--')

def generate_hsqc_table(hsqc_pairs, output_file='hsqc_peaks.txt'):
    """
    Generate a table of HSQC peaks.
    """
    with open(output_file, 'w') as f:
        f.write("HSQC Peak List\n")
        f.write("=" * 100 + "\n")
        f.write(f"{'Residue':<12} {'Proton':<10} {'Carbon':<10} {'1H (ppm)':<12} {'13C (ppm)':<12} {'Region':<15}\n")
        f.write("-" * 100 + "\n")
        
        # Sort by residue number
        sorted_pairs = sorted(hsqc_pairs, key=lambda x: x['residue_num'])
        
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
        # Group by region
        aliphatic = [p for p in hsqc_pairs if p['carbon_shift'] < 30]
        alpha_carbon = [p for p in hsqc_pairs if 30 <= p['carbon_shift'] < 60]
        other = [p for p in hsqc_pairs if 60 <= p['carbon_shift'] < 110]
        aromatic = [p for p in hsqc_pairs if p['carbon_shift'] >= 110]
        
        print(f"\nPeak distribution by region:")
        print(f"  Aliphatic (<30 ppm): {len(aliphatic)} peaks ({len(aliphatic)/len(hsqc_pairs)*100:.1f}%)")
        print(f"  α-Carbons (30-60 ppm): {len(alpha_carbon)} peaks ({len(alpha_carbon)/len(hsqc_pairs)*100:.1f}%)")
        print(f"  Other (60-110 ppm): {len(other)} peaks ({len(other)/len(hsqc_pairs)*100:.1f}%)")
        print(f"  Aromatic/Carbonyl (≥110 ppm): {len(aromatic)} peaks ({len(aromatic)/len(hsqc_pairs)*100:.1f}%)")

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
            return
        
        print(f"Identified {len(hsqc_pairs)} potential HSQC cross-peaks")
        
        # Print summary
        print_summary(hsqc_pairs, proton_atoms, carbon_atoms)
        
        # Generate output files
        generate_hsqc_table(hsqc_pairs)
        
        # Ask for labeling option
        print("\nLabeling options:")
        print("  1. none - No labels")
        print("  2. some - Label selected peaks (less crowded)")
        print("  3. all - Label ALL peaks")
        print("  4. region - Label only α-carbons and aromatics")
        print("  5. residues - Label only specific residues")
        
        label_choice = input("\nSelect labeling option (1-5): ").strip()
        
        label_options = {
            '1': 'none',
            '2': 'some', 
            '3': 'all',
            '4': 'region',
            '5': 'residues'
        }
        
        label_option = label_options.get(label_choice, 'some')
        
        # Ask if user wants zoomed regions
        zoom_choice = input("\nCreate additional zoomed regions? (y/n): ").strip().lower()
        
        if zoom_choice == 'y':
            # Create figure with zoomed regions
            plot_hsqc_with_zoom(hsqc_pairs, label_option)
        else:
            # Create standard plot
            plot_hsqc_spectrum(hsqc_pairs, label_option, figsize=(18, 12))
        
        # Show example peaks
        print("\nExample peaks from different regions:")
        print("-" * 70)
        print(f"{'Residue':<10} {'Proton-Carbon':<15} {'1H (ppm)':<10} {'13C (ppm)':<10} {'Region':<15}")
        print("-" * 70)
        
        # Show examples from each region
        for pair in hsqc_pairs[:10]:  # First 10
            c_shift = pair['carbon_shift']
            if c_shift < 30:
                region = "Aliphatic"
            elif c_shift < 60:
                region = "α-Carbon"
            elif c_shift < 110:
                region = "Aromatic/Other"
            else:
                region = "Aromatic/C=O"
            
            print(f"{pair['residue']:<10} "
                  f"{pair['proton_atom']}-{pair['carbon_atom']:<15} "
                  f"{pair['proton_shift']:<10.2f} "
                  f"{pair['carbon_shift']:<10.2f} "
                  f"{region:<15}")
            
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found!")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
