import SparkApi
#以下密钥信息从控制台获取
appid = "XXXX"     #填写控制台中获取的 APPID 信息
api_secret = "XXXX"   #填写控制台中获取的 APISecret 信息
api_key ="XXXX"    #填写控制台中获取的 APIKey 信息

#用于配置大模型版本，默认“general/generalv2”
# domain = "general"   # v1.5版本
domain = "generalv2"    # v2.0版本
#云端环境的服务地址
# Spark_url = "ws://spark-api.xf-yun.com/v1.1/chat"  # v1.5环境的地址
Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"  # v2.0环境的地址


text =[]

# length = 0

def getText(role,content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text

def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length

def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text
    


if __name__ == '__main__':
    with open("prompt.txt", "r", encoding="utf-8") as f:
        prompt = f.read()
    import os
    text.clear
    while(1):
        Input = input("\n" +"我:")
        question = checklen(getText("user", prompt.replace("{{requirements}}", Input)))
        SparkApi.answer =""
        print("星火:",end = "")
        SparkApi.main(appid,api_key,api_secret,Spark_url,domain,question)
        text = getText("assistant", SparkApi.answer)
        # print(str(text))
        for item in text:
            if item["role"] == "assistant":
                code_string = item["content"].split("```")[1].lstrip("python")

                # 指定要保存的文件名
                file_name = "temp.py"

                # 打开文件以写入模式
                with open(file_name, "w", encoding="utf-8") as file:
                    # 将字符串写入文件
                    file.write(code_string)
        os.system("python temp.py")
        print(text)

