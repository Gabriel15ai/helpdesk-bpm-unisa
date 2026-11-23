# Help Desk BPM — Projeto Integrador

Protótipo acadêmico de gerenciamento de chamados baseado no cenário didático do artigo da UNISA:
- AS-IS: solicitações dispersas, triagem manual e dificuldade de rastreamento.
- TO-BE: formulário único, classificação, fila responsável, atualização de status e registro da solução.

## Funcionalidades
- Cadastro de chamados com solicitante, setor, categoria, prioridade e descrição.
- Encaminhamento automático por categoria.
- Listagem, busca e filtro por status.
- Atualização para Aberto, Em andamento e Concluído.
- Exigência de solução registrada para concluir.
- Dashboard com totais por status.
- Banco SQLite.

## Executar localmente
Requer Python 3.10 ou superior.

```bash
pip install -r requirements.txt
python app.py
```
Abra http://127.0.0.1:5000

## Publicar pelo GitHub + Render
1. Crie um repositório no GitHub e envie todos os arquivos desta pasta.
2. Entre em https://render.com e crie uma conta.
3. Escolha New + > Blueprint e conecte o repositório.
4. O Render identificará o arquivo render.yaml. Confirme a criação do serviço.
5. Quando o deploy terminar, abra o endereço gerado.

## Observação acadêmica importante
Este é um protótipo demonstrativo. Os dados são inseridos para demonstração e não representam pesquisa de campo nem resultados reais. O banco SQLite local pode não ser persistente em hospedagens gratuitas que reiniciam o serviço. Para uso real, configure armazenamento persistente ou banco gerenciado.

## Relação com BPM
O sistema demonstra o fluxo TO-BE proposto no artigo: abertura por formulário único -> classificação -> encaminhamento -> execução -> registro da solução -> encerramento. Indicadores exibidos são contagens operacionais; para medir tempo de ciclo, retrabalho e satisfação em pesquisa real, seria necessário definir coleta e linha de base.
