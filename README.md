# webstringer
Monitor a website continuously for certain text/changes!



Exmaple docker:
```
(create webstringer subdirectory with apikey)
docker run -it --rm -v $(pwd)/webstringer/:/vol/ jefftadashi/webstringer

(for building on my master machine)
docker buildx build --platform linux/amd64,linux/arm64,linux/ppc64le,linux/s390x,linux/386,linux/arm/v7,linux/arm/v6 -t jefftadashi/webstringer:latest -t jefftadashi/webstringer:multi-arch --push .
```