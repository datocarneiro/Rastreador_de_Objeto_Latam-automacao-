document.addEventListener('DOMContentLoaded', function() {
    var exportButton = document.getElementById('exportExcelButton');

    exportButton.addEventListener('click', function() {
        // Realize uma solicitação AJAX para gerar o arquivo Excel
        var xhr = new XMLHttpRequest();
        xhr.open('GET', '/gerar_excel', true);
        xhr.responseType = 'blob';

        xhr.onload = function() {
            if (xhr.status === 200) {
                // Crie um link para fazer o download do arquivo Excel
                var blob = new Blob([xhr.response], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
                var link = document.createElement('a');
                link.href = window.URL.createObjectURL(blob);
                link.download = 'arquivo_excel.xlsx';
                link.click();
            }
        };

        xhr.send();
    });
});
