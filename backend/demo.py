"""
Script de Demostración del Sistema Judicial Blockchain
Muestra todas las funcionalidades principales del sistema
"""

from court_system import CourtSystem
from datetime import datetime, timedelta
import json


def print_separator(title: str = ""):
    """Imprime un separador visual"""
    print("\n" + "=" * 80)
    if title:
        print(f"  {title}")
        print("=" * 80)
    print()


def demo_judicial_blockchain():
    """
    Demostración completa del sistema judicial blockchain
    """
    print_separator("  SISTEMA JUDICIAL BLOCKCHAIN - DEMO")
    
    # 1. Inicializar el sistema
    print(" PASO 1: Inicializar Sistema Judicial")
    print("-" * 80)
    court = CourtSystem(difficulty=3)  # Dificultad reducida para demo
    
    # 2. Registrar jueces
    print_separator(" PASO 2: Registrar Jueces")
    judge1 = court.register_judge("María Rodríguez", "civil")
    judge2 = court.register_judge("Carlos Mendoza", "penal")
    judge3 = court.register_judge("Ana López", "laboral")
    
    # 3. Crear casos de ejemplo
    print_separator(" PASO 3: Crear Casos Judiciales")
    
    # Caso 1: Civil
    print("\n🔹 Caso Civil - Demanda por incumplimiento de contrato")
    court.create_case(
        case_id="EXP-2024-001",
        case_type="civil",
        plaintiff_name="Empresa Constructora ABC",
        defendant_name="Inversiones XYZ S.A.",
        judge_id=judge1,
        description="Demanda por incumplimiento de contrato de construcción. "
                   "Monto reclamado: $500,000 USD por trabajos no pagados.",
        miner_address="Secretaría_Judicial"
    )
    
    # Caso 2: Penal
    print("\n🔹 Caso Penal - Fraude financiero")
    court.create_case(
        case_id="EXP-2024-002",
        case_type="penal",
        plaintiff_name="Ministerio Público",
        defendant_name="Juan Pérez García",
        judge_id=judge2,
        description="Proceso penal por presunto fraude financiero. "
                   "Apropiación indebida de fondos corporativos.",
        miner_address="Fiscalía"
    )
    
    # Caso 3: Laboral
    print("\n🔹 Caso Laboral - Despido injustificado")
    court.create_case(
        case_id="EXP-2024-003",
        case_type="laboral",
        plaintiff_name="Pedro Martínez López",
        defendant_name="TechCorp Industries",
        judge_id=judge3,
        description="Demanda por despido injustificado y pago de indemnizaciones. "
                   "20 años de antigüedad.",
        miner_address="Juzgado_Laboral"
    )
    
    # 4. Añadir documentos a los casos
    print_separator(" PASO 4: Añadir Documentos y Evidencias")
    
    print("\n Documentos para EXP-2024-001 (Civil):")
    court.add_document(
        case_id="EXP-2024-001",
        document_name="Contrato_de_Construcción.pdf",
        document_content="CONTRATO DE CONSTRUCCIÓN firmado el 15/01/2024 entre ABC y XYZ...",
        uploader="Demandante_A",
        miner_address="Secretaría"
    )
    
    court.add_document(
        case_id="EXP-2024-001",
        document_name="Facturas_Impagadas.pdf",
        document_content="Factura #001 - $250,000, Factura #002 - $250,000, Total: $500,000",
        uploader="Demandante_A",
        miner_address="Secretaría"
    )
    
    court.add_document(
        case_id="EXP-2024-001",
        document_name="Correos_Electrónicos.pdf",
        document_content="Email 01/02/2024: Solicitando pago... Email 15/02/2024: Recordatorio...",
        uploader="Demandante_A",
        miner_address="Secretaría"
    )
    
    print("\n Documentos para EXP-2024-002 (Penal):")
    court.add_document(
        case_id="EXP-2024-002",
        document_name="Denuncia_Inicial.pdf",
        document_content="Denuncia presentada por CFO de la empresa el 10/03/2024...",
        uploader="Fiscalía",
        miner_address="Ministerio_Público"
    )
    
    court.add_document(
        case_id="EXP-2024-002",
        document_name="Estados_Financieros.xlsx",
        document_content="Análisis forense de movimientos bancarios irregulares...",
        uploader="Fiscalía",
        miner_address="Ministerio_Público"
    )
    
    print("\n Documentos para EXP-2024-003 (Laboral):")
    court.add_document(
        case_id="EXP-2024-003",
        document_name="Carta_de_Despido.pdf",
        document_content="Notificación de terminación laboral sin causa justificada...",
        uploader="Demandante",
        miner_address="Juzgado"
    )
    
    court.add_document(
        case_id="EXP-2024-003",
        document_name="Recibos_de_Nómina.pdf",
        document_content="Historial de pagos de enero 2004 a diciembre 2024...",
        uploader="Demandante",
        miner_address="Juzgado"
    )
    
    # 5. Programar audiencias
    print_separator(" PASO 5: Programar Audiencias")
    
    print("\n Audiencias para EXP-2024-001:")
    court.schedule_hearing(
        case_id="EXP-2024-001",
        hearing_type="Audiencia Preliminar",
        date="2024-04-15 10:00",
        location="Sala 3 - Juzgado Civil",
        miner_address="Secretaría"
    )
    
    court.schedule_hearing(
        case_id="EXP-2024-001",
        hearing_type="Audiencia de Juicio Oral",
        date="2024-05-20 09:00",
        location="Sala 3 - Juzgado Civil",
        miner_address="Secretaría"
    )
    
    print("\n Audiencias para EXP-2024-002:")
    court.schedule_hearing(
        case_id="EXP-2024-002",
        hearing_type="Audiencia de Imputación",
        date="2024-04-10 11:00",
        location="Sala 1 - Juzgado Penal",
        miner_address="Fiscalía"
    )
    
    print("\n Audiencias para EXP-2024-003:")
    court.schedule_hearing(
        case_id="EXP-2024-003",
        hearing_type="Audiencia de Conciliación",
        date="2024-04-08 14:00",
        location="Sala 2 - Juzgado Laboral",
        miner_address="Juzgado"
    )
    
    # 6. Emitir sentencias
    print_separator(" PASO 6: Emitir Sentencias")
    
    print("\n  Sentencia para EXP-2024-001:")
    court.issue_judgment(
        case_id="EXP-2024-001",
        ruling="a_favor_demandante",
        verdict="PROCEDENTE",
        details="Se condena al demandado al pago de $500,000 USD más intereses "
               "moratorios y costas procesales. Plazo de pago: 30 días.",
        miner_address="Juez_Rodriguez"
    )
    
    print("\n  Sentencia para EXP-2024-002:")
    court.issue_judgment(
        case_id="EXP-2024-002",
        ruling="a_favor_demandante",
        verdict="CULPABLE",
        details="Se declara culpable al acusado de fraude financiero. "
               "Pena: 5 años de prisión y restitución de $2,000,000 USD.",
        miner_address="Juez_Mendoza"
    )
    
    print("\n  Sentencia para EXP-2024-003:")
    court.issue_judgment(
        case_id="EXP-2024-003",
        ruling="mixto",
        verdict="PARCIALMENTE PROCEDENTE",
        details="Se declara el despido como injustificado. La empresa deberá pagar "
               "indemnización equivalente a 12 meses de salario más prestaciones. "
               "No procede la reinstalación solicitada.",
        miner_address="Juez_Lopez"
    )
    
    # 7. Mostrar detalles de un caso específico
    print_separator(" PASO 7: Consultar Detalles de Caso")
    
    print("\n🔍 Detalles completos de EXP-2024-001:")
    case_details = court.get_case_details("EXP-2024-001")
    print(json.dumps(case_details, indent=2, ensure_ascii=False))
    
    # 8. Mostrar historial de blockchain de un caso
    print_separator("PASO 8: Historial Blockchain de Caso")
    
    print("\n Historial completo de EXP-2024-002:")
    history = court.get_case_history("EXP-2024-002")
    for i, entry in enumerate(history, 1):
        print(f"\n  [{i}] Bloque #{entry['block']} - Hash: {entry['block_hash']}")
        print(f"      Acción: {entry['action']}")
        print(f"      Timestamp: {entry['timestamp']}")
        print(f"      Datos: {json.dumps(entry['data'], indent=6, ensure_ascii=False)}")
    
    # 9. Verificar integridad de la blockchain
    print_separator(" PASO 9: Verificar Integridad de la Blockchain")
    
    print("\n Verificando integridad de toda la cadena...")
    is_valid = court.verify_blockchain_integrity()
    
    if is_valid:
        print("\n ¡Blockchain íntegra! Todos los bloques son válidos.")
    else:
        print("\n ¡Advertencia! La blockchain ha sido comprometida.")
    
    # 10. Mostrar estadísticas del sistema
    print_separator(" PASO 10: Estadísticas del Sistema")
    
    stats = court.get_statistics()
    print("\n Estadísticas Generales:")
    print(f"   • Total de Bloques: {stats['total_blocks']}")
    print(f"   • Total de Transacciones: {stats['total_transactions']}")
    print(f"   • Casos Únicos: {stats['unique_cases']}")
    print(f"   • Total de Casos: {stats['total_cases']}")
    print(f"   • Jueces Registrados: {stats['total_judges']}")
    print(f"   • Dificultad de Minado: {stats['difficulty']}")
    
    print("\n Casos por Tipo:")
    for case_type, count in stats['case_types'].items():
        print(f"   • {case_type}: {count}")
    
    print("\n Casos por Estado:")
    for status, count in stats['cases_by_status'].items():
        print(f"   • {status}: {count}")
    
    # 11. Verificar documento
    print_separator(" PASO 11: Verificar Autenticidad de Documento")
    
    print("\n Verificando documento original:")
    verification = court.verify_document(
        case_id="EXP-2024-001",
        document_content="CONTRATO DE CONSTRUCCIÓN firmado el 15/01/2024 entre ABC y XYZ..."
    )
    
    if verification["verified"]:
        print(" Documento VERIFICADO - Existe en la blockchain")
        print(f"   Hash: {verification['document']['hash'][:32]}...")
        print(f"   Subido por: {verification['document']['uploader']}")
        print(f"   Fecha: {verification['document']['date']}")
    else:
        print(" Documento NO VERIFICADO - No existe en la blockchain")
    
    print("\n Verificando documento alterado:")
    verification_fake = court.verify_document(
        case_id="EXP-2024-001",
        document_content="CONTRATO ALTERADO con información falsa..."
    )
    
    if verification_fake["verified"]:
        print(" Documento VERIFICADO")
    else:
        print(" Documento NO VERIFICADO - El contenido no coincide")
    
    # 12. Mostrar blockchain completa
    print_separator(" PASO 12: Estructura de la Blockchain")
    
    print("\n Cadena de Bloques:")
    for block in court.blockchain.chain:
        print(f"\n  Bloque #{block.index}")
        print(f"  ├─ Hash: {block.hash[:32]}...")
        print(f"  ├─ Hash Anterior: {block.previous_hash[:32]}...")
        print(f"  ├─ Timestamp: {block.timestamp}")
        print(f"  ├─ Nonce: {block.nonce}")
        print(f"  └─ Transacciones: {len(block.transactions)}")
        
        for j, tx in enumerate(block.transactions, 1):
            print(f"      [{j}] {tx.case_id} - {tx.action}")
    
    print_separator(" DEMO COMPLETADA")
    print("\n El sistema judicial blockchain ha sido demostrado exitosamente.")
    print(" Todas las operaciones han sido registradas de forma inmutable.")
    print(" La integridad de la cadena ha sido verificada.")
    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    try:
        demo_judicial_blockchain()
    except KeyboardInterrupt:
        print("\n\n  Demo interrumpida por el usuario.")
    except Exception as e:
        print(f"\n\n Error durante la demo: {str(e)}")
        raise
