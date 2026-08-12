## Objetivo
Facilitar a vida do usuário permitindo que ele baixe o modelo da planilha base diretamente pela interface web (página inicial) da aplicação. O arquivo a ser baixado já existe e está localizado em `modelo/base_rastreamento.xlsx`.

## Alterações Propostas

### 1. Backend (Dato_Latam.py)
Precisamos de uma nova rota (endpoint) que sirva o arquivo Excel do modelo sempre que solicitada.

#### [MODIFY] Dato_Latam.py
Adicionaremos a nova rota `/download_modelo`:
```python
@app.route('/download_modelo')
def download_modelo():
    return send_file(
        'modelo/base_rastreamento.xlsx', 
        as_attachment=True, 
        download_name='base_rastreamento.xlsx'
    )
```

### 2. Frontend (Páginas HTML e Estilos CSS)
Vamos incluir um botão claro e visível na página inicial, na seção onde explicamos o layout da planilha base.

#### [MODIFY] templates/index.html
Na `div` com classe `paragrafo1`, logo após os itens explicativos (abaixo de `✅ Arquivo na extensão ".xlsx"`), inseriremos o botão:
```html
<a href='/download_modelo'><button type="button" class="botao-download">Baixar Planilha Modelo</button></a>
```

#### [MODIFY] static/style.css
Adicionaremos ou ajustaremos a classe `.botao-download` para que ela fique esteticamente parecida com os botões já existentes na aplicação, com uma cor de destaque agradável, garantindo a mesma identidade visual.

## Pontos de Atenção (User Review Required)
- **Localização do Botão:** O local sugerido é na seção "Layout planilha base:" (logo abaixo das instruções). Está de acordo ou prefere o botão mais abaixo, perto do "Consultar Pendentes"?

## Plano de Verificação

### Verificação Manual
1. Abrir a aplicação local (`python Dato_Latam.py`).
2. Acessar a página inicial.
3. Observar se o botão "Baixar Planilha Modelo" está visível e estilizado corretamente.
4. Clicar no botão e verificar se o download do arquivo `base_rastreamento.xlsx` inicia imediatamente e não apresenta erros no console.
5. Abrir o arquivo baixado para garantir que não está corrompido.
