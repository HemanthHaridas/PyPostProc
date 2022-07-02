from numpy      import array, dot, cross, pi
from sys        import argv
from subprocess import run
from socket     import gethostname
from platform   import architecture, python_version
from pathlib    import Path

def _initializePyPostProc():
    print("PyPostProc v.0.0.1\n\n")
    print("{:<80}".format("This Code is written by Hemanth Haridas and Chythra J N while at the Indian Institute "))
    print("{:<80}".format("of Technology Gandhinagar. Code is licensed under GPLv3, and you will have received a "))
    print("{:<80}".format("copy of the same from github along with this.\n"))
    print("{:<80}".format("For any kind of support and queries, please write to hemanth.h@iitgn.ac.in or raise an"))
    print("{:<80}".format("issue in the github repository for PyPostProc"))
    print("\n\n\n")
    print("hostname             :   {}".format(gethostname()))
    print("system architecture  :   {}".format(architecture()[0]))
    print("python version       :   {}".format(python_version()))

def _readstreamfile(_streamfileName, _residuename):
    with open(_streamfileName) as strfile:
        _streamfileBuffer   =   strfile.readlines()
        for lnumber, line in enumerate(_streamfileBuffer):
            if "RESI" in line:
                residueline     =   line.split()
                t_residuename   =   residueline[1]   
                try:
                    assert t_residuename == _residuename, "[ERROR]: Residue names do not match"
                except AssertionError as Message:
                    exit(Message)
            _startstreamLine    =   lnumber+2
            break

        _streamBuffer   =   []
        for line in _streamfileBuffer[_startstreamLine:]:
            if "GROUP" in line:
                pass
            if "ATOM" in line:
                t_streamline    =   line.split()
                _atomName       =   t_streamline[1]
                _streamBuffer.append(_atomName)

        _topologyBuffer =   []
        for line in _streamfileBuffer:
            if "BOND" in line:
                t_topologyline  =   line.split()[1:]
                _topologyBuffer.append((t_topologyline[0],t_topologyline[1]))
            if "END" in line:
                break

    return _streamBuffer, _topologyBuffer

def _extractQMCoordinates(_streamBuffer, _residuename):
    _gaussianlogfileName    =   input("Enter path to Gaussian log file : ")
    
    with open(_gaussianlogfileName) as gausslog:
        _logfileBuffer  =   gausslog.readlines()
        for lnumber, line in enumerate(_logfileBuffer):
            if "Input orientation" in line:
                _startcoordsLine    =   lnumber+5

        _coordsBuffer   =   []
        t_numberAtoms   =   len(_streamBuffer)

        for line in _logfileBuffer[_startcoordsLine:]:
            if "---" in line:
                break
            else:
                t_coordsline    =   line.split()[3:]
                _coordsline     =   [float(x) for x in t_coordsline]
                _coordsBuffer.append(_coordsline)
        _numberAtoms    =   len(_coordsBuffer)
        try:
            assert _numberAtoms == t_numberAtoms, "[ERROR]: Number of atoms in Gaussian log file {} and CHARMM stream file {} do not match".format(_numberAtoms, t_numberAtoms)
        except AssertionError as Message:
            exit(Message)

    return _coordsBuffer, _numberAtoms

def _writecrdFile(_streambuffer, _residuename, _coordsbuffer, _numberatoms):
    with open(_residuename.lower()+".gaussian.crd","w") as outcrd:
        outcrd.write("*Generated By PyPostProc\n*\n".upper())
        outcrd.write("{:10.0f}  {}\n".format(_numberatoms,"EXT"))
        for atomcounter, data in enumerate(zip(_streambuffer, _coordsbuffer)):
            outcrd.write("{:10.0f}{:10.0f}  {}      {:<8}{:20.10f}{:20.10f}{:20.10f}  {}{:7.0f}{:27.10f}\n".format(atomcounter+1, 1, _residuename, data[0], data[1][0], data[1][1], data[1][2], _residuename, 1, 0))
    print("CHARMM CRD file has been successfully generated")

def _generateNAMDconfigFile(_streamfilename, _residuename, _coordsbuffer, _numberatoms, _pathtoCHARMM, _dimensions):

    # generate CHARMM crd file
    _streambuffer, _topologybuffer  =   _readstreamfile(_streamfilename, _residuename)
    _writecrdFile(_streambuffer, _residuename, _coordsbuffer, _numberatoms)

    # generate pdb and psf file from CHARMM
    # solvate the structure using CHARMM
    # write NAMD configuration file

    pass

def main():
    try:
        assert len(argv) > 1, "Use PyPostProc as python PyPostProc.py < residue name > < CHARMM stream file >"
    except AssertionError as Message:
        exit(Message)

    _ResidueName    =   argv[1]
    _StreamfileName =   argv[2]

    _initializePyPostProc()
    print(" ")

    _StreamBuffer, _TopologyBuffer  =   _readstreamfile(_StreamfileName, _ResidueName)
    try:
        assert _StreamBuffer != [], "[ERROR]: Unable to parse CHARMM stream file"
    except AssertionError as Message:
        exit(Message)
    print("CHARMM stream file {} has been successfully parsed by PyPostProc\n\n".format(_StreamfileName))

    print("Enter the type of analysis to be performed:")
    print("1. Extract optimized coordinates from gaussian log file and generate corresponding CHARMM CRD file")
    print("2. Extract HF/MP2/CCSD(T) energies from gaussian log file")
    print("3. Compare two QM-QM/QM-MM or MM-MM geometries")
    print("4. Generate NAMD input file from optimized gaussian log file and CHARMM parameter files (Requires CHARMM)")
    _AnalysisType   =   input("Enter your choice (Default = 1) : ")

    if _AnalysisType == '1':
        _QMcoordsBuffer, _NumberAtoms   =   _extractQMCoordinates(_StreamBuffer, _ResidueName)  
        _writecrdFile(_StreamBuffer, _ResidueName, _QMcoordsBuffer, _NumberAtoms)

    if _AnalysisType == '2':
        pass

    if _AnalysisType == '3':
        pass

    if _AnalysisType == '4':
        _PathtoCHARMM                   =   input("Enter the full path to CHARMM executable : ")
        _QMcoordsBuffer, _NumberAtoms   =   _extractQMCoordinates(_StreamBuffer, _ResidueName)   
        _generateNAMDconfigFile(_StreamfileName, _ResidueName, _QMcoordsBuffer, _NumberAtoms, _PathtoCHARMM, 10.0)
#        run([_PathtoCHARMM,'-l'])

if __name__ == '__main__':
    main()  # Begin Analysis Code
