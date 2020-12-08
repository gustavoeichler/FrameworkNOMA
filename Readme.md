Este é o projeto Final da disciplina de Sistemas Multi Agentes, ofertada pela Universidade de Brasília no semestre 1 de 2020. Disciplina ofertada pela Professora Célia Ghedini.

O projeto consiste em um sistema Multi Agente para o pareamento de usuários e alocação de potência para usuários em uma rede de acesso NOMA.


Para rodar o sistema é necessário instalar o python 3.7.4, o pade e o matlab.


## Documentation

PADE is well documented. You can access the documentation here: [PADE documentation](https://pade.readthedocs.io/en/latest/)

## Dependencies

PADE is developed in [Python 3.7](https://www.python.org/) and has a [Twisted](https://twistedmatrix.com/trac/) core.

## Install

#### Via Python Package Index (PyPI):
```bash
$ pip install pade
```git reset --hard HEAD^

#### Via Github:
```bash
$ git clone https://github.com/greiufc/pade
$ cd pade
$ python setup.py install
```


#### Para rodar o sistema multiagente:
```bash
$ pade start-runtime --port 2704 MAS.py
``` 
#### Duvidas:
gustavoeichlerunb@gmail.com
