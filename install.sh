#!/bin/bash
# Initial installation for the assembly pipeline
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
echo -e "\nyes\n\nyes\n" | bash Miniconda3-latest-Linux-x86_64.sh
export PATH=~/miniconda3/bin:$PATH
conda update -y -n base conda
conda config --add channels defaults
conda config --add channels conda-forge
conda config --add channels bioconda
rm -f udocker.py
wget https://raw.githubusercontent.com/indigo-dc/udocker/7f6975c19c63c3d65ec6256c7cf5b2369d5c115d/udocker.py
chmod uog+x udocker.py
./udocker.py pull pakorhon/arrow:v0.0.4-beta
./udocker.py pull pakorhon/combinecats:v0.0.3-beta
./udocker.py pull pakorhon/decon:v0.0.3-beta
./udocker.py pull pakorhon/haplomerger:v0.0.5-beta
./udocker.py pull pakorhon/hdf5check:v0.0.4-beta
./udocker.py pull pakorhon/renamereads:v0.0.3-beta
./udocker.py pull pakorhon/repeatmodeler:v0.0.4-beta
rm -f udocker.py
conda install -y -p ~/miniconda3 udocker==1.1.1
sed 's/#!\/bin\/bash/#!\/bin\/bash\nexport CONDA_PREFIX=~\/miniconda3/1' ~/miniconda3/bin/udocker > udocker
chmod uog+x udocker
mv udocker ~/miniconda3/bin
#wget https://raw.githubusercontent.com/indigo-dc/udocker/7f6975c19c63c3d65ec6256c7cf5b2369d5c115d/udocker.py -P ~/miniconda3/bin
wget https://raw.githubusercontent.com/indigo-dc/udocker/7f6975c19c63c3d65ec6256c7cf5b2369d5c115d/udocker.py
sed 's/proot_killonexit = True/proot_killonexit = False/1' udocker.py > ~/miniconda3/bin/udocker.py
chmod uog+x ~/miniconda3/bin/udocker.py

pip install galaxy-lib==18.5.7
conda install -y -c conda-forge nodejs==10.4.1
conda install -y -c conda-forge git==2.18.0
pip install cwltool==v1.0.20180403145700
sed 's/        for key in env:/        if env != None:\n          for key in env:/1' ~/miniconda3/lib/python*/site-packages/cwltool/job.py > job.py
mv job.py ~/miniconda3/lib/python*/site-packages/cwltool
