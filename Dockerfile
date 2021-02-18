FROM python:3
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir kubernetes
COPY kube-scheduler.py kube-scheduler.py
CMD ["python", "kube_scheduler.py"]