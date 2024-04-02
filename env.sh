conda create -n cuda10 python=3.7 -y

conda activate cuda10

conda install cudnn=7.6.0 -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/win-64/

conda install cudatoolkit=10.0 -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/win-64/

pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

