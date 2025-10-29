"""
AI Text Corrector - Python Flask Version
Corrector de textos en español con IA usando Google Gemini
"""

from flask import Flask, render_template_string, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Configurar la API de Gemini
# IMPORTANTE: Configura tu API key como variable de entorno
# export GEMINI_API_KEY="tu_api_key_aqui"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Text Corrector</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 2rem;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            color: white;
            margin-bottom: 3rem;
        }
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }
        .header p {
            font-size: 1.1rem;
            opacity: 0.9;
        }
        .card {
            background: white;
            border-radius: 1rem;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }
        .card h2 {
            color: #667eea;
            margin-bottom: 1rem;
            font-size: 1.5rem;
        }
        textarea {
            width: 100%;
            min-height: 200px;
            padding: 1rem;
            border: 2px solid #e2e8f0;
            border-radius: 0.5rem;
            font-size: 1rem;
            font-family: inherit;
            resize: vertical;
            transition: border-color 0.3s;
        }
        textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        .button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 1rem 2rem;
            font-size: 1rem;
            border-radius: 0.5rem;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            font-weight: 600;
            margin-top: 1rem;
        }
        .button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        .button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }
        .result {
            background: #f7fafc;
            padding: 1.5rem;
            border-radius: 0.5rem;
            border: 2px solid #e2e8f0;
            margin-top: 1rem;
            line-height: 1.6;
        }
        .loading {
            display: none;
            text-align: center;
            color: #667eea;
            margin-top: 1rem;
        }
        .loading.show {
            display: block;
        }
        .error {
            background: #fed7d7;
            color: #c53030;
            padding: 1rem;
            border-radius: 0.5rem;
            margin-top: 1rem;
            display: none;
        }
        .error.show {
            display: block;
        }
        .copy-button {
            background: #48bb78;
            margin-left: 1rem;
        }
        .copy-button:hover {
            box-shadow: 0 5px 15px rgba(72, 187, 120, 0.4);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>✨ AI Text Corrector</h1>
            <p>Corrige la gramática y sintaxis de tus textos en español con inteligencia artificial</p>
        </div>

        <div class="card">
            <h2>Texto Original</h2>
            <textarea id="inputText" placeholder="Escribe o pega tu texto aquí..."></textarea>
            <button class="button" onclick="correctText()">Corregir Texto</button>
            <div class="loading" id="loading">Corrigiendo texto...</div>
            <div class="error" id="error"></div>
        </div>

        <div class="card" id="resultCard" style="display: none;">
            <h2>Texto Corregido</h2>
            <div class="result" id="result"></div>
            <button class="button copy-button" onclick="copyText()">Copiar Texto</button>
        </div>
    </div>

    <script>
        async function correctText() {
            const inputText = document.getElementById('inputText').value;
            const loading = document.getElementById('loading');
            const error = document.getElementById('error');
            const resultCard = document.getElementById('resultCard');
            
            if (!inputText.trim()) {
                error.textContent = 'Por favor, ingresa algún texto para corregir.';
                error.classList.add('show');
                return;
            }

            error.classList.remove('show');
            loading.classList.add('show');
            resultCard.style.display = 'none';

            try {
                const response = await fetch('/correct', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ text: inputText })
                });

                const data = await response.json();
                
                if (!response.ok) {
                    throw new Error(data.error || 'Error al corregir el texto');
                }

                document.getElementById('result').textContent = data.corrected_text;
                resultCard.style.display = 'block';
            } catch (err) {
                error.textContent = err.message;
                error.classList.add('show');
            } finally {
                loading.classList.remove('show');
            }
        }

        function copyText() {
            const text = document.getElementById('result').textContent;
            navigator.clipboard.writeText(text).then(() => {
                alert('¡Texto copiado al portapapeles!');
            });
        }

        // Permitir corregir con Enter (Ctrl/Cmd + Enter)
        document.getElementById('inputText').addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                correctText();
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Página principal"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/correct', methods=['POST'])
def correct_text():
    """Endpoint para corregir texto"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'No se proporcionó texto'}), 400
        
        if not GEMINI_API_KEY:
            return jsonify({
                'error': 'API key no configurada. Por favor configura GEMINI_API_KEY como variable de entorno.'
            }), 500
        
        # Configurar el modelo Gemini
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Prompt para corrección
        prompt = f"""Eres un experto corrector de gramática y sintaxis en español. Tu tarea es:
1. Corregir cualquier error gramatical
2. Arreglar problemas de sintaxis
3. Mejorar la claridad y fluidez
4. Mantener el significado y tono original
5. SOLO devolver el texto corregido sin explicaciones ni comentarios adicionales
6. Si el texto ya está correcto, devuélvelo tal cual

Texto a corregir:
{text}"""
        
        # Generar corrección
        response = model.generate_content(prompt)
        corrected_text = response.text.strip()
        
        return jsonify({'corrected_text': corrected_text})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    if not GEMINI_API_KEY:
        print("\n⚠️  ADVERTENCIA: No se encontró GEMINI_API_KEY")
        print("Por favor configura tu API key:")
        print("export GEMINI_API_KEY='tu_api_key_aqui'\n")
    
    print("\n🚀 Servidor iniciado en http://localhost:5000")
    print("📝 Presiona Ctrl+C para detener\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
