import re
import os
from collections import defaultdict

# --- Configuration ---
OUTPUT_FILENAME = "reading_list.md"

# The raw text data provided by the user
RAW_TEXT_DATA = """
PHYSICS
AC Circuits	E&M (Purcell & Morin): Chapter 8 (Alternating-Current Circuits)
Atomic & Molecular Structure	Not explicitly covered in these tables of contents.
Biot-Savart & Ampere's Laws	E&M (Purcell & Morin): Chapter 6 (The Magnetic Field)
Capacitors & Dielectrics	E&M (Purcell & Morin): Chapter 3 (Electric Fields Around Conductors), Chapter 10 (Electric Fields in Matter)
Electromagnetic Induction & Faraday's Law	E&M (Purcell & Morin): Chapter 7 (Electromagnetic Induction)
Electrostatics & Coulomb's Law	E&M (Purcell & Morin): Chapter 1 (Electrostatics: Charges and Fields)
Fluid Mechanics	Not explicitly covered in these tables of contents.
Gauss's Law	E&M (Purcell & Morin): Chapter 1 (Electrostatics...), Chapter 2 (The Electric Potential)
Geometric & Physical Optics	Not explicitly covered in these tables of contents.
Kinematics & Dynamics	Mechanics (Kleppner & Kolenkow): Chapter 1 (Vectors and Kinematics), Chapter 2 (Newton's Laws), Chapter 3 (Forces and Equations of Motion) <br> Calculus (Stewart): Chapter 13 (Vector Functions)
Kinetic Theory of Gases	Not explicitly covered in these tables of contents.
Magnetic Fields & Lorentz Force	E&M (Purcell & Morin): Chapter 5 (The Fields of Moving Charges), Chapter 6 (The Magnetic Field)
Mechanical Waves & Acoustics	Not explicitly covered in these tables of contents.
Ohm's & Kirchhoff's Laws	E&M (Purcell & Morin): Chapter 4 (Electric Currents)
Oscillations & Rigid Body Motion	Mechanics (Kleppner & Kolenkow): Chapter 6 (Topics in Dynamics), Chapter 7 (Angular Momentum...), Chapter 8 (Rigid Body Motion)
Thermodynamics	Not explicitly covered in these tables of contents.
Work, Energy, & Momentum	Mechanics (Kleppner & Kolenkow): Chapter 4 (Momentum), Chapter 5 (Work and Energy)
MATHEMATICS
Complex Numbers & Polynomials	Calculus (Stewart): Appendix G (Complex Numbers)
Derivatives & Taylor's Formula	Calculus (Stewart): Chapter 11 (Infinite Sequences and Series, specifically 11.10)
Determinants	This specific sub-topic of Linear Algebra is not listed as a chapter title.
Eigenvalues & Eigenvectors	This specific sub-topic of Linear Algebra is not listed as a chapter title.
Green's, Stokes', & Divergence Theorems	Calculus (Stewart): Chapter 16 (Vector Calculus) <br> E&M (Purcell & Morin): Chapter 2 (The Electric Potential, introduces the concepts)
Integrals & Barrow's Formula	Calculus (Stewart): Chapter 15 (Multiple Integrals)
Lagrange Multipliers	Calculus (Stewart): Chapter 14 (Partial Derivatives, specifically 14.8)
Matrices & Linear Equations	This specific sub-topic of Linear Algebra is not listed as a chapter title.
Multiple, Line, & Surface Integrals	Calculus (Stewart): Chapter 15 (Multiple Integrals), Chapter 16 (Vector Calculus)
Numerical & Power Series	Calculus (Stewart): Chapter 11 (Infinite Sequences and Series)
Ordinary Differential Equations	Calculus (Stewart): Chapter 17 (Second-Order Differential Equations)
Quadratic Forms, Conics, & Quadrics	Calculus (Stewart): Chapter 12 (Vectors and the Geometry of Space, specifically 12.6)
Sequences & Limits	Calculus (Stewart): Chapter 11 (Infinite Sequences and Series)
Vector Functions & Calculus	Calculus (Stewart): Chapter 13 (Vector Functions), Chapter 16 (Vector Calculus)
Vector Spaces & Subspaces	This specific sub-topic of Linear Algebra is not listed as a chapter title.
Vectors, Lines, & Planes	Calculus (Stewart): Chapter 12 (Vectors and the Geometry of Space) <br> Mechanics (Kleppner & Kolenkow): Chapter 1 (Vectors and Kinematics)
STATISTICS & PROBABILITY
Discrete & Continuous Distributions	Statistics (Devore): Chapter 3 (Variables aleatorias discretas...), Chapter 4 (Variables aleatorias continuas...)
Hypothesis Testing	Statistics (Devore): Chapter 8 (Pruebas de hipótesis...)
Probability & Bayes' Theorem	Statistics (Devore): Chapter 2 (Probabilidad)
Stochastic Processes	Not explicitly covered in these tables of contents.
"""

def parse_data_and_generate_list(text_data, output_file):
    """
    Parses the raw text data and generates a formatted Markdown file.
    """
    print("Parsing data to generate reading list...")
    
    reading_list = defaultdict(list)
    missing_topics = []
    
    # Book aliases for consistent naming
    book_aliases = {
        "E&M (Purcell & Morin)": "E&M (Purcell & Morin)",
        "Mechanics (Kleppner & Kolenkow)": "Mechanics (Kleppner & Kolenkow)",
        "Calculus (Stewart)": "Calculus (Stewart)",
        "Statistics (Devore, in Spanish)": "Statistics (Devore)"
    }
    
    # Regex to find any of the book names
    book_finder_regex = re.compile("|".join(re.escape(k) for k in book_aliases.keys()))

    for line in text_data.strip().split('\n'):
        line = line.strip()
        if not line or line in ["PHYSICS", "MATHEMATICS", "STATISTICS & PROBABILITY"]:
            continue
            
        topic, mapping_str = line.split('\t', 1)
        
        if "Not explicitly covered" in mapping_str or "not listed" in mapping_str:
            missing_topics.append(topic)
            continue
            
        # Split the line by <br> in case multiple books cover one topic
        book_sections = re.split(r'\s*<br>\s*', mapping_str)
        
        for section in book_sections:
            match = book_finder_regex.search(section)
            if match:
                book_name_raw = match.group(0)
                book_name_clean = book_aliases[book_name_raw]
                
                # The rest of the string after the book name contains the chapter(s)
                chapter_details = section.replace(f"{book_name_raw}:", "").strip()
                
                reading_list[book_name_clean].append((topic, chapter_details))

    print(f"Writing formatted list to '{output_file}'...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Textbook Reading List\n\n")
        f.write("This document outlines the relevant textbook chapters for each topic, based on the provided index.\n\n")
        f.write("---\n\n")

        # Sort books by name for a consistent order
        for book in sorted(reading_list.keys()):
            f.write(f"## {book}\n\n")
            # Sort topics alphabetically within each book section
            for topic, chapters in sorted(reading_list[book]):
                f.write(f"- **{topic}**: {chapters}\n")
            f.write("\n")
            
        f.write("---\n\n")
        f.write("## Topics without Textbook Chapters\n\n")
        f.write("The following topics were not explicitly covered in the provided tables of contents and may require external resources:\n\n")
        
        for topic in sorted(missing_topics):
            f.write(f"- {topic}\n")
            
    print("Done.")

def main():
    """Main function to run the script."""
    parse_data_and_generate_list(RAW_TEXT_DATA, OUTPUT_FILENAME)

if __name__ == "__main__":
    main()