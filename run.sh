docker run -it --rm -d -p 30193:80 --name jnascimento_web --userns=host \
  -v $PWD/site-content:/usr/share/nginx/html nginx 

