# Build with: docker build -t multicategory .
# Run with: docker run -it --publish 8090:8050 --detach --rm --net=multicategory --name multicategory-running multicategory
# docker exec -it <container id> bash
FROM python:3

#WORKDIR src

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8050

CMD [ "python", "src/app.py" ]