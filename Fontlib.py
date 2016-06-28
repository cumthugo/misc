from freetype import *

def to_c_str(text):
    ''' Convert python strings to null terminated c strings. '''
    cStr = create_string_buffer(text.encode(encoding='UTF-8'))
    return cast(pointer(cStr), POINTER(c_char))

def GetTextWidth(ft_eng_file,ft_chn_file,ft_size,text):
    eng_library = FT_Library()
    chn_library = FT_Library()

    eng_face    = FT_Face()
    chn_face    = FT_Face()
    pen         = FT_Vector()
    glyph       = FT_Glyph()
    bbox        = FT_BBox()
    glyph_bbox  = FT_BBox()
    num_chars   = len(text)

    pen.x = 0
    pen.y = 0
    
    error = FT_Init_FreeType( byref(eng_library) )
    error = FT_Init_FreeType( byref(chn_library) )
    error = FT_New_Face( eng_library, to_c_str(ft_eng_file), 0, byref(eng_face) )
    error = FT_New_Face( chn_library, to_c_str(ft_chn_file), 0, byref(chn_face) )
    error = FT_Set_Char_Size(eng_face, 0, ft_size * 64, 96, 96 )
    error = FT_Set_Char_Size(chn_face, 0, ft_size * 64, 96, 96 )

    eng_slot = eng_face.contents.glyph
    chn_slot = chn_face.contents.glyph

    bbox.xMin = bbox.yMin = 32000
    bbox.xMax = bbox.yMax = -32000
    
    for n in range(num_chars):
        # load glyph image into the slot (erase previous one)
        charcode = ord(text[n])
        eng_index = FT_Get_Char_Index( eng_face, charcode )
        chn_index = FT_Get_Char_Index( chn_slot, charcode )

        if eng_index != 0 or (eng_index == 0 and chn_index == 0): #use english slot
            FT_Load_Glyph( eng_face, eng_index, FT_LOAD_DEFAULT )
            FT_Get_Glyph(eng_slot,byref(glyph))
            FT_Glyph_Get_CBox(glyph,3,byref(glyph_bbox))

            # increment pen position
            pen.x += (eng_slot.contents.advance.x/64)
            pen.y += (eng_slot.contents.advance.y/64)
        else:
            FT_Load_Glyph( chn_slot, chn_index, FT_LOAD_DEFAULT )
            FT_Get_Glyph(chn_slot,byref(glyph))
            FT_Glyph_Get_CBox(glyph,3,byref(glyph_bbox))

            # increment pen position
            pen.x += (chn_slot.contents.advance.x/64)
            pen.y += (chn_slot.contents.advance.y/64)

        glyph_bbox.xMin += pen.x
        glyph_bbox.xMax += pen.x

        if glyph_bbox.xMin < bbox.xMin:
            bbox.xMin = glyph_bbox.xMin
	if glyph_bbox.xMax > bbox.xMax:
	    bbox.xMax = glyph_bbox.xMax

    if bbox.xMin > bbox.xMax:
        bbox.xMin = bbox.xMax = 0

    FT_Done_Face(eng_face)
    FT_Done_Face(chn_face)
    FT_Done_FreeType(eng_library)
    FT_Done_FreeType(chn_library)
    
    print bbox.xMin
    print bbox.xMax
    return bbox.xMax
