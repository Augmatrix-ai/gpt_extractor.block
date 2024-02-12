import io
import json
import base64
import requests
from typing import Dict, Union
import os
import openai
import re
from augmatrix.block_service.service_runner import ServerManager, ServiceRunner
from openai import OpenAI

class GPTExtractorTask(ServiceRunner):
    def __init__(self, logger: object) -> None:
        """
        Initialize GPT Extractor Task object.

        Parameters:
        logger (object): A logger object to log messages and errors.
        """
        self.logger = logger
        super().__init__(structure_json_path='./structure.json')

    def run(self, inputs, properties, credentials):
        """
        Perform extraction using OpenAI model.

        Parameters:
        inputs (Dict): A dictionary object containing the input data.
        properties (Dict): Additional properties for task execution.
        credentials (Dict): Credentials required for OpenAI API.

        Returns:
        Dict: Prediction results.
        """
        openai.organization = credentials.get("OPENAI_ORG", os.getenv("OPENAI_ORG", None))
        openai.api_key = credentials.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY", None))

        if openai.organization is None or openai.api_key is None:
            raise ValueError("OpenAI credentials are not provided")

        prompt = f"""
            Instructions
                1. Don't write code, directly perform task on the 'text'.
                2. Put __START__ and __END__ to indicate the start and end of he final output.
                3. If value does not exist then set \"\" .i.e is empty.

            Input 'text' to extract from
            ----------
            ```
                {inputs.text}
            ```
            ----------

            Output as shown below format as json
            ----------
            __START__
            ```{properties["outputFormatJson"]}```
            __END__
            ----------
        """
        client = OpenAI()
        
        # Use the updated method to create completions with the OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "system",
                "content": properties["instruct"]
            }, {
                "role": "user",
                "content": prompt
            }],
        )

        if not response.choices:
            raise ValueError("No response from OpenAI API.")
        
        response_text = response.choices[0].message.content.strip()
        print(response_text)
        start_text = r"__START__\n```"
        end_text = "```\n+__END__"
        match = re.search(f"{start_text}(?P<output>(.|\n)+){end_text}", response_text, re.DOTALL)

        if match:
            # Extracting the value from the named group 'extraction'
            extraction = match.group('output').strip()
        else:
            raise ValueError("Failed to extract JSON from response.")

        return {"predict": json.loads(extraction)}


if __name__ == "__main__":
    ServerManager(GPTExtractorTask(logger=None)).start(
        host="localhost",
        port=8083,
        # Assuming TLS/SSL is not a requirement for this migration example.
        # If secure communication is required, uncomment and provide paths to the certificate and private key.
        # private_key="certificates/private.pem",
        # cert_key="certificates/cert.pem"
    )