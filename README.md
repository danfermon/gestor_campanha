# Gestor de Campanha

## Sobre o projeto:
- O projeto consiste em uma campanha, na qual será realizado um sorteio de prêmios.
- O sistema será dividido em três frentes:(Um *web site de divulgação*, um *Web site com sistema integrado
para a administração da campanha* pelos usuários responsáveis e, um *Web site integrado ao sistema para cadastro
de participantes da promoção e sorteios*).

## Site de Divulgação Promocional:
- O Site consistirá, em uma página web, no formato landpage, que conterá as informações,
para o público em geral, sobre a promoção bem como a participação dos sorteios da campanha.

## Site de Gerenciamento da Campanha:
- ...

## Site de Cadastro de Participantes:
- ...

## Técnologias utilizadas no desenvolvimento:
- Linux Ubuntu - https://ubuntu.com/
- Python - (V.: Python 3.12.3) - https://www.python.org/
- Django - (V.: 5.2.3) - https://www.djangoproject.com/
- Django Rest Framework - https://www.django-rest-framework.org/
- PostgresSql - https://www.postgresql.org/
- Redis - https://app.redislabs.com/#/

## Dependências:

- Framework de desenvolvimento: 
    - Django : python3 -m pip install Django

- Para manipulação de imagens:
    - Pillow : python3 -m pip install Pillow
    - opencv : pip install opencv-python

- Para reqisições web:
    - Requests : pip install requests 

- Para análise de Dados:
    - Pandas : pip install pandas
    - Nmpy : pip install numpy
    - matplotlib pip install matplotlib


- Para comunicação com o Banco de Dados PostgresSql:
    - psycopg2-binary : pip install psycopg2-binary


## como rodar o projeto:
- 1 > Criar uma pasta para o projeto;
- 2 > Criar um ambiente virtual para colocar a o Django e as demais dependências - No meu pc chamei o ambiente de Dev;
- 3 > Clonar esse repositório : '''git clone https://github.com/DanatiellyCP/gestor_campanhax.git''';
- 4 > Instale todas as dependências mencionadas acima.
- 5 > No terminal abra a pasta do progeto
    - '''cd Pasta_Do_Projeto/campaign-manager''';
    - ative o ambiente virtual que foi criado : '''source dev/bin/activate'''
- 6 > Por fim suba o servidor local do django: '''python3 manage.py runserver'''

## Rodando o arquivo requirements.txt
- para instalar as dependencias necessárias do projeto, rode esse comando no terminal:
- pip install -r requirements.txt
- Dica o arquivo : requirements-prod.txt - tem as libs mais importantes para conseguir rodar localmente.



## Arquitetura do projeto:

'''
.
├── gestor_campanha
│ ├── README.md
│ ├── cupons
│ ├── db.sqlite3
│ ├── gestor_campanha
│ ├── lib64 -> lib
│ ├── manage.py
│ ├── media
│ ├── participantes
│ ├── procfile
│ ├── pyvenv.cfg
│ ├── requirements-prod.txt
│ ├── requirements.txt
│ ├── share
│ ├── skus_validos
│ ├── static
│ ├── staticfiles
│ ├── usuarios
│ └── utils
└── venv
    ├── bin
    ├── include
    ├── lib
    ├── lib64 -> lib
    └── pyvenv.cfg
'''
## Documentação:
- ... em andamento 🚀🛠️
