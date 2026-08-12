## Objetivo
Implementar uma barra de progresso em tempo real para que o usuário possa acompanhar visualmente o andamento do rastreamento dos objetos na Latam Cargo, considerando o total de pendentes como 100%. Isso resolve o problema atual onde a tela parece "travada" enquanto o backend está processando os dados através do Selenium.

## Alterações Propostas

### 1. Backend (Dato_Latam.py)
Precisamos mudar a forma como o rastreamento é executado. Atualmente, a rota `/resultado` bloqueia a página até que todas as consultas terminem. Vamos alterar isso para usar **Server-Sent Events (SSE)**.
Para manter simples e eficiente:
- Criaremos uma nova rota `/rastreando` que vai renderizar uma página com a barra de progresso.
- Criaremos uma rota `/stream` que vai executar o loop de `capturar_status_pendentes`, retornando `yield` a cada item processado com a contagem atual (`current`) e total (`total_pendentes`).
- Uma vez finalizado, os dados finais serão armazenados em uma variável global (em substituição à sessão baseada em cookies) e a página fará o redirecionamento automático para a rota `/resultado`, que passará a apenas exibir a tabela.

#### [MODIFY] Dato_Latam.py
Vamos incluir as importações necessárias (`Response`, `stream_with_context`, `json`) e adicionar as novas rotas. O código base da captura será transformado em um gerador (generator).

### 2. Frontend - Páginas HTML
Precisamos criar a nova página da barra de progresso e ajustar o botão "Iniciar Rastreamento" para apontar para o novo fluxo.

#### [MODIFY] templates/index.html
Alterar o link "Iniciar Rastreamento" de `<a href='/resultado'...>` para `<a href='/rastreando'...>`.

#### [NEW] templates/rastreando.html
Criar um novo arquivo HTML que exibe a barra de progresso. Usaremos JavaScript (`EventSource`) para escutar a rota `/stream` e atualizar a largura (`width`) da barra de progresso com base na fórmula `(current / total) * 100`. Ao receber o sinal de concluído, faremos um `window.location.href = '/resultado'`.

#### [MODIFY] static/style.css
Adicionar as classes CSS necessárias para estilizar a barra de progresso.

## Pontos de Atenção (User Review Required)

> [!CAUTION]
> Atualmente, os resultados (o DataFrame do Pandas) são armazenados na `session['df']` via Pickle. A sessão baseada em cookies do Flask tem um limite de **4 KB**. Se houver muitas pendências, a sessão pode estourar e dar erro. Como melhoria no novo fluxo (e para funcionar perfeitamente com SSE), vou alterar para que os resultados finais fiquem em uma variável de estado no servidor enquanto a aplicação for de uso local. Você concorda com essa mudança?

## Plano de Verificação

### Verificação Manual
1. Iniciar a aplicação localmente (`python Dato_Latam.py`).
2. Fazer o upload da planilha base no formato correto.
3. Clicar em "Iniciar Rastreamento".
4. Confirmar que a nova tela da barra de progresso é carregada imediatamente.
5. Observar a barra de progresso preenchendo de forma fluída.
6. Validar que, ao chegar em 100%, a página é redirecionada para a tabela.
7. Verificar a exportação em Excel.
