def DockLig_vina(lig_in, prot_in, center=None,size=None, outname = 'docklings',cleanfiles=True):
    """
    Wrapper function to flexibly dock small molecules to a user define volume in a protein using Autodock Vina.
    Input files are automatically converted to Autodock's pdbqt format. It is recommended that the protein and ligand
    have been correctly protonated.

    The accepted fileformats of the the protein and ligand are all of those accepted by Openbabel.

    Example
    --------
    DockLig_vina(ligand.mol2, protein.pdb, center = [3.3,4.3,23.7], cleanfiles=False)

    Parameters
    ----------
    lig_in : str
        The filename of ligand--including file extension (suffix)--you wish to dock, including file extension (suffix)
    prot_in: str
        The filename of the protein--including file extension (suffix)-- that the ligand will be docked into.
    center: list of floats
        The center of the docking search space in the form [x,y,z], where x, y, and z are in Angstroms
    size: list of floats
        The lengths of the cuboid search volume in the form [x,y,z], where x, y, and z are in Angstroms
    outname: str
        The naming scheme the docked configurations and log file. Do not include the file extension (suffix)
    cleanfiles: bool
        Whether to remove the intermediate pdbqt files that were necessary for AutoDock Vina

    Returns
    -------
    Docked structures (.pdbqt) and log file (.log) are written to the working directory
    """

    if center == None:
        print 'Fatal: must specify the center of the search space'
        return
    if size == None:
        size = [15,15,15]

    import subprocess

    # Checking whether the executable of Vina can be found
    if subprocess.call('vinaa',shell=True) != 1:
        print 'Autodock Vina not found. Cancelling docking.'
        return

    # Getting the file types of the ligand and receptor
    ligname = lig_in.split('.')[0]
    protname = prot_in.split('.')[0]
    ligtype = lig_in.split('.')[1]
    protype = prot_in.split('.')[1]

    # Generate the pdbqt file for the ligand
    cmd = 'obabel -i{0} {1} -o pdbqt -O {2}.pdbqt'.format(ligtype,lig_in,ligname)
    subprocess.call(cmd,shell=True)

    # Generate the pdbqt file for the protein
    cmd = 'obabel -i{0} {1} -o pdbqt -xr -O {2}.pdbqt'.format(protype,prot_in,protname)
    subprocess.call(cmd,shell=True)

    # Run AutoDock
    cmd = 'vina --receptor {0}.pdbqt --ligand {1}.pdbqt --center_x {2} --center_y {3} --center_z {4} --size_x {5} --size_y {6} --size_z {7} --out {8}.pdbqt --log {9}.log'.format(protname,ligname,center[0],center[1],center[2],size[0],size[1],size[2],outname,outname)
    print cmd
    subprocess.call(cmd,shell=True)

    if cleanfiles == True:
        cmd = 'rm {0}.pdbqt {1}.pdbqt'.format(ligname,protname)
        subprocess.call(cmd,shell=True)