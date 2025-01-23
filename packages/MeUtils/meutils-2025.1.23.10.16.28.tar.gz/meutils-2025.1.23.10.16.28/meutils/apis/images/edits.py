#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : image_tools
# @Time         : 2024/8/28 13:17
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.config_utils.lark_utils import get_next_token_for_polling
from meutils.schemas.image_types import ImageRequest, ImagesResponse
from meutils.schemas.image_types import ImageProcess

from meutils.io.files_utils import to_bytes, to_base64, to_url_fal

from meutils.notice.feishu import send_message as _send_message

BASE_URL = "https://image.baidu.com"

FEISHU_URL = "https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=jrWhAS"

send_message = partial(
    _send_message,
    title=__name__,
    url="https://open.feishu.cn/open-apis/bot/v2/hook/dc1eda96-348e-4cb5-9c7c-2d87d584ca18"
)


async def make_request_for_gitee(payload, token: Optional[str] = None, response_format: str = "url"):
    s = time.time()
    feishu_url = "https://xchatllm.feishu.cn/sheets/MekfsfVuohfUf1tsWV0cCvTmn3c?sheet=PDnO6X"
    token = token or await get_next_token_for_polling(feishu_url)

    headers = {
        "Authorization": f"Bearer {token}",
        "X-Failover-Enabled": "true",
        "X-Package": "1910"
    }

    files = {
        "image": ("_.png", payload.pop('image'))
    }
    base_url = "https://ai.gitee.com/v1"
    async with httpx.AsyncClient(base_url=base_url, headers=headers, timeout=60) as client:
        response = await client.post("/images/mattings", data=payload, files=files)
        response.raise_for_status()
        response = ImagesResponse(**response.json())
        if response_format == "url":
            url = await to_url_fal(response.data[0].b64_json, content_type="image/png")
            response.data[0].url = url
            response.data[0].b64_json = None
            response.timings = {"inference": time.time() - s}

        return response


async def make_request_for_baidu(payload, token: Optional[str] = None, response_format: str = "url"):
    s = time.time()
    token = token or await get_next_token_for_polling(feishu_url=FEISHU_URL, from_redis=True)
    headers = {
        'Cookie': token,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=60) as client:
        response = await client.post("/aigc/pccreate", data=payload)  # pcEditTaskid
        response.raise_for_status()
        data = response.json()

        logger.debug(data)

        image_base64 = None
        if task_id := data.get("pcEditTaskid"):
            for i in range(30):
                await asyncio.sleep(3)
                try:
                    response = await client.get(f'/aigc/pcquery?taskId={task_id}')
                    if data := response.json().get("picArr", []):
                        image_base64 = data[0].get("src")
                        break
                except Exception as e:
                    logger.error(e)
                    if i > 3: break

        if response_format == "url":
            url = await to_url_fal(image_base64, content_type="image/png")
            return ImagesResponse(data=[{"url": url}], timings={"inference": time.time() - s})
        else:
            return ImagesResponse(data=[{"b64_json": image_base64}], timings={"inference": time.time() - s})


async def edit_image(request: ImageProcess):
    image, mask = await asyncio.gather(to_base64(request.image), to_base64(request.mask))
    payload = {
        "type": "1",  # 去水印

        "picInfo": image,
        "picInfo2": mask,
        # "original_url": "", # 更快但是会有错误
    }

    if request.model == "remove-watermark":
        if mask:  ####### todo: mask 抠图
            payload['type'] = "2"
        return await make_request_for_baidu(payload, response_format=request.response_format)

    elif request.model == "clarity":
        payload['type'] = "3"
        return await make_request_for_baidu(payload, response_format=request.response_format)

    elif request.model == "expand":
        payload['type'] = "4"
        payload['ext_ratio'] = request.aspect_ratio
        return await make_request_for_baidu(payload, response_format=request.response_format)
    ################################################################################################

    elif request.model == "rmbg-2.0":
        payload = {
            "model": request.model,
            "image": await to_bytes(image),
        }
        return await make_request_for_gitee(payload, response_format=request.response_format)


if __name__ == '__main__':
    token = "BAIDUID=FF8BB4BF861992E2BF4A585A37366236:FG=1; BAIDUID_BFESS=FF8BB4BF861992E2BF4A585A37366236:FG=1; BIDUPSID=FF8BB4BF861992E2BF4A585A37366236; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm; userFrom=null; ab_sr=1.0.1_NjY5OWZiZDg5YTJmYTQzNWUyNzU1YjBmN2FlMDFiNjMyOTVhMDE3ZWVlYWY5N2Y2MTg4NGI1MzRmMmVjMjQyZjlhZTU2MmM1NDRlMmU4YzgwMzRiMjUyYTc4ZjY1OTcxZTE4OTA4YTlmMWIwZWUzNTdiMzlhZTRiM2IzYTQ0MjgyMzc2MjQwMGRlYzZlZDhjOTg5Yzg4NWVjMTNiZmVmZQ==; BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm; H_WISE_SIDS=60273_60360_60623_60664_60678_60684_60700"

    url = "https://oss.ffire.cc/files/kling_watermark.png"
    # url = "https://s22-def.ap4r.com/bs2/upload-ylab-stunt-sgp/se/ai_portal_sgp_queue_mmu_txt2img_aiweb/9c520b80-efc2-4321-8f0e-f1d34d483ddd/1.png"

    request = ImageProcess(
        model="remove-watermark",
        # model="clarity",
        # model="expand",
        # model="rmbg-2.0",

        image=url,
        # mask=url,

        # response_format="b64_json"
    )
    arun(edit_image(request))

    # arun(image_edit(request))
