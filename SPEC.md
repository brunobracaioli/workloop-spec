# Workloop Spec

**Especificação do Workloop Agêntico**

| | |
|---|---|
| Versão | 0.1.0-rc5 (rascunho para revisão) |
| Status | Draft · Request for Comments |
| Data | 2026-08-18 |
| Autor | Bruno Bracaioli · B2 Tech · protocolo AISAC |
| URL canônica | https://workloop.b2tech.io |
| DOI | https://doi.org/10.5281/zenodo.22004648 |
| Licença | CC BY 4.0 |
| Repositório | https://github.com/brunobracaioli/workloop-spec |

## Resumo

Um **workloop agêntico** é um sistema de dois ou mais loops agênticos que interagem entre si por canais explícitos. Quando todos os participantes estão sob uma mesma autoridade de política (a organização que os criou), o workloop é **governado**, e esta especificação exige que nenhuma interação entre loops e nenhuma ação com efeito externo ocorra sem passar por um gate determinístico que impõe as políticas e regras de negócio dessa autoridade. Quando o grafo cruza a fronteira da autoridade, o workloop é **aberto** e valem regras defensivas. O documento define os termos, o invariante ("liberdade dentro do loop, gate determinístico em toda interface"), os corolários, requisitos operacionais e critérios de conformidade.

## Abstract (EN)

An **agentic workloop** is a system of two or more agentic loops that interact through explicit channels. When every participant sits under one policy authority (the organization that created them), the workloop is **governed**: no inter-loop interaction and no externally effecting action may occur without passing through a deterministic gate that enforces that authority's policies and business rules. When the graph crosses the authority boundary, the workloop is **open** and defensive rules apply. This specification defines the terms, the invariant ("freedom inside the loop, a deterministic gate at every interface"), corollaries, operational requirements and conformance criteria.

## 1. Motivação

Loops agênticos, processos em que um modelo decide ações e usa ferramentas até parar, deixaram de ser unidades isoladas. Em operação real, um loop de atendimento grava no CRM que outro loop lê; um loop de mídia publica o que outro loop comenta; um loop pede a outro que execute o que ele mesmo não pode. É nessa interação que a conformidade se perde. Dentro de um loop, prompts, skills e instruções são política *não determinística*: o modelo pode ou não obedecer. A organização precisa de um lugar onde a política é imposta por código, não pedida por prompt. Esse lugar é a interface: entre loops, e entre loop e mundo.

O vocabulário existente não cobre esse objeto. "Agent loop" descreve um loop. "Workflow agêntico" descreve um processo com passos de modelo dentro de um único runtime. "Agent mesh" descreve infraestrutura de tráfego, identidade e roteamento entre agentes. Nenhum nomeia o *sistema de loops autônomos governado por regra de negócio na interface*. **Workloop** nomeia isso, em oposição direta a workflow: workflow é o grafo acíclico que um runtime possui; workloop é o sistema de loops que interagem sob uma autoridade.

Um workloop agêntico governado é o que se costuma chamar de "empresa operada por IA", com uma precisão que o uso popular omite: a operação é agêntica; a governança é humana e determinística. Loops executam; a autoridade define políticas, envelope e escalonamento; meta-loops (DEF-14) aprimoram dentro do envelope. Esta especificação não descreve, nem permite, uma organização em que o modelo define a própria política. A tese, em duas frases: autonomia probabilística para pensar; governança determinística para agir.

## 2. Convenções e terminologia

As palavras-chave **DEVE**, **NÃO DEVE**, **DEVERIA**, **NÃO DEVERIA** e **PODE** correspondem, respectivamente, a MUST, MUST NOT, SHOULD, SHOULD NOT e MAY, conforme RFC 2119 e RFC 8174, e só têm sentido normativo quando grafadas em maiúsculas, inclusive nas flexões de número (DEVEM, PODEM).

Identificadores: `DEF-n` (definições), `INV-n` (invariante), `COR-n` (corolários), `REQ-n` (requisitos operacionais), `OPEN-n` (workloop aberto), `CONF-n` (conformidade). Referencie cláusulas por identificador.

"Modelo" designa qualquer componente cuja saída não é verificável estaticamente, tipicamente um modelo de linguagem, independentemente de sua temperatura ou de quão previsível pareça.

Seções marcadas como *informativas* não criam obrigações.

## 3. Definições

**DEF-1 · Loop agêntico.** Processo autônomo, com gatilho próprio (evento, agenda ou mensagem) e ciclo de vida próprio, em que um modelo decide iterativamente ações (incluindo uso de ferramentas e emissão de mensagens) até uma condição de parada. Pode ser durável (estado persistido entre falhas) ou não; a durabilidade não é definidora.

**DEF-2 · Autoridade de política.** A organização, ou unidade dela, que cria e opera loops e cujas políticas e regras de negócio devem ser impostas. Um participante está *sob* a autoridade quando ela pode alterá-lo, interrompê-lo e inspecioná-lo.

**DEF-3 · Canal.** Meio explícito pelo qual loops interagem: (a) mensagem direcionada; (b) evento publicado e consumido; (c) estado compartilhado *mediado*: repositório, banco, arquivo ou serviço cujo acesso passa por um mediador que aplica gate. Estado compartilhado sem mediador não é canal (ver COR-3).

**DEF-4 · Interface.** Ponto em que uma interação atravessa a fronteira de um loop ou de um workloop (DEF-13): emissão de mensagem ou evento, escrita em estado compartilhado, ou ação com efeito externo. É onde o gate reside. Não confundir com interface de programação ou de usuário: aqui, interface é a fronteira gateada de um loop ou workloop.

**DEF-5 · Ação com efeito externo.** Qualquer ação cujo efeito é observável fora do loop: mensagem enviada, registro escrito, publicação, transação, chamada a sistema de terceiros.

**DEF-6 · Gate determinístico.** Predicado computável, avaliado na interface, cujo resultado é *permitir*, *bloquear* ou *escalar*, e cujo valor é função exclusiva de estado determinístico (schema, allow-lists, autoridade efetiva da cadeia, orçamento, contagem de saltos, janela temporal, procedência) e nunca do julgamento de um modelo. Determinístico significa: mesma entrada, mesmo resultado; verificável por teste; reproduzível em auditoria.

**DEF-7 · Regra decidível na interface.** Regra de negócio cuja violação pode ser detectada por gate determinístico a partir da mensagem ou ação e do estado disponível: regras estruturais, quantitativas, de autorização, temporais e de procedência. **Regra não decidível** é a que exige interpretação semântica: adequação, veracidade, tom, promessa implícita.

**DEF-8 · Autoridade efetiva da cadeia.** Conjunto de permissões resultante da interseção das autoridades dos loops ao longo da cadeia de delegação que originou uma ação. Nunca é maior que a autoridade do originador.

**DEF-9 · Contrato de workloop (workloop contract).** Especificação da interface de um loop, ou de um workloop composto no nível do workloop (DEF-13): schemas de entrada e saída, ações com efeito externo declaradas, escopo de autoridade, orçamentos (custo, saltos, taxa) e os gates aplicáveis.

**DEF-10 · Workloop agêntico.** Sistema de dois ou mais loops agênticos que interagem por canais. PODE incluir componentes não agênticos (serviços, APIs, workflows determinísticos, mediadores), que participam de canais e interfaces sem serem loops; o termo cobre o conjunto.

**DEF-11 · Workloop agêntico governado.** Sistema de dois ou mais loops agênticos que interagem por canais explícitos (mensagem, evento ou estado compartilhado mediado), sob uma autoridade de política (a organização que os criou), em que nenhuma interação entre loops e nenhuma ação com efeito externo ocorre sem passar por gate determinístico que impõe as políticas e regras de negócio dessa autoridade.

**DEF-12 · Workloop aberto.** Workloop cujo grafo cruza a fronteira da autoridade; o operador só coloca gate nos próprios arcos e passa a exigir terminação e marcação de auto-origem em toda saída.

**DEF-13 · Workloop composto.** Workloop cujos participantes incluem outros workloops. Cada workloop participante expõe um contrato (DEF-9) no nível do workloop, não só dos seus loops. Distinguem-se três interfaces: interna (entre loops de um mesmo workloop), entre workloops (fronteira de um workloop participante) e externa (fronteira da autoridade, seção 7). O invariante e os corolários aplicam-se em todos os níveis. A autoridade de um workloop participante é subconjunto da autoridade do workloop que o contém (COR-1).

**DEF-14 · Meta-loop.** Loop agêntico cujas saídas alteram outros loops (prompts, parâmetros, modelos, conteúdo, agenda, alocação de orçamento dentro de tetos) a partir de dados do próprio workloop. Rege-se por REQ-6.

*Nota.* "Governado" e "aberto" descrevem o escopo da autoridade sobre o grafo. "Conforme" descreve a satisfação desta especificação (seção 8). Um workloop governado que viola o invariante não é conforme; continua sendo governado.

## 4. Invariante: liberdade dentro do loop, gate determinístico em toda interface

O modelo é livre dentro do loop. Nada atravessa uma interface sem gate determinístico. Em uma linha: autonomia probabilística para pensar, governança determinística para agir.

**INV-1** Toda interação entre loops DEVE ocorrer por canal explícito (DEF-3).

**INV-2** Toda interação entre loops e toda ação com efeito externo DEVE passar por ao menos um gate determinístico (DEF-6) na interface.

**INV-3** O predicado de um gate DEVE ser função exclusiva de estado determinístico e NÃO DEVE depender do julgamento de um modelo. Verificação por modelo PODE existir como camada adicional, mas não conta como gate.

**INV-4** Um gate NÃO DEVE ser contornável, desabilitável ou reescrito pelo loop que ele governa. O gate reside fora do controle do modelo (hook, mediador, proxy, política de plataforma), e NÃO DEVE existir caminho sem gate para a mesma interface.

**INV-5** A autoridade DEVE classificar suas regras de negócio em decidíveis e não decidíveis na interface (DEF-7). Regras decidíveis DEVEM ser impostas por gate. Regras não decidíveis DEVEM ser convertidas em estrutura sempre que possível (ações enumeradas, saídas tipadas, templates com variáveis validadas) e, no que restar, tratadas como probabilísticas (verificação por modelo e/ou revisão humana), com escalonamento humano obrigatório acima de limiar de impacto definido pela autoridade. Regras não decidíveis NÃO DEVEM ser declaradas como garantidas.

**INV-6** A camada determinística sozinha DEVE limitar o dano máximo do sistema (envelope): na hipótese de falha total das camadas probabilísticas, nenhuma ação fora do envelope é possível.

## 5. Corolários

**COR-1 · Atenuação de autoridade.** A autoridade efetiva de uma ação é a interseção das autoridades ao longo da cadeia (DEF-8). Um loop NÃO DEVE obter, ao delegar a outro, permissão que não possui. Gates DEVEM avaliar a autoridade efetiva da cadeia, e não apenas a do loop executor. A atenuação vale também para a hierarquia de composição (DEF-13): um workloop participante nunca tem autoridade maior que a do workloop que o contém. Isso exige que toda interação carregue a origem (COR-2).

**COR-2 · Rastreabilidade.** Toda interação DEVE carregar identificador de origem (loop originador e autoridade) e identificador de trace ponta a ponta, propagados a cada salto. Toda decisão de gate DEVE ser registrada com: instante, trace, interface, gate, entrada avaliada (ou seu hash), resultado e versão da política aplicada. O log de decisões dos gates é o artefato de conformidade do sistema.

**COR-3 · Canal implícito é defeito.** Interação entre loops fora de canal gateado, por efeitos colaterais não mediados em arquivos, registros, publicações ou qualquer estado compartilhado sem mediador, é defeito de arquitetura, não integração. Sistemas conformes DEVEM mediar todo estado compartilhado por gate ou impedir o acesso direto.

## 6. Requisitos operacionais

**REQ-1 · Terminação.** Toda conversa entre loops DEVE ter orçamento de saltos e/ou de custo, e cooldown por par (origem, destino) e por assunto; gates DEVEM bloquear ou escalar quando excedidos. Loops de modelo não param sozinhos.

**REQ-2 · Procedência e contaminação.** Mensagens entre loops DEVEM separar dado de instrução por estrutura tipada. Conteúdo originado fora da autoridade DEVE carregar rótulo de procedência, e gates PODEM restringir ações a jusante na presença de conteúdo assim rotulado. Gates não detectam injeção; limitam o que ela alcança.

**REQ-3 · Idempotência e concorrência.** Ações com efeito externo DEVEM ser idempotentes ou protegidas por chave de idempotência. Acesso concorrente a estado compartilhado DEVE ser serializado (lease ou lock) ou convergente.

**REQ-4 · Contrato publicado.** Todo loop DEVE expor seu contrato de workloop (DEF-9), e o contrato DEVE ser versionado.

**REQ-5 · Interrupção.** A autoridade DEVE poder interromper qualquer loop e qualquer canal por meio independente do modelo, e essa capacidade DEVE ser testada periodicamente.

**REQ-6 · Meta-loop e auto-aprimoramento.** Toda saída de um meta-loop (DEF-14) que altera outro loop é ação com efeito externo (DEF-5) e DEVE passar por gate. Alterações em políticas, gates, contratos ou no envelope (INV-6) NÃO DEVEM ser executadas por meta-loop; DEVEM passar por uma interface de mudança de política, com autoridade humana, versionamento e registro (COR-2). Auto-aprimoramento é permitido dentro do envelope; o envelope não se automodifica. Um meta-loop NÃO DEVE alterar os gates que o governam (INV-4).

## 7. Workloop aberto

Quando o grafo cruza a fronteira da autoridade:

**OPEN-1** O operador DEVE aplicar gate determinístico em todo arco de saída sob seu controle, tratando cada saída como potencialmente fechando um ciclo.

**OPEN-2** O operador DEVE marcar a auto-origem de toda saída: metadado fora de banda onde o meio preserva (cabeçalhos de e-mail ou HTTP, contexto de trace, trailers), marcador em banda onde não preserva; e DEVE reconhecer a própria marca na entrada, tratando-a como retorno.

**OPEN-3** O operador DEVE impor terminação (orçamento de saltos, cooldown) e DEVE monitorar o meio por recorrência (taxa, quase-duplicata), porque marcadores não sobrevivem a transformação semântica de terceiros.

**OPEN-4** O operador NÃO DEVE presumir observabilidade ponta a ponta nem confiar em gate de terceiros.

**OPEN-5** Toda saída de um workloop governado para fora da autoridade é uma interface de workloop aberto e DEVE cumprir OPEN-1 a OPEN-4.

## 8. Conformidade

**CONF-L · Loop conforme.** Um loop é conforme quando: expõe contrato versionado (REQ-4); toda saída passa por gate (INV-2, INV-3, INV-4); propaga origem e trace (COR-2); suas ações com efeito externo são idempotentes (REQ-3); respeita orçamentos (REQ-1); e pode ser interrompido por meio independente do modelo (REQ-5).

**CONF-S · Sistema conforme.** Um workloop governado é conforme quando: toda interface tem gate, nos três níveis (INV-1, INV-2, DEF-13); a classificação de regras está publicada e o envelope definido (INV-5, INV-6); gates avaliam a autoridade efetiva da cadeia e da hierarquia (COR-1); o log de decisões é completo (COR-2); não há estado compartilhado não mediado (COR-3); todo meta-loop cumpre REQ-6; e suas interfaces externas cumprem a seção 7.

**CONF-D · Declaração.** "Conforme com Workloop Spec 0.1.0" só PODE ser afirmado quando todos os DEVE aplicáveis são satisfeitos e verificáveis por evidência: testes dos gates e log de decisões.

## 9. O que não é workloop

*Informativo.*

- Um único loop agêntico, mesmo com hooks. Hooks são gates intra-loop, o precedente direto desta especificação, mas um loop não é workloop.
- Um workflow com ciclo dentro de um único runtime cujos nós não têm gatilho e ciclo de vida próprios (grafo de estados com nós de modelo, pipeline orquestrado). É workflow agêntico.
- Integração orientada a eventos sem arco decidido por modelo (sagas, ETL, automações determinísticas). Pode formar workloop; não é agêntico.
- Loops de terceiros interagindo com os seus sem que você controle a política deles. Não é governado; é workloop aberto (seção 7).
- Uma organização em que o modelo define a própria política. Está fora desta especificação.

## 10. Exemplo canônico

*Informativo.*

Uma empresa opera três loops:

- **L1 · Atendimento**: recebe mensagens (WhatsApp, DM), qualifica e grava o lead no CRM.
- **L2 · Ofertas**: lê leads qualificados, decide a oferta e envia a proposta, que pode incluir desconto.
- **L3 · Mídia**: publica conteúdo, responde comentários e encaminha interessados a L1.

**Canais.** CRM como estado compartilhado mediado (um mediador aplica gate em toda escrita e leitura); barramento de eventos (`lead.qualificado`, `oferta.enviada`, `comentario.interessado`); mensagens diretas L1→L2 para pedidos.

**Gates decidíveis.** Schema do lead; allow-list de destinatários com opt-in; teto de desconto por perfil; janela de horário; orçamento diário de mensagens; orçamento de saltos por conversa; taxa por destinatário.

**Regra não decidível convertida em estrutura.** "Não prometa o que não pode cumprir" não é decidível. L2 só envia templates aprovados com variáveis validadas (valor e prazo dentro de faixas); não escreve texto livre na interface. O que resta de semântico passa por revisão probabilística e, acima do limiar de impacto, por humano.

**Autoridade da cadeia (COR-1).** L1 não tem permissão de desconto. Se L1 pede a L2 "ofereça 30%", o gate de L2 avalia a autoridade efetiva (origem L1, sem permissão de desconto) e bloqueia ou escala. L2 concede desconto só quando a cadeia autoriza.

**Rastreabilidade (COR-2).** Um único trace liga a DM inicial, o lead no CRM e a oferta enviada; cada gate registra a decisão com a versão da política.

**Defeito (COR-3).** Se L3 lê diretamente a planilha que L1 escreve, sem mediador, é canal implícito. Correção: mediar a planilha ou substituí-la por evento.

**Interface aberta (seção 7).** Um comentário de bot de terceiros no post de L3 é entrada de fora da autoridade; REQ-2 rotula a procedência. A resposta de L3 é saída para fora da autoridade; cumpre OPEN-1 a OPEN-4.

**Composição (DEF-13).** Os três loops formam um workloop de domínio (vendas). A empresa opera outros (mídia paga, produção de conteúdo, dados) que se compõem com este; a interface entre workloops tem gate e contrato no nível do workloop, e a autoridade de cada um é subconjunto da autoridade da empresa.

**Meta-loop (DEF-14, REQ-6).** Um loop de dados lê os logs de gates e os resultados dos demais e ajusta, dentro do envelope, prompts de L1, templates ativos de L2 e horários de L3. Ao concluir que o teto de desconto deveria subir, não altera o gate: emite uma proposta para a interface de mudança de política, que um humano aprova e versiona.

## 11. Relação com trabalhos anteriores

*Informativo.*

- **Hooks de agentes de código** (por exemplo, no Claude Code): código determinístico executado em pontos do ciclo, capaz de bloquear a ação independentemente do que o modelo decidiu. É o gate intra-loop; esta especificação estende a ideia à interface entre loops.
- **Policy as code e admission control** (OPA, Cedar, admission controllers do Kubernetes): predicado determinístico avaliado fora do componente governado. Mesmo princípio de separação; aqui aplicado a regra de negócio.
- **Service mesh, agent mesh e agent gateways**: política de tráfego, identidade e roteamento entre serviços e agentes. Infraestrutura. Esta especificação trata de política de domínio na interface e é complementar.
- **Sistemas multiagente clássicos** (MAS, FIPA): comunicação e coordenação entre agentes. Esta especificação assume modelo opaco e concentra-se em enforcement.
- **Prevenção de loops em sistemas distribuídos**: RFC 3834 (respostas automáticas), contagem de saltos em SMTP, detecção de recursão em plataformas serverless, a regra do GitHub Actions para eventos gerados por `GITHUB_TOKEN`. Precedentes das cláusulas OPEN.
- **CaMeL** (Debenedetti et al., 2025): capacidades e políticas determinísticas sobre o fluxo de dados contra injeção de prompt. Precedente de REQ-2.
- **Confused deputy e atenuação de capacidades** (Hardy, 1988; modelo de capacidades de objeto). Precedente de COR-1.

## 12. Nome, licença e citação

**Nome.** "Workloop" e "workloop agêntico" são termos do protocolo AISAC (Bruno Bracaioli / B2 Tech). Use livremente, com atribuição a esta especificação. Não há marca registrada sobre o termo.

**Licença.** Este texto está licenciado sob Creative Commons Atribuição 4.0 Internacional (CC BY 4.0). Você pode copiar, redistribuir, adaptar e usar comercialmente, desde que atribua a autoria e indique alterações.

**Como citar.** Bracaioli, B. (2026). *Workloop Spec: Especificação do Workloop Agêntico* (versão 0.1.0). B2 Tech / protocolo AISAC. DOI: 10.5281/zenodo.22004648. URL canônica: https://workloop.b2tech.io. Repositório: https://github.com/brunobracaioli/workloop-spec.

## 13. Versionamento desta especificação

Esta especificação segue Semantic Versioning: **MAJOR** para mudança incompatível em definições nucleares (DEF-10 a DEF-13) ou no invariante; **MINOR** para novos requisitos ou corolários e ampliações compatíveis; **PATCH** para correções editoriais. Rascunhos usam o sufixo `-rcN`. Toda mudança é registrada em `CHANGELOG.md`.

## Apêndice A: Checklist de conformidade

| Item | Cláusula | Evidência esperada |
|---|---|---|
| Toda interação entre loops ocorre por canal explícito | INV-1 | Inventário de canais; nenhum acesso direto a estado compartilhado |
| Toda interface tem gate determinístico | INV-2 | Mapa de interfaces × gates |
| Nenhum gate depende de julgamento de modelo | INV-3 | Código dos gates; testes de determinismo |
| Gates não contornáveis pelo loop governado | INV-4 | Localização do gate fora do runtime do modelo; ausência de caminho sem gate |
| Regras classificadas; envelope definido | INV-5, INV-6 | Documento de classificação; limites do envelope |
| Gates avaliam autoridade efetiva da cadeia | COR-1 | Propagação de origem; testes de delegação bloqueada |
| Origem e trace propagados; log de decisões completo | COR-2 | Amostra de trace ponta a ponta; log com versão da política |
| Nenhum estado compartilhado não mediado | COR-3 | Auditoria de acessos |
| Orçamentos de saltos, custo e cooldown | REQ-1 | Configuração e teste de conversa que excede o orçamento |
| Dado separado de instrução; procedência rotulada | REQ-2 | Schemas de mensagem; rótulos |
| Idempotência e serialização | REQ-3 | Chaves de idempotência; leases |
| Contratos publicados e versionados | REQ-4 | Contratos por loop |
| Interrupção independente do modelo, testada | REQ-5 | Registro do teste de interrupção |
| Interfaces entre workloops têm gate e contrato no nível do workloop | DEF-13, REQ-4 | Contratos por workloop; mapa de interfaces entre workloops |
| Meta-loops só alteram dentro do envelope; mudanças de política passam pela interface humana | REQ-6 | Log de saídas do meta-loop; registro de mudanças de política com aprovador e versão |
| Interfaces externas cumprem OPEN-1 a OPEN-4 | Seção 7 | Marcação de auto-origem; monitoramento de recorrência |
