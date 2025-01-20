FROM python:3.13.1-slim

WORKDIR /code

# 先复制requirements.txt文件并安装依赖
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 只有在代码有更新时，才会执行下面的复制操作
COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]