import os
import subprocess

try:
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
except ImportError:
    subprocess.check_call(['pip', 'install', 'python-docx'])
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()

# Page 1
p = doc.add_paragraph('Mənzil alqı satqısı barədə')
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p = doc.add_paragraph('MÜQAVİLƏ № AS - 06/13/03/2026')
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p = doc.add_paragraph('" 13" mart 2026-ci il')
p.alignment = WD_ALIGN_PARAGRAPH.RIGHT

p = doc.add_paragraph(
    "Bundan sonra Satıcı adlandırılacaq Məmmədova Nəzakət Mirzə qızının "
    "(Ş/V AZE13129263, FİN:4UN2V5F) nümayəndəsi Rzayev Asif Vasif oğlu "
    "(Ş/V AA0358927, FİN:2V40HFN) şəxsində bir tərəfdən, Bundan sonra Alıcı "
    "adlandırılacaq Süleymanov Cəlil Eyvaz oğlu (Ş/V AA6138400, FİN:0VZ815H) "
    "şəxsində digər tərəfdən aşağıdakılar barədə bu müqaviləni bağladılar."
)

p = doc.add_paragraph('1.Müqavilənin predmeti')
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

p = doc.add_paragraph(
    "1.1 Bu müqavilə ilə Satıcı tərəfindən Abşeron rayonu,Xırdalan şəhəri,Sülh "
    "küçəsi ünvanında yerləşən(reyestr nömrəsi 308013158333,qeydiyyat nömrəsi "
    "1626003656, qeydiyyat tarixi 26.01.2026) torpaq sahəsində, Satıcının bilavasitə "
    "özü tərəfindən inşa edilməkdə olan yaşayış binasının 2-ci giriş 3-ci mərtəbədə "
    "ümumi sahəsi 51,45 kv.m olan 1(bir) otaqlı 111 saylı mənzili Alıcıya satır. Alıcı "
    "isə həmin mənzilin tam dəyərini bu müqavilə ilə razılaşdırılmış müddətdə "
    "ödəyir."
)

p = doc.add_paragraph("1.2 İnşa ediləcək yaşayış binası aşağıda sadalananlarla təchiz olunacaq;")
doc.add_paragraph("a) Lift")
doc.add_paragraph("b) Mərkəzi su-kanalizasiya sistemi (Mənzillərin girişinə qədər)")
doc.add_paragraph("c) Qaz (Mənzillərin girişinə qədər)")
doc.add_paragraph("d) İşıq (Mənzillərin girişinə qədər)")
doc.add_paragraph("e) Giriş qapısı")
doc.add_paragraph("f) Pəncərələr")

p = doc.add_paragraph(
    "Binanın fasadı Satıcı tərəfindən proyektə uyğun olaraq şəkilləndirilir. "
    "Gələcəkdə mənzil sahibləri tərəfindən fasada dəyişikliklərin olunmasına yol "
    "verilmir."
)

p = doc.add_paragraph('2. Tərəflərin vəzifələri')
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

p = doc.add_paragraph(
    "2.1 Satıcı inşaatda istifadə olunan materialların keyfiyyətli olmasına görə "
    "məsuliyyət daşıyır."
)

p = doc.add_paragraph(
    "2.2 Mənzilin sahəsi mənzilə daxil olan divarların mərkəzindən mərkəzinə "
    "hesablanır."
)

doc.add_page_break()

# Page 2
p = doc.add_paragraph(
    "2.3 Alıcı yaşayış binasının fasadında: paltar asmamaq, soyuducu və "
    "barmaqlıqlar quraşdırmamaq, eyvanları bağlamamaq və yaşayış binasının xarici "
    "görünüşünə xələl gətirən və ya qonşulara hər hansı bir şəkildə ziyan vura biləcək "
    "əşyaların quraşdırmamaq və hər hansı konstruktiv dəyişiklikləri etməməyi "
    "öhdəsinə götürür."
)

p = doc.add_paragraph('3. Tərəflərin hüquqları')
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

p = doc.add_paragraph(
    "3.1 Alıcı tərəfindən ödənişlərin vaxtında həyata keçirilməməsi baş verərsə "
    "Satıcı müqaviləyə birtərəfli qaydada xitam verə bilər. Bu halda Alıcıya mənzil "
    "üçün ödənilmiş vəsaitin geri qaytarılması yalnız həmin mənzil digər şəxsə "
    "satıldıqdan sonra həyata keçirilir. Bu zaman Alıcı tərəfindən Satıcıya dəymiş "
    "zərər həmin məbləğdən çıxılır. Zərərin hesablanmasında digər alıcıların "
    "maraqları da nəzərə alınır"
)

p = doc.add_paragraph(
    "3.2 Mənzillər sahiblərinə təhvil verildikdən sonra binanın saxlanılması ilə "
    "bağlı (dam örtüyünün, dəhlizlərin, girişlərin və fasadın cari təmiri, eləcə də "
    "həyətyanı sahənin və dəhlizlərin, girişlərin işıqlandırılması və təmizlənməsi) "
    "Satıcının Alıcı qarşısında mənzilin dəyərinə aid oluna biləcək heç bir öhdəçiliyi "
    "qalmır. Satıcı tərəfindən Binanın saxlanılması Satıcı və Alıcılar arasında əlavə "
    "müqavilə əsasında ödənişli əsaslarla qanunvericiliyə uyğun şəkildə həyata "
    "keçirilə bilər."
)

p = doc.add_paragraph(
    "3.3 Eləcə də təqdim olunan mənzil müqavilədə nəzərdə tutulan təchizatlarla "
    "təmin olunmadığı halda Alıcı mənzildən imtina etmək və pulunu geri tələb "
    "etmək hüququnu özündə saxlayır."
)

p = doc.add_paragraph('4. Mənzilin qiyməti və ödəniş şərtləri')
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

p = doc.add_paragraph(
    "4.1 Təqdim olunacaq mənzilin dəyəri 61740 (altmış bir min yeddi yüz qırx) "
    "manat təşkil edir. Alıcı məbləğin 61740 (altmış bir min yeddi yüz qırx) "
    "manatını nağd şəkildə ödəyir."
)

p = doc.add_paragraph('5. Fors-major')
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

p = doc.add_paragraph(
    "5.1 Tərəflər qarşısıalınmaz hallar baş verdiyi təqdirdə bu barədə 10 gün "
    "ərzində bir-birini xəbərdar etməklə məsuliyyətdən tam və ya qismən azad ola "
    "bilər."
)

p = doc.add_paragraph('6. Digər şərtlər')
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

p = doc.add_paragraph(
    "6.1 Tərəflər arasında mübahisələr əvvəlcə qarşılıqlı razılaşma yolu ilə, bu "
    "mümkün olmadıqda Azərbaycan Respublikasının qüvvədə olan qanunvericiliyi "
    "əsasında baxıla bilər."
)

doc.add_page_break()

# Page 3
p = doc.add_paragraph('7. Müqavilənin müddəti')
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

p = doc.add_paragraph(
    "7.1 Müqavilə imzalandığı gündən qüvvəyə minir və Tərəflər öz vəzifələrini "
    "yerinə yetirənə qədər öz qüvvəsində qalır."
)

p = doc.add_paragraph(
    "7.2 Bu müqaviləyə hər hansı əlavə və ya dəyişiklik edildikdə tərəflərin "
    "imzaladığı müqaviləyə əlavələr tərtib olunur."
)

p = doc.add_paragraph(
    "7.3 Bu müqavilə hər biri tərəflərdən birində qalmaq şərti ilə 2 nüsxədə tərtib "
    "olunur və eyni hüquqi qüvvəyə malikdir."
)

doc.add_paragraph("")

# Signatures Table
table = doc.add_table(rows=1, cols=2)
hdr_cells = table.rows[0].cells
hdr_cells[0].text = 'Satıcı:'
hdr_cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
hdr_cells[1].text = 'Alıcı:'
hdr_cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

row_cells = table.add_row().cells
row_cells[0].text = 'Rzayev Asif Vasif oğlu\n(Məmmədova Nəzakət Mirzə qızı\nəvəzinə Gəncə şəhər 6 saylı notariat\nofisində 11.03.2026 tarixdə verilmiş\n7E-3010 reyestr nömrəli etibarnamə\nəsasında imza etdi)'
row_cells[1].text = 'Süleymanov Cəlil Eyvaz oğlu'

row_cells = table.add_row().cells
row_cells[0].text = 'Ş/V AA6345329, FİN:1670T07'
row_cells[1].text = 'Ş/V AA6138400, FİN:0VZ815H'

row_cells = table.add_row().cells
row_cells[0].text = 'İmza: _______________________'
row_cells[1].text = 'İmza: _______________________'

row_cells = table.add_row().cells
row_cells[0].text = 'Əlaqə nömrəsi:'
row_cells[1].text = 'Əlaqə nömrəsi:'

doc.save('c:\\Users\\User\\.gemini\\antigravity\\scratch\\backend\\Contract.docx')
