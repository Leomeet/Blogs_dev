"""a configuration file for project information display"""

MODELS_JSON = {
    "models": {
        "GPT-3": {
            "name": "GPT-3",
            "info": """
                    Open ai's API with custom dataset

                    - dataset
                    ```
                    apa_blogs_data
                    ```
                    """,
            "keys": ["OPENAI_API_KEY"],
        },
        "GPT-4": {
            "name": "GPT-4",
            "info": """
                    Open ai's API with custom dataset

                    - dataset
                    ```
                    apa_blogs_data
                    ```
                    """,
            "keys": ["OPENAI_API_KEY"],
        },
        "falcon": {
            "name": "falcon",
            "conn": "https://runtime.sagemaker.us-east-1.amazonaws.com/endpoints/huggingface-pytorch-tgi-inference-2023-07-06-11-47-55-487/invocations",
            "info": """
            Falcon-7B is a 7B parameters causal decoder-only model trained on 1,500B tokens of RefinedWeb, offering superior performance, optimized inference architecture, and available under the Apache 2.0 license.
            
            - model name
            ```
            falcon-7B
            ```
            """,
            "keys": ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN"],
        },
        "Bloomz": {
            "name": "Bloomz",
            "conn": "",
            "info": """
            BLOOMZ & mT0 are crosslingual models that can understand and execute human instructions in multiple languages without prior training on specific tasks or languages.


            - model name
            ```
            Bloomz-7B
            ```
            """,
            "keys": ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN"],
        },
    }
}
