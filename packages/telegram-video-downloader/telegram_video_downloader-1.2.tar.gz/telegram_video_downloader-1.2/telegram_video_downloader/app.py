
from quart import Quart, request, Response, stream_with_context
from urllib.parse import urlparse
from telethon import TelegramClient, events
from telethon.tl.types import MessageEntityTextUrl, DocumentAttributeFilename
import re
import os
import argparse
import asyncio
import mimetypes


def parse_args():
    parser = argparse.ArgumentParser(description='Telegram Video Downloader')
    parser.add_argument('--api_id', help='Your Telegram API ID', default=os.getenv('API_ID'))
    parser.add_argument('--api_hash', help='Your Telegram API Hash', default=os.getenv('API_HASH'))
    parser.add_argument('--session_file', help='Session file name', default=os.getenv('SESSION_FILE', 'session_name'))
    parser.add_argument('--mode', help='Your Telegram API ID', default='http')
    parser.add_argument('--url', help='Your Telegram message URL with media', default=None)
    parser.add_argument('--output', help='Your output folder', default=None)
    parser.add_argument('--prefix', help='Your output file prfeix', default=None)

    args = parser.parse_args()
    return args


def sanitize_filename(filename):
    """
    Reemplaza caracteres no válidos en los nombres de archivo con guiones bajos.
    """
    # Esta expresión regular reemplaza cualquier caracter que no sea alfanumérico, 
    # guion, guion bajo, punto o espacio por un guion bajo.
    return re.sub(r'[^\w\-_\. ]', '_', filename)

def obtener_extension(mime_type, default='bin'):
    """
    Devuelve la extensión de archivo basada en el mime_type. 
    Si no se encuentra una extensión, usa el valor por defecto.
    """
    extension = mimetypes.guess_extension(mime_type)
    if extension:
        return extension.lstrip('.')  # Remover el punto inicial
    return default

def generar_nombre_alternativo(texto_mensaje, id_mensaje, mime_type=''):
    """
    Genera un nombre de archivo alternativo basado en el nombre del canal y el texto del mensaje.
    
    :param nombre_canal: Nombre del canal.
    :param texto_mensaje: Texto del mensaje.
    :param id_mensaje: ID del mensaje.
    :param mime_type: Tipo MIME del archivo.
    :return: Nombre del archivo generado.
    """
    # Eliminar saltos de línea y espacios adicionales del texto del mensaje
    texto_mensaje_plano = texto_mensaje.replace('\n', ' ').strip()
    
    # Opcional: limitar la longitud para evitar nombres de archivo excesivamente largos
    longitud_maxima = 100
    if len(texto_mensaje_plano) > longitud_maxima:
        texto_mensaje_plano = texto_mensaje_plano[:longitud_maxima] + '...'
    
    # Combinar el nombre del canal y el texto del mensaje
    nombre_combinado = f"{texto_mensaje_plano}"
    
    # Sanitizar el nombre para eliminar caracteres inválidos
    nombre_combinado = sanitize_filename(nombre_combinado)
    
    # Determinar la extensión del archivo basada en el mime_type
    extension_archivo = obtener_extension(mime_type, default='bin')
    
    # Construir el nombre final del archivo
    nombre_archivo = f"{nombre_combinado}.{extension_archivo}"
    
    return nombre_archivo

def extraer_usuario_desde_url(url):
    """
    Extrae el nombre de usuario del canal desde una URL de Telegram.
    """
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.strip('/').split('/')
    if len(path_parts) >= 1:
        return path_parts[0]
    return None

async def obtener_nombre_canal_desde_url(url):
    """
    Obtiene el nombre del canal (título) a partir de la URL del mensaje.
    """
    # Extraer el nombre de usuario del canal desde la URL
    username = extraer_usuario_desde_url(url)
    if not username:
        print("No se pudo extraer el nombre de usuario del canal desde la URL.")
        return None
    
    try:
        # Obtener la entidad del canal
        entidad = await client.get_entity(username)
        # Obtener el nombre del canal (título)
        nombre_canal = entidad.title
        return nombre_canal
    except Exception as e:
        print(f"Error al obtener la entidad del canal: {e}")
        return username

# Initialization of the Telegram client
args = parse_args()
client = TelegramClient(args.session_file, args.api_id, args.api_hash)
app = Quart(__name__)
CHUNK_SIZE = 1 * 1024 * 1024  # 1MB

async def download_generator(client, document, start, end):
    pos = start
    remaining = end - start + 1
    async for chunk in client.iter_download(document, offset=pos, limit=remaining):
        yield chunk
        remaining -= len(chunk)
        if remaining <= 0:
            break

async def download_url(url, output, prefix):
    split_url = url.split('/')
    channel = split_url[3]  if not split_url[3] == 'c' else split_url[4]
    message_id = int(split_url[-1])
    nombre_canal = prefix
    if not prefix:
        nombre_canal = await obtener_nombre_canal_desde_url(url)
        if not nombre_canal:
            nombre_canal = "Unknown"

    await client.start()

    try:
        message = await client.get_messages(int(channel) if channel.isdigit() else channel, ids=int(message_id))
    except:
        message = await client.get_messages(int(f'-100{channel}'), ids=int(message_id))
    if not message or not hasattr(message, 'media'):
        return "Message not found or it doesn't contain any media", 404
    
    file_name = None  # Nombre por defecto si no se encuentra el nombre del archivo
    # Intentar obtener el file_name desde los atributos del documento principal
    if hasattr(message.media, 'document') and hasattr(message.media.document, 'attributes'):
        for attribute in message.media.document.attributes:
            if hasattr(attribute, 'file_name'):
                file_name = attribute.file_name
                break

    # Si no se encontró o es un nombre generado por MTProto, buscar en alt_documents
    if not file_name or file_name.startswith('mtproto:'):
        if hasattr(message.media, 'alt_documents'):
            if message.media.alt_documents:
                for alt_doc in message.media.alt_documents:
                    if hasattr(alt_doc, 'attributes'):
                        for attribute in alt_doc.attributes:
                            if hasattr(attribute, 'file_name'):
                                potential_file_name = attribute.file_name
                                if not potential_file_name.startswith('mtproto:'):
                                    file_name = potential_file_name
                                    break
                    if file_name and not file_name.startswith('mtproto:'):
                        break

    # Si aún no se encontró un file_name válido, generar uno alternativo
    if not file_name or file_name.startswith('mtproto:'):
        # Obtener el texto del mensaje y eliminar saltos de línea
        texto_mensaje = message.message if hasattr(message, 'message') else ''
        
        # Obtener el mime_type si está disponible
        mime_type = ''
        if hasattr(message.media, 'document') and hasattr(message.media.document, 'mime_type'):
            mime_type = message.media.document.mime_type
        elif hasattr(message.media, 'alt_documents') and len(message.media.alt_documents) > 0:
            mime_type = message.media.alt_documents[0].mime_type  # Por ejemplo, usa el mime_type del primer alt_document
        
        # Generar el nombre de archivo alternativo
        file_name = generar_nombre_alternativo(texto_mensaje, message.id, mime_type)

    if file_name:
        print(f"Nombre del archivo encontrado: {file_name}")
    else:
        print("No se encontró un nombre de archivo en el mensaje.")
            

    def progress_callback(current_bytes, total_bytes):
        print(f"\rDownloaded {current_bytes} out of {total_bytes} bytes: {(current_bytes/total_bytes)*100:.1f}%", end='')

    file_name = f"{nombre_canal} - {file_name}"

    # Asegúrate de imprimir una nueva línea después de la descarga
    file_path = await client.download_media(message.media, file=os.path.join(output, file_name), progress_callback=progress_callback)
    print("\nFile downloaded to", file_path)

    return file_path
    
@app.route("/telegram/direct/<telegram_id>")
async def telegram_direct(telegram_id):
    channel = telegram_id.split('-')[0]
    video_id = int(telegram_id.split('-')[1])
    if not video_id:
        return "Video ID is required", 400

    await client.start()
    try:
        message = await client.get_messages(int(channel) if channel.isdigit() else channel, ids=int(video_id))
    except:
        message = await client.get_messages(int(f'-100{channel}'), ids=int(video_id))
    
    if not message or not hasattr(message, 'media'):
        return "Message not found or it doesn't contain any media", 404

    document = message.media.document
    file_size = document.size

    range_header = request.headers.get("Range")
    start, end = 0, file_size - 1 # Suposiciones iniciales
    headers = {
        "Accept-Ranges": "bytes", 
    }

    if range_header:
        match = re.match(r"bytes=(\d+)-(\d*)", range_header)
        if match:
            start, end = match.groups()
            start = int(start)
            end = int(end) if end else file_size - 1

            headers["Content-Range"] = f"bytes {start}-{end}/{file_size}"
            headers["Content-Length"] = str(end - start + 1)
            status_code = 206  # Partial Content
        else:
            return "Invalid Range header", 416  # Range Not Satisfiable
    else:
        status_code = 200  # OK
        headers["Content-Length"] = str(file_size)

    return Response(download_generator(client, document, start, end), status=status_code, headers=headers, content_type="video/mp4")

def main():
    if args.mode == 'http':
        app.run(port=5151)
    elif args.mode == 'download':
        if args.url and args.output:
            if 'https://t.me/':
                asyncio.run(download_url(args.url, args.output, args.prefix))
            else:
                print('Starts Telegram message URL with https://t.me/...')
        else:
            print('With download mode a message url and output are required')

    
if __name__ == '__main__':
    main()