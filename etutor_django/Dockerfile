
FROM python:3.8   
 
ENV APP=/home/app/etutor  
 
RUN mkdir -p $APP  

WORKDIR $APP  

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  
 
RUN pip install --upgrade pip  

COPY . $APP  
  
RUN pip install -r requirements.txt  

CMD $APP/startup.sh  