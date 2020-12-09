Este é o projeto Final da disciplina de Sistemas Multi Agentes, ofertada pela Universidade de Brasília no semestre 1 de 2020. Disciplina ofertada pela Professora Célia Ghedini.

O projeto consiste em um sistema Multi Agente para o pareamento de usuários e alocação de potência para usuários em uma rede de acesso NOMA.


## Atenção!!
É necessário instalar o framework PADE e o MATLAB para o funcionamento do sistema.


Para a instalação do PADE:

## Documentation

PADE is well documented. You can access the documentation here: [PADE documentation](https://pade.readthedocs.io/en/latest/)

## Dependencies

PADE is developed in [Python 3.7](https://www.python.org/) and has a [Twisted](https://twistedmatrix.com/trac/) core.

## Install

#### Via Python Package Index (PyPI):
```bash
$ pip install pade
```

#### Via Github:
```bash
$ git clone https://github.com/greiufc/pade
$ cd pade
$ python setup.py install
```

See the complete process in this video: [HOW TO install PADE](https://asciinema.org/a/ELHfOxZnMUjZyLa8bITJ0AQnP)



### Para Rodar o sistema, abra um terminal no local do código e digite o comando:
```bash
$ pade start-runtime --port 2704 MAS.py
```
## Resumo do sistema:
O sistema multiagente consiste em um cenário de transmissão downlink, onde um antena transmite dados a usuários presentes na rede. No cenário proposto existem 3 usuários, o sistema multiagente deve analizar as condições de canal de cada usuário e assim parear dois dos três usuários para realizar uma transmissão não ortogonal (NOMA).
Utilizando o protocolo contract net, implementado em PADE, os usuários receberem um Call For Propose (CFP) do agente controlador, devem informar suas condições de canal, ou seja o ganho de canal em dB, sendo o ganho a oferta realizada no protocolo. O agente controlador ao receber as três ofertas deve analizar qual dos usuários formarão o par que deve atingir as maiores médias de throughput. O calculo do throughput atingível é feito em Matlab, sendo o raciocínio do agente controlador, que retorna o par de usuários selecionado e qual parcela da potência de transmissão deve ser alocada para cada um dos usuários pareados.
A imagem abaixo mostra o o funcionamento do algoritmo com os três usuários enviando propostas, e ao final o agente controlador aceita duas propostas e rejeita. As duas propostas aceitas indicam quais usuários foram pareados.

![alt tag](https://github.com/gustavoeichler/FrameworkNOMA/blob/master/MAS_Contract_Net.png)
