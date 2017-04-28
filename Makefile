NAME = bufferapp/slack-channels

build:
	docker build -t $(NAME) .

dev:
	docker run -it -v $(PWD):/work -v $(PWD)/.ipython:/root/.ipython --rm $(NAME) bash

notebook:
	docker run -p 8888:8888 -v $(PWD):/work -it --rm $(NAME)
