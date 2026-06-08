import uvicorn
import sys

print("Loading config...")
try:
    config = uvicorn.Config("server:app", host="127.0.0.1", port=8089)
    config.load()
    app = config.loaded_app
    print("ASGI App loaded successfully!")
    print("Middleware:")
    for middleware in app.user_middleware:
        print(f"  {middleware.cls.__name__} options: {middleware.options}")
    print("SUCCESS")
except Exception as e:
    print(f"ERROR: {type(e)} - {str(e)}")
    import traceback
    traceback.print_exc()
