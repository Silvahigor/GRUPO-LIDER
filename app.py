from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

TOKENS = {
    "SHOPPARTNER": "",
    "MAQLIDER": ""
}

@app.route('/buscar', methods=['POST'])
def buscar_variacoes():
    data = request.get_json()
    ad_id = data.get('ad_id', '').strip()
    empresa = data.get('empresa')
    token = data.get('token', '').strip()

    if not ad_id or not empresa or not token:
        return jsonify({"error": "Dados inválidos"}), 400

    full_id = f"MLB{ad_id}" if not ad_id.upper().startswith("MLB") else ad_id.upper()
    url = f'https://api.mercadolibre.com/items/{full_id}?include_attributes=all'

    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return jsonify({
            "error": "Erro ao consultar anúncio",
            "status": response.status_code,
            "body": response.text
        }), 400

    data = response.json()
    pai = {"id": data.get("id"), "title": data.get("title")}
    variacoes = []

    for v in data.get("variations", []):
        sku = next((attr.get('value_name') for attr in v.get('attributes', []) if attr.get('id') == 'SELLER_SKU'), 'SKU não encontrado')
        variacoes.append({"id": v.get("id"), "sku": sku})

    return jsonify({"pai": pai, "variacoes": variacoes})

if __name__ == '__main__':
    app.run(debug=True)