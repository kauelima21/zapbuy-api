import os
import shutil
import subprocess
import boto3

# Configurações
LAYER_NAME = "PillowLayer"
PYTHON_VERSION = "python3.12"
AWS_REGION = "sa-east-1"

# Diretórios temporários
LAYER_DIR = "layer_build"
PYTHON_LIB_DIR = os.path.join(LAYER_DIR, "python")


def install_pillow():
    """Instala o Pillow compatível com AWS Lambda (ARM64)."""
    print("📦 Instalando Pillow para ARM64...")
    os.makedirs(PYTHON_LIB_DIR, exist_ok=True)

    subprocess.run(
        [
            "pip",
            "install",
            "--platform",
            "manylinux2014_aarch64",
            "--only-binary=:all:",
            "--target",
            PYTHON_LIB_DIR,
            "--upgrade",
            "Pillow",
        ],
        check=True,
    )


def package_layer():
    """Compacta a layer para upload."""
    print("🗜 Compactando a Layer...")
    shutil.make_archive("pillow-layer", "zip", LAYER_DIR)


def publish_layer():
    """Publica a layer no AWS Lambda."""
    print("🚀 Publicando Layer na AWS...")

    lambda_client = boto3.client("lambda", region_name=AWS_REGION)

    with open("pillow-layer.zip", "rb") as zip_file:
        response = lambda_client.publish_layer_version(
            LayerName=LAYER_NAME,
            Description="Pillow para AWS Lambda ARM64",
            Content={"ZipFile": zip_file.read()},
            CompatibleRuntimes=[PYTHON_VERSION],
            CompatibleArchitectures=["arm64"],
        )

    layer_arn = response["LayerVersionArn"]
    print(f"✅ Layer publicada com sucesso: {layer_arn}")


def cleanup():
    """Remove arquivos temporários."""
    print("🧹 Limpando arquivos temporários...")
    shutil.rmtree(LAYER_DIR, ignore_errors=True)
    os.remove("pillow-layer.zip")


if __name__ == "__main__":
    install_pillow()
    package_layer()
    publish_layer()
    cleanup()
    print("🎉 Processo concluído com sucesso!")
