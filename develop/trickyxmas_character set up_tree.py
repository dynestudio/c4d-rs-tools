import c4d
from c4d import gui

# tags IDs
TAG_REDSHIFT_ID                   = 1036222
TAG_REDSHIFT_REFERENCE_SNAPSHOT   = 1
TAG_TEXTURE_PROJECTION_UVW        = 6
TAG_TEXTURE_PROJECTION_SPHERICAL  = 0

# viewport colors
tree_color_blue   = c4d.Vector(0.1215,0.3176,0.8117)
tree_color_lime   = c4d.Vector(0.7333,0.9019,0.1333)
tree_color_white  = c4d.Vector(0.7607,0.7607,0.7607) 

tree_nameslist      = [ 'Main Parent', 'Cube.5', 'Cube.4', 'Cube.3', 'Cube.2']
tree_layer_mats     = '_lights_'
tree_layer_objs     = 'arbol'

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
                    displacement, dis_max, dis_scale, dis_autobump, 
                    reference, ref_source, obj_id, obj_id_value):
    # get obj tags
    obj_tags = obj.GetTags()
    # define tag
    if not obj_tags:
        tag = obj.MakeTag(TAG_REDSHIFT_ID) # new tag
    else:
        obj_tags_types = [] # list of tag types
        for t in obj_tags:
            obj_tags_types.append(t.GetType())
            if t.GetType() == TAG_REDSHIFT_ID:
                tag = t
        if not TAG_REDSHIFT_ID in obj_tags_types:
            tag = obj.MakeTag(TAG_REDSHIFT_ID)

    # basic tab
    tag[c4d.ID_LAYER_LINK] = layer
    # geometry tab
    if geometry:
        tag[c4d.REDSHIFT_OBJECT_GEOMETRY_OVERRIDE]                = geometry
        tag[c4d.REDSHIFT_OBJECT_GEOMETRY_SUBDIVISIONENABLED]      = tessellation
        tag[c4d.REDSHIFT_OBJECT_GEOMETRY_MINTESSELLATIONLENGTH]   = tess_min
        tag[c4d.REDSHIFT_OBJECT_GEOMETRY_MAXTESSELLATIONSUBDIVS]  = tess_max
    # displacement tab
    if displacement:
        tag[c4d.REDSHIFT_OBJECT_GEOMETRY_DISPLACEMENTENABLED]     = displacement
        tag[c4d.REDSHIFT_OBJECT_GEOMETRY_MAXDISPLACEMENT]         = dis_max
        tag[c4d.REDSHIFT_OBJECT_GEOMETRY_DISPLACEMENTSCALE]       = dis_scale
        tag[c4d.REDSHIFT_OBJECT_GEOMETRY_AUTOBUMPENABLED]         = dis_autobump
    # reference projection
    if reference:
        tag[c4d.REDSHIFT_OBJECT_REFERENCE_SOURCE]             = ref_source
        c4d.CallButton(tag(), c4d.REDSHIFT_OBJECT_REFERENCE_BUTTON_CAPTURE)
    # object id tab
    if obj_id:
        tag[c4d.REDSHIFT_OBJECT_OBJECTID_OVERRIDE]            = obj_id
        tag[c4d.REDSHIFT_OBJECT_OBJECTID_ID]                  = obj_id_value

    return tag

def find_layer(layer_name):
    root = doc.GetLayerObjectRoot()
    LayersList = root.GetChildren() 
    layer = None
    for l in LayersList:
        if l.GetName() == layer_name:
            layer = l
    return layer

def find_mat(mat_list, mat_name):
    for mat in mat_list:
        if mat[c4d.ID_BASELIST_NAME] == mat_name:
            return mat
        else:
            return None

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
    layer = find_layer(tree_layer_objs)
    if not layer:
        gui.MessageDialog('this scene does not have the needed geometry layer.')
        return
    layer_mats = find_layer(tree_layer_mats)
    if not layer:
        gui.MessageDialog('this scene does not have the needed material layer.')
        return
    # get mats
    mats            = doc.GetMaterials()
    mats_character  = []
    for mat in mats:
        if mat[c4d.ID_LAYER_LINK].GetName() == tree_layer_mats:
            mats_character.append(mat)

    # ------------------------------------------------------

    # add_redshift_tag(obj,layer,0,0,0,0,0,0,0,0,0,0,0,0) # template function

    # ------------------------------------------------------

    # main parent commands
    add_redshift_tag(obj_list[0], layer, True, True, 1, 3,0,0,0,0,0,0,1,30)  # add main redshift tag
    obj_list[0][c4d.ID_LAYER_LINK] = layer                        # add main parent to obj layer
    obj_list.remove(obj_list[0])                                  # remove main parent from obj list

    # children ops
    for obj in obj_list:
        if obj.GetName() == 'Cube.4':
            display_color(obj,tree_color_blue) # display color
            obj[c4d.ID_LAYER_LINK] = layer     # add layer
            addTexTag(obj, layer, find_mat(mats_character,'Lambert3'), TAG_TEXTURE_PROJECTION_UVW)          # add material
            add_redshift_tag(obj,layer,0,0,0,0,0,0,0,0,0,0,0,0) # add redshift tag
        elif obj.GetName() == 'Cube.5':
            display_color(obj,tree_color_blue) # display color
            obj[c4d.ID_LAYER_LINK] = layer     # add layer
            addTexTag(obj, layer, find_mat(mats_character,'Lambert3'), TAG_TEXTURE_PROJECTION_UVW)          # add material
            add_redshift_tag(obj,layer,0,0,0,0,0,0,0,0,True,TAG_REDSHIFT_REFERENCE_SNAPSHOT,0,0) # add redshift tag


    c4d.EventAdd()

# Execute main()
if __name__=='__main__':
    main()