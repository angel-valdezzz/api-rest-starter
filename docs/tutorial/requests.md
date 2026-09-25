# Peticiones con requests

`requests` traduce una llamada Python a una petición HTTP. La variable `response` te deja inspeccionar la respuesta.

## Consultar: GET

```python
response = requests.get(f"{api_url}/users/1", timeout=10)
assert response.status_code == 200
assert response.json()["id"] == 1
```

`timeout=10` limita la espera de red. `response.json()` convierte un cuerpo JSON válido a objetos Python. Si la respuesta no es JSON, usa `response.text` o `response.content`.

## Crear: POST con JSON

```python
payload = {"name": "Angel"}
response = requests.post(f"{api_url}/users", json=payload, timeout=10)
assert response.status_code == 201
```

`json=payload` serializa el diccionario como JSON y configura el tipo de contenido correspondiente.

## Enviar formulario: POST con data

```python
response = requests.post(
    f"{api_url}/echo-form",
    data={"nombre": "Angel", "rol": "QA"},
    timeout=10,
)
assert response.status_code == 200
```

Con un diccionario en `data=`, `requests` codifica un formulario `application/x-www-form-urlencoded`. Es el equivalente al apartado **x-www-form-urlencoded** de Postman. Para un cuerpo JSON de Postman usa `json=`, no `data=`.

## Otras partes frecuentes

```python
requests.get(url, params={"page": 2}, timeout=10)        # ?page=2
requests.get(url, headers={"Accept": "application/json"}, timeout=10)
requests.delete(url, timeout=10)
```

!!! warning "Al trabajar con servicios reales"
    No incluyas tokens, contraseñas ni datos personales en el HTML. El ejemplo muestra el cuerpo porque usa datos ficticios; adapta `registrar_http()` antes de registrar tráfico sensible.
