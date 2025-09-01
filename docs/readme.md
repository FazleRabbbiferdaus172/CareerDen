this project requires latex installed in you system:
1. using docker to install latex?

In terminal 
1. run a container using following command
```
docker run -d --name latex_server -v "$(pwd)"/<input_dir>:/workdir/<input_dir> -v "$(pwd)"/<output_dir>:/workdir/<output_dir> texlive/texlive:latest tail -f /dev/null
```

alternatively following command could be used to run container with current user

```
docker run -d --user "$(id -u):$(id -g)" --name latex_server -v "$(pwd)"/<input_dir>:/workdir/<input_dir> -v "$(pwd)"/<output_dir>:/workdir/<output_dir> texlive/texlive:latest tail -f /dev/null
```

2. to generate a pdf file out of tex file to generate a pdf of same name
```
docker exec latex_server2 pdflatex --output-directory=./<output_dir> ./<input_dir>/<filename>.tex
```
___