import ply.lex as lex
import ply.yacc as yacc

# Definición de los tokens
tokens = (
    'CFDI_COMPROBANTE',
    'CFDI_EMISOR',
    'CFDI_RECEPTOR',
    'CFDI_CONCEPTO',
    'VERSION',
    'RFC',
    'MONEDA',
    'TOTAL',
    'SUBTOTAL',
    'USO_CFDI',
    'FECHA',
)

# Expresiones regulares para cada token
# Aceptamos tanto las etiquetas de apertura como las de autocierre
t_CFDI_COMPROBANTE = r'<cfdi:Comprobante[^>]*?>'  # Acepta etiquetas con atributos
t_CFDI_EMISOR = r'<cfdi:Emisor[^>]*?>'  # Acepta etiquetas con atributos
t_CFDI_RECEPTOR = r'<cfdi:Receptor[^>]*?\/?>'  # Ajustado para aceptar etiquetas de autocierre
t_CFDI_CONCEPTO = r'<cfdi:Concepto[^>]*?>'  # Acepta etiquetas con atributos

# Atributos que son comunes en las etiquetas
t_VERSION = r'Version="[^"]*"'  # Acepta valores como "3.3"
t_RFC = r'Rfc="[^"]*"'  # Acepta valores como "AAA010101AAA"
t_MONEDA = r'Moneda="[^"]*"'  # Acepta valores como "MXN"
t_TOTAL = r'Total="[^"]*"'  # Acepta valores como "100.00"
t_SUBTOTAL = r'SubTotal="[^"]*"'  # Acepta valores como "100.00"
t_USO_CFDI = r'UsoCFDI="[^"]*"'  # Acepta valores como "G03"
t_FECHA = r'Fecha="[^"]*"'  # Acepta valores como "2023-01-01T12:00:00"

# Ignorar espacios en blanco y saltos de línea
t_ignore = " \t\n\r"

# Manejar errores de token no definido
def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}' en la posición {t.lexpos}")
    t.lexer.skip(1)

# Definir la gramática (análisis sintáctico)
def p_comprobante(p):
    'comprobante : CFDI_COMPROBANTE emisor receptor conceptos'
    print("Estructura del comprobante válida")

def p_emisor(p):
    'emisor : CFDI_EMISOR RFC VERSION MONEDA TOTAL FECHA'

def p_receptor(p):
    'receptor : CFDI_RECEPTOR RFC USO_CFDI'

def p_conceptos(p):
    'conceptos : CFDI_CONCEPTO'
    print("Conceptos validados")

# Regla para manejar errores de sintaxis
def p_error(p):
    if p:
        print("Error de sintaxis: %s" % p.value)
    else:
        print("Error de sintaxis en el final del archivo.")

# Función principal para analizar el archivo XML
def validate_xml(file_path):
    # Leer el archivo XML como texto
    with open(file_path, 'r', encoding='utf-8') as f:
        xml_text = f.read()

    lexer = lex.lex()  # Crear el lexer (analizador léxico)
    parser = yacc.yacc()  # Crear el parser (analizador sintáctico)
    
    # Análisis léxico
    lexer.input(xml_text)
    
    # Analizar sintácticamente el XML
    result = parser.parse(xml_text)

    if result:
        print("El archivo XML es válido.")
    else:
        print("El archivo XML es inválido.")

# Probar la función con un archivo XML
validate_xml("cfdi_valido.xml")  # Sustituir con el nombre del archivo de prueba
