from fastapi import FastAPI
from Backend.routers import users,bot

app = FastAPI()

# include routers
app.include_router(users.router)
app.include_router(bot.router)
@app.get("/")
def root():
    return {"msg": "Soulbloom API running "}


# to start database
# ./mongod --dbpath D:\soulbloom\db
