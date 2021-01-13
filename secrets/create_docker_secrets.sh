#!/bin/bash

# Extra script to use external secrets instead of .txt files from this directory.
# Modify 'docker-compose.yml' file first and in secrets section set 'external: true' instead of 'file: ./path'.
# Run it on swarm manager machine and then remove this file.

echo "postgresql://admin:password@db/northwind" | sudo docker secret create db_uri -
echo "admin" | sudo docker secret create login -
echo "password" | sudo docker secret create password -
echo "Acf6UcFexAEmTjjuHcNJWTiS07SiJ1UC24p7XofwuJD0pPX_jJBRf3RbnivVvkT6fJ8vZbFAezJA5vfM" | sudo docker secret create paypal_client -
echo "EPXxxbwo-sKBW764n9LKDVytixvLXBeGTsf9E8ZVHzKpBaGrH-8ejxfF9lp7UiDsCbfsDUR9321DNwOa" | sudo docker secret create paypal_secret -
