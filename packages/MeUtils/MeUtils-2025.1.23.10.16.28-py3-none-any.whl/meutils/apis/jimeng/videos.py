#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : lip_sync
# @Time         : 2025/1/3 16:17
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
"""
1. 上传图片 image_to_avatar检测
2. 上传视频 video_to_avatar检测
3. 上传音频+创建任务

"""
from meutils.pipe import *
from meutils.str_utils.json_utils import json_path

from meutils.schemas.jimeng_types import BASE_URL, MODELS_MAP, FEISHU_URL
from meutils.schemas.video_types import LipsyncVideoRquest
from meutils.schemas.task_types import TaskResponse
from meutils.apis.jimeng.common import create_draft_content, get_headers, check_token
from meutils.apis.jimeng.files import upload_for_image, upload_for_video

from meutils.config_utils.lark_utils import get_next_token_for_polling

from fake_useragent import UserAgent

ua = UserAgent()


async def create_realman_avatar(image_uri, token: str):
    url = "/mweb/v1/create_realman_avatar"
    headers = get_headers(url, token)

    payload = {
        "input_list": [
            {
                "image_uri": image_uri,
                "submit_id": str(uuid.uuid4()),
                "mode": 0
            },
            {
                "image_uri": image_uri,
                "submit_id": str(uuid.uuid4()),
                "mode": 1
            }
        ]
    }
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=60) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        logger.debug(bjson(data))  # 1914628189186

        if task_ids := json_path(data, "$..task_id"):
            return task_ids
        else:  # task_id 解析失败
            raise Exception("create_realman_avatar failed: task_id 解析失败")

        # mget_generate_task
        # todo: 从任务结果解析 resource_id_std, resource_id_loopy


async def get_task(task_ids):
    """
    $..image_to_avatar 成功： 先检测图片or视频
    :param task_ids:
    :return:
    """
    if isinstance(task_ids, str):
        task_ids = [task_ids]

    token = "916fed81175f5186a2c05375699ea40d"


    url = "/mweb/v1/mget_generate_task"
    headers = get_headers(url, token)

    payload = {"task_id_list": task_ids}
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=60) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        logger.debug(bjson(data))

        if messages := json_path(data, "$..image_to_avatar.message"):
            if message := "".join(messages):  # and "fail" in message
                logger.error(message)
            else:
                logger.info("image_to_avatar success")

                if resource_id_stds := json_path(data, "$..resource_id_std"):
                    resource_id_std = "".join(resource_id_stds)

                if resource_id_loopys := json_path(data, "$..resource_id_loopy"):
                    resource_id_loopy = "".join(resource_id_loopys)
                # return TaskResponse()



async def create_task(request: LipsyncVideoRquest, token: Optional[str] = None):
    # token = token or await get_next_token_for_polling(FEISHU_URL, check_token)
    token = "7c5e148d9fa858e3180c42f843c20454"  # 年付
    token = "916fed81175f5186a2c05375699ea40d"  # 月付

    url = "/mweb/v1/batch_generate_video"

    headers = get_headers(url, token)

    i2v_opt = {}
    v2v_opt = {}
    if request.video_url:
        v2v_opt = {}

    payload = {
        "submit_id": "",
        "task_extra": "{\"promptSource\":\"photo_lip_sync\",\"generateTimes\":1,\"lipSyncInfo\":{\"sourceType\":\"local-file\",\"name\":\"vyFWygmZsIZlUO4s0nr2n.wav\"},\"isUseAiGenPrompt\":false,\"batchNumber\":1}",
        "http_common_info": {
            "aid": 513695
        },
        "input": {
            "seed": 3112889115,
            "video_gen_inputs": [
                {
                    "v2v_opt": {},
                    "i2v_opt": {
                        "realman_avatar": {
                            "enable": True,
                            "origin_image": {
                                # "width": 800,
                                # "height": 1200,
                                "image_uri": "tos-cn-i-tb4s082cfz/4dead1bfc8e84572a91f2e047016a351",
                                "image_url": ""
                            },
                            "origin_audio": {
                                # "duration": 9.976625,
                                "vid": "v02870g10004cu8d4r7og65j2vr5opb0"
                            },

                            "resource_id_std": "381c534f-bcef-482e-8f17-5b30b64e41a1",
                            "resource_id_loopy": "b9ac51cb-e26c-4b63-81d9-34ed24053032",
                            #
                            # "tts_info": "{\"name\":\"vyFWygmZsIZlUO4s0nr2n.wav\",\"source_type\":\"local-file\"}"
                        }
                    },
                    "audio_vid": "v02870g10004cu8d4r7og65j2vr5opb0",
                    "video_mode": 4
                }
            ]
        },
        "mode": "workbench",
        "history_option": {},
        "commerce_info": {
            "resource_id": "generate_video",
            "resource_id_type": "str",
            "resource_sub_type": "aigc",
            "benefit_type": "lip_sync_avatar_std",  # 5积分
            # "benefit_type": "lip_sync_avatar_lively" # 10积分
        },
        "scene": "lip_sync_image",
        "client_trace_data": {},
        "submit_id_list": [
            str(uuid.uuid4())
        ]
    }

    # if request.image_url:
    #     i2v_opt = {
    #         "realman_avatar": {
    #             "enable": True,
    #             "origin_image": {
    #                 "width": 800,
    #                 "height": 1200,  ######## 没必要把
    #                 "image_uri": request.image_url,
    #                 "image_url": ""
    #             },
    #             "resource_id_loopy": "9c397499-a59f-47b5-9bfd-e1397ec62f61",
    #             "resource_id_std": "0a8c8d72-5543-4e9e-8843-c03fe5b3a8c7",
    #             "origin_audio": {
    #                 "duration": 9.976625,
    #                 "vid": "v03870g10004cu6vpgfog65nc9ivupg0"
    #             },
    #             "tts_info": "{\"name\":\"vyFWygmZsIZlUO4s0nr2n.wav\",\"source_type\":\"local-file\"}"
    #         }
    #     }
    #
    # payload = {
    #     "submit_id": "",
    #     "task_extra": "{\"promptSource\":\"photo_lip_sync\",\"generateTimes\":1,\"lipSyncInfo\":{\"sourceType\":\"local-file\",\"name\":\"vyFWygmZsIZlUO4s0nr2n.wav\"},\"isUseAiGenPrompt\":false,\"batchNumber\":1}",
    #     "http_common_info": {
    #         "aid": 513695
    #     },
    #     "input": {
    #         "seed": 2032846910,
    #         "video_gen_inputs": [
    #             {
    #                 "v2v_opt": v2v_opt,
    #                 "i2v_opt": i2v_opt,
    #                 "audio_vid": "v03870g10004cu6vpgfog65nc9ivupg0",
    #                 "video_mode": 4
    #             }
    #         ]
    #     },
    #     "mode": "workbench",
    #     "history_option": {},
    #     "commerce_info": {
    #         "resource_id": "generate_video",
    #         "resource_id_type": "str",
    #         "resource_sub_type": "aigc",
    #         "benefit_type": "lip_sync_avatar_std"
    #     },
    #     "scene": "lip_sync_image",
    #     "client_trace_data": {},
    #     "submit_id_list": [
    #         "4717038e-f4fd-4c1c-b5a5-39ae4118099c"
    #     ]
    # }

    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=60) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        logger.debug(bjson(data))

    if task_ids := json_path(data, "$..task.task_id"):
        task_id = task_ids[0]
        return TaskResponse(task_id=task_id, system_fingerprint=token)


if __name__ == '__main__':
    # image_uri = "tos-cn-i-tb4s082cfz/387649a361e546f89549bd3510ab926d"
    # task_ids = arun(create_realman_avatar(image_uri, token="7c5e148d9fa858e3180c42f843c20454"))
    # arun(mget_generate_task(task_ids))
    r = arun(create_task(LipsyncVideoRquest()))
    arun(get_task(r.task_id))
