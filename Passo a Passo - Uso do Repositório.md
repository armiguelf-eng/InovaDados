# Início
1. Card é criado no Notion e preenchido.
2. Assim que for preenchido, o usuário envia o arquivo .md anexado; o claude deve: 
	1. ler o arquivo;
	2. encontrar o card referenciado no Laboratório de inovação do Notion;
	3. Criar um diretório dentro de iniciativas com nome <nomedocard>;
	4.  Criar um diretório dentro de <nomedocard> com nome <materials>;
	5. copiar o template de card.md:
		1. adicionar à <materials>;
		2. preencher com as informações do card referenciado;
	6. Copiar o template de tasks.md:
		1.adicionar à <materials>;
		2. preencher com as informações do card referenciado;
	7. Avisar o usuário que ele pode dar push e commit;
# Fim
Ao fim da sprint:
1. O usuário avisa o claude que a sprint terminou;
2. O claude deve checar os arquivos que estão em artefatos e materials;
3. O claude deve abrir o diretório relatório, e usar o código relatorio.tex para gerar o pdf a partir de todos os arquivos .md anexados;
4. O arquivo pdf, assim que gerado, deve ser anexado à aba "artefatos" no card do Notion.
