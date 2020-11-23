# Build with: docker build -t multicategory .
# Run with: docker run -it --publish 8050:8080 --detach --rm --name multicategory-running multicategory
FROM python:3

#WORKDIR src

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8050

CMD [ "python", "src/app.py" ]