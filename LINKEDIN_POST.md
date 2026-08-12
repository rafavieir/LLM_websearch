# LinkedIn Post Draft

Montei um projetinho de homelab pra testar uma ideia que acho bem massa:

e se uma IA local nao respondesse so com o que ja "sabe", mas pesquisasse
primeiro, juntasse as evidencias e criasse a propria ideia em cima do que
encontrou?

Usei Python + Ollama + Qwen rodando local/VPS, com uma ferramenta de websearch
integrada.

O fluxo ficou assim:

1. eu faco uma pergunta;
2. o agente entende quando precisa de informacao atual;
3. ele pesquisa na web;
4. o modelo gera uma ideia propria baseada nos resultados;
5. depois ele responde usando essa ideia e as fontes encontradas.

Usei Ollama pra manter o ambiente local, Qwen por ser leve pra esse tipo de
homelab, Python pela facilidade de integrar tudo, e ddgs pra fazer a busca web
sem depender de uma API paga.

E pequeno, mas mostra bem o caminho que venho explorando: IA local + ferramentas
+ contexto + um passo de raciocinio antes da resposta.

Repo: <cole aqui o link do GitHub>

#Homelab #Python #Ollama #Qwen #IA #LLM #Automacao
