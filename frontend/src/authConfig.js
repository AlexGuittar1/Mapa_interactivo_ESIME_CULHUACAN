// ARCHIVO: src/authConfig.js
// CONFIGURACION DE AUTENTICACION Y SERVICIOS EXTERNOS
// Mantiene las llaves y redirecciones correspondientes al proveedor Microsoft Entra ID (Azure AD).

import { PublicClientApplication } from "@azure/msal-browser";

export const msalConfig = {
    auth: {
        clientId: "YOUR_CLIENT_ID_HERE", // REEMPLAZAR IDENTIFICADOR DE AZURE
        authority: "https://login.microsoftonline.com/common",
        redirectUri: "http://localhost:5173",
    },
    cache: {
        cacheLocation: "sessionStorage",
        storeAuthStateInCookie: false,
    }
};

export const loginRequest = {
    scopes: ["User.Read"]
};

export const msalInstance = new PublicClientApplication(msalConfig);
