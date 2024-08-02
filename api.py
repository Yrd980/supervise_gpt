import asyncio
import time
from typing import Any, Dict, Callable

from fastapi import UploadFile, File
from tenacity import stop_after_attempt, retry, wait_exponential

from api_requests import APIRequest
from config import Config
from constant import AutoSupervision
from model import SuperViseGroup

# 创建一个信号量来限制并发请求数
MAX_CONCURRENT_REQUESTS = 5
semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)


# 创建一个简单的限流器
class RateLimiter:
    def __init__(self, calls_per_second):
        self.calls_per_second = calls_per_second
        self.last_call_time = 0

    async def wait(self):
        current_time = time.time()
        time_since_last_call = current_time - self.last_call_time
        if time_since_last_call < 1 / self.calls_per_second:
            await asyncio.sleep(1 / self.calls_per_second - time_since_last_call)
        self.last_call_time = time.time()


rate_limiter = RateLimiter(1)  # 每秒最多1个请求


# Retry decorator
def retry_async(retries: int = 3, delay: float = 1.0):
    def decorator(func: Callable):
        async def wrapper(*args, **kwargs):
            last_exception = None
            for _ in range(retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    await asyncio.sleep(delay)
            raise last_exception

        return wrapper

    return decorator


async def api_request(url: str, data: Dict[str, Any]):
    if not data:
        return {"error": "No data provided"}
    try:
        response = await APIRequest.post(url, data=data)
        return response
    except Exception as e:
        return {"error": str(e)}


async def upload_file(file: UploadFile = File(...)):
    if not file:
        return {"error": "No file provided"}
    try:
        file_content = await file.read()
        files = {'file': file_content}
        return await APIRequest.post(Config.UPLOAD_FILE_URL, files=files)
    except Exception as e:
        return {"error": str(e)}


async def check_atom_rule(rule):
    return await api_request(Config.CHECK_ATOM_RULE_URL, {"rule": rule})


async def split_atomic_rules(rule):
    return await api_request(Config.SPLIT_ATOMIC_RULES_URL, {"rule": rule})


# 重试装饰器，最多重试3次，每次等待时间指数增长
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
async def identify_rules(rule):
    return await api_request(Config.IDENTIFY_RULES_URL, {"rule": rule})


async def classify_rules(rule):
    return await api_request(Config.CLASSIFY_RULES_URL, {"rule": rule})


async def process_rule(rule) -> SuperViseGroup:
    identify_rule_result = await identify_rules(rule)

    data_value = identify_rule_result['data']

    auto_supervised_value = AutoSupervision.AUTO_SUPERVISED.value

    if data_value == auto_supervised_value:
        classification = await classify_rules(rule)

        # 确保分类结果中的category和type是有效的
        category = classification.get('category', "") if classification else ""
        supervise_type = classification.get('type', "") if classification else ""

        return SuperViseGroup(
            supervise=str(auto_supervised_value),
            supervise_category=category,
            supervise_type=supervise_type
        )
    else:
        return SuperViseGroup(
            supervise=str(AutoSupervision.NOT_AUTO_SUPERVISED.value),
            supervise_category="",
            supervise_type=""
        )


@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=1, max=10))
async def extract_common_element(rule, category):
    async with semaphore:
        await rate_limiter.wait()
        return await api_request(Config.EXTRACT_COMMON_RULES_URL, {"rule": rule, "category": category})


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
async def generate_cdsrl(rule, category, entity_info):
    return await api_request(Config.GENERATE_CDSRL_URL,
                             {"rule": rule, "category": category, "entity_info": entity_info})
