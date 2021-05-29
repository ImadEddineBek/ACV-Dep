IMAGE_NAME = training_yolov4
TAG = latest

build:
	docker build -t $(IMAGE_NAME):$(TAG) .

push: build login
	docker push  $(IMAGE_NAME):$(TAG)

clean:
	docker rmi -f (IMAGE_NAME):$(TAG)



