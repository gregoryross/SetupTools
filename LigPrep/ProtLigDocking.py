

def DockLig_vina(lig_in, prot_in, center=None,size=None, outname = 'docklings',cleanfiles=False):

    if center == None:
        print 'Fatal: must specify the center of the search space'
        return
    if size == None:
        size = [15,15,15]

    import subprocess

    # Getting the file types of the ligand and receptor
    ligname = lig_in.split('.')[0]
    protname = prot_in.split('.')[0]
    ligtype = lig_in.split('.')[1]
    protype = prot_in.split('.')[1]

    # Generate the pdbqt file for the ligand
    cmd = 'obabel -i{0} {1} -o pdbqt -O {2}.pdbqt'.format(ligtype,lig_in,ligname)
    subprocess.call(cmd,shell=True)

    # Generate the pdbqt file for the protein
    cmd = 'obabel -i{0} {1} -o pdbqt -rx -O {2}.pdbqt'.format(protype,prot_in,protname)
    subprocess.call(cmd,shell=True)

    # Run AutoDock
    cmd = 'vina --receptor {0}.pdbqt --ligand {1}.pdbqt --center_x {2} --center_y {3} --center_z {4}' \
          ' --size_x {5} --size_y {6} --size_z {7} --out {8}.pdbqt --log {9}.log'.format(protname,ligname,center[0],center[1],center[2],size[0],size[1],size[2],outname,outname)
    subprocess.call(cmd,shell=True)

    if cleanfiles == True:
        cmd = 'rm {0}.pdbqt {1}.pdbqt'.format(ligname,protname)
        subprocess.call(cmd,shell=True)