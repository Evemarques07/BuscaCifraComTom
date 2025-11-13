#!/usr/bin/env python3

import sys
import re
import os
import webbrowser
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted, PageBreak, KeepTogether, Frame, PageTemplate
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.doctemplate import BaseDocTemplate
from reportlab.platypus.frames import Frame


NOTAS = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
NOTAS_FLAT = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
NOTAS_PORTUGUESAS = ['Dó', 'Dó#', 'Ré', 'Ré#', 'Mi', 'Fá', 'Fá#', 'Sol', 'Sol#', 'Lá', 'Lá#', 'Si']

EQUIVALENCIAS = {
    'C#': 'Db', 'Db': 'C#',
    'D#': 'Eb', 'Eb': 'D#',
    'F#': 'Gb', 'Gb': 'F#',
    'G#': 'Ab', 'Ab': 'G#',
    'A#': 'Bb', 'Bb': 'A#'
}


class CifraClubStandalone:
    
    def __init__(self):
        self.base_url = "https://www.cifraclub.com.br/"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def buscar_cifra(self, artista: str, musica: str) -> dict:
        url = f"{self.base_url}{artista}/{musica}"
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            resultado = {
                'url': url,
                'artista': self._extrair_artista(soup),
                'musica': self._extrair_musica(soup),
                'tom_original': self._extrair_tom_original(soup),
                'cifra': self._extrair_cifra(soup),
                'youtube_url': self._extrair_youtube(soup)
            }
            
            return resultado
            
        except requests.exceptions.RequestException as e:
            return {'erro': f'Erro ao buscar cifra: {str(e)}'}
        except Exception as e:
            return {'erro': f'Erro ao processar cifra: {str(e)}'}
    
    def _extrair_artista(self, soup):
        tag = soup.find('h2', class_='t3')
        return tag.text.strip() if tag else 'Desconhecido'
    
    def _extrair_musica(self, soup):
        tag = soup.find('h1', class_='t1')
        return tag.text.strip() if tag else 'Desconhecida'
    
    def _extrair_tom_original(self, soup):
        tom_span = soup.find('span', id='cifra_tom')
        if tom_span:
            link = tom_span.find('a')
            if link:
                tom = link.text.strip()
                if tom:
                    return tom
        
        pre = soup.find('pre')
        if pre:
            texto = pre.text
            match = re.search(r'Tom:\s*([A-G][#b]?[m]?)', texto, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def _extrair_cifra(self, soup):
        pre = soup.find('pre')
        if pre:
            return pre.text.strip()
        return 'Cifra não encontrada'
    
    def _extrair_youtube(self, soup):
        try:
            html_text = str(soup)
            match = re.search(r'youtube\.com/watch\?v=([A-Za-z0-9_-]+)', html_text)
            if match:
                video_id = match.group(1)
                return f"https://www.youtube.com/watch?v={video_id}"
            
            match2 = re.search(r'youtu\.be/([A-Za-z0-9_-]+)', html_text)
            if match2:
                video_id = match2.group(1)
                return f"https://www.youtube.com/watch?v={video_id}"
        except:
            pass
        return None
    
    def transpor_cifra(self, cifra: str, semitons: int) -> str:
        if semitons == 0:
            return cifra
        
        linhas = cifra.split('\n')
        linhas_transpostas = []
        
        for linha in linhas:
            if self._e_linha_de_acordes(linha):
                linha_transposta = self._transpor_linha(linha, semitons)
            else:
                linha_transposta = linha
            linhas_transpostas.append(linha_transposta)
        
        return '\n'.join(linhas_transpostas)
    
    def _e_linha_de_acordes(self, linha: str) -> bool:
        linha_limpa = linha.strip()
        
        if not linha_limpa or linha_limpa.startswith('[') or len(linha_limpa) < 2:
            return False
        
        if linha.startswith('    ') and not re.match(r'^\s+[A-G][#b]?', linha):
            return False
        
        if linha_limpa.startswith('(') and linha_limpa.endswith(')'):
            return True
        
        if '  ' in linha or '\t' in linha:
            palavras = linha_limpa.split()
            if len(palavras) <= 8:
                acordes = re.findall(r'\b[A-G][#b]?[m]?[0-9]?[^\s]{0,5}\b', linha)
                if len(acordes) >= max(2, len(palavras) * 0.6):
                    return True
        
        return False
    
    def _transpor_linha(self, linha: str, semitons: int) -> str:
        padrao = r'([A-G])([#b]?)([^\s]*?)(?=\s|$|/|\))'
        
        def transpor_acorde(match):
            nota_base = match.group(1)
            acidente = match.group(2) if match.group(2) else ''
            modificador = match.group(3) if match.group(3) else ''
            
            nota_completa = nota_base + acidente.upper()
            
            nota_transposta = self._transpor_nota(nota_completa, semitons)
            
            if acidente and acidente.islower():
                if '#' in nota_transposta:
                    nota_transposta = nota_transposta
                elif nota_transposta[-1] in ['b', 'B']:
                    nota_transposta = nota_transposta[:-1] + 'b'
            
            return f"{nota_transposta}{modificador}"
        
        return re.sub(padrao, transpor_acorde, linha)
    
    def _transpor_nota(self, nota: str, semitons: int) -> str:
        nota_original = nota
        nota = nota.upper().replace('B', 'b').upper()
        
        if len(nota) > 1 and nota[1] in ['b', 'B']:
            nota = nota[0] + 'b'
        
        if nota in NOTAS:
            indice = NOTAS.index(nota)
            usar_sustenido = True
        elif nota in NOTAS_FLAT:
            indice = NOTAS_FLAT.index(nota)
            usar_sustenido = False
        else:
            return nota_original
        
        novo_indice = (indice + semitons) % 12
        
        if usar_sustenido or '#' in nota_original:
            return NOTAS[novo_indice]
        else:
            return NOTAS_FLAT[novo_indice]
    
    def calcular_semitons_entre_tons(self, tom_origem: str, tom_destino: str) -> int:
        nota_origem = tom_origem.replace('m', '').strip()
        nota_destino = tom_destino.replace('m', '').strip()
        
        nota_origem = nota_origem.upper().replace('B', 'b')
        nota_destino = nota_destino.upper().replace('B', 'b')
        
        indice_origem = None
        indice_destino = None
        
        if nota_origem in NOTAS:
            indice_origem = NOTAS.index(nota_origem)
        elif nota_origem in NOTAS_FLAT:
            indice_origem = NOTAS_FLAT.index(nota_origem)
        
        if nota_destino in NOTAS:
            indice_destino = NOTAS.index(nota_destino)
        elif nota_destino in NOTAS_FLAT:
            indice_destino = NOTAS_FLAT.index(nota_destino)
        
        if indice_origem is None or indice_destino is None:
            return 0
        
        semitons = (indice_destino - indice_origem) % 12
        
        if semitons > 6:
            semitons = semitons - 12
        
        return semitons
    
    def exibir_cifra(self, dados: dict, semitons: int = 0, tom_destino: str = None):
        if 'erro' in dados:
            print(f"\n❌ {dados['erro']}\n")
            return
        
        if tom_destino and dados.get('tom_original'):
            semitons = self.calcular_semitons_entre_tons(dados['tom_original'], tom_destino)
        
        print("\n" + "="*70)
        print(f"🎵 {dados['musica']} - {dados['artista']}")
        print("="*70)
        
        if dados.get('tom_original'):
            tom_exibir = dados['tom_original']
            if semitons != 0:
                tom_transposto = self._transpor_nota(
                    dados['tom_original'].split('m')[0], 
                    semitons
                )
                sufixo = 'm' if 'm' in dados['tom_original'] else ''
                tom_exibir = f"{tom_transposto}{sufixo}"
                print(f"Tom original: {dados['tom_original']} → Tom atual: {tom_exibir}")
                print(f"Transposição: {'+' if semitons > 0 else ''}{semitons} semitons")
            else:
                print(f"Tom: {tom_exibir}")
        
        if dados.get('youtube_url'):
            print(f"YouTube: {dados['youtube_url']}")
        
        print(f"Fonte: {dados['url']}")
        print("="*70 + "\n")
        
        cifra = dados['cifra']
        if semitons != 0:
            cifra = self.transpor_cifra(cifra, semitons)
        
        print(cifra)
        print("\n" + "="*70 + "\n")
    
    def salvar_pdf(self, dados: dict, semitons: int = 0, tom_destino: str = None, abrir_automaticamente: bool = False):
        if 'erro' in dados:
            print(f"\n❌ {dados['erro']}\n")
            return None
        
        if tom_destino and dados.get('tom_original'):
            semitons = self.calcular_semitons_entre_tons(dados['tom_original'], tom_destino)
        
        pasta_pdf = "pdf"
        if not os.path.exists(pasta_pdf):
            os.makedirs(pasta_pdf)
        
        tom_exibir = dados.get('tom_original', 'SemTom')
        if semitons != 0 and dados.get('tom_original'):
            tom_transposto = self._transpor_nota(
                dados['tom_original'].split('m')[0], 
                semitons
            )
            sufixo = 'm' if 'm' in dados['tom_original'] else ''
            tom_exibir = f"{tom_transposto}{sufixo}"
        
        nome_arquivo = f"{dados['artista']}_{dados['musica']}_{tom_exibir}.pdf"
        nome_arquivo = nome_arquivo.replace(' ', '_').replace('/', '_')
        caminho_pdf = os.path.join(pasta_pdf, nome_arquivo)
        
        cifra = dados['cifra']
        if semitons != 0:
            cifra = self.transpor_cifra(cifra, semitons)
        
        frame_width = (A4[0] - 4*cm) / 2
        frame_height = A4[1] - 7*cm
        
        frame1 = Frame(1.5*cm, 2*cm, frame_width, frame_height, id='col1', 
                      leftPadding=0, rightPadding=10, topPadding=0, bottomPadding=0)
        frame2 = Frame(1.5*cm + frame_width + 1*cm, 2*cm, frame_width, frame_height, id='col2',
                      leftPadding=10, rightPadding=0, topPadding=0, bottomPadding=0)
        
        def header_footer(canvas, doc):
            canvas.saveState()
            
            canvas.setFont('Helvetica-Bold', 14)
            title = f"{dados['musica']} - {dados['artista']}"
            canvas.drawCentredString(A4[0]/2, A4[1] - 1.5*cm, title)
            
            canvas.setFont('Helvetica', 9)
            y_pos = A4[1] - 2*cm
            
            if dados.get('tom_original'):
                if semitons != 0:
                    info_tom = f"Tom original: {dados['tom_original']} → Tom atual: {tom_exibir} ({'+' if semitons > 0 else ''}{semitons} semitons)"
                else:
                    info_tom = f"Tom: {tom_exibir}"
                canvas.drawCentredString(A4[0]/2, y_pos, info_tom)
                y_pos -= 0.4*cm
            
            if dados.get('youtube_url'):
                canvas.drawCentredString(A4[0]/2, y_pos, f"YouTube: {dados['youtube_url']}")
                y_pos -= 0.4*cm
            
            canvas.setFont('Helvetica', 8)
            canvas.drawCentredString(A4[0]/2, y_pos, f"Fonte: {dados['url']}")
            
            canvas.setFont('Helvetica', 8)
            canvas.drawCentredString(A4[0]/2, 1*cm, f"Página {doc.page}")
            
            canvas.restoreState()
        
        template = PageTemplate(id='TwoCol', frames=[frame1, frame2], onPage=header_footer)
        doc = SimpleDocTemplate(caminho_pdf, pagesize=A4,
                                rightMargin=1.5*cm, leftMargin=1.5*cm,
                                topMargin=4*cm, bottomMargin=1.5*cm)
        doc.addPageTemplates([template])
        
        story = []
        styles = getSampleStyleSheet()
        
        code_style = ParagraphStyle(
            'Code',
            parent=styles['Code'],
            fontSize=8,
            fontName='Courier',
            leftIndent=0,
            rightIndent=0,
            spaceAfter=2,
            spaceBefore=0,
            leading=10,
            keepWithNext=False
        )
        
        linhas = cifra.split('\n')
        i = 0
        while i < len(linhas):
            linha = linhas[i]
            
            if linha.strip():
                is_section = linha.strip().startswith('[')
                is_chord_line = self._e_linha_de_acordes(linha)
                
                if is_section:
                    if i > 0:
                        story.append(Spacer(1, 0.3*cm))
                    story.append(Preformatted(linha, code_style))
                elif is_chord_line and i + 1 < len(linhas) and linhas[i + 1].strip() and not linhas[i + 1].strip().startswith('['):
                    combined = linha + '\n' + linhas[i + 1]
                    story.append(KeepTogether([Preformatted(combined, code_style)]))
                    i += 1
                else:
                    story.append(Preformatted(linha, code_style))
            else:
                story.append(Spacer(1, 0.15*cm))
            
            i += 1
        
        doc.build(story)
        
        if abrir_automaticamente:
            try:
                caminho_absoluto = os.path.abspath(caminho_pdf)
                webbrowser.open(f'file:///{caminho_absoluto}')
            except:
                pass
        
        return caminho_pdf


def main():
    if len(sys.argv) < 3:
        print("Uso: python cifra_standalone.py <artista> <musica> [semitons|tom] [--pdf] [--abrir]")
        print("\nExemplos:")
        print("  python cifra_standalone.py coldplay the-scientist")
        print("  python cifra_standalone.py coldplay the-scientist 2")
        print("  python cifra_standalone.py coldplay the-scientist -3")
        print("  python cifra_standalone.py coldplay the-scientist C")
        print("  python cifra_standalone.py coldplay the-scientist D#")
        print("  python cifra_standalone.py coldplay the-scientist Cm")
        print("  python cifra_standalone.py coldplay the-scientist Bb")
        print("  python cifra_standalone.py coldplay the-scientist C --pdf")
        print("  python cifra_standalone.py coldplay the-scientist C --pdf --abrir")
        print("  python cifra_standalone.py coldplay the-scientist 2 --abrir")
        print("\nDica:")
        print("  - Use números positivos/negativos para transpor por semitons")
        print("  - Use notas (C, D, E, F, G, A, B) com # ou b para transpor para um tom específico")
        print("  - Adicione 'm' após a nota para tons menores (Cm, Dm, etc.)")
        print("  - Use --pdf para salvar em PDF na pasta /pdf")
        print("  - Use --abrir para salvar e abrir o PDF automaticamente")
        sys.exit(1)
    
    artista = sys.argv[1]
    musica = sys.argv[2]
    
    tom_destino = None
    semitons = 0
    salvar_em_pdf = False
    abrir_pdf = False
    
    if len(sys.argv) > 3:
        for i in range(3, len(sys.argv)):
            argumento = sys.argv[i].strip()
            
            if argumento.lower() == '--pdf':
                salvar_em_pdf = True
            elif argumento.lower() == '--abrir':
                salvar_em_pdf = True
                abrir_pdf = True
            else:
                try:
                    semitons = int(argumento)
                except ValueError:
                    tom_destino = argumento
    
    print(f"\n🔍 Buscando cifra de '{musica}' - {artista}...")
    
    cifra_club = CifraClubStandalone()
    dados = cifra_club.buscar_cifra(artista, musica)
    
    if tom_destino:
        cifra_club.exibir_cifra(dados, tom_destino=tom_destino)
    else:
        cifra_club.exibir_cifra(dados, semitons=semitons)
    
    if salvar_em_pdf:
        print("\n💾 Salvando em PDF...")
        if tom_destino:
            caminho = cifra_club.salvar_pdf(dados, tom_destino=tom_destino, abrir_automaticamente=abrir_pdf)
        else:
            caminho = cifra_club.salvar_pdf(dados, semitons=semitons, abrir_automaticamente=abrir_pdf)
        
        if caminho:
            if abrir_pdf:
                print(f"✅ PDF salvo e aberto: {caminho}\n")
            else:
                print(f"✅ PDF salvo em: {caminho}\n")


if __name__ == "__main__":
    main()
