"""Build the printable IUT-style maintenance report from REPORT.md."""
from pathlib import Path
import re
from html import escape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak, Preformatted, KeepTogether)
from reportlab.lib.utils import ImageReader

root = Path(__file__).resolve().parents[1]
out = root / 'AddressBook_Maintenance_Report.pdf'
PAGE_W, PAGE_H = A4
WIDTH = PAGE_W - 120
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyLab', fontName='Times-Roman', fontSize=11,
    leading=13.6, spaceAfter=5, splitLongWords=True))
styles.add(ParagraphStyle(name='CellLab', fontName='Times-Roman', fontSize=9.3,
    leading=11.5, splitLongWords=True))
styles.add(ParagraphStyle(name='CellHead', parent=styles['CellLab'], fontName='Times-Bold'))
styles.add(ParagraphStyle(name='CaptionLab', fontName='Times-Italic', fontSize=9,
    leading=11.5, alignment=TA_CENTER, spaceAfter=7))
styles.add(ParagraphStyle(name='CodeLab', fontName='Courier', fontSize=8.6,
    leading=11, backColor=colors.HexColor('#f5f5f5'), borderPadding=7,
    spaceBefore=4, spaceAfter=9))
styles.add(ParagraphStyle(name='CoverInstitution', fontName='Times-Bold', fontSize=16,
    leading=20, alignment=TA_CENTER, spaceAfter=5))
styles.add(ParagraphStyle(name='CoverSmall', fontName='Times-Roman', fontSize=11.5,
    leading=15.5, alignment=TA_CENTER))
styles.add(ParagraphStyle(name='CoverTitle', fontName='Times-Bold', fontSize=21,
    leading=27, alignment=TA_CENTER, spaceAfter=12))
styles.add(ParagraphStyle(name='CoverLabel', fontName='Times-Bold', fontSize=11.5,
    leading=16))
styles.add(ParagraphStyle(name='CoverValue', fontName='Times-Roman', fontSize=11.5,
    leading=16))
for name,size in [('Heading1',15), ('Heading2',11.5)]:
    styles[name].fontName='Times-Bold'; styles[name].fontSize=size
    styles[name].leading=size+4; styles[name].textColor=colors.black
    styles[name].spaceBefore=6 if name=='Heading2' else 0
    styles[name].spaceAfter=4 if name=='Heading2' else 12
    styles[name].keepWithNext=True

def markup(s):
    s=escape(s.strip())
    s=re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',s)
    s=re.sub(r'`(.*?)`',r'<font name="Courier" size="9">\1</font>',s)
    return s

def para(s,style='BodyLab'):
    return Paragraph(markup(s),styles[style])

story=[Spacer(1,8),para('ISLAMIC UNIVERSITY OF TECHNOLOGY','CoverInstitution'),
    para('Organization of Islamic Cooperation','CoverSmall'),
    para('Board Bazar, Gazipur','CoverSmall'),Spacer(1,19)]
logo=root/'assets/iut-logo.png';lw,lh=ImageReader(str(logo)).getSize();scale=min(110/lw,165/lh)
story += [Image(str(logo),width=lw*scale,height=lh*scale),Spacer(1,22),
    para('Software Maintenance Lab Final','CoverSmall'),Spacer(1,7),
    Paragraph('Software Maintenance of<br/>AddressBook Level 3',styles['CoverTitle']),
    para('Four Categories of Maintenance with Tool-Based Verification','CoverSmall'),Spacer(1,30)]
rows=[('Name','Md. Abid Shahriar'),('Student ID','210042155'),('Program','BSc in Software Engineering'),
    ('Department','Computer Science and Engineering'),('Course Code','SWE 4802'),
    ('Report Date','26 October 2026')]
cover=Table([[para(k,'CoverLabel'),para(': '+v,'CoverValue')] for k,v in rows],
    colWidths=[112,WIDTH-112],hAlign='LEFT')
cover.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),
    ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
story += [cover,Spacer(1,23),para('Submitted To','CoverLabel'),Spacer(1,4),
    para('Lutfun Nahar Lota','CoverValue'),para('Assistant Professor','CoverValue'),
    para('Department of CSE, IUT','CoverValue'),PageBreak()]

source=(root/'REPORT.md').read_text().split('<!-- report-body -->',1)[1]
lines=source.splitlines();i=0;figure=0
while i<len(lines):
    line=lines[i].strip()
    if not line:i+=1;continue
    if line=='<!-- pagebreak -->':story.append(PageBreak());i+=1;continue
    if line.startswith('```'):
        code=[];i+=1
        while i<len(lines) and not lines[i].startswith('```'):
            code.append(lines[i]);i+=1
        story.append(Preformatted('\n'.join(code),styles['CodeLab']));i+=1;continue
    im=re.match(r'!\[(.*?)\]\((.*?)\)',line)
    if im:
        alt,path=im.groups();w,h=ImageReader(str(root/path)).getSize()
        maxh=210 if ('ui-' in path or '/intellij/' in path) else (175 if 'architecture' in path else 140)
        scale=min(WIDTH/w,maxh/h);figure+=1
        story.append(KeepTogether([Spacer(1,4),Image(str(root/path),width=w*scale,height=h*scale),
            Spacer(1,4),para(f'Figure {figure}. {alt}','CaptionLab')]))
        i+=1;continue
    if line.startswith('|'):
        rows=[]
        while i<len(lines) and lines[i].strip().startswith('|'):
            row=[x.strip() for x in lines[i].strip().strip('|').split('|')]
            if not all(re.fullmatch(r'[:\- ]+',x) for x in row):rows.append(row)
            i+=1
        if len(rows[0])==2:widths=[WIDTH-45,45] if rows[0][0]=='Section' else [145,WIDTH-145]
        elif rows[0][0]=='ID':widths=[53,108,WIDTH-161]
        else:widths=[100,175,WIDTH-275]
        table=Table([[para(c,'CellHead' if n==0 else 'CellLab') for c in row]
            for n,row in enumerate(rows)],colWidths=widths,repeatRows=1,hAlign='LEFT')
        table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#eeeeee')),
            ('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),
            ('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),5),
            ('BOTTOMPADDING',(0,0),(-1,-1),5),('LINEBELOW',(0,0),(-1,0),0.65,colors.black),
            ('LINEBELOW',(0,1),(-1,-1),0.25,colors.HexColor('#cccccc'))]))
        story += [table,Spacer(1,8)];continue
    if line.startswith('## '):story.append(para(line[3:],'Heading1'));i+=1;continue
    if line.startswith('### '):story.append(para(line[4:],'Heading2'));i+=1;continue
    if re.match(r'^\d+\. ',line):story.append(para(line));i+=1;continue
    chunks=[line];i+=1
    while i<len(lines) and lines[i].strip() and not re.match(r'^(?:#|\||!\[|<!--|```|\d+\. )',lines[i].strip()):
        chunks.append(lines[i].strip());i+=1
    story.append(para(' '.join(chunks)))

def page(canvas,doc):
    canvas.saveState()
    if doc.page>1:
        canvas.setFont('Times-Roman',8.5);canvas.setFillColor(colors.HexColor('#444444'))
        canvas.drawString(60,PAGE_H-34,'SWE 4802 | Software Maintenance Lab')
        canvas.drawRightString(PAGE_W-60,PAGE_H-34,'AddressBook Level 3')
        canvas.setStrokeColor(colors.HexColor('#aaaaaa'));canvas.setLineWidth(.4)
        canvas.line(60,PAGE_H-40,PAGE_W-60,PAGE_H-40)
        canvas.drawCentredString(PAGE_W/2,29,str(doc.page-1))
    canvas.restoreState()
SimpleDocTemplate(str(out),pagesize=A4,rightMargin=60,leftMargin=60,
    topMargin=57,bottomMargin=48,title='Software Maintenance of AddressBook Level 3',
    author='Md. Abid Shahriar',subject='SWE 4802 Software Maintenance Lab Final',
    allowSplitting=True).build(story,onFirstPage=page,onLaterPages=page)
print(out)
