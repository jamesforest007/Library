# Waitress configuration
host = "127.0.0.1"
port = 8000
threads = 4  # Number of threads to handle requests
url_scheme = 'http'  # URL scheme to use
url_prefix = ''  # URL prefix if behind a proxy

# Buffer settings
buffer_size = 65535
cleanup_interval = 30
channel_timeout = 60 