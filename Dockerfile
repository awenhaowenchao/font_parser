FROM python:3.6
LABEL author="wenchao.hao"

#代码复制过来后的路径
RUN mkdir -p /code/font_parser /code/font_parser/config /code/font_parser/parser /code/font_parser/web
ADD ./config /code/font_parser/config
ADD ./parser /code/font_parser/parser
ADD ./web /code/font_parser/web
ENV PYTHONPATH=/code/font_parser:/usr/local/lib/python3.6/site-packages:$PYTHONPATH
WORKDIR /code

#安装需要的python库
RUN pip install requests
RUN pip install flask
RUN pip install werkzeug
RUN pip install fonttools

CMD ["python", "/code/font_parser/web/processer.py"]