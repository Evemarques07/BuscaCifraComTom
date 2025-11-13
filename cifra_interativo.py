#!/usr/bin/env python3

import re
from cifra_standalone import CifraClubStandalone


def main():
    print("\n" + "="*70)
    print("🎸 CIFRACLUB - Buscador de Cifras com Transposição")
    print("="*70 + "\n")
    
    artista = input("Nome do artista (ex: coldplay): ").strip().lower().replace(" ", "-")
    musica = input("Nome da música (ex: the-scientist): ").strip().lower().replace(" ", "-")
    
    if not artista or not musica:
        print("\n❌ Artista e música são obrigatórios!\n")
        return
    
    print(f"\n🔍 Buscando cifra...")
    cifra_club = CifraClubStandalone()
    dados = cifra_club.buscar_cifra(artista, musica)
    
    if 'erro' in dados:
        print(f"\n❌ {dados['erro']}\n")
        return
    
    cifra_club.exibir_cifra(dados, 0)
    
    ultimo_semitom = 0
    ultimo_tom = None
    
    while True:
        print("\n" + "="*70)
        print("Opções:")
        print("  [número] - Transpor por semitons (ex: 2, -3)")
        print("  [tom] - Transpor para um tom específico (ex: C, D#, Cm, Bb)")
        print("  [0] - Ver tom original")
        print("  [pdf] - Salvar a cifra atual em PDF")
        print("  [abrir] - Salvar e abrir o PDF automaticamente")
        print("  [s] - Sair")
        print("="*70)
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao.lower() == 's':
            print("\n👋 Até logo!\n")
            break
        
        if opcao.lower() == 'pdf':
            print("\n💾 Salvando em PDF...")
            caminho = cifra_club.salvar_pdf(dados, semitons=ultimo_semitom, tom_destino=ultimo_tom)
            if caminho:
                print(f"✅ PDF salvo em: {caminho}\n")
            continue
        
        if opcao.lower() == 'abrir':
            print("\n💾 Salvando e abrindo PDF...")
            caminho = cifra_club.salvar_pdf(dados, semitons=ultimo_semitom, tom_destino=ultimo_tom, abrir_automaticamente=True)
            if caminho:
                print(f"✅ PDF salvo e aberto: {caminho}\n")
            continue
        
        try:
            semitons = int(opcao)
            if -12 <= semitons <= 12:
                cifra_club.exibir_cifra(dados, semitons=semitons)
                ultimo_semitom = semitons
                ultimo_tom = None
            else:
                print("\n⚠️  Use valores entre -12 e 12 semitons\n")
        except ValueError:
            if opcao and re.match(r'^[A-G][#b]?m?$', opcao, re.IGNORECASE):
                cifra_club.exibir_cifra(dados, tom_destino=opcao)
                ultimo_tom = opcao
                ultimo_semitom = 0
            else:
                print("\n⚠️  Opção inválida! Use um número, um tom (ex: C, D#, Cm), 'pdf', 'abrir' ou 's' para sair\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Até logo!\n")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}\n")
