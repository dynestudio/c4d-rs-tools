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
elf_color_blue       = c4d.Vector(0.1725,0.2117,0.4705)
elf_color_white      = c4d.Vector(0.7019,0.7019,0.7019)
elf_color_cyan       = c4d.Vector(0.1960,0.5803,0.8196)
elf_color_black      = c4d.Vector(0.1019,0.1019,0.1019)
elf_color_lightblue  = c4d.Vector(0.7098,0.7019,0.7411)
elf_color_red        = c4d.Vector(0.6588,0.2588,0.3294)
elf_color_pink       = c4d.Vector(0.6705,0.5411,0.6196)

# names
elf01_nameslist    = ['T_shirt','Pants','Nose','Lice_R_5','Lice_R_4','Lice_R_3','Lice_R_2','Lice_R_1','Lice_L_5','Lice_L_4','Lice_L_3',
                        'Lice_L_2','Lice_L_1','Hat2','Hand_R','Hand_L','Hair','Button','Boot_R','Boot_L','Body','Mouth_geo','Eye_R_geo','Eye_L_geo','Hat']
elf_matslist       = ['Elf_Boots Laces','Elf_Boots','Elf_Elf_Hat Lines','Elf_Elf_Hat Circle','Elf_Arms and Legs Cloth','Elf_Cloth Light Blue',
                        'Elf_Cloth Dark Grey','Elf_Clorh Pink','Elf_Clorh Blue','Elf_Hands','Elf_Eyes and Mouth','Elf_Hair White','Elf_Hair Blue','Elf_Nose Blue','Elf_Nose Red','Elf_Body']
elf_layer_mats     = 'Materials Duende'
elf_layer_objs     = 'Duende'

# external documents
elf_document_materials     = "Y:\\My Drive\\Dyne - LLL\\Xmas Card 2019\\04_3D\\01_C4D\\02_ScnElements\\EP00_ACT00\\TrickyXmas_Materials_Duende_v12 (Mats Only).c4d"
elf_document_tags          = "Y:\\My Drive\\Dyne - LLL\\Xmas Card 2019\\04_3D\\01_C4D\\02_ScnElements\\EP00_ACT00\\TrickyXmas_Materials_Duende_v12 (Tags).c4d"

# ------------------------------------------------------

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

    # get original obj list
    obj_list_origin = get_allObjs(doc.GetFirstObject())

    # ------------------------------------------------------

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

    # move all abc objs into a main parent null
    null = c4d.BaseObject(c4d.Onull)
    null_name = load_dlg.split('\\')
    null_name = null_name[-1] ; null_name = null_name.split('.')
    null[c4d.ID_BASELIST_NAME] = null_name[0]
    null.InsertBefore(obj_list[0])
    null.SetBit(c4d.BIT_ACTIVE)

    for obj in obj_list:
        obj.InsertUnderLast(null)

    main_geo = doc.SearchObject('_geo_')
    if main_geo:
        null.InsertUnder(main_geo)

    # make obj list with children
    obj_list = get_allObjs(null)
    for obj in obj_list_origin:
        if obj in obj_list:
            obj_list.remove(obj)
        else:
            continue

    # ------------------------------------------------------
    # import external documents

    # import materials and layers
    c4d.documents.MergeDocument(doc, elf_document_materials, c4d.SCENEFILTER_OBJECTS|c4d.SCENEFILTER_MATERIALS , None)
    obj_mat = doc.SearchObject('Materials_Duende') # find new object
    obj_mat.Remove() # delete null obj

    # ------------------------------------------------------

    # get layer
    layer = find_layer(elf_layer_objs)
    if not layer:
            return

    layer_mats = find_layer(elf_layer_mats)
    if not layer:
        gui.MessageDialog('this scene does not have the needed material layer.')
        return
    # get mats
    mats            = doc.GetMaterials()
    mats_character  = []
    for mat in mats:
        if  mat[c4d.ID_LAYER_LINK]:
            if mat[c4d.ID_LAYER_LINK].GetName() == elf_layer_mats:
                mats_character.append(mat)

    # ------------------------------------------------------

    # import tags from external document *delete them in child ops
    c4d.documents.MergeDocument(doc, elf_document_tags, c4d.SCENEFILTER_OBJECTS|c4d.SCENEFILTER_MATERIALS , None)
    obj_tag_pants2  = doc.SearchObject('Pants2')
    obj_tag_body    = doc.SearchObject('Body')

    # ------------------------------------------------------

    # add all objs in layer
    for obj in obj_list:
        obj[c4d.ID_LAYER_LINK] = layer

    # ------------------------------------------------------

    # main parent commands
    main_parent = null
    add_redshift_tag(main_parent, layer, True, True, 4, 6,0,0,0,0,0,0,1,40)  # add main redshift tag
    obj_list.remove(null)                                  # remove main parent from obj list

    # ------------------------------------------------------

    # add_redshift_tag(obj,layer,geometry,tessellation,tess_min,tess_max,displacement,dis_max,dis_scale,dis_autobump,reference,ref_source,obj_id,obj_id_value) # add redshift tag

    # ------------------------------------------------------

    # children ops
    for obj in obj_list:
        if obj.GetName() == elf01_nameslist[0]: # T_shirt
            display_color(obj,elf_color_lightblue) # display color
            addTexTag(obj, layer, find_mat(mats_character,elf_matslist[5]), TAG_TEXTURE_PROJECTION_UVW,'') # add material - Elf_Cloth Light Blue
            add_redshift_tag(obj,layer,0,0,0,0,False,0,0,0,True,True,0,0) # add redshift tag
        
        elif obj.GetName() == elf01_nameslist[1]: # Pants
            display_color(obj,elf_color_blue) # display color
            addTexTag(obj, layer, find_mat(mats_character,elf_matslist[12]), TAG_TEXTURE_PROJECTION_UVW,'') # add material - Elf_Hair Blue
            add_redshift_tag(obj,layer,0,0,0,0,False,0,0,0,True,True,0,0) # add redshift tag
        
        elif obj.GetName() == elf01_nameslist[2]: # Nose
            display_color(obj,elf_color_red) # display color
            addTexTag(obj, layer, find_mat(mats_character,elf_matslist[14]), TAG_TEXTURE_PROJECTION_UVW,'') # add material - Elf_Nose Red
            add_redshift_tag(obj,layer,0,0,0,0,False,0,0,0,True,True,0,0) # add redshift tag
        
        elif obj.GetName() == elf01_nameslist[3]: # Lice_R_5
            display_color(obj,elf_color_white) # display color
            addTexTag(obj, layer, find_mat(mats_character,elf_matslist[0]), TAG_TEXTURE_PROJECTION_UVW,'') # add material - Elf_Boots Laces
            add_redshift_tag(obj,layer,0,0,0,0,False,0,0,0,True,True,0,0) # add redshift tag

        elif obj.GetName() == elf01_nameslist[4]: # Lice_R_4
            display_color(obj,elf_color_white) # display color
            addTexTag(obj, layer, find_mat(mats_character,elf_matslist[0]), TAG_TEXTURE_PROJECTION_UVW,'') # add material - Elf_Boots Laces
            add_redshift_tag(obj,layer,0,0,0,0,False,0,0,0,True,True,0,0) # add redshift tag  

        elif obj.GetName() == elf01_nameslist[5]: # Lice_R_3
            display_color(obj,elf_color_white) # display color
            addTexTag(obj, layer, find_mat(mats_character,elf_matslist[0]), TAG_TEXTURE_PROJECTION_UVW, '') # add material - Elf_Boots Laces
            add_redshift_tag(obj,layer,0,0,0,0,False,0,0,0,True,True,0,0) # add redshift tag

        elif obj.GetName() == elf01_nameslist[6]: # Lice_R_2
            display_color(obj,elf_color_white) # display color
            addTexTag(obj, layer, find_mat(mats_character,elf_matslist[0]), TAG_TEXTURE_PROJECTION_UVW,'') # add material - Elf_Boots Laces
            add_redshift_tag(obj,layer,0,0,0,0,False,0,0,0,True,True,0,0) # add redshift tag

        elif obj.GetName() == elf01_nameslist[7]: # Lice_R_1
            display_color(obj,elf_color_white) # display color
            addTexTag(obj, layer, find_mat(mats_character,elf_matslist[0]), TAG_TEXTURE_PROJECTION_UVW,'') # add material - Elf_Boots Laces
            add_redshift_tag(obj,layer,0,0,0,0,False,0,0,0,True,True,0,0) # add redshift tag

        elif obj.GetName() == elf01_nameslist[8]: # Lice_L_5
            display_color(obj,elf_color_white) # display color
            addTexTag(obj, layer, find_mat(mats_character,elf_matslist[0]), TAG_TEXTURE_PROJECTION_UVW,'') # add material - Elf_Boots Laces
            add_redshift_tag(obj,layer,0,0,0,0,False,0,0,0,True,True,0,0) # add redshift tag

        elif obj.GetName() == elf01_nameslist[9]: # Lice_L_4
            display_color(obj,elf_color_white) # display color
            addTexTag(obj, layer, find_mat(mats_character,elf_matslist[0]), TAG_TEXTURE_PROJECTION_UVW,'') # add material - Elf_Boots Laces
            add_redshift_tag(obj,layer,0,0,0,0,False,0,0,0,True,True,0,0) # add redshift tag
        
        elif obj.GetName() == elf01_nameslist[10]: # Lice_L_3
            display_color(obj,elf_color_white) # display color
            addTexTag(obj, layer, find_mat(mats_character,elf_matslist[0]), TAG_TEXTURE_PROJECTION_UVW,'') # add material - Elf_Boots Laces
            add_redshift_tag(obj,layer,0,0,0,0,False,0,0,0,True,True,0,0) # add redshift tag

        elif obj.GetName() == elf01_nameslist[11]: # Lice_L_2
            display_color(obj,elf_color_white) # display color
            addTexTag(obj, layer, find_mat(mats_character,elf_matslist[0]), TAG_TEXTURE_PROJECTION_UVW,'') # add material - Elf_Boots Laces
            add_redshift_tag(obj,layer,0,0,0,0,False,0,0,0,True,True,0,0) # add redshift tag
 
        elif obj.GetName() == elf01_nameslist[12]: # Lice_L_1
            display_color(obj,elf_color_white) # display color
            addTexTag(obj, layer, find_mat(mats_character,elf_matslist[0]), TAG_TEXTURE_PROJECTION_UVW,'') # add material - Elf_Boots Laces
            add_redshift_tag(obj,layer,0,0,0,0,False,0,0,0,True,True,0,0) # add redshift tag

        elif obj.GetName() == elf01_nameslist[13]: # Hat2
            display_color(obj,elf_color_lightblue) # display color
            addTexTag(obj, layer, find_mat(mats_character,elf_matslist[3]), TAG_TEXTURE_PROJECTION_UVW,'') # add material - Tree_Ribbon and Gloves Cloth
            add_redshift_tag(obj,layer,0,0,0,0,False,0,0,0,True,True,True,44) # add redshift tag

        elif obj.GetName() == elf01_nameslist[24]: # Hat
            display_color(obj,elf_color_lightblue) # display color
            addTexTag(obj, layer, find_mat(mats_character,elf_matslist[3]), TAG_TEXTURE_PROJECTION_UVW,'') # add material - Tree_Ribbon and Gloves Cloth
            add_redshift_tag(obj,layer,0,0,0,0,False,0,0,0,True,True,True,44) # add redshift tag

        elif obj.GetName() == elf01_nameslist[14]: # Hand_R
            display_color(obj,elf_color_lightblue) # display color
            addTexTag(obj, layer, find_mat(mats_character,elf_matslist[9]), TAG_TEXTURE_PROJECTION_UVW,'') # add material - Elf_Hands
            add_redshift_tag(obj,layer,True,True,0,3,False,0,0,0,True,True,True,45) # add redshift tag

        elif obj.GetName() == elf01_nameslist[15]: # Hand_L
            display_color(obj,elf_color_lightblue) # display color
            addTexTag(obj, layer, find_mat(mats_character,elf_matslist[9]), TAG_TEXTURE_PROJECTION_UVW,'') # add material - Elf_Hands
            add_redshift_tag(obj,layer,True,True,0,3,False,0,0,0,True,True,True,45) # add redshift tag

        elif obj.GetName() == elf01_nameslist[16]: # Hair
            display_color(obj,elf_color_blue) # display color
            addTexTag(obj, layer, find_mat(mats_character,elf_matslist[12]), TAG_TEXTURE_PROJECTION_UVW,'') # add material - Elf_Hair Blue
            add_redshift_tag(obj,layer,0,0,0,0,False,0,0,0,True,True,True,43) # add redshift tag

        elif obj.GetName() == elf01_nameslist[17]: # Button
            display_color(obj,elf_color_blue) # display color
            addTexTag(obj, layer, find_mat(mats_character,elf_matslist[8]), TAG_TEXTURE_PROJECTION_UVW,'') # add material - Elf_Clorh Blue
            add_redshift_tag(obj,layer,0,0,0,0,False,0,0,0,True,True,0,0) # add redshift tag

        elif obj.GetName() == elf01_nameslist[18]: # Boot_R
            display_color(obj,elf_color_black) # display color
            addTexTag(obj, layer, find_mat(mats_character,elf_matslist[1]), TAG_TEXTURE_PROJECTION_UVW,'') # add material - Elf_Boots
            add_redshift_tag(obj,layer,0,0,0,0,False,0,0,0,True,True,0,0) # add redshift tag

        elif obj.GetName() == elf01_nameslist[19]: # Boot_L
            display_color(obj,elf_color_black) # display color
            addTexTag(obj, layer, find_mat(mats_character,elf_matslist[1]), TAG_TEXTURE_PROJECTION_UVW,'') # add material - Elf_Boots
            add_redshift_tag(obj,layer,0,0,0,0,False,0,0,0,True,True,0,0) # add redshift tag

        elif obj.GetName() == elf01_nameslist[20]: # Body
            obj = make_editable(obj)
            display_color(obj,elf_color_cyan) # display color
            tag = tag_copy(obj_tag_body, c4d.Tpolygonselection,obj) # copy polygon selection tags
            addTexTag(obj, layer, find_mat(mats_character,elf_matslist[15]), TAG_TEXTURE_PROJECTION_UVW,tag.GetName()) # add material - Elf_Body
            addTexTag(obj, layer, find_mat(mats_character,elf_matslist[4]), TAG_TEXTURE_PROJECTION_UVW,'') # add material - Elf_Arms and Legs Cloth
            add_redshift_tag(obj,layer,0,0,0,0,False,0,0,0,True,True,True,42) # add redshift tag
            tag_copy(obj_tag_body, c4d.Tvertexmap,obj) # copy polygon selection tags

        elif obj.GetName() == elf01_nameslist[21]: # Mouth_geo
            display_color(obj,elf_color_black) # display color
            addTexTag(obj, layer, find_mat(mats_character,elf_matslist[10]), TAG_TEXTURE_PROJECTION_UVW,'') # add material - Elf_Eyes and Mouth
            add_redshift_tag(obj,layer,0,0,0,0,False,0,0,0,True,True,0,0) # add redshift tag

        elif obj.GetName() == elf01_nameslist[22]: # Eye_R_geo
            display_color(obj,elf_color_black) # display color
            addTexTag(obj, layer, find_mat(mats_character,elf_matslist[10]), TAG_TEXTURE_PROJECTION_UVW,'') # add material - Elf_Eyes and Mouth
            add_redshift_tag(obj,layer,0,0,0,0,False,0,0,0,True,True,True,41) # add redshift tag

        elif obj.GetName() == elf01_nameslist[23]: # Eye_L_geo
            display_color(obj,elf_color_black) # display color
            addTexTag(obj, layer, find_mat(mats_character,elf_matslist[10]), TAG_TEXTURE_PROJECTION_UVW,'') # add material - Elf_Eyes and Mouth
            add_redshift_tag(obj,layer,0,0,0,0,False,0,0,0,True,True,True,41) # add redshift tag

        else:
            None

    # ------------------------------------------------------

    # remove imported objects
    obj_tag_body.Remove()
    obj_tag_pants2.Remove()

    # ------------------------------------------------------

    c4d.EventAdd()

    print 'Elf 01 imported successfully.'

# Execute main()
if __name__=='__main__':
    main()