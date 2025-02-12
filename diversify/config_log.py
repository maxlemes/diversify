# config_log.py

import logging

# Configuração do log
logging.basicConfig(
    filename="operacoes_banco.log", 
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)
