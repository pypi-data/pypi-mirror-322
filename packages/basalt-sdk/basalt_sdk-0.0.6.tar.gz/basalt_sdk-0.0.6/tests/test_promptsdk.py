import unittest
from unittest.mock import MagicMock
from parameterized import parameterized

from promptsdk import PromptSDK
from logger import Logger
from dtos import PromptResponse, PromptModel, GetPromptDTO
from endpoints.get_prompt import GetPromptEndpoint, GetPromptEndpointResponse

logger = Logger()
mocked_api = MagicMock()
mocked_api.invoke.return_value = (None, GetPromptEndpointResponse(
	warning=None,
	prompt=PromptResponse(
		text="Some prompt",
		model=PromptModel(
			provider="open-ai",
			model="gpt-4o",
			version="latest",
			parameters={
				"temperature": 0.7,
				"topP": 1,
				"maxLength": 4096,
				"responseFormat": "text"
			}
		)
	)
))
mocked_cache = MagicMock()
mocked_cache.get.return_value = None

fallback_cache = MagicMock()
fallback_cache.get.return_value = None

class TestPromptSDK(unittest.TestCase):

	def test_uses_correct_endpoint(self):
		prompt = PromptSDK(
			mocked_api,
			cache=mocked_cache,
			fallback_cache=fallback_cache,
			logger=logger
		)

		prompt.get("slug")

		endpoint = mocked_api.invoke.call_args[0][0]

		self.assertEqual(endpoint, GetPromptEndpoint)

	@parameterized.expand([
		# (slug, version, tag)
		("slug", "version", "tag"),
		("slug", "version", None),
		("slug", None, "tag"),
		("slug", None, None),
	])
	def test_passes_correct_dto(self, slug, version, tag):
		prompt = PromptSDK(
			mocked_api,
			cache=mocked_cache,
			fallback_cache=fallback_cache,
			logger=logger
		)

		prompt.get(slug, version=version, tag=tag)

		dto = mocked_api.invoke.call_args[0][1]

		self.assertEqual(
			dto,
			GetPromptDTO(slug=slug, version=version, tag=tag)
		)

	def test_forwards_api_error(self):
		mocked_api = MagicMock()
		mocked_api.invoke.return_value = (Exception("Some error"), None)

		prompt = PromptSDK(
			mocked_api,
			cache=mocked_cache,
			fallback_cache=fallback_cache,
			logger=logger
		)

		err, res = prompt.get("slug")

		self.assertIsInstance(err, Exception)
		self.assertIsNone(res)

	def test_replaces_variabels(self):
		mocked_api = MagicMock()
		mocked_api.invoke.return_value = (None, GetPromptEndpointResponse(
			warning=None,
			prompt=PromptResponse(
				text="Say hello {{name}}",
				model=PromptModel(
					provider="open-ai",
					model="gpt-4o",
					version="latest",
					parameters={
						"temperature": 0.7,
						"topP": 1,
						"maxLength": 4096,
						"responseFormat": "text"
					}
				)
			)
		))

		prompt = PromptSDK(
			mocked_api,
			cache=mocked_cache,
			fallback_cache=fallback_cache,
			logger=logger
		)

		_, prompt = prompt.get("slug", variables={ "name": "Basalt" })

		self.assertEqual(prompt.text, "Say hello Basalt")

	def test_saves_raw_prompt_to_cache(self):
		mocked_api = MagicMock()
		mocked_api.invoke.return_value = (None, GetPromptEndpointResponse(
			warning=None,
			prompt=PromptResponse(
				text="Say hello {{name}}",
				model=PromptModel(
					provider="open-ai",
					model="gpt-4o",
					version="latest",
					parameters={
						"temperature": 0.7,
						"topP": 1,
						"maxLength": 4096,
						"responseFormat": "text"
					}
				)
			)
		))

		mocked_cache = MagicMock()
		mocked_cache.get.return_value = None

		prompt = PromptSDK(
			mocked_api,
			cache=mocked_cache,
			fallback_cache=fallback_cache,
			logger=logger
		)

		prompt.get("slug", variables={ "name": "Basalt" })

		mocked_cache.put.assert_called_once()
		
		cached_value = mocked_cache.put.call_args[0][1]

		self.assertEqual(cached_value.text, "Say hello {{name}}")

	def test_does_not_request_when_cache_hit(self):
		mocked_api = MagicMock()

		mocked_cache = MagicMock()
		mocked_cache.get.return_value = PromptResponse(
			text="Say hello {{name}}",
			model=PromptModel(
				provider="open-ai",
				model="gpt-4o",
				version="latest",
				parameters={
					"temperature": 0.7,
					"topP": 1,
					"maxLength": 4096,
					"responseFormat": "text"
				}
			)
		)

		prompt = PromptSDK(
			mocked_api,
			cache=mocked_cache,
			fallback_cache=fallback_cache,
			logger=logger
		)
		err, res = prompt.get("slug", variables={ "name": "Cached" })

		mocked_api.invoke.assert_not_called()

		self.assertIsNone(err)
		self.assertEqual(res.text, "Say hello Cached")
  
	def test_caches_in_fallback_forever(self):
		mocked_api = MagicMock()
		mocked_api.invoke.return_value = (None, GetPromptEndpointResponse(
			warning=None,
			prompt=PromptResponse(
				text="Say hello {{name}}",
				model=PromptModel(
					provider="open-ai",
					model="gpt-4o",
					version="latest",
					parameters={
						"temperature": 0.7,
						"topP": 1,
						"maxLength": 4096,
						"responseFormat": "text"
					}
				)
			)
		))

		mocked_cache = MagicMock()
		mocked_cache.get.return_value = None

		prompt = PromptSDK(
			mocked_api,
			cache=mocked_cache,
			fallback_cache=fallback_cache,
			logger=logger
		)

		prompt.get("slug", variables={ "name": "Cached" })

		fallback_cache.put.assert_called_once()
  
	def test_uses_fallback_cache_on_api_failure(self):
		mocked_api = MagicMock()
		mocked_api.invoke.return_value = (Exception("Some error"), None)
  
		fallback_cache = MagicMock()
		fallback_cache.get.return_value = PromptResponse(
				text="From fallback cache",
				model=PromptModel(
					provider="open-ai",
					model="gpt-4o",
					version="latest",
					parameters={
						"temperature": 0.7,
						"topP": 1,
						"maxLength": 4096,
						"responseFormat": "text"
					}
				)
			)

		prompt = PromptSDK(
			mocked_api,
			cache=mocked_cache,
			fallback_cache=fallback_cache,
			logger=logger
		)

		_, res = prompt.get("slug", variables={ "name": "Cached" })

		fallback_cache.get.assert_called_once()
		self.assertEqual(res.text, "From fallback cache")