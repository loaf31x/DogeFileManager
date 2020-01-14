### Requirements
* Python 3
* Flask
* Flask-RESTful & Flask HTTPAuth

### Installation

```
python3 -m pip install flask flask_restful flask_httpauth
```

### Usage

```
python3 app.py
```

### Sample Nginx configuration
"manager-server" -> address on which uwsgi is listening.  
"/manager-src" -> path to project files

```
  server {
    listen 443 ssl http2;
    
    server_name manager.lab.local;

    location / {
      uwsgi_pass manager-server:3031;
      include uwsgi_params;
    }

    location /files {
      # Allows API use from other apps
      add_header 'Access-Control-Allow-Origin' "$http_origin" always;
      add_header 'Access-Control-Allow-Credentials' 'true' always;
      add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS' always;
      add_header 'Access-Control-Allow-Headers' 'Accept,Authorization,Cache-Control,Content-Type,DNT,If-Modified-Since,Keep-Alive,Origin,User-Agent,X-Requested-With' always;

      uwsgi_pass manager-server:3031;
      include uwsgi_params;
    }

    location /static {
      alias /manager-src/static/;
    }
  }
```
