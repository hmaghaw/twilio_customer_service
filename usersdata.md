sudo yum update -y
sudo amazon-linux-extras install docker -y
sudo service docker start
sudo systemctl enable docker
sudo usermod -aG docker $USER
sudo curl -L "https://github.com/docker/compose/releases/download/v2.17.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo chmod 666 /var/run/docker.sock
docker-compose --version


# certbot
sudo amazon-linux-extras enable epel
sudo yum clean metadata
sudo yum install epel-release
sudo yum install -y certbot certbot-dns-route53
hash -r
/usr/bin/certbot --version
sudo /usr/bin/certbot certonly --dns-route53 -d "*.coffeehome.ca" -d "coffeehome.ca"
```angular2html
IMPORTANT NOTES:
 - Congratulations! Your certificate and chain have been saved at:
   /etc/letsencrypt/live/coffeehome.ca/fullchain.pem
   Your key file has been saved at:
   /etc/letsencrypt/live/coffeehome.ca/privkey.pem
   Your certificate will expire on 2025-08-22. To obtain a new or
   tweaked version of this certificate in the future, simply run
   certbot again. To non-interactively renew *all* of your
   certificates, run "certbot renew"
 - If you like Certbot, please consider supporting our work by:

   Donating to ISRG / Let's Encrypt:   https://letsencrypt.org/donate
   Donating to EFF:                    https://eff.org/donate-le
```



sudo yum install nginx -y  # for Amazon Linux 2

sudo systemctl enable nginx

sudo systemctl start nginx


sudo nginx -t

sudo nano /etc/nginx/conf.d/coffeehome.conf
## Old
```angular2html
server {
    listen 80;
    server_name coffeehome.ca www.coffeehome.ca;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name coffeehome.ca www.coffeehome.ca;

    ssl_certificate /etc/letsencrypt/live/coffeehome.ca/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/coffeehome.ca/privkey.pem;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}

```
## New
```angular2html
server {
    listen 80;
    server_name coffeehome.ca www.coffeehome.ca;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name coffeehome.ca www.coffeehome.ca;

    ssl_certificate /etc/letsencrypt/live/coffeehome.ca/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/coffeehome.ca/privkey.pem;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /api/dental_clinic/ {
        proxy_pass http://localhost:5001/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        rewrite ^/api/dental_clinic/?(.*)$ /$1 break;
    }
}

```

```angular2html
sudo systemctl reload nginx
```
sudo chmod 644 /opt/n8n/certs/*.pem