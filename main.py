## Multimodal agent connecting tools.
# by Boris Alzamora
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI, OpenAI
from dotenv import load_dotenv
import uuid
import os
import openai
import requests
load_dotenv()

class Toolbox:
    @tool()
    def obtener_caso(folder_path = "./casos/") -> str:
        """
        Retorna un caso de la lista con los casos de siniestros registradoa en la bandeja de atencion del especialista
        de este contenido se podra obtener el ID del CASO
        """
        files_data=[]
        if not os.path.exists(folder_path):
             print(f"Folder '{folder_path}' no existe.")
        try:
            files = os.listdir(folder_path)
            
            if not files:
                print(f"Sin casos en '{folder_path}'.")
                return None
            
            # Cargar cada archivo
            for filename in files:
                file_path = os.path.join(folder_path, filename)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = f.read()
                    print(f"Loaded: {filename}")
                    return data
                except Exception as e:
                    print(f"Error reading {filename}: {e}")
        
            return files_data
        except Exception as e:
            print(f"Error accessing folder '{folder_path}': {e}")
            return files_data

    @tool()
    def guardar_reporte(reporte: str, idcaso: str, carpeta = "./reportes/") -> int:
        """
        Guarda el reporte en formato MD en la ruta de reportes
        El reporte del siniestro tiene referencias en su contenido a las imagenes ya persistidas en otras rutas

        Args:
            reporte (str): reporte a ser guardado en formato markdown donde las imagenes estan referenciadas.
            idcaso (str): el id del caso que del cual se esta escribiendo.
            carpeta (str): Ruta de la carpeta donde se guardarán los reportes.

        Returns:
            string con la ruta o path hacia el reporte
        """
        if not os.path.exists(carpeta):
             os.mkdir(carpeta)
             print(f"Folder '{carpeta}' creado.")
        else:
            name = str(uuid.uuid4())+"-report.md"
            ruta_completa = os.path.join(carpeta, name)
            with open(ruta_completa, "w", encoding="utf-8") as r:
                r.write(reporte)
            print(f"Archivo guardado en: {ruta_completa}")
        return ruta_completa
    
    @tool
    def obtener_entrevista(id_caso: str, carpeta: str = "./entrevistas/") -> str:
        """
        Obtiene la transcripcion de la entrevista que salio en podcast noticiero que hablaron sobre el accidente
        este podcast tiene varios episodios por lo que sera necesario el id del caso.
        internamente hace uso de whisper para obtener el audio del podcast y transcribirlo.
        
        Args:
            id_caso (str): Identificador único del caso de siniestro.
            carpeta (str, optional): Ruta donde se almacenan las entrevistas. Por defecto "./entrevistas/".
            
        Returns:
            str: Transcripcion completa de la entrevista publicada en un podcast de un noticiero local
            donde cubren el accidente en referencia
                 
        Raises:
            FileNotFoundError: Si la carpeta de entrevistas no existe.
            ValueError: Si el id_caso no es válido o no existe una entrevista asociada.
        """
        if not os.path.exists(carpeta):
            return None
        try:
            transcripts = "./transcripts/"
            if os.path.exists(transcripts):
                files = os.listdir(transcripts)
                for file in files:
                    with open(file, "r") as f:
                        transcription = f.read()
                    break
                return transcription
            else:
                os.mkdir("./transcripts/")
            
            audiofile = ""
            files = os.listdir(carpeta)
            if not files:
                print(f"Sin casos en '{carpeta}'.")
                return None
            else: # tenemos entrevistas
                for filename in files:
                    audiofile = str(os.path.join(carpeta, filename))
                    break
                
            client = OpenAI()

            audio_file= open(audiofile, "rb")

            transcription = client.audio.transcriptions.create(
                model="gpt-4o-transcribe", 
                file=audio_file
            )

            with open(os.path.join(transcripts, "transcript.txt"), "w") as f:
                f.write(transcription.text)
            return transcription.text
            
        except Exception as e:
            print(f"Error accessing folder '{carpeta}': {e}")
            return None
        
    
    @tool
    def generar_croquis_accidente(descripcion: str, carpeta: str = "./images", formato: str = "PNG") -> str:
        """
        Genera imágenes de croquis del accidente de tránsito basadas en las descripciones proporcionadas.
        Utiliza modelos de IA generativa para crear representaciones visuales de la escena del accidente.

        Args:
            Descripcion: La descripcion textuales del accidente, debe ser clara y detallada, incluyendo:
            - Posición de los vehículos
            - Dirección del impacto
            - Elementos del entorno (semáforos, señales, etc.)
            - Condiciones de la vía
            carpeta: ruta donde se dejara la imagen generada
            formato: la extension con la cual se guardara el archivo
        Returns:
            La ruta donde fue guardada la imagen generada del croquis del accidente.
        Raises:
            ValueError: Si alguna descripción está vacía o no es lo suficientemente detallada.
            RuntimeError: Si hay un error en la generación de las imágenes.
        """
        try:
            # Generate the image
            response = openai.images.generate(
                model="dall-e-3",  # Specify the DALL-E model (e.g., "dall-e-2" or "dall-e-3")
                prompt=descripcion,
                n=1,  # Number of images to generate
                size="1024x1024",  # Image size (e.g., "256x256", "512x512", "1024x1024")
                quality="standard" # Or "hd" for higher quality images
            )
            image_url = response.data[0].url
            print(f"Generated image URL: {image_url}")

            image_data = requests.get(image_url).content
            image_path = os.path.join(carpeta, str(uuid.uuid4())+f"-imagen.{formato.lower()}")
            with open(image_path, "wb") as f:
                f.write(image_data)
            print(f"Image saved as {image_path}")
            return "."+image_path
        except Exception as e:
            print(f"An error occurred: {e}")
        return None


if __name__ == "__main__":
    model="gpt-4o-mini"
    temp=0.1
    # Instance attributes
    llm = ChatOpenAI(model=model, temperature=temp)
    toolbox = Toolbox()
    agent = create_agent(
        model=llm,
        system_prompt="""Eres un especialista en la toma de información de los accidentes de tránsito de la aseguradora Calma S.A.
            tu objetivo principal es redactar el reporte de accidentes cuando uno de estos ocurre, a los cuales determinaras caso de siniestro
            Tienes una bandeja de atencion donde llegan los casos, para ello debes apoyarte de tus herramientas para obtener un caso y obtener la
            informacion asociada al mismo.
            Tu reporte final debe ser elaborado en formato markdown, incluyendo una imagen generada del croquis del accidente y datos relevantes para el reporte.
            Una vez tengas tu reporte elaborado, debe ser guardado en la carpeta "reportes"
            """,
        tools=[toolbox.generar_croquis_accidente, toolbox.guardar_reporte, toolbox.obtener_caso, toolbox.obtener_entrevista],
        debug=False
    )
    response = agent.invoke({"query": "Genera el reporte de siniestro, junto con el croquis del accidente, busca mi caso con el ID_CASO: 00012025"})
    print(response)