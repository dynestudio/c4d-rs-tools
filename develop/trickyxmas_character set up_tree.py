import c4d
from c4d import gui

# REDSHFT tag ID
REDSHIFT_TAG_ID = 1036222


# viewport colors
tree_color_blue  = c4d.Vector(0.1215,0.3176,0.8117)
tree_color_lime  = c4d.Vector(0.7333,0.9019,0.1333)
tree_color_white = c4d.Vector(0.7607,0.7607,0.7607) 

character_namelist_tree = [ 'Main Parent', 'Cube.5', 'Cube.4', 'Cube.3', 'Cube.2']
character_layer_mats = '_lights_'
character_layer_objs = 'arbol'

def get_allObjs(root_selection):
    def GetNextObject(op): # object manager iteration
        if not op: return None
        if op.GetDown(): return op.GetDown()
        while not op.GetNext() and op.GetUp(): op = op.GetUp()
        return op.GetNext()

    # get first obj
    first_obj = root_selection #doc.GetFirstObject()
    if not first_obj:
        return None
    # list of all objects in the scene
    list_objs = []
    # add the first obj
    list_objs.append(first_obj) 

    # obj loop iteration
    while first_obj:          
        first_obj = GetNextObject(first_obj)
        if first_obj:
            list_objs.append(first_obj)

    return list_objs

def addTag(obj, tag_ID):
    # get obj tags
    obj_tags = obj.GetTags()

    if not obj_tags:
        tag = obj.MakeTag(tag_ID) # new tag
    else:
        obj_tags_types = [] # list of tag types
        for t in obj_tags:
            obj_tags_types.append(t.GetType())
            if t.GetType() == tag_ID:
                tag = t

        if not tag_ID in obj_tags_types:
            tag = obj.MakeTag(tag_ID)

    return tag

def add_redshift_tag(obj, layer, geometry, tessellation, tess_min, tess_max, 
                    displacement, dis_max, dis_min, dis_auto, 
                    reference, ref_source, obj_id, obj_id_value):
    # get obj tags
    obj_tags = obj.GetTags()

    if not obj_tags:
        tag = obj.MakeTag(REDSHIFT_TAG_ID) # new tag
    else:
        obj_tags_types = [] # list of tag types
        for t in obj_tags:
            obj_tags_types.append(t.GetType())
            if t.GetType() == REDSHIFT_TAG_ID:
                tag = t

        if not REDSHIFT_TAG_ID in obj_tags_types:
            tag = obj.MakeTag(REDSHIFT_TAG_ID)

    tag[c4d.ID_LAYER_LINK] = layer

    return tag

def find_layer(layer_name):
    root = doc.GetLayerObjectRoot()
    LayersList = root.GetChildren() 
    layer = None
    for l in LayersList:
        if l.GetName() == layer_name:
            layer = l
    return layer


def addTexTag(obj, layer, mat, projection):
    textag = c4d.TextureTag()
    textag.SetMaterial(mat)
    textag[c4d.ID_BASELIST_NAME] = mat[c4d.ID_BASELIST_NAME]
    textag[c4d.TEXTURETAG_PROJECTION] = projection
    textag[c4d.ID_LAYER_LINK] = layer
    obj.InsertTag(textag)
    return textag

def display_color(obj, color):
    obj[c4d.ID_BASEOBJECT_USECOLOR]  = 2 # display color mode on
    obj[c4d.ID_BASEOBJECT_COLOR]     = color
    return True

# Main function
def main():
    # get objs
    obj_list = get_allObjs(op)
    if not obj_list:
        gui.MessageDialog('please select the parent object.')
        return
    # get layer
    layer = find_layer(character_layer_objs)
    if not layer:
        gui.MessageDialog('this scene does not have the needed geometry layer.')
        return
    layer_mats = find_layer(character_layer_mats)
    if not layer:
        gui.MessageDialog('this scene does not have the needed material layer.')
        return
    # get mats
    mats            = doc.GetMaterials()
    mats_character  = []
    for mat in mats:
        if mat[c4d.ID_LAYER_LINK].GetName() == character_layer_mats:
            mats_character.append(mat)

    # ------------------------------------------------------

    # main parent commands
    add_redshift_tag(obj_list[0], layer,0,0,0,0,0,0,0,0,0,0,0,0) # add main redshift tag
    obj_list[0][c4d.ID_LAYER_LINK] = layer # add main parent to obj layer
    obj_list.remove(obj_list[0])                          # remove main parent from obj list

    # children ops
    for obj in obj_list:
        display_color(obj,tree_color_blue)

    #tag = addTag(obj, c4d.Tcompositing)

    c4d.EventAdd()

# Execute main()
if __name__=='__main__':
    main()