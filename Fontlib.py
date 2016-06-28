from freetype import *

def to_c_str(text):
    ''' Convert python strings to null terminated c strings. '''
    cStr = create_string_buffer(text.encode(encoding='UTF-8'))
    return cast(pointer(cStr), POINTER(c_char))

def GetTextWidth(ft_file,ft_size,text):
    library = FT_Library()
    #matrix  = FT_Matrix()
    face    = FT_Face()
    pen     = FT_Vector()
    glyph   = FT_Glyph()
    bbox    = FT_BBox()
    glyph_bbox = FT_BBox()
    num_chars = len(text)

    pen.x = 0
    pen.y = 0
    
    error = FT_Init_FreeType( byref(library) )
    error = FT_New_Face( library, to_c_str(ft_file), 0, byref(face) )
    error = FT_Set_Char_Size( face, 0, ft_size * 64, 96, 96 )

    slot = face.contents.glyph

    bbox.xMin = bbox.yMin = 32000
    bbox.xMax = bbox.yMax = -32000
    
    for n in range(num_chars):
        # load glyph image into the slot (erase previous one)
        charcode = ord(text[n])
        index = FT_Get_Char_Index( face, charcode )
        FT_Load_Glyph( face, index, FT_LOAD_DEFAULT )
        FT_Get_Glyph(slot,byref(glyph))
        FT_Glyph_Get_CBox(glyph,3,byref(glyph_bbox))

        glyph_bbox.xMin += pen.x
        glyph_bbox.xMax += pen.x

        if glyph_bbox.xMin < bbox.xMin:
            bbox.xMin = glyph_bbox.xMin
	if glyph_bbox.xMax > bbox.xMax:
	    bbox.xMax = glyph_bbox.xMax
	    
        # increment pen position
        pen.x += (slot.contents.advance.x/64)
        pen.y += (slot.contents.advance.y/64)
     
    if bbox.xMin > bbox.xMax:
        bbox.xMin = bbox.xMax = 0
    FT_Done_Face(face)
    FT_Done_FreeType(library)
    
    print bbox.xMin
    print bbox.xMax
    return bbox.xMax
