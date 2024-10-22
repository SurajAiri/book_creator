import subprocess

def get_ollama_models():
    try:
        # Run the `ollama list` command and capture the output
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, check=True)
        
        # Split the output into lines
        lines = result.stdout.splitlines()
        
        # Initialize an empty list to store model names
        model_names = []
        
        # Iterate over the lines starting from the second one (skip the header)
        for line in lines[1:]:
            # Split the line by spaces to get the columns (NAME, ID, SIZE, etc.)
            parts = line.split()
            if parts:
                # The first element is the model name (e.g., llama3.2:latest)
                model_name_with_version = parts[0]
                # Split by ':' to remove the version and get the model name (e.g., llama3.2)
                model_name = model_name_with_version.split(':')[0]
                # Add the model name to the list
                model_names.append(model_name)
        
        return model_names

    except subprocess.CalledProcessError as e:
        # Handle errors if the command fails
        print(f"Error occurred: {e}")
        return []

# Call the function and print the list of model names
model_list = get_ollama_models()
print(model_list)