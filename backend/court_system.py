"""
Sistema de Gestión Judicial sobre Blockchain
Proporciona funcionalidades de alto nivel para gestionar casos judiciales
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import hashlib
from blockchain import JudicialBlockchain, JudicialTransaction


class CourtSystem:
    """
    Sistema de gestión judicial que utiliza blockchain
    Maneja operaciones de casos, documentos, audiencias y sentencias
    """

    def __init__(self, difficulty: int = 4):
        self.blockchain = JudicialBlockchain(difficulty)
        self.cases: Dict[str, Dict] = {}  # Cache de casos activos
        self.judges: Dict[str, str] = {}  # Registro de jueces

    def register_judge(self, name: str, specialty: str) -> str:
        """Registra un juez en el sistema y genera su seudónimo hash"""
        judge_hash = hashlib.sha256(f"{name}_{specialty}".encode()).hexdigest()[:16]
        judge_id = f"Juez_{name.replace(' ', '_')}_{judge_hash}"
        self.judges[judge_id] = specialty
        print(f"👨‍⚖️  Juez registrado: {judge_id} (Especialidad: {specialty})")
        return judge_id

    def _generate_party_hash(self, party_name: str, role: str) -> str:
        """Genera un hash seudónimo para una parte involucrada"""
        return hashlib.sha256(f"{party_name}_{role}".encode()).hexdigest()[:16]

    def create_case(
        self,
        case_id: str,
        case_type: str,  # civil, penal, laboral
        plaintiff_name: str,
        defendant_name: str,
        judge_id: str,
        description: str,
        miner_address: str = "Sistema"
    ) -> bool:
        """
        Crea un nuevo caso judicial en la blockchain
        """
        # Validar tipo de caso
        valid_types = ["civil", "penal", "laboral"]
        if case_type not in valid_types:
            print(f" Tipo de caso inválido. Use: {', '.join(valid_types)}")
            return False

        # Generar hashes para las partes
        plaintiff_hash = self._generate_party_hash(plaintiff_name, "plaintiff")
        defendant_hash = self._generate_party_hash(defendant_name, "defendant")

        # Crear transacción
        transaction = JudicialTransaction(
            case_id=case_id,
            action="create_case",
            parties={
                "plaintiff": f"Demandante_{plaintiff_hash}",
                "defendant": f"Demandado_{defendant_hash}"
            },
            judge=judge_id,
            data={
                "type": case_type,
                "description": description,
                "status": "presentado",
                "plaintiff_name_hash": plaintiff_hash,
                "defendant_name_hash": defendant_hash
            },
            timestamp=datetime.now().isoformat()
        )

        # Añadir a blockchain
        if self.blockchain.add_transaction(transaction):
            # Minar inmediatamente para confirmación
            self.blockchain.mine_pending_transactions(miner_address)
            
            # Actualizar cache de casos
            self.cases[case_id] = {
                "type": case_type,
                "status": "presentado",
                "judge": judge_id,
                "parties": transaction.parties,
                "created_at": transaction.timestamp,
                "documents": [],
                "hearings": [],
                "judgment": None
            }
            
            print(f"  Caso creado: {case_id} ({case_type})")
            return True
        
        return False

    def add_document(
        self,
        case_id: str,
        document_name: str,
        document_content: str,
        uploader: str,
        miner_address: str = "Sistema"
    ) -> bool:
        """
        Añade un documento/evidencia a un caso (almacena solo el hash)
        """
        if case_id not in self.cases:
            print(f" Caso {case_id} no encontrado")
            return False

        # Generar hash del documento (NO almacenamos contenido real)
        doc_hash = hashlib.sha256(document_content.encode()).hexdigest()

        # Crear transacción
        transaction = JudicialTransaction(
            case_id=case_id,
            action="add_document",
            parties=self.cases[case_id]["parties"],
            judge=self.cases[case_id]["judge"],
            data={
                "document_name": document_name,
                "document_hash": doc_hash,
                "uploader": uploader,
                "upload_date": datetime.now().isoformat()
            },
            timestamp=datetime.now().isoformat()
        )

        if self.blockchain.add_transaction(transaction):
            self.blockchain.mine_pending_transactions(miner_address)
            
            # Actualizar cache
            self.cases[case_id]["documents"].append({
                "name": document_name,
                "hash": doc_hash,
                "uploader": uploader,
                "date": transaction.timestamp
            })
            
            print(f" Documento añadido a {case_id}: {document_name}")
            return True
        
        return False

    def schedule_hearing(
        self,
        case_id: str,
        hearing_type: str,
        date: str,
        location: str,
        miner_address: str = "Sistema"
    ) -> bool:
        """
        Programa una audiencia para un caso
        """
        if case_id not in self.cases:
            print(f" Caso {case_id} no encontrado")
            return False

        transaction = JudicialTransaction(
            case_id=case_id,
            action="schedule_hearing",
            parties=self.cases[case_id]["parties"],
            judge=self.cases[case_id]["judge"],
            data={
                "hearing_type": hearing_type,
                "date": date,
                "location": location,
                "scheduled_at": datetime.now().isoformat()
            },
            timestamp=datetime.now().isoformat()
        )

        if self.blockchain.add_transaction(transaction):
            self.blockchain.mine_pending_transactions(miner_address)
            
            # Actualizar cache
            self.cases[case_id]["hearings"].append({
                "type": hearing_type,
                "date": date,
                "location": location
            })
            
            # Cambiar estado
            if self.cases[case_id]["status"] == "presentado":
                self.cases[case_id]["status"] = "en_proceso"
            
            print(f" Audiencia programada para {case_id}: {hearing_type} - {date}")
            return True
        
        return False

    def issue_judgment(
        self,
        case_id: str,
        ruling: str,
        verdict: str,
        details: str,
        miner_address: str = "Sistema"
    ) -> bool:
        """
        Emite una sentencia/fallo para un caso
        """
        if case_id not in self.cases:
            print(f" Caso {case_id} no encontrado")
            return False

        transaction = JudicialTransaction(
            case_id=case_id,
            action="issue_judgment",
            parties=self.cases[case_id]["parties"],
            judge=self.cases[case_id]["judge"],
            data={
                "ruling": ruling,  # a_favor_demandante, a_favor_demandado, mixto
                "verdict": verdict,
                "details": details,
                "judgment_date": datetime.now().isoformat()
            },
            timestamp=datetime.now().isoformat()
        )

        if self.blockchain.add_transaction(transaction):
            self.blockchain.mine_pending_transactions(miner_address)
            
            # Actualizar cache
            self.cases[case_id]["judgment"] = {
                "ruling": ruling,
                "verdict": verdict,
                "details": details,
                "date": transaction.timestamp
            }
            self.cases[case_id]["status"] = "resuelto"
            
            print(f"  Sentencia emitida para {case_id}: {ruling}")
            return True
        
        return False

    def get_case_details(self, case_id: str) -> Optional[Dict]:
        """Obtiene los detalles completos de un caso"""
        if case_id not in self.cases:
            print(f" Caso {case_id} no encontrado")
            return None
        
        return self.cases[case_id]

    def get_case_history(self, case_id: str) -> List[Dict]:
        """Obtiene el historial completo de transacciones de un caso"""
        return self.blockchain.get_case_history(case_id)

    def verify_document(self, case_id: str, document_content: str) -> Optional[Dict]:
        """
        Verifica si un documento existe en un caso comparando su hash
        """
        if case_id not in self.cases:
            return None

        doc_hash = hashlib.sha256(document_content.encode()).hexdigest()
        
        for doc in self.cases[case_id]["documents"]:
            if doc["hash"] == doc_hash:
                return {
                    "verified": True,
                    "document": doc
                }
        
        return {"verified": False}

    def get_all_cases(self) -> Dict[str, Dict]:
        """Retorna todos los casos del sistema"""
        return self.cases

    def get_statistics(self) -> Dict:
        """Obtiene estadísticas del sistema judicial"""
        blockchain_stats = self.blockchain.get_statistics()
        
        # Estadísticas de casos
        status_count = {}
        for case in self.cases.values():
            status = case["status"]
            status_count[status] = status_count.get(status, 0) + 1
        
        return {
            **blockchain_stats,
            "total_cases": len(self.cases),
            "total_judges": len(self.judges),
            "cases_by_status": status_count
        }

    def verify_blockchain_integrity(self) -> bool:
        """Verifica la integridad de la blockchain"""
        return self.blockchain.is_chain_valid()

    def export_blockchain(self) -> Dict:
        """Exporta la blockchain completa"""
        return self.blockchain.to_dict()
