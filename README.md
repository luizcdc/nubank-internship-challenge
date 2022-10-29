# Code Challenge: Autorizador

> Um sistema que autoriza ou rejeita transações seguindo regras predefinidas

Desafio de código para o exercício de *pair programming* do processo seletivo para estágio 2023 do Nubank. Leia as especificações do desafio no documento [neste link](spec-ptbr.pdf).

## Decisões de Implementação

- A solução foi implementada em Python 3.
- Optei por aplicar orientação a objetos por ser um paradigma adequado ao Python e adequadamente adaptável ao problema.
- As classes definidas são *Transaction*, *Account*, *Violation* e uma classe para cada violação.
- Cada violação herda da classe *Violation*, que herda da classe built-in *Exception*.
  - *Violations* possuem o método estático *validate()*, que indica se a violação foi infringida ou não.
- A classe *Account* possui o atributo estático *validations*, que é uma coleção de possíveis *Violations*. 
  - É possível adicionar uma nova regra ao sistema ao adicioná-la em *Account.validations*, pois o método *Account.authorize()* sempre verifica que nenhuma da coleção de *validations* é infringida.

## Estado do projeto

- [x] Função `authorize()` implementada
  - [x] Subtrai limite em caso de sucesso
  - [x] Adiciona transação ao histórico em caso de sucesso
  - [x] Verificação de `account-not-active` implementada
  - [x] Verificação de `first-transaction-above-threshold` implementada
  - [x] Verificação de `insufficient-limit` implementada
  - [ ] Verificação de `highfrequency-small-interval` implementada
  - [ ] Verificação de `doubled-transaction` implementada
- [x] Testes
  - [ ] Subtrai limite em caso de sucesso
  - [ ] Adiciona transação ao histórico em caso de sucesso
  - [x] Verificação de `account-not-active`
  - [x] Verificação de `first-transaction-above-threshold`
  - [x] Verificação de `insufficient-limit`
  - [ ] Verificação de `highfrequency-small-interval`
  - [ ] Verificação de `doubled-transaction`

## Agradecimentos

Agradeço aos Nubankers Julia Jardine, Gabriel Marinho, e Vinicius Vieira Gomes pela atenção, orientação, e gentileza ao receber as pessoas candidatas, conduzir o exercício e nos sanar as dúvidas que surgiram.

Agradeço também às pessoas candidatas que fizeram parte do meu grupo de exercício pela discussão do problema com sugestões pertinentes e compartilhamento das suas visões.
