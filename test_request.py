import requests
import json #Formatea la salida JSON
from unidecode import unidecode 

#URL base de la API en FastAPI 
BASE_URL = "http://127.0.0.1:8000"

#Función auxiliar para imprimir títulos de sección principal
def print_section(title: str):
    print("\n" + "-" * 70)
    print(f"🚀 {title.upper()} ---")
    print("-" * 70 + "\n")

#Función auxiliar para imprimir un título de sub-sección
def print_subsection(description: str):
    print("\n" + "-" * 70)
    print(description)
    print("-" * 70 + "\n")   

#Función auxiliar para imprimir las respuestas de la API
def print_api_response(response, action_description=""):
    #Imprime la respuesta de la API de forma formateada
    status_code = response.status_code
    status_emoji = ""
    if 200 <= status_code < 300:
        status_emoji = "✅ ÉXITO"
    elif 400 <= status_code < 500:
        status_emoji = "❌ CLIENTE ERROR"
    elif 500 <= status_code < 600:
        status_emoji = "⚠️ SERVIDOR ERROR"
    else:
        status_emoji = "❓ INESPERADO"

    print(f"{action_description} -> Código de estado: {status_code} ({status_emoji})")

    try:
        #Intenta parsear la respuesta como JSON
        json_data = response.json()
        if isinstance(json_data, list):
            #Si la respuesta es una lista la imprime con formato
            print(f"Lista de libros:\n{json.dumps(json_data, indent=2, ensure_ascii=False)}\n")
        else:
            #Si es un solo objeto JSON, lo imprime con formato
            print(f"Respuesta: {json.dumps(json_data, indent=2, ensure_ascii=False)}\n")
    except json.decoder.JSONDecodeError as e:
        #Si la respuesta no es un JSON válido, imprime el error y el texto
        print(f"⚠️ Error al interpretar la respuesta como JSON: {e}")
        print(f"Contenido recibido (no JSON válido):\n{response.text}\n")
    except Exception as e:
        #Captura cualquier otra excepción inesperada durante el procesamiento de la respuesta
        print(f"⚠️ Ocurrió un error inesperado al procesar la respuesta: {e}")
        print(f"Contenido recibido:\n{response.text}\n")


#Mensaje de bienvenida 
if __name__ == "__main__":
    print("\n" + "-" * 70)
    print("---  Bienvenid@ a tu API de libros 📚  ---")
    print("-" * 70 + "\n")


#1. Lista de libros a añadir a la base de datos 
print("➕ Añadiendo libro(s) a la base de datos...\n")
books_to_add = [
    {
        "title": "El Problema de los Tres Cuerpos",
        "author": "Liu Cixin",
        "year": 2008,
        "cover_url": "https://images.cdn1.buscalibre.com/fit-in/360x360/b2/d1/b2d184715ec2e5b7c02b28c89b703e7c.jpg",
        "is_read": True
    },
    {
        "title": "Dune",
        "author": "Frank Herbert",
        "year": 1965, 
        "cover_url": "https://images.cdn2.buscalibre.com/fit-in/360x360/bb/e3/bbe330768997a38758838d61399e5306.jpg",
        "is_read": False
    },
    {
        "title": "La Bibliotecaria de Auschwitz",
        "author": "Antonio Iturbe",
        "year": 2012,
        "cover_url": "https://images.cdn1.buscalibre.com/fit-in/360x360/f8/46/f8469d453880436d43e5797276536b13.jpg",
        "is_read": False
    },
    {
        "title": "Romper el Círculo",
        "author": "Colleen Hoover",
        "year": 2016,
        "cover_url": "https://images.cdn1.buscalibre.com/fit-in/360x360/ed/d1/edd1273977ef29d6600c3c6f600f7226.jpg",
        "is_read": False
    },
    {
        "title": "Hábitos Atómicos",
        "author": "James Clear",
        "year": 2018,
        "cover_url": "https://images.cdn1.buscalibre.com/fit-in/360x360/6a/c5/6ac5a40735d4668b8e0e643a6d13d2f2.jpg",
        "is_read": True
    },
    {
        "title": "Reina Roja",
        "author": "Juan Gómez-Jurado",
        "year": 2018,
        "cover_url": "https://images.cdn2.buscalibre.com/fit-in/360x360/1c/65/1c65d642337d1d22bb1ee8168270562e.jpg",
        "is_read": False
    },
    {
        "title": "El Arte de No Amargarse la Vida",
        "author": "Rafael Santandreu",
        "year": 2012,
        "cover_url": "https://images.cdn1.buscalibre.com/fit-in/360x360/12/f2/12f2c8d28a3f854b73b27b9933180b18.jpg",
        "is_read": False
    }
]
#Recorre la lista y añade cada libro con una petición POST
for book_data in books_to_add:
    response = requests.post(f"{BASE_URL}/books/", json=book_data) #Envía el libro en formato JSON
    print_api_response(response, f"➕ Añadiendo libro: '{book_data['title']}'")

#Intento de añadir un libro que ya existe en la base de datos por título (GET /books)
print_subsection("Intentando añadir un libro que ya existe...") #Se espera recibir un error 409
duplicate_book_data = {
    "title": "El Problema de los Tres Cuerpos",
    "author": "Anónimo",  #Cambiamos el autor pero eso no debe afectar a la duplicidad
    "year": 2023,
    "cover_url": "https://images.cdn1.buscalibre.com/fit-in/360x360/b2/d1/b2d184715ec2e5b7c02b28c89b703e7c.jpg",
    "is_read": False,
}
response = requests.post(f"{BASE_URL}/books/", json=duplicate_book_data)
print_api_response(response, f"Añadiendo el libro duplicado '{duplicate_book_data['title']}'")


#2. PRUEBAS DE CONSULTAS DE LIBROS (GET /books/ y GET /books/{title})
print_section("--- 🔍 INICIANDO PRUEBAS DE CONSULTA DE LIBROS ---")
#Consulta todos los libros que tenemos en la base de datos con una petición GET /books/
print("Consultando todos los libros de la base de datos...\n")
response = requests.get(f"{BASE_URL}/books/")
print_api_response(response, "Obteniendo todos los libros")

#Buscar un libro que ya existe en la base de datos (GET /books/{title}) 
print_subsection("Buscando un libro existente por título...")
search_title_found = "Dune"
response = requests.get(f"{BASE_URL}/books/{search_title_found}")
print_api_response(response, f"Buscando el libro: '{search_title_found}'")

#Buscar un libro que no existen la base de datos (GET /books/{title})
print_subsection("Buscando un libro que NO existe en la base de datos...") #Se espera como resultado un error 404
search_title_not_found = "Pepa Pimienta"
response = requests.get(f"{BASE_URL}/books/{search_title_not_found}")
print_api_response(response, f"Buscando el título: '{search_title_not_found}'")


#3. PRUEBAS DE ACTUALIZACIÓN DE LIBROS (PUT /books/{book_id})
print_section("--- 🔄 INICIANDO PRUEBAS DE ACTUALIZACIÓN DE LIBROS ---")

#Marcar un libro como leído (PUT /books/{title}/read)
print("Marcando como 'leído' el libro 'Romper el Círculo'\n")
update_title_read = "Romper el Círculo"
update_data = {"is_read": True}
response = requests.put(f"{BASE_URL}/books/{update_title_read}", json=update_data) #Envía el título original en la URL
print_api_response(response, f"Actualizando el libro {update_title_read} al estado: leído")

#Verificar si un libro se encuentra en estado leido o no (GET /books/{title})
print_subsection("Verificando el estado de lectura del libro 'Romper el Círculo'")
response = requests.get(f"{BASE_URL}/books/{update_title_read}")
if response.status_code == 200:
    try:
        book_info = response.json()
        #Verifica el campo 'is_read' de la respuesta JSON
        read_status_text = "✅ leído" if book_info.get("is_read", False) else "❌ no leído"
        print(f" Resultado: El libro '{update_title_read}' está {read_status_text}\n")
    except json.decoder.JSONDecodeError:
        print(f" ⚠️ Error: La respuesta para verificar el estado de '{update_title_read}' no es JSON válido.")
        print(f" Contenido recibido:\n{response.text}\n")
    except Exception as e:
        print(f" ⚠️ Ocurrió un error inesperado al procesar la verificación: {e}")
        print(f" Contenido recibido:\n{response.text}\n")
else:
    print_api_response(response, f"Error al intentar obtener el libro '{update_title_read}' para verificar su estado")

#Eliminar un libro (DELETE /books/{title})
print_section("--- 🗑️ INICIANDO PRUEBAS DE ELIMINACIÓN DE LIBROS ---")
print("Eliminando el libro 'El Arte de No Amargarse la Vida'\n")
book_title_to_delete = "El Arte de No Amargarse la Vida"
response = requests.delete(f"{BASE_URL}/books/{book_title_to_delete}")
print_api_response(response, f"Eliminando el libro: '{book_title_to_delete}'")

#Eliminar un libro que no existe (DELETE /books/{title})
print("Intentando eliminar un libro que NO existe")  # Se espera error 404
non_existent_title_delete = "La Casa de Bernarda Alba"
response = requests.delete(f"{BASE_URL}/books/{non_existent_title_delete}")
print_api_response(response, f"Eliminando el libro '{non_existent_title_delete}'")
