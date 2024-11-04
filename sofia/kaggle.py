import kagglehub

# Download latest version
path = kagglehub.dataset_download("shrutimechlearn/customer-data")

print("Path to dataset files:", path)