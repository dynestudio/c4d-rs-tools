"""
rs triplanar - set projection

Author: Carlos Dordelly
Website: http://dyne.studio
Original functions from: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: rs_TriplanarSetProjection
Description-US: Change triplanar projection type on selected materials.
Written for Maxon Cinema 4D R21.115
"""
# Libraries
import c4d
try:
    import redshift
except:
    pass
from operator import attrgetter

# Classes
class nodeObject(object):
    def __init__(self, obj):
        self.node = obj # Node object

# Functions
def triplanar_maptype(nodeMaster):
    nodes = [] # Initialize a list
    root = nodeMaster.GetRoot() # Get node master root
    nodeMaster.AddUndo() # Add undo for changing nodes
    for node in root.GetChildren(): # Iterate through nodes
        nodes.append(nodeObject(node)) # Create nodeObject and add it to a list

    if nodes: # If there is nodes
        # Node settings and ports
        for i in range(0, len(nodes)): # Iterate through collected nodes
            node = nodes[i].node # Get node
            if node.GetOperatorID() == 1036227:
                if node[c4d.GV_REDSHIFT_SHADER_META_CLASSNAME] == "TriPlanar":
                    node[c4d.REDSHIFT_SHADER_TRIPLANAR_PROJSPACETYPE] = 2 # change mapping type to Reference


def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    materials = doc.GetMaterials() # Get materials
    try: # Try to execute following script
        for m in materials: # Iterate through materials
            if m.GetBit(c4d.BIT_ACTIVE): # If material is selected
                rsnm = redshift.GetRSMaterialNodeMaster(m) # Get Redshift material node master
                triplanar_maptype(rsnm) # Run the main function
    except: # Otherwise
        pass # Do nothing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()