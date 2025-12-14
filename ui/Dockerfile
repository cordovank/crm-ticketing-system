FROM cordn29/crmsys:0.2.0-amd64

WORKDIR /app

COPY app.py ./ui/app.py
COPY start.sh ./start.sh

EXPOSE 7860

CMD ["sh", "/app/start.sh"]