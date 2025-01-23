# TorchImageClass

**TorchImageClass** é uma biblioteca em Python que fornece um conjunto de ferramentas e utilitários para **classificação de imagens** usando [PyTorch](https://pytorch.org/). Ela visa facilitar o **treinamento**, **validação** e **inferência** de redes neurais voltadas a tarefas de classificação.

---

## Sumário

- [Motivação](#motivação)
- [Principais Recursos](#principais-recursos)
- [Instalação](#instalação)

---

## Motivação

Modelos de classificação de imagens são amplamente usados em aplicações de visão computacional, desde identificação de objetos até detecção de doenças em exames de imagem. O **TorchImageClass** simplifica esse processo, fornecendo:

- **Arquiteturas** pré-definidas (ResNet, etc.) ou personalizáveis.  
- **Data loaders** e **transforms** para imagens.  
- **Treinamento** com otimização, métricas e *early stopping*.  
- **Práticas de *logging* e salvamento de modelos** (checkpoints).  
- **Inferência** em lote ou em imagens individuais.

---

## Principais Recursos

1. **Fácil inicialização de Modelos**  
   - Classes prontas para ResNet, VGG, etc., com poucas linhas de código.

2. **Treinamento Automatizado**  
   - Loop de treino e validação com métricas integradas (acurácia, precisão, recall).

3. **Data Augmentation Simplificada**  
   - Integração direta com `torchvision.transforms`.

4. **Suporte a GPU/CPU**  
   - Reconhecimento automático de dispositivo (CUDA/ROCm ou CPU).

5. **Exportação de Modelos**  
   - Salva pesos em formatos `.pth` ou `.pt`.

---

## Instalação

Para instalar via [PyPI](https://pypi.org/):

```bash
pip install TorchImageClass
```
## Como usar

```bash
from TorchImageClass import train_model

model, history = train_model(
    base_dir="data/images for prediction of treated tuberculosis",
    num_epochs=20,
    image_size=(224,224),
    batch_size=8,
    num_classes=2,
    patience=5,
    model_save_path="best_model.pth"
)

print("Final History:", history)
print("Trained model:", model)

