# Cómo Personalizar el Mapa de la Escuela

Para reemplazar el mapa genérico con el mapa específico de la ESIME, tienes dos opciones:

## Opción 1: Superponer una imagen (Plano Oficial)

Si tienes una imagen (`.png`, `.jpg`, `.svg`) del plano de la escuela:

1.  **Guarda la imagen** en la carpeta `frontend/public/` (por ejemplo, llámala `mapa_esime.png`).
2.  **Edita el archivo** `frontend/src/mapConfig.js`.
3.  Cambia `enabled` a `true` y ajusta las coordenadas de las esquinas (`bounds`) para que coincidan con la realidad:

```javascript
overlay: {
    enabled: true,
    imageUrl: '/mapa_esime.png',
    bounds: [
        [19.310000, -99.113000], // Coordenada Sur-Oeste
        [19.312500, -99.110500]  // Coordenada Norte-Este
    ]
}
```

> **Tip**: Para encontrar las coordenadas, puedes usar Google Maps, hacer clic derecho en las esquinas de la escuela y copiar la latitud/longitud.

## Opción 2: Usar solo marcadores reales

Si no tienes una imagen pero quieres que los puntos (Edificios) estén 100% precisos:

1.  Abre `poblar_bd.py`.
2.  Edita la lista `edificios` con las coordenadas exactas de cada edificio.
3.  Vuelve a correr el script de población:
    ```bash
    rm instance/campus.db
    python3 poblar_bd.py
    ```
