# BotSheets

Pacote para integração de RPA com planilhas privadas do google sheets

## Instalação:
 ```bash
 pip install botsheets
 ```

## Exemplo de uso:
```python
from botsheets import Gsheets
url_sheet = 'https://docs.google.com/spreadsheets/d/<sheetid>/...'
gsh = Gsheets()
# Na variavel ambiente solicitada no terminal informe o caminho do arquivo json com as credenciais de acesso obtida no google console
gsh.login()
gsh.acess_spreadsheet(url_sheet)
gsh.set_sheet_name('Página1')
print(gsh.get_all_records())
gsh.set_sheet_name('Página2')
print(gsh.get_all_records())
gsh.clear_sheet()
```