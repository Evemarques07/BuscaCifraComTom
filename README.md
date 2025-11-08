# Cifra Club - Buscador de Cifras com Transposição

Scripts Python para buscar cifras do CifraClub e transpor tons musicais de forma simples e rápida.

## 🚀 Instalação

1. Instale as dependências:

```bash
pip install -r requirements-standalone.txt
```

Ou instale manualmente:

```bash
pip install requests beautifulsoup4
```

## 📖 Como Usar

Existem dois modos de uso:

### 1. Modo Interativo (Recomendado para iniciantes)

Execute o script interativo que guia você passo a passo:

```bash
python cifra_interativo.py
```

O script pedirá o artista, música e permitirá transpor interativamente.

### 2. Modo Linha de Comando

Para uso direto, use a sintaxe:

```bash
python cifra_standalone.py <artista> <musica> [semitons|tom]
```

Você pode transpor de duas formas:
- **Por semitons**: use números (ex: `2`, `-3`)
- **Para um tom específico**: use notas musicais (ex: `C`, `D#`, `Cm`, `Bb`)

### Exemplos

**Modo Interativo:**
```bash
python cifra_interativo.py
# Siga as instruções na tela
```

**Modo Linha de Comando:**

1. **Buscar uma cifra no tom original:**
```bash
python cifra_standalone.py coldplay the-scientist
```

2. **Transpor por semitons (+2 semitons acima):**
```bash
python cifra_standalone.py coldplay the-scientist 2
```

3. **Transpor por semitons (-3 semitons abaixo):**
```bash
python cifra_standalone.py coldplay the-scientist -3
```

4. **Transpor para um tom específico (C):**
```bash
python cifra_standalone.py coldplay the-scientist C
```

5. **Transpor para tom com sustenido (D#):**
```bash
python cifra_standalone.py coldplay the-scientist D#
```

6. **Transpor para tom com bemol (Bb):**
```bash
python cifra_standalone.py coldplay the-scientist Bb
```

7. **Transpor para tom menor (Cm):**
```bash
python cifra_standalone.py coldplay the-scientist Cm
```

8. **Outros exemplos:**
```bash
python cifra_standalone.py legiao-urbana faroeste-caboclo
python cifra_standalone.py beatles let-it-be G
python cifra_standalone.py charlie-brown-jr ceu-azul -2
python cifra_standalone.py projeto-sola isaias-53 Am
```

## 🎵 Transposição de Tons

O script permite transpor a cifra de **duas formas**:

### 1. Por Semitons (Intervalos)

Use números para subir ou descer tons:

- **Números positivos** (+1, +2, +3...): sobem o tom (mais agudo)
- **Números negativos** (-1, -2, -3...): descem o tom (mais grave)
- **0 ou omitido**: mantém o tom original

### 2. Para Tom Específico (Direto)

Use a notação musical para ir direto para um tom:

- **Notas naturais**: `C`, `D`, `E`, `F`, `G`, `A`, `B`
- **Com sustenido**: `C#`, `D#`, `F#`, `G#`, `A#`
- **Com bemol**: `Db`, `Eb`, `Gb`, `Ab`, `Bb`
- **Tons menores**: adicione `m` (ex: `Cm`, `Dm`, `F#m`, `Bbm`)

**Exemplos:**
```bash
# Tom original: F, quero em C
python cifra_standalone.py coldplay the-scientist C

# Tom original: F, quero em D#
python cifra_standalone.py coldplay the-scientist D#

# Tom original: D, quero em Am (menor)
python cifra_standalone.py beatles let-it-be Am
```

### Escala de Semitons

Para quem prefere trabalhar com intervalos:

- **+1**: meio tom acima (ex: C → C#)
- **+2**: um tom acima (ex: C → D)
- **+3**: um tom e meio acima (ex: C → D#)
- **+12**: uma oitava acima (volta ao mesmo tom)

### Exemplos Práticos de Transposição

**Por Semitons:**

| Tom Original | +2 semitons | -3 semitons |
|--------------|-------------|-------------|
| C            | D           | A           |
| G            | A           | E           |
| Am           | Bm          | F#m         |
| E7           | F#7         | C#7         |

**Para Tom Específico:**

| Tom Original | Destino | Resultado                          |
|--------------|---------|-------------------------------------|
| F            | C       | Desce 5 semitons                   |
| D            | G       | Sobe 5 semitons                    |
| Am           | Dm      | Sobe 5 semitons (mantém menor)     |
| E            | C#m     | Desce 3 semitons (para menor)      |

## 🎼 Recursos

- ✅ **Modo interativo** e **linha de comando**
- ✅ Busca cifras diretamente do CifraClub
- ✅ **Transpõe por semitons** (intervalos: +2, -3, etc.)
- ✅ **Transpõe para tom específico** (direto: C, D#, Cm, etc.)
- ✅ Suporta acordes com sustenidos (#) e bemóis (b)
- ✅ Suporta acordes complexos (7, m7, dim, aug, etc.)
- ✅ **Detecta automaticamente tom menor** (preserva o "m")
- ✅ Exibe link do YouTube quando disponível
- ✅ Interface amigável no terminal
- ✅ Leve e rápido (sem dependências pesadas)

## 🔧 Requisitos

- Python 3.6+
- Conexão com a internet

## 💡 Dicas

1. Use o nome do artista e música exatamente como aparecem na URL do CifraClub
2. Substitua espaços por hífens: "Hotel California" → "hotel-california"
3. Remova acentos: "Legião Urbana" → "legiao-urbana"
4. Para encontrar a URL correta, acesse o CifraClub pelo navegador primeiro
5. **Transpor para tom específico é mais intuitivo**: use `C`, `D#`, `Cm` em vez de calcular semitons
6. **O script detecta automaticamente o tom original** da cifra
7. **Tons menores são preservados**: se o original é menor, adicione `m` ao destino

## 📝 Notas Técnicas

**cifra_standalone.py:**
- Faz requisições HTTP diretas (sem Selenium)
- Processa HTML com BeautifulSoup
- Implementa algoritmo de transposição cromática
- Preserva formatação e letras da cifra original
- Pode ser usado via linha de comando

**cifra_interativo.py:**
- Interface amigável para usuários
- Menu interativo de transposição
- Reutiliza a lógica do cifra_standalone.py
- Ideal para quem prefere não usar linha de comando

## ⚠️ Limitações

- Depende da estrutura HTML do CifraClub (pode precisar de ajustes se o site mudar)
- Requer conexão com internet
- Não funciona offline
- Algumas cifras podem não ter todos os metadados (tom, YouTube, etc.)

## 🤝 Estrutura do Projeto

| Arquivo                      | Descrição                                           |
|------------------------------|-----------------------------------------------------|
| `cifra_standalone.py`        | Script principal com lógica de busca e transposição |
| `cifra_interativo.py`        | Interface interativa amigável                       |
| `requirements-standalone.txt`| Dependências do projeto                             |
| `README-STANDALONE.md`       | Esta documentação                                   |

### Como Funcionam

- **cifra_standalone.py**: Pode ser usado diretamente via linha de comando com argumentos
- **cifra_interativo.py**: Importa e usa a classe `CifraClubStandalone` em modo interativo

## 📄 Exemplo de Saída

**Modo Interativo:**
```
======================================================================
🎸 CIFRACLUB - Buscador de Cifras com Transposição
======================================================================

Nome do artista (ex: coldplay): coldplay
Nome da música (ex: the-scientist): the-scientist

🔍 Buscando cifra...

======================================================================
🎵 The Scientist - Coldplay
======================================================================
Tom: Dm
YouTube: https://www.youtube.com/watch?v=RB-RcX5DS5A
Fonte: https://www.cifraclub.com.br/coldplay/the-scientist
======================================================================

[Primeira Parte]

Dm7             C9
    Come up to meet you
              G
Tell you I'm sorry
...

======================================================================
Opções:
  [número] - Transpor por semitons (ex: 2, -3)
  [tom] - Transpor para um tom específico (ex: C, D#, Cm, Bb)
  [0] - Ver tom original
  [s] - Sair
======================================================================

Escolha uma opção: C
```

**Modo Linha de Comando:**
```
🔍 Buscando cifra de 'the-scientist' - coldplay...

======================================================================
🎵 The Scientist - Coldplay
======================================================================
Tom original: Dm → Tom atual: Em
Transposição: +2 semitons
YouTube: https://www.youtube.com/watch?v=RB-RcX5DS5A
Fonte: https://www.cifraclub.com.br/coldplay/the-scientist
======================================================================

[Primeira Parte]

Em7             C9
    Come up to meet you
              G
Tell you I'm sorry
...
```

## 🐛 Solução de Problemas

**Erro "Não foi possível resolver a importação":**
```bash
pip install --upgrade requests beautifulsoup4
```

**Erro "Cifra não encontrada":**
- Verifique se o nome do artista e música estão corretos
- Use hífens em vez de espaços
- Remova acentos e caracteres especiais

**Erro de conexão:**
- Verifique sua conexão com internet
- O CifraClub pode estar temporariamente indisponível
