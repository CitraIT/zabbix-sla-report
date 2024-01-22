# Relatório de Disponibilidade (SLA) do Zabbix  
Este projeto é uma aplicação web para exibir a medição de SLA de Serviços no zabbix de forma gráfica e com seleção de período.  

Pré-Requisitos:  
- Docker instalado
- URL e Chave API de acesso ao Zabbix


Instalação:  
1. Clone o projeto no host docker. ex.:
```
git clone https://github.com/citrait/zabbix-sla-report.git
```  
2. Modifique o arquivo docker-compose.yml e edite as variáveis contendo o login e senha do usuário administrador conforme desejar.
```
 environment:
            - DJANGO_SUPERUSER_EMAIL=support@contoso.corp
            - DJANGO_SUPERUSER_USERNAME=admin
            - DJANGO_SUPERUSER_PASSWORD=admin
```
3. Ainda no arquivo docker-compose.yml edite a variável de CSRF (DJANGO_TRUSTED_ORIGINS) e preencha com o IP ou hostname que será usado para acessar esta aplicação (geralmente é a URL que será digitada).
```
environment:
            [...]
            - DJANGO_TRUSTED_ORIGINS=https://192.168.100.44
```
5. Faça o deploy dos containers:
```
docker compose up -d
```

6. Monitore e aguarde a inicialiação dos containers. O container webserver (nginx) inicia rápido, mas o container app precisa de mais tempo para instalar as dependencias.
```
docker compose logs -f
# pressione Control+C para parar os logs
```

7. Acesse a aplicação Web através da URL definida.
8. Realize login com o usuário e senha definidos anteriormente.
9. Insira os dados de integração com o zabbix clicando em Preferências > Integração Zabbix.
10. Crie os clientes.
11. Registre os SLA's selecionando a qual cliente pertencem. Obs.: o nome do SLA precisa corresponder exatamente como o nome de SLA cadastrado no Zabbix.
12. Tire seu relatório através do menu Relatórios > SLA por cliente.
![image](https://github.com/CitraIT/zabbix-sla-report/assets/91758384/742fdf8b-4274-462c-ab60-fcb798f4904a)


