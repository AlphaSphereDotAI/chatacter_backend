variable "IMAGE" {
  default = "ghcr.io/alphaspheredotai/chatacter_backend"
}
target "default" {
  name = item.name
  matrix = {
  	item = [
  	  {
    		name = "chatacter_backend_app"
    		context = "https://github.com/AlphaSphereDotAI/chatacter_backend_app.git"
    		tags = [ "${IMAGE}_app:dev", "${IMAGE}_app:latest" ]
  	  },
  		{
    		name = "chatacter_backend_video_generator"
    		context = "https://github.com/AlphaSphereDotAI/chatacter_backend_video_generator.git"
    		tags = [ "${IMAGE}_video_generator:dev", "${IMAGE}_video_generator:latest" ]
  	  },
  		{
    		name = "chatacter_backend_voice_generator"
    		context = "https://github.com/AlphaSphereDotAI/chatacter_backend_voice_generator.git"
    		tags = [ "${IMAGE}_voice_generator:dev", "${IMAGE}_voice_generator:latest" ]
  	  }
  	]
  }
  tags = item.tags
  dockerfile = "Dockerfile"
  context = item.context
  platforms = [ "linux/amd64", "linux/arm64" ]
  cache_from = [
    {
      type = "gha"
    }
  ]
  cache_to =[
    {
      type = "gha"
      mode = "max"
    }
  ]
}
