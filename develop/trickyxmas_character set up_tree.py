import c4d
from c4d import gui, utils, storage

# tags IDs
TAG_REDSHIFT_ID                   = 1036222
TAG_REDSHIFT_REFERENCE_SNAPSHOT   = 1
TAG_TEXTURE_PROJECTION_UVW        = 6
TAG_TEXTURE_PROJECTION_SPHERICAL  = 0

# obj IDs
OBJ_ABC_GENERATOR  = 1028083

# colors
tree_color_blue      = c4d.Vector(0.1215,0.3176,0.8117)
tree_color_lime      = c4d.Vector(0.7333,0.9019,0.1333)
tree_color_white     = c4d.Vector(0.7607,0.7607,0.7607)
tree_color_geolayer  = c4d.Vector(0.3137,0.5921,1)

# names
tree_nameslist      = ['R_XmasTree_eyelid_top','R_XmasTree_eyelid_botton','R_XmasTree_eye','L_XmasTree_eyelid_top',
                       'L_XmasTree_eyelid_botton','L_XmasTree_eye','XmasTree_tongue','XmasTree_teeths','XmasTree_legs',
                       'XmasTree_top_2','XmasTree_top_1','XmasTree_band','XmasTree_Knot_3','XmasTree_Knot_2','XmasTree_Knot_1','XmasTree_gloves','XmasTree_body']
tree_matslist       = ['Tree_Ribbon and Gloves Cloth','Tree_Teeths','Tree_Tongue','Tree_Eye','Tree_Eye_Iris','Tree_Body']
tree_layer_mats     = 'Materials_Arbol'
tree_layer_objs     = 'Arbol'

# external documents
tree_document_materials     = "Y:\\My Drive\\Dyne - LLL\\Xmas Card 2019\\04_3D\\01_C4D\\02_ScnElements\\EP00_ACT00\\TrickyXmas_Materials_Arbol_v14 (Mats Only).c4d"
tree_document_eyeslightrig  = "Y:\\My Drive\\Dyne - LLL\\Xmas Card 2019\\04_3D\\01_C4D\\02_ScnElements\\EP00_ACT00\\TrickyXmas_Materials_Arbol_v14 (Eyes lights rig).c4d"
tree_document_tags          = "Y:\\My Drive\\Dyne - LLL\\Xmas Card 2019\\04_3D\\01_C4D\\02_ScnElements\\EP00_ACT00\\TrickyXmas_Materials_Arbol_v14 (Tags).c4d"

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

def addTexTag(obj, layer, mat, projection, selection):
    textag = c4d.TextureTag()
    textag.SetMaterial(mat)
    textag[c4d.ID_BASELIST_NAME] = mat[c4d.ID_BASELIST_NAME]
    textag[c4d.TEXTURETAG_PROJECTION] = projection
    textag[c4d.TEXTURETAG_RESTRICTION] = selection
    textag[c4d.ID_LAYER_LINK] = layer
    obj.InsertTag(textag)
    return textag

def tag_copy(obj_origin, tag_type, obj_target):
    obj_tags = obj_origin.GetTags()
    for tag in obj_tags:
        if tag.CheckType(tag_type):
            tag = tag.GetClone()
            obj_target.InsertTag(tag)
            return tag
        else:
            None

def add_layer(name,color):
    root = doc.GetLayerObjectRoot()
    layer = c4d.documents.LayerObject() # new Layer
    layer.SetName(name)  
    layer[c4d.ID_LAYER_COLOR] = color
    layer.InsertUnder(root)
    return layer

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
            material = mat
            return material
        else:
            material = None
    return material

def display_color(obj, color):
    obj[c4d.ID_BASEOBJECT_USECOLOR]  = 2 # display color mode on
    obj[c4d.ID_BASEOBJECT_COLOR]     = color
    return True

def make_editable(obj):
    obj_next = obj.GetNext()
    if not obj_next:
        obj_next = obj.GetPred()
    obj_list = [obj]
    # make obj editable
    obj_poly = c4d.utils.SendModelingCommand(c4d.MCOMMAND_MAKEEDITABLE,obj_list)
    # return obj only
    obj_new = obj_poly[0] ; doc.InsertObject(obj_new)
    # organize new obj in obj manager
    firstObj = doc.GetFirstObject() # get new editable object
    firstObj.InsertBefore(obj_next)

    return obj_new

# Main function
def main():
    # ------------------------------------------------------

    '''
    # get objs
    obj_list = get_allObjs(op)
    if not obj_list:
        gui.MessageDialog('please select the parent object.')
        return
    '''
    # load external alembic
    load_dlg = c4d.storage.LoadDialog(type=c4d.FILESELECTTYPE_ANYTHING, title="", flags=c4d.FILESELECT_LOAD, force_suffix="", def_path="", def_file="")
    if not load_dlg:
        return
    c4d.documents.MergeDocument(doc, load_dlg, c4d.SCENEFILTER_OBJECTS|c4d.SCENEFILTER_MATERIALS , None)

    # loop elements to organize new alembic objs
    obj = doc.GetFirstObject()
    obj_loop = True
    obj_list = [obj]
    # abc objs loop iterations
    while obj_loop:
        obj = obj.GetNext()
        if obj.GetType() == OBJ_ABC_GENERATOR:
            obj_list.append(obj)
        else:
            obj_loop = False

    #for obj in obj_list:
    #    obj.SetBit(c4d.BIT_ACTIVE)

    if len(obj_list) == 1:
        nullm = obj_list[0].GetMg()
    else:
        nullm = c4d.Matrix()
        nullm.off = sum([ob.GetMg().off for ob in obj_list])/ len(obj_list)
    
    null = c4d.BaseObject(c4d.Onull)
    null[c4d.ID_BASELIST_NAME] = 'nombre de prueba'
    null.InsertBefore(obj_list[0])
    null.SetBit(c4d.BIT_ACTIVE)
    null.SetMg(nullm)
    
    for ob in obj_list:
        m = ob.GetMg()
        ob.InsertUnderLast(null)
        ob.DelBit(c4d.BIT_ACTIVE)
        ob.SetMg(m)
    
    # meter null de rig en null de lights

    # ------------------------------------------------------
    # import external documents

    # import materials and layers
    c4d.documents.MergeDocument(doc, tree_document_materials, c4d.SCENEFILTER_OBJECTS|c4d.SCENEFILTER_MATERIALS , None)
    obj_mat = doc.SearchObject('Materials_Arbol') # find new object
    obj_mat.Remove() # delete null obj

    # import eyes lights rig
    c4d.documents.MergeDocument(doc, tree_document_eyeslightrig, c4d.SCENEFILTER_OBJECTS|c4d.SCENEFILTER_MATERIALS , None)
    obj_eyes_lighstrig = doc.SearchObject('Eyes Rig') # find new object

    # ------------------------------------------------------

    # get layer
    layer = find_layer(tree_layer_objs)
    if not layer:
            return

    layer_mats = find_layer(tree_layer_mats)
    if not layer:
        gui.MessageDialog('this scene does not have the needed material layer.')
        return
    # get mats
    mats            = doc.GetMaterials()
    mats_character  = []
    for mat in mats:
        if  mat[c4d.ID_LAYER_LINK]:
            if mat[c4d.ID_LAYER_LINK].GetName() == tree_layer_mats:
                mats_character.append(mat)

    # ------------------------------------------------------

    # add eyes geometries into eyes lights rig
    tree_eye_r = make_editable(doc.SearchObject('R_XmasTree_eye'))
    tree_eye_l = make_editable(doc.SearchObject('L_XmasTree_eye'))
    obj_eyes_lighstrig[c4d.ID_USERDATA,3] = tree_eye_r # add right eye
    obj_eyes_lighstrig[c4d.ID_USERDATA,6] = tree_eye_l # add left eye

    # add geometries into include light lists
    lightR_InEx = c4d.InExcludeData() ; lightR_InEx.InsertObject(tree_eye_r, 1)
    lightL_InEx = c4d.InExcludeData() ; lightL_InEx.InsertObject(tree_eye_l, 1)
    light_eye_R = doc.SearchObject('Eye R - Disc Light') ; light_eye_L = doc.SearchObject('Eye L - Disc Light') 
    light_eye_R[c4d.REDSHIFT_LIGHT_EXCLUSION_LIST] = lightR_InEx
    light_eye_L[c4d.REDSHIFT_LIGHT_EXCLUSION_LIST] = lightL_InEx

    # ------------------------------------------------------

    # import tags from external document *delete them in child ops
    c4d.documents.MergeDocument(doc, tree_document_tags, c4d.SCENEFILTER_OBJECTS|c4d.SCENEFILTER_MATERIALS , None)
    obj_tag_eyes   = doc.SearchObject('R_XmasTree_eye_tags')
    obj_tag_tongue = doc.SearchObject('XmasTree_tongue_tags')
    obj_tag_body   = doc.SearchObject('XmasTree_body_tags')

    # ------------------------------------------------------

    # add_redshift_tag(obj,layer,geometry,tessellation,tess_min,tess_max,displacement,dis_max,dis_scale,dis_autobump,reference,ref_source,obj_id,obj_id_value) # add redshift tag

    # ------------------------------------------------------

    # main parent commands
    main_parent = null
    add_redshift_tag(main_parent, layer, True, True, 1, 3,0,0,0,0,0,0,1,30)  # add main redshift tag
    main_parent[c4d.ID_LAYER_LINK] = layer                        # add main parent to obj layer
    #obj_list.remove(obj_list[0])                                  # remove main parent from obj list

    # ------------------------------------------------------

    # children ops
    for obj in obj_list:
        if obj.GetName() == tree_nameslist[0]: # R_XmasTree_eyelid_top
            display_color(obj,tree_color_blue) # display color
            obj[c4d.ID_LAYER_LINK] = layer     # add layer
            addTexTag(obj, layer, find_mat(mats_character,tree_matslist[5]), TAG_TEXTURE_PROJECTION_UVW,'') # add material - Tree_Body
            add_redshift_tag(obj,layer, True,True,0,3,True,1,1,False,True,TAG_REDSHIFT_REFERENCE_SNAPSHOT,False,False) # add redshift tag
        
        elif obj.GetName() == tree_nameslist[1]: # R_XmasTree_eyelid_botton
            display_color(obj,tree_color_blue) # display color
            obj[c4d.ID_LAYER_LINK] = layer     # add layer
            addTexTag(obj, layer, find_mat(mats_character,tree_matslist[5]), TAG_TEXTURE_PROJECTION_UVW,'') # add material - Tree_Body
            add_redshift_tag(obj,layer, True,True,0,3,True,1,1,False,True,TAG_REDSHIFT_REFERENCE_SNAPSHOT,False,False) # add redshift tag
        
        elif obj.GetName() == tree_nameslist[2]: # R_XmasTree_eye
            #display_color(obj,tree_color_white) # display color
            obj[c4d.ID_LAYER_LINK] = layer     # add layer
            tag = tag_copy(obj_tag_eyes, c4d.Tpolygonselection,obj) # copy polygon selection tags
            addTexTag(obj, layer, find_mat(mats_character,tree_matslist[3]), TAG_TEXTURE_PROJECTION_UVW, tag.GetName()) # add material - Tree_Eye
            addTexTag(obj, layer, find_mat(mats_character,tree_matslist[4]), TAG_TEXTURE_PROJECTION_UVW, '') # add material - Tree_Iris
            add_redshift_tag(obj,layer,0,0,0,0,0,0,0,0,True,TAG_REDSHIFT_REFERENCE_SNAPSHOT,0,0) # add redshift tag
        
        elif obj.GetName() == tree_nameslist[3]: # L_XmasTree_eyelid_top
            display_color(obj,tree_color_blue) # display color
            obj[c4d.ID_LAYER_LINK] = layer     # add layer
            addTexTag(obj, layer, find_mat(mats_character,tree_matslist[5]), TAG_TEXTURE_PROJECTION_UVW,'') # add material - Tree_Body
            add_redshift_tag(obj,layer, True,True,0,3,True,1,1,False,True,TAG_REDSHIFT_REFERENCE_SNAPSHOT,False,False) # add redshift tag
        
        elif obj.GetName() == tree_nameslist[4]: # L_XmasTree_eyelid_botton
            display_color(obj,tree_color_blue) # display color
            obj[c4d.ID_LAYER_LINK] = layer     # add layer
            addTexTag(obj, layer, find_mat(mats_character,tree_matslist[5]), TAG_TEXTURE_PROJECTION_UVW,'') # add material - Tree_Body
            add_redshift_tag(obj,layer, True,True,0,3,True,1,1,False,True,TAG_REDSHIFT_REFERENCE_SNAPSHOT,False,False) # add redshift tag
        
        elif obj.GetName() == tree_nameslist[5]: # L_XmasTree_eye
            #display_color(obj,tree_color_white) # display color
            obj[c4d.ID_LAYER_LINK] = layer     # add layer
            tag = tag_copy(obj_tag_eyes, c4d.Tpolygonselection,obj) # copy polygon selection tags
            obj_tag_eyes.Remove()
            addTexTag(obj, layer, find_mat(mats_character,tree_matslist[3]), TAG_TEXTURE_PROJECTION_UVW, tag.GetName()) # add material - Tree_Eye
            addTexTag(obj, layer, find_mat(mats_character,tree_matslist[4]), TAG_TEXTURE_PROJECTION_UVW, '') # add material - Tree_Iris
            add_redshift_tag(obj,layer,0,0,0,0,0,0,0,0,True,TAG_REDSHIFT_REFERENCE_SNAPSHOT,0,0) # add redshift tag

        elif obj.GetName() == tree_nameslist[6]: # XmasTree_tongue
            obj = make_editable(obj)
            display_color(obj,tree_color_blue) # display color
            obj[c4d.ID_LAYER_LINK] = layer     # add layer
            addTexTag(obj, layer, find_mat(mats_character,tree_matslist[2]), TAG_TEXTURE_PROJECTION_UVW,'') # add material - Tree_Tongue
            add_redshift_tag(obj,layer,0,0,0,0,0,0,0,0,True,TAG_REDSHIFT_REFERENCE_SNAPSHOT,True,32) # add redshift tag
            tag_copy(obj_tag_tongue, c4d.Tvertexmap,obj) # copy polygon selection tags
            obj_tag_tongue.Remove()

        elif obj.GetName() == tree_nameslist[7]: # XmasTree_teeths
            display_color(obj,tree_color_white) # display color
            obj[c4d.ID_LAYER_LINK] = layer     # add layer
            addTexTag(obj, layer, find_mat(mats_character,tree_matslist[1]), TAG_TEXTURE_PROJECTION_UVW,'') # add material - Tree_Teeths
            add_redshift_tag(obj,layer,0,0,0,0,0,0,0,0,True,TAG_REDSHIFT_REFERENCE_SNAPSHOT,0,0) # add redshift tag

        elif obj.GetName() == tree_nameslist[8]: # XmasTree_legs
            display_color(obj,tree_color_blue) # display color
            obj[c4d.ID_LAYER_LINK] = layer     # add layer
            addTexTag(obj, layer, find_mat(mats_character,tree_matslist[5]), TAG_TEXTURE_PROJECTION_SPHERICAL,'') # add material - Tree_Body
            add_redshift_tag(obj,layer,True,True,0,3,True,1,1,False,True,TAG_REDSHIFT_REFERENCE_SNAPSHOT,False,False) # add redshift tag

        elif obj.GetName() == tree_nameslist[9]: # XmasTree_top_2
            display_color(obj,tree_color_lime) # display color
            obj[c4d.ID_LAYER_LINK] = layer     # add layer
            addTexTag(obj, layer, find_mat(mats_character,tree_matslist[0]), TAG_TEXTURE_PROJECTION_UVW,'') # add material - Tree_Ribbon and Gloves Cloth
            add_redshift_tag(obj,layer,0,0,0,0,0,0,0,0,True,TAG_REDSHIFT_REFERENCE_SNAPSHOT,True,31) # add redshift tag
        
        elif obj.GetName() == tree_nameslist[10]: # XmasTree_top_1
            display_color(obj,tree_color_lime) # display color
            obj[c4d.ID_LAYER_LINK] = layer     # add layer
            addTexTag(obj, layer, find_mat(mats_character,tree_matslist[0]), TAG_TEXTURE_PROJECTION_UVW,'') # add material - Tree_Ribbon and Gloves Cloth
            add_redshift_tag(obj,layer,0,0,0,0,0,0,0,0,True,TAG_REDSHIFT_REFERENCE_SNAPSHOT,True,31) # add redshift tag

        elif obj.GetName() == tree_nameslist[11]: # XmasTree_band
            display_color(obj,tree_color_lime) # display color
            obj[c4d.ID_LAYER_LINK] = layer     # add layer
            addTexTag(obj, layer, find_mat(mats_character,tree_matslist[0]), TAG_TEXTURE_PROJECTION_UVW,'') # add material - Tree_Ribbon and Gloves Cloth
            add_redshift_tag(obj,layer,0,0,0,0,0,0,0,0,True,TAG_REDSHIFT_REFERENCE_SNAPSHOT,True,31) # add redshift tag
 
        elif obj.GetName() == tree_nameslist[12]: # XmasTree_Knot_3
            display_color(obj,tree_color_lime) # display color
            obj[c4d.ID_LAYER_LINK] = layer     # add layer
            addTexTag(obj, layer, find_mat(mats_character,tree_matslist[0]), TAG_TEXTURE_PROJECTION_UVW,'') # add material - Tree_Ribbon and Gloves Cloth
            add_redshift_tag(obj,layer,0,0,0,0,0,0,0,0,True,TAG_REDSHIFT_REFERENCE_SNAPSHOT,True,31) # add redshift tag

        elif obj.GetName() == tree_nameslist[13]: # XmasTree_Knot_2
            display_color(obj,tree_color_lime) # display color
            obj[c4d.ID_LAYER_LINK] = layer     # add layer
            addTexTag(obj, layer, find_mat(mats_character,tree_matslist[0]), TAG_TEXTURE_PROJECTION_UVW,'') # add material - Tree_Ribbon and Gloves Cloth
            add_redshift_tag(obj,layer,0,0,0,0,0,0,0,0,True,TAG_REDSHIFT_REFERENCE_SNAPSHOT,True,31) # add redshift tag

        elif obj.GetName() == tree_nameslist[14]: # XmasTree_Knot_1
            display_color(obj,tree_color_lime) # display color
            obj[c4d.ID_LAYER_LINK] = layer     # add layer
            addTexTag(obj, layer, find_mat(mats_character,tree_matslist[0]), TAG_TEXTURE_PROJECTION_UVW,'') # add material - Tree_Ribbon and Gloves Cloth
            add_redshift_tag(obj,layer,0,0,0,0,0,0,0,0,True,TAG_REDSHIFT_REFERENCE_SNAPSHOT,True,31) # add redshift tag

        elif obj.GetName() == tree_nameslist[15]: # XmasTree_gloves
            display_color(obj,tree_color_lime) # display color
            obj[c4d.ID_LAYER_LINK] = layer     # add layer
            addTexTag(obj, layer, find_mat(mats_character,tree_matslist[0]), TAG_TEXTURE_PROJECTION_UVW,'') # add material - Tree_Ribbon and Gloves Cloth
            add_redshift_tag(obj,layer,0,0,0,0,0,0,0,0,True,TAG_REDSHIFT_REFERENCE_SNAPSHOT,True,31) # add redshift tag

        elif obj.GetName() == tree_nameslist[16]: # XmasTree_body
            obj = make_editable(obj)
            display_color(obj,tree_color_blue) # display color
            obj[c4d.ID_LAYER_LINK] = layer     # add layer
            addTexTag(obj, layer, find_mat(mats_character,tree_matslist[5]), TAG_TEXTURE_PROJECTION_SPHERICAL,'') # add material - Tree_Body
            add_redshift_tag(obj,layer,True,True,0,3,True,1,1,False,True,TAG_REDSHIFT_REFERENCE_SNAPSHOT,0,0) # add redshift tag
            tag_copy(obj_tag_body, c4d.Tvertexmap,obj) # copy polygon selection tags
            obj_tag_body.Remove()

        else:
            None

        # ------------------------------------------------------

    c4d.EventAdd()

# Execute main()
if __name__=='__main__':
    main()