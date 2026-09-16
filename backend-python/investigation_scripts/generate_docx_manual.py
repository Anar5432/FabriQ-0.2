import zipfile

def generate_docx(filename):
    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>"""

    rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""

    doc_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>"""

    styles_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Times New Roman" w:eastAsia="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
        <w:sz w:val="24"/>
        <w:szCs w:val="24"/>
      </w:rPr>
    </w:rPrDefault>
    <w:pPrDefault>
      <w:pPr>
        <w:spacing w:after="0" w:line="360" w:lineRule="auto"/>
      </w:pPr>
    </w:pPrDefault>
  </w:docDefaults>
</w:styles>"""

    doc_xml_start = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>"""
  
    doc_xml_end = """
    <w:sectPr>
      <w:pgSz w:w="11906" w:h="16838"/>
      <w:pgMar w:top="1134" w:right="850" w:bottom="1134" w:left="1701" w:header="720" w:footer="720" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>"""

    def esc(t):
        return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

    doc_xml = doc_xml_start

    def add_p(text, align=None, indent=None, bold=False, italic=False, page_break=False, space_before=False, tab_pos=None):
        nonlocal doc_xml
        pPr = ""
        tags = []
        if align:
            tags.append(f'<w:jc w:val="{align}"/>')
        if indent == "first":
            tags.append('<w:ind w:firstLine="709"/>')
        elif indent == "list":
            tags.append('<w:ind w:left="709"/>')
            
        if space_before:
            tags.append('<w:spacing w:before="240"/>')

        if tab_pos:
            tags.append(f'<w:tabs><w:tab w:val="left" w:pos="{tab_pos}"/></w:tabs>')

        if tags:
            pPr = f"<w:pPr>{''.join(tags)}</w:pPr>"
            
        br_pb = '<w:br w:type="page"/>' if page_break else ''
        b_tag = '<w:b/>' if bold else ''
        i_tag = '<w:i/>' if italic else ''
        rPr_inner = f"{b_tag}{i_tag}"
        rPr = f"<w:rPr>{rPr_inner}</w:rPr>" if rPr_inner else ""
        
        runs = []
        if page_break:
             runs.append(f"<w:r>{br_pb}</w:r>")
             
        parts = text.split("[TAB]")
        for idx, part in enumerate(parts):
            if idx > 0:
                runs.append(f'<w:r>{rPr}<w:tab/></w:r>')
            runs.append(f'<w:r>{rPr}<w:t xml:space="preserve">{esc(part)}</w:t></w:r>')
            
        doc_xml += f"\n    <w:p>{pPr}{''.join(runs)}</w:p>"

    # Page 1
    add_p("Mənzil alqı satqısı barədə", align="center", italic=True)
    add_p("MÜQAVİLƏ № AS - 06/13/03/2026", align="center", bold=True)
    add_p('" 13" mart 2026-ci il', align="right", bold=True)
    add_p("")
    
    add_p(
        "Bundan sonra Satıcı adlandırılacaq Məmmədova Nəzakət Mirzə qızının "
        "(Ş/V AZE13129263, FİN:4UN2V5F) nümayəndəsi Rzayev Asif Vasif oğlu "
        "(Ş/V AA0358927, FİN:2V40HFN) şəxsində bir tərəfdən, Bundan sonra Alıcı "
        "adlandırılacaq Süleymanov Cəlil Eyvaz oğlu (Ş/V AA6138400, FİN:0VZ815H) "
        "şəxsində digər tərəfdən aşağıdakılar barədə bu müqaviləni bağladılar.", 
        align="both", indent="first"
    )
    
    add_p("")
    add_p("1.Müqavilənin predmeti", align="center", bold=True)
    
    add_p(
        "1.1 Bu müqavilə ilə Satıcı tərəfindən Abşeron rayonu,Xırdalan şəhəri,Sülh "
        "küçəsi ünvanında yerləşən(reyestr nömrəsi 308013158333,qeydiyyat nömrəsi "
        "1626003656, qeydiyyat tarixi 26.01.2026) torpaq sahəsində, Satıcının bilavasitə "
        "özü tərəfindən inşa edilməkdə olan yaşayış binasının 2-ci giriş 3-ci mərtəbədə "
        "ümumi sahəsi 51,45 kv.m olan 1(bir) otaqlı 111 saylı mənzili Alıcıya satır. Alıcı "
        "isə həmin mənzilin tam dəyərini bu müqavilə ilə razılaşdırılmış müddətdə "
        "ödəyir.", 
        align="both", indent="first"
    )
    
    add_p("")
    add_p("1.2 İnşa ediləcək yaşayış binası aşağıda sadalananlarla təchiz olunacaq;", align="both", indent="first")
    
    add_p("a) Lift", indent="list")
    add_p("b) Mərkəzi su-kanalizasiya sistemi (Mənzillərin girişinə qədər)", indent="list")
    add_p("c) Qaz (Mənzillərin girişinə qədər)", indent="list")
    add_p("d) İşıq (Mənzillərin girişinə qədər)", indent="list")
    add_p("e) Giriş qapısı", indent="list")
    add_p("f) Pəncərələr", indent="list")
    
    add_p("")
    add_p(
        "Binanın fasadı Satıcı tərəfindən proyektə uyğun olaraq şəkilləndirilir. "
        "Gələcəkdə mənzil sahibləri tərəfindən fasada dəyişikliklərin olunmasına yol "
        "verilmir.", 
        align="both", indent="first"
    )
    
    add_p("")
    add_p("2. Tərəflərin vəzifələri", align="center", bold=True)
    
    add_p(
        "2.1 Satıcı inşaatda istifadə olunan materialların keyfiyyətli olmasına görə "
        "məsuliyyət daşıyır.", 
        align="both", indent="first"
    )
    
    add_p("")
    add_p(
        "2.2 Mənzilin sahəsi mənzilə daxil olan divarların mərkəzindən mərkəzinə "
        "hesablanır.", 
        align="both", indent="first"
    )
    
    # Page 2
    add_p(
        "2.3 Alıcı yaşayış binasının fasadında: paltar asmamaq, soyuducu və "
        "barmaqlıqlar quraşdırmamaq, eyvanları bağlamamaq və yaşayış binasının xarici "
        "görünüşünə xələl gətirən və ya qonşulara hər hansı bir şəkildə ziyan vura biləcək "
        "əşyaların quraşdırmamaq və hər hansı konstruktiv dəyişiklikləri etməməyi "
        "öhdəsinə götürür.", 
        align="both", indent="first", page_break=True
    )
    
    add_p("")
    add_p("3. Tərəflərin hüquqları", align="center", bold=True)
    
    add_p(
        "3.1 Alıcı tərəfindən ödənişlərin vaxtında həyata keçirilməməsi baş verərsə "
        "Satıcı müqaviləyə birtərəfli qaydada xitam verə bilər. Bu halda Alıcıya mənzil "
        "üçün ödənilmiş vəsaitin geri qaytarılması yalnız həmin mənzil digər şəxsə "
        "satıldıqdan sonra həyata keçirilir. Bu zaman Alıcı tərəfindən Satıcıya dəymiş "
        "zərər həmin məbləğdən çıxılır. Zərərin hesablanmasında digər alıcıların "
        "maraqları da nəzərə alınır", 
        align="both", indent="first"
    )
    
    add_p("")
    add_p(
        "3.2 Mənzillər sahiblərinə təhvil verildikdən sonra binanın saxlanılması ilə "
        "bağlı (dam örtüyünün, dəhlizlərin, girişlərin və fasadın cari təmiri, eləcə də "
        "həyətyanı sahənin və dəhlizlərin, girişlərin işıqlandırılması və təmizlənməsi) "
        "Satıcının Alıcı qarşısında mənzilin dəyərinə aid oluna biləcək heç bir öhdəçiliyi "
        "qalmır. Satıcı tərəfindən Binanın saxlanılması Satıcı və Alıcılar arasında əlavə "
        "müqavilə əsasında ödənişli əsaslarla qanunvericiliyə uyğun şəkildə həyata "
        "keçirilə bilər.", 
        align="both", indent="first"
    )
    
    add_p("")
    add_p(
        "3.3 Eləcə də təqdim olunan mənzil müqavilədə nəzərdə tutulan təchizatlarla "
        "təmin olunmadığı halda Alıcı mənzildən imtina etmək və pulunu geri tələb "
        "etmək hüququnu özündə saxlayır.", 
        align="both", indent="first"
    )
    
    add_p("")
    add_p("4. Mənzilin qiyməti və ödəniş şərtləri", align="center", bold=True)
    
    add_p(
        "4.1 Təqdim olunacaq mənzilin dəyəri 61740 (altmış bir min yeddi yüz qırx) "
        "manat təşkil edir. Alıcı məbləğin 61740 (altmış bir min yeddi yüz qırx) "
        "manatını nağd şəkildə ödəyir.", 
        align="both", indent="first"
    )
    
    add_p("")
    add_p("5. Fors-major", align="center", bold=True)
    
    add_p(
        "5.1 Tərəflər qarşısıalınmaz hallar baş verdiyi təqdirdə bu barədə 10 gün "
        "ərzində bir-birini xəbərdar etməklə məsuliyyətdən tam və ya qismən azad ola "
        "bilər.", 
        align="both", indent="first"
    )
    
    add_p("")
    add_p("6. Digər şərtlər", align="center", bold=True)
    
    add_p(
        "6.1 Tərəflər arasında mübahisələr əvvəlcə qarşılıqlı razılaşma yolu ilə, bu "
        "mümkün olmadıqda Azərbaycan Respublikasının qüvvədə olan qanunvericiliyi "
        "əsasında baxıla bilər.", 
        align="both", indent="first"
    )
    
    # Page 3
    add_p("7. Müqavilənin müddəti", align="center", bold=True, page_break=True)
    
    add_p(
        "7.1 Müqavilə imzalandığı gündən qüvvəyə minir və Tərəflər öz vəzifələrini "
        "yerinə yetirənə qədər öz qüvvəsində qalır.", 
        align="both", indent="first"
    )
    
    add_p("")
    add_p(
        "7.2 Bu müqaviləyə hər hansı əlavə və ya dəyişiklik edildikdə tərəflərin "
        "imzaladığı müqaviləyə əlavələr tərtib olunur.", 
        align="both", indent="first"
    )
    
    add_p("")
    add_p(
        "7.3 Bu müqavilə hər biri tərəflərdən birində qalmaq şərti ilə 2 nüsxədə tərtib "
        "olunur və eyni hüquqi qüvvəyə malikdir.", 
        align="both", indent="first"
    )
    
    add_p("")
    add_p("")
    
    # Plain text signatures using tabs!
    tab_stop = 5500 # Position for the second column
    
    add_p("Satıcı:[TAB]Alıcı:", bold=True, tab_pos=tab_stop)
    add_p("")
    
    add_p("Rzayev Asif Vasif oğlu[TAB]Süleymanov Cəlil Eyvaz oğlu", tab_pos=tab_stop)
    add_p("(Məmmədova Nəzakət Mirzə qızı[TAB]", tab_pos=tab_stop)
    add_p("əvəzinə Gəncə şəhər 6 saylı notariat[TAB]", tab_pos=tab_stop)
    add_p("ofisində 11.03.2026 tarixdə verilmiş[TAB]", tab_pos=tab_stop)
    add_p("7E-3010 reyestr nömrəli etibarnamə[TAB]", tab_pos=tab_stop)
    add_p("əsasında imza etdi)[TAB]", tab_pos=tab_stop)
    add_p("")
    add_p("Ş/V AA6345329, FİN:1670T07[TAB]Ş/V AA6138400, FİN:0VZ815H", tab_pos=tab_stop)
    add_p("")
    add_p("İmza: _______________________[TAB]İmza: _______________________", tab_pos=tab_stop)
    add_p("")
    add_p("Əlaqə nömrəsi:[TAB]Əlaqə nömrəsi:", tab_pos=tab_stop)
    
    doc_xml += doc_xml_end

    with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', content_types)
        zf.writestr('_rels/.rels', rels)
        zf.writestr('word/_rels/document.xml.rels', doc_rels)
        zf.writestr('word/styles.xml', styles_xml)
        zf.writestr('word/document.xml', doc_xml)

generate_docx(r"c:\Users\User\.gemini\antigravity\scratch\backend\Contract.docx")
