FROM python:3.8
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# COPY client_end_script.py maingui.py client_end_script_helper.py perfcheck.py plotcpu.py /app/
# ENV l=10
# ENV u=30
# ENV s=10
# ENV t=30
# CMD python3 client_end_script.py -l $l -u $u -s $s -t $t
CMD ["python3", "client_end_script.py", "-l", "10", "-u", "30", "-s", "10", "-t", "20"]