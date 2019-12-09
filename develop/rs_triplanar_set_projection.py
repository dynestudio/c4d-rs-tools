"""
AR_AddRSTextureControllers

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_AddRSTextureControllers
Description-US: Creates individual scale, offset and rotate control nodes for Redshift texture and triplanar nodes.
Written for Maxon Cinema 4D R21.026
"""
# Libraries
import c4d
try:
    import redshift
except:
    pass
from operator import attrgetter
from c4d import utils as u

# Classes
class nodeObject(object):
    def __init__(self, obj, px, py, sx, sy):
        self.node = obj # Node object
        self.px = px # X position
        self.py = py # Y position
        self.sx = sx # X scale
        self.sy = sy # Y scale

# Functions
def GetPortIndex(node, portId):
    inPorts = node.GetInPorts()
    for i, port in enumerate(inPorts):
        if port.GetMainID() == portId:
            return i

def AddControllers(nodeMaster):
    nodes = [] # Initialize a list
    root = nodeMaster.GetRoot() # Get node master root
    nodeMaster.AddUndo() # Add undo for changing nodes
    for node in root.GetChildren(): # Iterate through nodes
        if node.GetBit(c4d.BIT_ACTIVE): # If node is selected
            bc  = node.GetData() # Get copy of base container
            bsc = bc.GetContainer(c4d.ID_SHAPECONTAINER) # Get copy of shape container
            bcd = bsc.GetContainer(c4d.ID_OPERATORCONTAINER) # Get copy of operator container
            px  = bcd.GetReal(100) # Get x position
            py  = bcd.GetReal(101) # Get y position
            sx  = bcd.GetReal(108) # Get x scale
            sy  = bcd.GetReal(109) # Get y scale
            nodes.append(nodeObject(node, px, py, sx, sy)) # Create nodeObject and add it to a list

    if nodes: # If there is nodes
        firstNode = min(nodes, key=attrgetter('py')) # Get the node with the minimum y position value

        # Node generation
        scaleNode = nodeMaster.CreateNode(root, 400001120, firstNode.node, x = -1, y = -1) # Crete a constant node (RS)
        offsetNode = nodeMaster.CreateNode(root, 400001120, firstNode.node, x = -1, y = -1)
        rotateNode = nodeMaster.CreateNode(root, 400001120, firstNode.node, x = -1, y = -1)
        newNodes = [scaleNode, offsetNode, rotateNode]

        scaleNode.SetBit(c4d.BIT_ACTIVE) # Select node
        offsetNode.SetBit(c4d.BIT_ACTIVE) # Select node
        rotateNode.SetBit(c4d.BIT_ACTIVE) # Select node

        # Node settings and ports
        for i in range(0, len(nodes)): # Iterate through collected nodes
            node = nodes[i].node # Get node
            node.DelBit(c4d.BIT_ACTIVE)
            if node.GetOperatorID() == 1036227:
                if node[c4d.GV_REDSHIFT_SHADER_META_CLASSNAME] == "TriPlanar":
                    print node[c4d.ID_BASELIST_NAME]
                    node[c4d.REDSHIFT_SHADER_TRIPLANAR_PROJSPACETYPE] = 3 




def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    materials = doc.GetMaterials() # Get materials
    try: # Try to execute following script
        for m in materials: # Iterate through materials
            if m.GetBit(c4d.BIT_ACTIVE): # If material is selected
                rsnm = redshift.GetRSMaterialNodeMaster(m) # Get Redshift material node master
                AddControllers(rsnm) # Run the main function
    except: # Otherwise
        pass # Do nothing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()