"""
Sistema de Blockchain para Gestión de Casos Judiciales
Implementación de clases Block, Blockchain y transacciones judiciales
"""

import hashlib
import json
from datetime import datetime
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class JudicialTransaction:
    """Representa una transacción judicial en la blockchain"""
    case_id: str
    action: str  # create_case, add_document, schedule_hearing, issue_judgment
    parties: Dict[str, str]  # {"plaintiff": "hash1", "defendant": "hash2"}
    judge: str
    data: Dict[str, Any]
    timestamp: str

    def to_dict(self) -> Dict:
        """Convierte la transacción a diccionario"""
        return asdict(self)

    def to_json(self) -> str:
        """Convierte la transacción a JSON string"""
        return json.dumps(self.to_dict(), sort_keys=True)


class Block:
    """
    Representa un bloque en la blockchain judicial
    Contiene transacciones, hash del bloque anterior, nonce para PoW
    """

    def __init__(
        self,
        index: int,
        transactions: List[JudicialTransaction],
        previous_hash: str,
        timestamp: Optional[str] = None,
        nonce: int = 0
    ):
        self.index = index
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.timestamp = timestamp or datetime.now().isoformat()
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """
        Calcula el hash SHA-256 del bloque
        Incluye todos los datos del bloque en el cálculo
        """
        # Serializar transacciones
        transactions_data = [tx.to_dict() for tx in self.transactions]
        
        block_data = {
            "index": self.index,
            "transactions": transactions_data,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "nonce": self.nonce
        }
        
        block_string = json.dumps(block_data, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty: int = 4) -> None:
        """
        Implementa Proof of Work simple
        Busca un nonce que genere un hash con 'difficulty' ceros al inicio
        """
        target = "0" * difficulty
        
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()
        
        print(f"✓ Bloque minado: {self.hash[:16]}... (nonce: {self.nonce})")

    def to_dict(self) -> Dict:
        """Convierte el bloque a diccionario"""
        return {
            "index": self.index,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "nonce": self.nonce,
            "hash": self.hash
        }


class JudicialBlockchain:
    """
    Blockchain especializada para gestión de casos judiciales
    Maneja la cadena de bloques y validaciones
    """

    def __init__(self, difficulty: int = 4):
        self.chain: List[Block] = []
        self.pending_transactions: List[JudicialTransaction] = []
        self.difficulty = difficulty
        self.mining_reward = 1  # Recompensa simbólica por minar
        self.create_genesis_block()

    def create_genesis_block(self) -> None:
        """Crea el bloque génesis (primer bloque de la cadena)"""
        genesis_transaction = JudicialTransaction(
            case_id="GENESIS-0",
            action="create_case",
            parties={"plaintiff": "Sistema", "defendant": "N/A"},
            judge="Sistema_Judicial",
            data={"description": "Bloque génesis del sistema judicial"},
            timestamp=datetime.now().isoformat()
        )
        
        genesis_block = Block(0, [genesis_transaction], "0")
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
        print("  Blockchain judicial inicializada con bloque génesis")

    def get_latest_block(self) -> Block:
        """Retorna el último bloque de la cadena"""
        return self.chain[-1]

    def add_transaction(self, transaction: JudicialTransaction) -> bool:
        """
        Añade una transacción a la lista de pendientes
        Valida que la transacción tenga datos válidos
        """
        if not transaction.case_id or not transaction.action:
            print(" Transacción inválida: falta case_id o action")
            return False
        
        self.pending_transactions.append(transaction)
        print(f" Transacción añadida: {transaction.case_id} - {transaction.action}")
        return True

    def mine_pending_transactions(self, miner_address: str) -> Block:
        """
        Mina un nuevo bloque con las transacciones pendientes
        Añade el bloque a la cadena y limpia las transacciones pendientes
        """
        if not self.pending_transactions:
            print("  No hay transacciones pendientes para minar")
            return None

        # Crear nuevo bloque
        block = Block(
            index=len(self.chain),
            transactions=self.pending_transactions,
            previous_hash=self.get_latest_block().hash
        )

        # Minar el bloque (Proof of Work)
        block.mine_block(self.difficulty)

        # Añadir a la cadena
        self.chain.append(block)
        
        # Limpiar transacciones pendientes
        self.pending_transactions = []
        
        print(f"  Bloque #{block.index} minado por {miner_address}")
        return block

    def is_chain_valid(self) -> bool:
        """
        Verifica la integridad de toda la cadena
        Comprueba hashes y enlaces entre bloques
        """
        # Verificar desde el segundo bloque (índice 1)
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Verificar que el hash del bloque sea correcto
            if current_block.hash != current_block.calculate_hash():
                print(f" Hash inválido en bloque #{i}")
                return False

            # Verificar que el previous_hash coincida
            if current_block.previous_hash != previous_block.hash:
                print(f" Enlace roto entre bloques #{i-1} y #{i}")
                return False

            # Verificar proof of work
            if not current_block.hash.startswith("0" * self.difficulty):
                print(f" Proof of Work inválido en bloque #{i}")
                return False

        print(" Blockchain válida - Integridad verificada")
        return True

    def get_case_history(self, case_id: str) -> List[Dict]:
        """
        Obtiene todo el historial de transacciones de un caso específico
        """
        history = []
        
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.case_id == case_id:
                    history.append({
                        "block": block.index,
                        "timestamp": transaction.timestamp,
                        "action": transaction.action,
                        "data": transaction.data,
                        "block_hash": block.hash[:16] + "..."
                    })
        
        return history

    def get_statistics(self) -> Dict:
        """Retorna estadísticas básicas de la blockchain"""
        total_transactions = sum(len(block.transactions) for block in self.chain)
        
        # Contar tipos de casos
        case_types = {}
        cases_set = set()
        
        for block in self.chain:
            for tx in block.transactions:
                cases_set.add(tx.case_id)
                case_type = tx.data.get("type", "unknown")
                case_types[case_type] = case_types.get(case_type, 0) + 1
        
        return {
            "total_blocks": len(self.chain),
            "total_transactions": total_transactions,
            "unique_cases": len(cases_set),
            "pending_transactions": len(self.pending_transactions),
            "case_types": case_types,
            "difficulty": self.difficulty
        }

    def to_dict(self) -> Dict:
        """Convierte la blockchain completa a diccionario"""
        return {
            "chain": [block.to_dict() for block in self.chain],
            "pending_transactions": [tx.to_dict() for tx in self.pending_transactions],
            "difficulty": self.difficulty
        }
