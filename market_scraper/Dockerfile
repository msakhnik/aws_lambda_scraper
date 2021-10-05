FROM public.ecr.aws/lambda/python:3.9

COPY src/ ${LAMBDA_TASK_ROOT}/

COPY src/requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}" --upgrade
RUN  ls -a ${LAMBDA_TASK_ROOT}/
RUN  ls -a ${LAMBDA_TASK_ROOT}/scraper/
ENV PYTHONPATH "${PYTHONPATH}:/${LAMBDA_TASK_ROOT}"

CMD [ "lambda_handler.handler" ]
