# conda create -n jupyterlab-ext --override-channels --strict-channel-priority -c conda-forge -c nodefaults jupyterlab=4 nodejs=20 git copier=9 jinja2-time


#     conda activate jupyterlab-ext

pip install -ve .

jlpm install
jlpm run build

jupyter lab


Release:

python -m build
twine upload dist/* -u=__token__ -p=pypi-massive_token_code
