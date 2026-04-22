FROM node:18-alpine AS builder
WORKDIR /app
COPY package.json .
RUN npm install --legacy-peer-deps && \
    npm install ajv@^8.11.0 ajv-keywords@^5.0.0 --legacy-peer-deps
COPY . .
ENV GENERATE_SOURCEMAP=false
ENV DISABLE_ESLINT_PLUGIN=true
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx-frontend.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
