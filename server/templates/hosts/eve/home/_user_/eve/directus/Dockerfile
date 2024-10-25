FROM directus/directus:11

USER root
RUN corepack enable
USER node

# Workaround to be able to install extensions with 'node' user, only required in v11.1.1
# See https://github.com/directus/directus/issues/23822#issuecomment-2422328156
RUN rm node_modules/.modules.yaml

RUN pnpm install directus-extension-sync
