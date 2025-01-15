# 使用带 CUDA 12.2 的 Ubuntu 22.04 作为基础镜像
FROM nvidia/cuda:12.2.0-devel-ubuntu22.04

# 设置工作目录
WORKDIR /workspace

# 更新系统并安装基本工具
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-17-jdk \
    maven \
    git \
    wget \
    curl \
    bzip2 \
    ca-certificates \
    libglib2.0-0 \
    libx11-6 \
    libxext6 \
    libsm6 \
    libxrender1 \
    x11-utils \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 安装 Anaconda
RUN wget https://repo.anaconda.com/archive/Anaconda3-2024.10-1-Linux-x86_64.sh -O /tmp/anaconda.sh && \
    bash /tmp/anaconda.sh -b -p /opt/conda && \
    rm /tmp/anaconda.sh

# 配置 Anaconda 路径
ENV PATH="/opt/conda/bin:${PATH}"

# 安装 PyTorch（官方推荐方式）
RUN conda install -y -c conda-forge mamba && \
    mamba install -y -c pytorch -c nvidia \
        pytorch==2.5.0 \
        torchvision==0.20.0 \
        torchaudio==2.5.0 \
        pytorch-cuda=11.8

# 安装 Python 依赖
RUN conda install -y -c conda-forge \
    numpy=1.26.4 \
    pandas=2.2.2 \
    scipy=1.13.1 \
    scikit-learn=1.4.2 \
    matplotlib=3.8.4 \
    seaborn=0.13.2 \
    jupyterlab=4.0.11 \
    notebook=7.0.8 \
    ipykernel=6.28.0 \
    transformers=4.46.1 \
    tokenizers=0.20.1 \
    huggingface_hub=0.26.2 \
    langchain=0.3.14 \
    langchain-community=0.3.14 \
    sentence-transformers=3.2.1 \
    accelerate=1.0.1 \
    bitsandbytes=0.44.1 \
    safetensors=0.4.5 \
    faiss-cpu=1.9.0 \
    flask=3.0.3 \
    && conda clean --all -y

# 预下载 WebDriverManager 以避免 Selenium 启动时下载
RUN mkdir -p /root/.cache/webdriver

# 设置默认入口命令
CMD ["/bin/bash"]
