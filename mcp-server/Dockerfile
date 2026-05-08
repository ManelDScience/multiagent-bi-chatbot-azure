#Usa una imagen base de Node.js ligera (Linux Alpine)
FROM node:20-alpine

#Define la carpeta de trabajo dentro del contenedor
WORKDIR /app

#Copia packagejson y package-loc.json al contentedor
COPY package*.json ./
#Instala dependencias dentor del contenedor
RUN npm install

#Copia todo el código restante al contenedor
COPY . .

#Indica que el servicio usa el puerto 3000 (Informativo)
EXPOSE 3000

#Comando que se ejecuta al arrancar el contenedor
CMD ["node", "server.js"]
