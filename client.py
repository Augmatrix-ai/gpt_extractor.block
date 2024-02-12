from augmatrix.block_service.client_runner import ClientRunner

def main():
    # Initialize the client with the server's URL
    client = ClientRunner(url='http://0.0.0.0:8083/')

    # Load the PDF file and specify properties and credentials
    with open("testdata/table.txt", "rb") as fr:
        inputs = {
            "text": fr.read()
        }
        properties = {
            "instruct": "Extract required output json fileds from the give text.",
            "outputFormatJson": "{\n    \"Insured Name\": \"\",\n    \"Insurance No\": \"\",\n    \"Total Premium\": \"\",\n    \"next premium date\": \"\"\n}"
        }
        credentials = {}

        # Call the function with the specified inputs, properties, and credentials
        outputs = client.call_function(
            structure="structure.json",
            func_args=properties,
            inputs=inputs,
            credentials=credentials
        )

        print(outputs)

if __name__ == "__main__":
    main()
