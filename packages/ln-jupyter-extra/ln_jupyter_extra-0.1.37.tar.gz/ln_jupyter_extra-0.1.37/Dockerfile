# 使用官方JupyterLab基础镜像
FROM jupyter/minimal-notebook:latest

COPY ./dist/ln_jupyter_extra-0.1.36-py3-none-any.whl  /opt/conda/ln_jupyter_extra-0.1.36-py3-none-any.whl

RUN pip install /opt/conda/ln_jupyter_extra-0.1.36-py3-none-any.whl

#RUN pip install jupyterlab-language-pack-zh-CN

# 切换回默认的jovyan用户
USER jovyan

# 设置工作目录
WORKDIR /home/jovyan/work

# 暴露JupyterLab默认端口
EXPOSE 8888

# 启动JupyterLab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root","--NotebookApp.token=''"]