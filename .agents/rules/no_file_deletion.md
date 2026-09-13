# Regra: Proibição de Deleção de Arquivos

- **NUNCA** execute comandos de deleção de arquivos ou diretórios (como `rm`, `rmdir`, `del`, `erase`, `unlink`, `Remove-Item`, `git rm`, etc.).
- Se a solicitação do usuário envolver remover ou deletar um arquivo do projeto, informe ao usuário que a deleção de arquivos está bloqueada pelas regras e pelo hook de segurança do projeto.
