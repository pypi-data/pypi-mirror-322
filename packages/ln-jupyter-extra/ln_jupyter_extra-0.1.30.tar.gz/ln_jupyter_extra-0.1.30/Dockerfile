# 使用官方JupyterLab基础镜像
FROM jupyter/base-notebook:latest

COPY ./jupyter_lab_config.py /opt/conda/etc/jupyter/jupyter_lab_config.py

# 创建环境配置文件
RUN mkdir -p /opt/conda/share/jupyter/lab/static/config && \
    echo 'window.__ENV__ = { \
        API_BASE_URL: process.env.API_BASE_URL || window.location.origin, \
        AUTH_TOKEN: process.env.AUTH_TOKEN \
    };' > /opt/conda/share/jupyter/lab/static/config/env.js

RUN pip install ln_jupyter_extra 

#RUN pip install jupyterlab-language-pack-zh-CN

# 切换回默认的jovyan用户
USER jovyan

# 设置工作目录
WORKDIR /home/jovyan/work

# 暴露JupyterLab默认端口
EXPOSE 8888

# 启动JupyterLab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root","--NotebookApp.token=''","--ServerApp.allow_query_parameters=True"]