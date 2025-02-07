from fastapi.middleware.cors import CORSMiddleware

def configCORS (app):
    if inProd: 
        app.add_middleware(
        CORSMiddleware,
        allow_origins = prodOrigins,
        allow_credentials = prodAllowedCredentials,
        allow_methods = prodMethods,
        allow_headers = prodHeaders,
        )
    elif inDev:
        app.add_middleware(
        CORSMiddleware,
        allow_origins = devOrigins,
        allow_credentials = devAllowedCredentials,
        allow_methods = devMethods,
        allow_headers = devHeaders,
        )
