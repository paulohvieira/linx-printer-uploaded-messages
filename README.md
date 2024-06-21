
# Interpretador de Mensagens LINX / LINX Message Interpreter

Este repositório contém um código para interpretação de mensagens de impressoras de jato contínuo da LINX. O código foi testado com os modelos LINX 7900 e LINX 8900 e é utilizado para ler, processar e interpretar mensagens de texto contidas em um arquivo *.dat.
Foi usado como referência o manual Remote Communications Interface(RCI) Reference Manual Linx 5900, 7900, 8800, 8900, CJ400 & Linx 10. MP65969–7, Linx RCI Reference Manual, March 2021

This repository contains code for interpreting continuous inkjet printer messages from LINX. The code has been tested with LINX models LINX 7900 e LINX 8900 and is used to read, process, and interpret text messages contained in a *.dat file.
The Remote Communications Interface (RCI) Reference Manual Linx 5900, 7900, 8800, 8900, CJ400 & Linx 10. MP65969–7, Linx RCI Reference Manual, March 2021 was used as reference.

## Estrutura do Repositório / Repository Structure

- 'App.py': Ponto de entrada.
- 'messages_util.py': O script principal que contém a lógica para leitura e interpretação das mensagens.
- 'messages.dat': O arquivo que contém as mensagens a serem processadas. **Este arquivo deve estar no mesmo nível de diretório que o** messages_util.py.

- 'App.py': Entry point.
- 'messages_util.py': The main script that contains the logic for reading and interpreting the messages.
- 'messages.dat': The file containing the messages to be processed. **This file must be at the same directory level as** 'messages_util.py'.

## Como Usar / How to Use
Para utilizar o interpretador de mensagens, siga os passos abaixo:

1. Certifique-se de que o arquivo 'messages.dat' está no mesmo nível de diretório que o arquivo 'messages_util.py'.
2. Execute o script 'App.py' utilizando Python

1. Ensure that the 'messages.dat' file is at the same directory level as the 'messages_util.py' file.
2. Run the 'App.py' script using Python.

## Exemplo de uso / Usage Example

```console
python App.py
```

## Requisitos
- Pyhton3.x

## Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e enviar pull requests.

## Message Structure

### Message Header
The message header contains information relevant to the entire message and includes the following fields:

- **Message Length in Bytes:** 2 bytes (0 to 65535)
- **Message Length in Rasters:** 2 bytes (0 to 65535)
- **EHT Setting:** 1 byte (0 to 16)
- **Inter Raster Width:** 2 bytes (0 to 65535)
- **Print Delay:** 2 bytes (0 to 65535)
- **Message Name:** 16 bytes (15 characters + null terminator)
- **Message Type:** 16 bytes (15 characters + null terminator)

Total message header length is 41 bytes.

## Field Structure

### Field Header
Each field in the message includes a header with the following information:

- **Field Header Character:** 1 byte
- **Field Type:** 1 byte
- **Field Length in Bytes:** 2 bytes
- **Y Position:** 1 byte
- **X Position:** 2 bytes
- **Field Length in Rasters:** 2 bytes
- **Field Height in Drops:** 1 byte
- **Format 3:** 1 byte
- **Bold Multiplier:** 1 byte
- **Text Length:** 1 byte
- **Format 1:** 1 byte
- **Format 2:** 1 byte
- **Linkage:** 1 byte
- **Data Set Name:** 16 bytes (15 characters + null terminator)

Total field header length is 32 bytes.