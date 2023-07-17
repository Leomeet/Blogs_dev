# APA - BlogsGPT

> an interactive chatbot powerd  by OpenAI and langchain to chat with your custom dataset

to have a communicative interface with your own document/data.

## Installing / Getting started

### Docker setup for vector database:

make sure that you have docker installed and running in your system (install docker- [ubuntu](https://docs.docker.com/engine/install/ubuntu/) , [windows](https://docs.docker.com/desktop/install/windows-install/) )
- navigate to ```milvus-setup``` directory
- check docker is running or not using ```systemctl status docker```  
(for windows ```docker --version```)
- inside milvus-setup run ```sudo docker compose up -d```
(it will take a few min.)
  
#### Virtual Environment  
creating a new virtual enviroment is preferred (you can use conda,virualenv etc.).

```shell
pip install -r requirements.txt
```

it willl download all the dependancies needed to run the interface

**_add your credentials to your .env file or export them in your terminal_**

```
#adding code to environment using .env
OPENAI_API_KEY=<your-key>
AWS_ACCESS_KEY_ID=<your-key>
AWS_SECRET_ACCESS_KEY=<your-key>
AWS_SESSION_TOKEN=<your-key>
```

OR

```shell
# Exporting credentials
export OPENAI_API_KEY=<your-key>
export AWS_ACCESS_KEY_ID=<your-key>
export AWS_SECRET_ACCESS_KEY=<your-key>
export AWS_SESSION_TOKEN=<your-key>
```

## running:

```shell
cd blogsGpt
streamlit run app.py
```

## Developing

#### Enable Devloper's mode
1. find ```config.ini``` file inside ```blogsgpt```
2. set ```DEV_MODE``` to ```Enable or Disable```(case sensitive) 

    ```config
    [DEV]
    DEV_MODE = Enable    
    ```
    this mode will provide amount and token information for each query made for OPENAI and a fail safe for non set enviroment variable like AWS ACCESS KEY

### Built With

- python
- streamlit
- milvus db

#### Dataset Information

a blogs dataset holding information in json format for each blog

#### Libraries

- langchain
- openai
- faiss
