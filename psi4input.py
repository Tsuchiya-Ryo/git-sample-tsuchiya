# 途端に計算したくなった時用。

# This function outputs rough atom coordinates of input molecule and creates a file for DFT calculation on Psi4
# Generation of the geometry is based on ETKDGv2
# (cartesian coordinate)

'''
    x: smiles or xyz or mol object
    flag: declare the type of x
    
    thread: number of cpu threads
    mem: number of memory applied
    input_name: the input file name for calculation(actually this function's output name)
    output_name: the output file name of calculation log
    functional: default value is "sto-3g"
    basis: default value is "3-21g"
    method: calculation method. default value is "energy"
    charge: default value is 0
    spin: default value is 0
    gname: name of atom coordinates. default value is "GeometryName"
    
'''

from rdkit import Chem
from rdkit.Chem import AllChem

def mol2dft(x, flag, thread=4, mem=4, input_name="input.py", output_name="output.log", functional="sto-3g", basis="3-21g", method="energy", charge=0, spin=0, gname="GeometryName"):
    if flag not in ["mol", "xyz", "smiles"]:
        print("ArgumentError:\
               \n\tMOL, SMILES and XYZ objects are acceptable.\
               \n\t(flag = 'mol' or 'smiles' or 'xyz' must be written.)")
        return

    elif flag == "mol":
        MOL = Chem.AddHs(x)
        AllChem.EmbedMolecule(MOL, AllChem.ETKDGv2())
        XYZ = Chem.rdmolfiles.MolToXYZBlock(MOL)
        XYZ = "\n".join(str(XYZ).splitlines()[2:])
        
    elif flag == "xyz":
        XYZ = "\n".join(str(x).splitlines()[2:])
        
    elif flag == "smiles":
        MOL = Chem.MolFromSmiles(x)
        MOL = Chem.AddHs(MOL)
        AllChem.EmbedMolecule(MOL, AllChem.ETKDGv2())
        XYZ = Chem.rdmolfiles.MolToXYZBlock(MOL)
        XYZ = "\n".join(str(XYZ).splitlines()[2:])
        
    f = open(input_name, "w")
    text = ["import psi4",
            "import datetime",
            "import time",
            "t = datetime.datetime.fromtimestamp(time.time())\n",
            "psi4.set_num_threads(nthread={})".format(int(thread)),
            "psi4.set_memory('{}GB')".format(mem),
            "psi4.set_output_file('{}')".format(str(output_name)),
            "\n{} = psi4.geometry('''".format(gname),
            "{} {}".format(int(charge), int(spin)),            
            XYZ,
            "''')\n",
            "psi4.{}('{}/{}')".format(method, functional, basis)]
    f.write("\n".join(text))
    f.close