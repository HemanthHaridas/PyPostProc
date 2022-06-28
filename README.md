# PyPostProc
A Python Code to generate and analyze CHARMM and NAMD files. 

### Usage
python3 PyPostProc.py < residue name > < full path to CGenFF style stream file >

### Dependencies
1. The code is written for Python versions of 3.5 and above, eventhough the code does not check for the Python version. However, It is recommended that the code be run using Python3. The code may also not work on Windows Machines. 
2. Stream file required by the Code must comply to the CGenFF stream file style, with one residue per stream file.
3. Code requires a valid path to the CHARMM executable for the generation of PSF and PDB files required for generating NAMD configuration files.

### Current Capabilities
1. Generate CHARMM compatible CRD files from Gaussian optimized geometries.
2. Extract HF/MP2/CCSD(T) Energies from Gaussian output files.
3. Compare two geometries (QM-MM, MM-MM or QM-QM).
4. Generate NAMD input files from Gaussian optimized geometries.
