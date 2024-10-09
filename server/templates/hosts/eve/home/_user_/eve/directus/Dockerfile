FROM directus/directus:11

USER root
RUN corepack enable
RUN pnpm install directus-extension-sync
USER node
