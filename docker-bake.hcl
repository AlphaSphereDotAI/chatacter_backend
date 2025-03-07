variable "IMAGE" {
  default = "ghcr.io/AlphaSphereDotAI/chatacter_backend"
}
variable "TAG" {
  default = "dev"
}
target "default" {
  name = item.name
  matrix = {
	item = [
	  {
		name = "chatacter_backend_app"
		context = "https://github.com/AlphaSphereDotAI/chatacter_backend_app"
		tags = [ "${IMAGE}_app:${TAG}", "${IMAGE}_app:latest" ]
	  }, {
		name = "chatacter_backend_video_generator"
		context = "https://github.com/AlphaSphereDotAI/chatacter_backend_video_generator"
		tags = [ "${IMAGE}_video_generator:${TAG}", "${IMAGE}_video_generator:latest" ]
	  }, {
		name = "chatacter_backend_voice_generator"
		context = "https://github.com/AlphaSphereDotAI/chatacter_backend_voice_generator"
		tags = [ "${IMAGE}_voice_generator:${TAG}", "${IMAGE}_voice_generator:latest" ]
	  }
	]
  }
  tags = item.tags
  dockerfile = "Dockerfile"
  context = item.context
  platforms = [ "linux/amd64", "linux/arm64" ]
  args = {
	VERSION = TAG
  }
}
