FROM node:18-alpine AS builder
WORKDIR /app

COPY package*.json .

RUN npm ci

COPY . .

RUN NODE_OPTIONS=--max_old_space_size=4096 npm run build
RUN npm prune --production


FROM node:18-alpine
WORKDIR /app

COPY --from=builder /app/build build/
COPY --from=builder /app/node_modules node_modules/
COPY package.json .

EXPOSE 3000

ENV NODE_ENV=production
ENV PORT=3000

CMD [ "node", "build" ]