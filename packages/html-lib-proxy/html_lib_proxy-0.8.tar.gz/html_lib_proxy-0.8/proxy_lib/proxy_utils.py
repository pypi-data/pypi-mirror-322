import requests
from bs4 import BeautifulSoup

def get_and_update_counter(max_len):
    """
    读取计数器值，使用后+1并保存，超过最大值时重置为0
    
    Args:
        file_path: txt文件路径
        max_len: 最大长度值
    
    Returns:
        current: 当前的计数值
    """
    try:
        file_path = 'counter.txt'
        # 读取文件
        with open(file_path, 'r') as f:
            current = int(f.read().strip())
    except (FileNotFoundError, ValueError):
        # 如果文件不存在或内容无效，从0开始
        current = 0
    
    # 获取当前值用于返回
    value_to_return = current
    
    # 计算下一个值
    next_value = (current + 1) % max_len
    
    # 将新值写回文件
    with open(file_path, 'w') as f:
        f.write(str(next_value))
    
    return value_to_return
# print(get_and_update_counter(3))

def get_ip_list(file_path):
    """
    从 ips.txt 文件中读取 IP 地址列表
    """
    ip_list = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                ip = line.strip()
                if ip:
                    ip_list.append(ip)
    except FileNotFoundError:
        print(f"文件 {file_path} 不存在.")
    except IOError:
        print(f"读取文件 {file_path} 时出现错误.")
    return ip_list

# # 调用函数获取 IP 地址列表
# ip_list = get_ip_list('ips.txt')
# for ip in ip_list:
#     print(ip)



def p_proxy(ips, username, pwd):
    '''
    ips = [ , , ,]
    '''
    port = 5000
    proxy_ips = []
    for ip in ips:
        proxy_ips.append(f"{ip}:{port}")
    
    # TingProxy认证信息
    proxy_username = username  # 替换为实际的用户名
    proxy_password = pwd    # 替换为实际的密码

    # 使用计数器实现轮询
    count = get_and_update_counter(len(proxy_ips))
    
    # 获取当前代理
    current_proxy = proxy_ips[count]
    print(f'current_proxy{current_proxy}')
    
    # 设置代理(包含认证信息)
    proxies = {
        "http": f"http://{proxy_username}:{proxy_password}@{current_proxy}",
        "https": f"http://{proxy_username}:{proxy_password}@{current_proxy}"
    }
    return proxies

# 简单版
# @retry(stop_max_attempt_number=3, wait_fixed=2000)  # 最多重试3次，每次间隔2秒
def get_html_by_proxy(url, username, pwd):

    ips = get_ip_list('ips.txt')

    proxies =p_proxy(ips, username, pwd)
    
    # 定义请求头
    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0",  # 模拟浏览器请求
        # "Accept-Language": "zh-CN"  # 用户偏好语言为中文
    }

    try:
        # 发送GET请求，使用代理
        response = requests.get(
            url, 
            headers=headers, 
            proxies=proxies,
            timeout=60
        )

        # 检查响应状态码
        if response.status_code == 200:
            try:
                # 解析数据
                data = response.text
                return data, None
            except ValueError:
                msg = "响应不是有效的JSON格式"
                return None, msg
        else:
            msg =  f"请求失败，状态码: {response.status_code} URL: {url}"
            return None, msg
            
    except requests.exceptions.RequestException as e:
        msg =  f"请求发生错误: {e} URL: {url}"
        return None, msg

def get_html_by_proxy_cn(url, username, pwd):
    # 获取代理 IP 列表
    ips = get_ip_list('ips.txt')

    # 构造代理
    proxies = p_proxy(ips, username, pwd)
    
    # 定义请求头
    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0",  # 模拟浏览器请求
        # "Accept-Language": "zh-CN"  # 用户偏好语言为中文
    }

    try:
        # 发送 GET 请求，使用代理
        response = requests.get(
            url, 
            headers=headers, 
            proxies=proxies,
            timeout=60
        )

        # 检查响应状态码
        if response.status_code == 200:
            try:
                # 设置响应的编码为 UTF-8
                response.encoding = 'utf-8'

                # 解析数据
                data = response.text
                return data, None
            except ValueError:
                msg = "响应不是有效的JSON格式"
                return None, msg
        else:
            msg = f"请求失败，状态码: {response.status_code} URL: {url}"
            return None, msg
            
    except requests.exceptions.RequestException as e:
        msg = f"请求发生错误: {e} URL: {url}"
        return None, msg
