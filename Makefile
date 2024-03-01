.PHONY: all vendor build publish

all: vendor build

build:
	hatch build

publish: build
	hatch publish

vendor: .peru/lastimports
	peru reup

.peru/lastimports: peru.yaml
	peru sync
