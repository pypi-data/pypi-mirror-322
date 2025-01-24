from __future__ import annotations

from pydantic import BaseModel


class Image(BaseModel):
    #: The base64-encoded JSON of the generated image, if `response_format` is `b64_json`
    b64_json: str | None = None

    #: The URL of the generated image, if `response_format` is `url` (default)
    url: str | None = None


class ImageResponse(BaseModel):
    # Unique object identifier.
    id: str

    #: Model used for Image Generation
    model: str

    #: The object type, which is always `text_to_image`.
    object: str

    #: The Unix timestamp of when the completion was created.
    created: float

    #: Data object which is a list of Image objects.
    data: list[Image]

    # TODO: for all requests
    # generation_time: float


class ImageSamplingParams(BaseModel):
    #: Characteristics to avoid in the image being generated
    negative_prompt: str | None = "blurry"

    #: The initial value used to generate random numbers. Set a unique seed for reproducible image results.
    seed: int | None = 27

    #: The amount by which the seed value increases with each iteration. Adjust this to create a series of visually consistent, yet unique images
    seed_increment: int | None = 100

    #: The number of images to generate
    n: int | None = 1

    #: The total inference steps taken during image generation. Higher steps improve quality but increase generation time.
    num_inference_steps: int | None = 20

    #: Width x Height of every image being generated
    size: str | None = "512x512"

    #: Controls how closely the image follows the input text. Increase for more adherence, decrease for creativity and diversity
    guidance_scale: float | None = 6.5

    # TODO:
    #: cache_interval
    cache_interval: int | None = None

    #: Response format to be used | Can be `b64_json` or `url`
    response_format: str | None = "b64_json"


class ImageRequest(ImageSamplingParams):
    #: Prompt to be used for Image Generation.
    prompt: str

    #: Model to be used for Image Generation.
    model: str

    #: Should it be a Streaming Request or Not
    stream: bool
