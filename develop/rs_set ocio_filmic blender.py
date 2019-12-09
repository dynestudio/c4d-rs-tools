import c4d
from c4d import gui

# global ids
REDSHIFT_RENDERER      = 1036219
REDSHIFT_POSTFX        = 1040189
doc                    = c4d.documents.GetActiveDocument()
renderdata             = doc.GetActiveRenderData()
rdata                  = renderdata.GetData()
# ocio config ids
ocio_path              = 'Y:\\My Drive\\_FuLib\\filmic-blender-master\\config.ocio'
ocio_view_transform    = 'Filmic Log Encoding Base (sRGB)'
lut_basecontrast_path_win  = 'C:\\ProgramData\\Redshift\\Data\\LUT\\FilmicLUTs\\Filmic Base Contrast.cube'

# get redshift postfx
def GetRedshiftPostFXSettings():
    # find the active Redshift PostFX render settings
    videopost = renderdata.GetFirstVideoPost()
    while videopost:
        if videopost.GetType() == REDSHIFT_POSTFX:
            return videopost;
        videopost = videopost.GetNext()
             
    return None

def rs_ocio_filmic_setting():
    # find the Redshift video post data   
    redshift_postfx_settings = GetRedshiftPostFXSettings()
    # setting up - color management settings
    redshift_postfx_settings[c4d.REDSHIFT_POSTEFFECTS_COLORMANAGEMENT_ENABLED]                          = True
    redshift_postfx_settings[c4d.REDSHIFT_POSTEFFECTS_COLORMANAGEMENT_COMPENSATE_VIEW_TRANSFORM]        = True
    redshift_postfx_settings[c4d.REDSHIFT_POSTEFFECTS_COLORMANAGEMENT_DISPLAY_MODE]                     = 3 # OCIO view transform
    redshift_postfx_settings[c4d.REDSHIFT_POSTEFFECTS_COLORMANAGEMENT_OCIO_FILE]                        = ocio_path
    # setting up - lut settings
    redshift_postfx_settings[c4d.REDSHIFT_POSTEFFECTS_LUT_ENABLED]                        = True
    redshift_postfx_settings[c4d.REDSHIFT_POSTEFFECTS_LUT_FILE]                           = lut_basecontrast_path_win
    redshift_postfx_settings[c4d.REDSHIFT_POSTEFFECTS_LUT_LOG_INPUT]                      = False
    redshift_postfx_settings[c4d.REDSHIFT_POSTEFFECTS_LUT_APPLY_BEFORE_COLOR_MANAGEMENT]  = True
    redshift_postfx_settings[c4d.REDSHIFT_POSTEFFECTS_LUT_STRENGTH]                       = 1
    

def main():
    # get document render engine
    render_engine = rdata[c4d.RDATA_RENDERENGINE]
    # if render engine = rs do ocio filmic preset
    if render_engine == REDSHIFT_RENDERER:
        rs_ocio_filmic_setting()
    else:
        None
    #Update the scene
    c4d.EventAdd()


if __name__=='__main__':
    main()