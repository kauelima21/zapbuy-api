import os
import subprocess
import shutil
import boto3

LAYER_NAME = "marshmallow"
PYTHON_VERSION = "python3.12"
OUTPUT_DIR = "marshmallow_layer"
ZIP_FILE = f"{LAYER_NAME}.zip"

def create_layer_directory():
    # Cria estrutura: marshmallow_layer/python
    layer_path = os.path.join(OUTPUT_DIR, 'python')
    os.makedirs(layer_path, exist_ok=True)
    print(f"📁 Diretório criado em: {layer_path}")

    # Instala o marshmallow no diretório da layer
    print("📦 Instalando marshmallow...")
    subprocess.check_call([
        "pip", "install", "marshmallow",
        "-t", layer_path
    ])
    print("✅ Marshmallow instalado com sucesso.")

def package_layer():
    # Empacota o diretório em um .zip
    print("📦 Empacotando a layer...")
    shutil.make_archive(LAYER_NAME, 'zip', OUTPUT_DIR)
    print(f"✅ Layer empacotada como {ZIP_FILE}")

def publish_layer():
    # Publica a layer usando Boto3
    print("🚀 Fazendo deploy da layer para AWS Lambda...")
    client = boto3.client('lambda')

    with open(ZIP_FILE, 'rb') as zip_file:
        response = client.publish_layer_version(
            LayerName=LAYER_NAME,
            Description="Layer com Marshmallow",
            Content={'ZipFile': zip_file.read()},
            CompatibleRuntimes=[PYTHON_VERSION]
        )

    layer_arn = response['LayerVersionArn']
    print(f"✅ Deploy concluído. Layer ARN: {layer_arn}")

def cleanup():
    # Remove arquivos temporários
    print("🧹 Limpando arquivos temporários...")
    shutil.rmtree(OUTPUT_DIR)
    os.remove(ZIP_FILE)
    print("✅ Limpeza concluída.")

if __name__ == "__main__":
    try:
        create_layer_directory()
        package_layer()
        publish_layer()
    finally:
        cleanup()
